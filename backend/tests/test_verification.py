"""
Automated Verification Test Suite for NyayaAI.
Tests:
1. Incorrect section numbers
2. Repealed laws
3. Commencement dates (temporal validity)
4. Unsupported procedural deadlines
5. Misleading legal conclusions in education disputes
6. Rejection of unverified/hallucinated citations
7. Mandatory metadata fields on every claim
"""

import pytest
from app.services.legal_db import (
    lookup_provision,
    check_temporal_validity,
    check_education_dispute,
    STATUTES_REGISTRY
)
from app.agents.citation_verifier import LegalCitationVerificationAgent, UNVERIFIED_NOTICE


class TestCitationVerification:
    def setup_method(self):
        self.agent = LegalCitationVerificationAgent()

    # ── Test 1: Incorrect Section Numbers ────────────────────────────────────
    def test_incorrect_section_numbers_rejected(self):
        """Verify that out-of-range or non-existent section numbers are rejected."""
        # Consumer Protection Act 2019 only has 107 sections. Section 138 does not exist.
        res = lookup_provision("Consumer Protection Act, 2019", "138")
        assert res is not None
        assert res.get("provision") is None
        assert "does not exist" in res.get("error", "")

        # Test verification agent rejects it and sets UNVERIFIED_NOTICE
        claim = self.agent._verify_single_citation(
            act_name="Consumer Protection Act, 2019",
            section_number="138",
            alleged_desc="cheque bounce",
            incident_date="2024-01-01",
            jurisdiction="India",
            timestamp="2026-11-18T00:00:00Z",
            sources=[]
        )
        assert claim.is_verified is False
        assert claim.confidence_level in ["refuted", "unverified"]
        assert UNVERIFIED_NOTICE in claim.exact_provision_text or UNVERIFIED_NOTICE in claim.verification_notes

    # ── Test 2: Repealed Laws ────────────────────────────────────────────────
    def test_repealed_laws_detected(self):
        """Verify that repealed statutes are flagged when cited for recent incidents."""
        # Consumer Protection Act 1986 was repealed in July 2020
        res = check_temporal_validity("Consumer Protection Act, 1986", "2024-05-15")
        assert res["status"] == "repealed_prior"
        assert res["in_force"] is False
        assert "repealed" in res["note"].lower()

        claim = self.agent._verify_single_citation(
            act_name="Consumer Protection Act, 1986",
            section_number="12",
            alleged_desc="filing complaint",
            incident_date="2024-05-15",
            jurisdiction="India",
            timestamp="2026-11-18T00:00:00Z",
            sources=[]
        )
        assert claim.in_force_on_incident_date is False or claim.confidence_level in ["caution", "unverified", "refuted"]

    # ── Test 3: Commencement Dates (Temporal Validity) ───────────────────────
    def test_commencement_dates_checked(self):
        """Verify that an Act cannot be applied to an incident date prior to its commencement."""
        # Bharatiya Nyaya Sanhita, 2023 commenced on 1 July 2024.
        # An incident on 15 January 2023 cannot be prosecuted prospectively under BNS 2023.
        res = check_temporal_validity("Bharatiya Nyaya Sanhita, 2023", "2023-01-15")
        assert res["status"] == "not_yet_in_force"
        assert res["in_force"] is False
        assert "NOT in force on the incident date" in res["note"]

        # Conversely, on 15 August 2024 it is validly in force
        res_post = check_temporal_validity("Bharatiya Nyaya Sanhita, 2023", "2024-08-15")
        assert res_post["status"] == "in_force"
        assert res_post["in_force"] is True

    # ── Test 4: Unsupported Deadlines Detected ────────────────────────────────
    def test_unsupported_deadlines_flagged(self):
        """Verify that unsupported limitation periods are flagged with statutory corrections."""
        hallucinated_text = "You must file your complaint before the district commission within 15 days or your right is lost."
        warnings = self.agent._audit_deadlines(hallucinated_text)
        assert len(warnings) > 0
        assert any("2 years" in w for w in warnings)

    # ── Test 5: Education Disputes Evaluation ─────────────────────────────────
    def test_education_dispute_evaluates_ugc_and_sc_precedents(self):
        """
        Verify that college/exam/degree disputes trigger mandatory evaluation of
        UGC 2023 regulations and Supreme Court precedents (Surjeet Kaur, P.T. Koshy)
        before recommending consumer litigation.
        """
        edu_query = "I paid my college examination fee, but the university refused my hall ticket."
        eval_result = check_education_dispute(edu_query)
        assert eval_result is not None
        assert eval_result["is_education_dispute"] is True
        assert "Surjeet Kaur" in eval_result["supreme_court_precedent"]
        assert "P.T. Koshy" in eval_result["supreme_court_precedent"]
        assert "UGC" in eval_result["primary_ugc_regulation"]
        assert "Manu Solanki" in eval_result["judicial_exception"]

        # Run end-to-end verification
        draft = "You can immediately file a case in the consumer forum against the university under Section 35."
        enhanced, claims, summary = self.agent.verify_response(
            draft_answer=draft,
            question=edu_query,
            jurisdiction="India",
            incident_date="2024-01-01",
            retrieved_sources=[]
        )
        assert summary.education_dispute_evaluated is True
        assert "Maharshi Dayanand University v. Surjeet Kaur" in enhanced
        assert "UGC (Redressal of Grievances of Students) Regulations, 2023" in enhanced

    # ── Test 6: Plausible Hallucinated Citation Rejected ───────────────────────
    def test_hallucinated_citation_rejected_with_standard_notice(self):
        """Ensure that plausible but fake Acts are not accepted without verification."""
        fake_act = "National Academic Fee Refund Act, 2021"
        fake_sec = "14A"

        claim = self.agent._verify_single_citation(
            act_name=fake_act,
            section_number=fake_sec,
            alleged_desc="automatic refund of fees within 48 hours",
            incident_date=None,
            jurisdiction="India",
            timestamp="2026-11-18T00:00:00Z",
            sources=[]
        )
        assert claim.is_verified is False
        assert claim.confidence_level == "unverified"
        assert UNVERIFIED_NOTICE in claim.exact_provision_text or UNVERIFIED_NOTICE in claim.verification_notes

    # ── Test 7: Mandatory Output Metadata Verified ────────────────────────────
    def test_mandatory_metadata_attributes_present(self):
        """Verify that every legal claim maintains the complete mandatory metadata specification."""
        claim = self.agent._verify_single_citation(
            act_name="Consumer Protection Act, 2019",
            section_number="35",
            alleged_desc="manner of filing complaint",
            incident_date="2024-01-01",
            jurisdiction="India",
            timestamp="2026-11-18T00:00:00Z",
            sources=[]
        )

        # Mandatory fields check
        assert claim.act_name != ""
        assert claim.section_number == "35"
        assert claim.exact_provision_text != ""
        assert claim.official_source != ""
        assert claim.effective_date != ""
        assert claim.current_status != ""
        assert isinstance(claim.relevant_judicial_precedents, list)
        assert claim.jurisdiction != ""
        assert claim.verification_timestamp != ""
        assert claim.confidence_level in ["verified", "caution", "unverified", "refuted"]
        assert claim.claim_type in ["statutory", "judicial_precedent", "regulatory_norm", "practical_recommendation"]
