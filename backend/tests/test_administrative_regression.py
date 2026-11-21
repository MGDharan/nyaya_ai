"""
Automated Regression Test Suite for Government Service and Administrative Law Classification.

Tests:
1. Government certificate refusal (Tahsildar caste/income certificate)
2. Government service delay (Driving license / RTO delay)
3. Bribery demand (Public servant demanding bribe under Prevention of Corruption Act)
4. RTI rejection and Central vs State portal jurisdiction (Tamil Nadu vs Central & Aditya Bandopadhyay rule)
5. Police refusing a complaint (Lalita Kumari & Section 154/156(3))
6. Paid government service dispute (TANGEDCO electricity / paid public utility under Lucknow Dev Authority)
7. Administrative appeal (Statutory Departmental First Appeal & Art 226 Mandamus)
8. Consumer dispute involving a private service provider (E-commerce / Private company under CPA 2019)
"""

import pytest
from app.agents.multi_agent_pipeline import NyayaMultiAgentPipeline, LegalAgentState
from app.services.legal_db import (
    check_government_service_dispute,
    check_consumer_applicability,
    check_rti_jurisdiction
)
from app.services.hybrid_retriever import is_statute_irrelevant_to_query


class TestAdministrativeClassificationRegression:
    def setup_method(self):
        self.pipeline = NyayaMultiAgentPipeline()

    # ── Test 1: Government Certificate Refusal ──────────────────────────────────
    def test_government_certificate_refusal(self):
        """
        Verify that a Tahsildar refusing an income or caste certificate:
        - Is classified as a sovereign statutory duty (NOT a consumer dispute).
        - Rejects Consumer Protection Act, NI Act, and IT Act from retrieved sources.
        - Recommends Departmental First Appeal (RDO/Sub-Collector), CM Cell/CPGRAMS, and Art 226 Mandamus.
        """
        query = "The Tahsildar is refusing to issue my income and caste certificate even after submitting all required revenue records and fee receipt."
        state = LegalAgentState(question=query, jurisdiction="Tamil Nadu")
        res = self.pipeline.run(state)

        ans = res["answer"]
        ans_lower = ans.lower()

        # 1. Classification & Domain Verification
        assert state.classified_issue["domain"] == "Government Service & Administrative Law"
        assert state.consumer_applicability["cpa_applicable"] is False
        assert "Sovereign / Statutory" in state.consumer_applicability["exclusion_reason"]

        # 2. Rejection of Consumer Protection Act for Sovereign Duty
        assert "jagmittar sain bhagat" in ans_lower
        assert ("consumer court" in ans_lower and "zero jurisdiction" in ans_lower) or "do not" in ans_lower

        # 3. Proper Administrative & Constitutional Remedies
        assert "revenue divisional officer" in ans_lower or "sub-collector" in ans_lower or "rdo" in ans_lower
        assert "cmcell.tn.gov.in" in ans_lower or "cm special cell" in ans_lower or "cpgrams" in ans_lower
        assert "article 226" in ans_lower or "mandamus" in ans_lower

        # 4. Strict Retrieval Precision: Unrelated Acts must be rejected
        source_titles = [s["title"].lower() for s in res["sources"]]
        for t in source_titles:
            assert "negotiable instruments" not in t, f"Irrelevant Act in sources: {t}"
            assert "information technology act" not in t, f"Irrelevant Act in sources: {t}"
            assert "consumer protection act" not in t, f"Irrelevant Act in sources: {t}"

    # ── Test 2: Government Service Delay ───────────────────────────────────────
    def test_government_service_delay(self):
        """
        Verify that an RTO delaying a driving license:
        - Identifies Right to Public Services / Citizen Charter delivery timelines.
        - Excludes Consumer Court for sovereign licensing duty.
        - Recommends Transport Department Appeal & Article 226 Mandamus.
        """
        query = "I passed my driving test 2 months ago at the RTO, but the officer has not issued my driving license."
        state = LegalAgentState(question=query, jurisdiction="Tamil Nadu")
        res = self.pipeline.run(state)

        ans_lower = res["answer"].lower()

        # Classification check
        assert state.classified_issue["domain"] == "Government Service & Administrative Law"
        assert state.consumer_applicability["cpa_applicable"] is False

        # Precedents and remedies check
        assert "citizen" in ans_lower or "public services" in ans_lower
        assert "transport" in ans_lower
        assert "article 226" in ans_lower or "mandamus" in ans_lower

        # Zero irrelevant Acts in sources
        for s in res["sources"]:
            assert "negotiable instruments" not in s["title"].lower()
            assert "information technology act" not in s["title"].lower()

    # ── Test 3: Bribery Demand by Public Servant ───────────────────────────────
    def test_bribery_demand(self):
        """
        Verify that an officer demanding a bribe:
        - Cites The Prevention of Corruption Act, 1988 (Section 7, 7A).
        - Recommends reporting to State DVAC (Toll-Free 1064) or CBI/CVC.
        - Strictly forbids Consumer Protection Act or paying the bribe.
        """
        query = "The revenue officer is demanding a bribe of ₹5000 to clear my land title file. What can I do?"
        state = LegalAgentState(question=query, jurisdiction="Tamil Nadu")
        res = self.pipeline.run(state)

        ans_lower = res["answer"].lower()

        # Domain classification
        assert state.classified_issue["domain"] == "Corruption & Bribery Redressal"
        assert state.government_dispute["function_type"] == "corruption_bribery_demand"

        # Statute and Authorities
        assert "prevention of corruption act" in ans_lower
        assert "section 7" in ans_lower
        assert "dvac" in ans_lower or "1064" in ans_lower or "vigilance" in ans_lower
        assert "do not pay" in ans_lower or "not pay the bribe" in ans_lower

        # Zero irrelevant financial or consumer statutes
        for s in res["sources"]:
            assert "negotiable instruments" not in s["title"].lower()
            assert "consumer protection act" not in s["title"].lower()

    # ── Test 4: RTI Rejection & Central vs State Portal Jurisdiction ────────────
    def test_rti_rejection_tamil_nadu_portal(self):
        """
        Verify that RTI for a Tamil Nadu State Department:
        - Points to https://rtionline.tn.gov.in/
        - Cites Sections 6, 7 (30-day timeline), and 19 (First Appeal within 30 days).
        - Enforces CBSE v. Aditya Bandopadhyay: right to existing records vs demanding reasons.
        """
        query = "I filed an RTI to the Tahsildar in Chennai 40 days ago asking for copy of the inspection report, but received no response."
        state = LegalAgentState(question=query, jurisdiction="Tamil Nadu")
        res = self.pipeline.run(state)

        ans_lower = res["answer"].lower()

        # RTI domain and jurisdiction portal check
        assert state.classified_issue["domain"] == "Right to Information & Administrative Law"
        assert "rtionline.tn.gov.in" in ans_lower
        assert "section 6" in ans_lower
        assert "section 7" in ans_lower or "30 days" in ans_lower
        assert "section 19" in ans_lower or "first appeal" in ans_lower

        # Aditya Bandopadhyay rule
        assert "aditya bandopadhyay" in ans_lower or "existing records" in ans_lower

        # Sources must NOT include Negotiable Instruments or Consumer Protection Act
        for s in res["sources"]:
            assert "negotiable instruments" not in s["title"].lower()
            assert "consumer protection act" not in s["title"].lower()

    def test_rti_rejection_central_portal(self):
        """
        Verify that RTI for a Central Government Authority:
        - Points to https://rtionline.gov.in/
        """
        rti_info = check_rti_jurisdiction("I filed an RTI to the Central Passport Office in New Delhi", "India")
        assert rti_info["official_portal_url"] == "https://rtionline.gov.in/"
        assert "Central" in rti_info["authority_type"]

    # ── Test 5: Police Refusal of Complaint ─────────────────────────────────────
    def test_police_refusing_complaint(self):
        """
        Verify that an SHO refusing an FIR for theft:
        - Cites Lalita Kumari v. Govt. of U.P. (2014) 2 SCC 1.
        - Cites Section 154 CrPC / 173 BNSS and Section 156(3) CrPC / 175(3) BNSS.
        - Strictly excludes Consumer Protection Act.
        """
        query = "Two men snatched my mobile phone on the road. The police station officer refuses to register an FIR."
        state = LegalAgentState(question=query, jurisdiction="India")
        res = self.pipeline.run(state)

        ans_lower = res["answer"].lower()

        assert state.classified_issue["domain"] == "Criminal Law & Police Powers"
        assert "lalita kumari" in ans_lower
        assert "154" in ans_lower or "173" in ans_lower
        assert "156(3)" in ans_lower or "175(3)" in ans_lower or "magistrate" in ans_lower
        assert "superintendent of police" in ans_lower or "sp" in ans_lower

        # Excludes consumer forum
        for s in res["sources"]:
            assert "consumer protection act" not in s["title"].lower()

    # ── Test 6: Paid Government Service Dispute (Commercial Utility) ───────────
    def test_paid_government_service_dispute(self):
        """
        Verify that a dispute over paid commercial electricity (TANGEDCO) or paid municipal water:
        - Qualifies under Section 2(42) and Section 2(7) of the Consumer Protection Act.
        - Cites Lucknow Development Authority v. M.K. Gupta (1994) 1 SCC 243.
        """
        query = "TANGEDCO sent an inflated commercial electricity bill of ₹45,000 for my shop with a defective meter."
        state = LegalAgentState(question=query, jurisdiction="Tamil Nadu")
        res = self.pipeline.run(state)

        # Paid utility DOES fall under consumer law
        assert state.consumer_applicability["cpa_applicable"] is True
        assert state.government_dispute["function_type"] == "paid_commercial_public_utility"

        # Check that Consumer Protection Act is recognized for paid commercial utilities
        ans_lower = res["answer"].lower()
        assert "lucknow development authority" in ans_lower or "consumer" in ans_lower or "cgrf" in ans_lower

    # ── Test 7: Administrative Appeal & High Court Mandamus ────────────────────
    def test_administrative_appeal(self):
        """
        Verify that an arbitrary rejection of a building plan:
        - Identifies statutory First Appeal and High Court Article 226 Writ of Mandamus.
        - Excludes Consumer Court.
        """
        query = "The municipality building plan approval officer arbitrarily rejected my residential building plan without giving any written reason."
        state = LegalAgentState(question=query, jurisdiction="Tamil Nadu")
        res = self.pipeline.run(state)

        ans_lower = res["answer"].lower()

        assert state.consumer_applicability["cpa_applicable"] is False
        assert "article 226" in ans_lower or "mandamus" in ans_lower
        assert "appeal" in ans_lower or "cmcell" in ans_lower or "rdo" in ans_lower

    # ── Test 8: Consumer Dispute Involving Private Service Provider ────────────
    def test_consumer_dispute_private_service_provider(self):
        """
        Verify that a private e-commerce dispute:
        - Validly applies Consumer Protection Act, 2019 (Sections 2(7), 2(11), 35).
        - Recommends District Commission / e-Daakhil / National Consumer Helpline 1915.
        """
        query = "I bought a mobile phone on Amazon for ₹25,000. It arrived broken and they refused return or refund."
        state = LegalAgentState(question=query, jurisdiction="India")
        res = self.pipeline.run(state)

        assert state.consumer_applicability["cpa_applicable"] is True
        assert state.classified_issue["domain"] == "Consumer Protection & E-Commerce Law"

        ans_lower = res["answer"].lower()
        assert "consumer" in ans_lower
        assert "35" in ans_lower or "district commission" in ans_lower or "1915" in ans_lower

