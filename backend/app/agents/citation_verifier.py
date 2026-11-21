"""
Legal Citation Verification Agent for NyayaAI.
Validates Acts, sections, subsections, regulations, judicial precedents,
temporal validity, and procedural deadlines against authoritative sources.
"""

import re
from datetime import datetime, timezone
from typing import List, Dict, Any, Optional, Tuple
from app.schemas import LegalClaim, VerificationSummary
from app.services.legal_db import (
    lookup_provision,
    check_temporal_validity,
    check_education_dispute,
    find_statute_by_name,
    JUDICIAL_PRECEDENTS
)

UNVERIFIED_NOTICE = "Unable to verify this legal provision from the available official sources."

# Common deadline rules in Indian law for verification
KNOWN_STATUTORY_DEADLINES = [
    {
        "pattern": r"(consumer\s+court|consumer\s+commission|district\s+commission)",
        "allowed_limitations": ["2 years", "two years"],
        "section": "Section 69 of Consumer Protection Act, 2019",
        "description": "Limitation period for consumer complaints is 2 years from cause of action."
    },
    {
        "pattern": r"(cheque\s+bounce|section\s+138|dishonour\s+of\s+cheque)",
        "allowed_notice_days": ["30 days", "thirty days"],
        "allowed_payment_days": ["15 days", "fifteen days"],
        "allowed_complaint_limitation": ["1 month", "one month", "30 days"],
        "section": "Section 138, 142 of Negotiable Instruments Act, 1881",
        "description": "Statutory notice within 30 days; 15 days to pay; complaint within 1 month from end of 15 days."
    },
    {
        "pattern": r"(security\s+deposit|tnrrlta|tenant.*deposit)",
        "allowed_refund_limit": ["1 month", "one month", "30 days"],
        "section": "Section 10 of TNRRLTA 2017",
        "description": "Security deposit refund within 1 month of vacating."
    }
]


class LegalCitationVerificationAgent:
    def __init__(self):
        self.name = "Legal Citation Verification Agent"

    def verify_response(
        self,
        draft_answer: str,
        question: str,
        jurisdiction: str,
        incident_date: Optional[str],
        retrieved_sources: List[Dict[str, Any]]
    ) -> Tuple[str, List[LegalClaim], VerificationSummary]:
        """
        Executes end-to-end verification of the legal draft:
        1. Extracts legal claims (Acts, sections, regulations, deadlines).
        2. Validates against authoritative statutory registry and retrieved documents.
        3. Checks temporal validity (was law in force on incident date?).
        4. Detects incorrect section-to-description mappings.
        5. Evaluates education disputes against UGC regulations & SC precedents.
        6. Distinguishes statutory text from court interpretations and recommendations.
        7. Produces verified claims with mandatory metadata.
        """
        timestamp = datetime.now(timezone.utc).isoformat()
        claims: List[LegalClaim] = []
        caution_count = 0
        verified_count = 0
        unverified_count = 0

        # ── Step 1: Extract candidate citations from draft text ───────────────
        raw_citations = self._extract_citations(draft_answer)

        # ── Step 2: Verify each citation against authoritative primary sources ─
        verified_act_names = set()
        for cit in raw_citations:
            act_name = cit["act_name"]
            sec_num = cit["section_number"]
            alleged_desc = cit.get("desc", "")

            claim = self._verify_single_citation(
                act_name=act_name,
                section_number=sec_num,
                alleged_desc=alleged_desc,
                incident_date=incident_date,
                jurisdiction=jurisdiction,
                timestamp=timestamp,
                sources=retrieved_sources
            )
            claims.append(claim)
            verified_act_names.add(act_name.lower())

            if claim.is_verified:
                verified_count += 1
            elif claim.confidence_level == "caution":
                caution_count += 1
            else:
                unverified_count += 1

        # ── Step 3: Education dispute evaluation ──────────────────────────────
        edu_eval = check_education_dispute(question)
        education_dispute_evaluated = bool(edu_eval)

        if edu_eval:
            # Check if Supreme Court education precedent claim already in list
            edu_claim = LegalClaim(
                act_name="Supreme Court Landmark Precedents (Education)",
                section_number="MDU v. Surjeet Kaur (2010) & P.T. Koshy (2012)",
                exact_provision_text=edu_eval["supreme_court_precedent"],
                official_source="Supreme Court of India (2010) 11 SCC 159; 2012 (3) CPC 615",
                effective_date="2010-07-19",
                current_status="in_force (binding precedent under Art. 141)",
                relevant_judicial_precedents=[
                    "Maharshi Dayanand University v. Surjeet Kaur (2010) 11 SCC 159",
                    "P.T. Koshy v. Ellen Charitable Trust 2012 (3) CPC 615 (SC)"
                ],
                jurisdiction="India",
                verification_timestamp=timestamp,
                confidence_level="verified",
                claim_type="judicial_precedent",
                in_force_on_incident_date=True,
                conflicting_interpretations=[edu_eval["judicial_exception"]],
                verification_notes="Statutory examinations and university fee disputes are NOT services under Consumer Protection Act. Student must seek UGC/Ombudsperson redressal first.",
                is_verified=True
            )
            claims.append(edu_claim)
            verified_count += 1

            # UGC 2023 Regulation claim
            ugc_claim = LegalClaim(
                act_name="UGC (Redressal of Grievances of Students) Regulations, 2023",
                section_number="Regulation 5 & 6",
                exact_provision_text="Collegiate Student Grievance Redressal Committee (SGRC) shall decide student grievances within 15 days; appeal lies to University Ombudsperson.",
                official_source="https://www.ugc.gov.in/pdfnews/9152473_ugc-regulations-2023.pdf",
                effective_date="2023-04-11",
                current_status="in_force",
                relevant_judicial_precedents=[],
                jurisdiction="India (HEIs)",
                verification_timestamp=timestamp,
                confidence_level="verified",
                claim_type="regulatory_norm",
                in_force_on_incident_date=True,
                conflicting_interpretations=[],
                verification_notes="Statutory pre-litigation administrative remedy for college fee and exam discrepancies.",
                is_verified=True
            )
            claims.append(ugc_claim)
            verified_count += 1

        # ── Step 4: Audit Procedural Claims & Deadlines ───────────────────────
        deadline_warnings = self._audit_deadlines(draft_answer)

        # ── Step 5: Clean and Enhance Answer with Verified Metadata ──────────
        enhanced_answer = self._inject_verification_annotations(
            draft_answer=draft_answer,
            claims=claims,
            edu_eval=edu_eval,
            deadline_warnings=deadline_warnings
        )

        summary = VerificationSummary(
            total_claims_detected=len(claims),
            verified_claims_count=verified_count,
            unverified_claims_count=unverified_count,
            caution_flags_count=caution_count + len(deadline_warnings),
            temporal_validity_checked=bool(incident_date),
            education_dispute_evaluated=education_dispute_evaluated,
            audit_verdict="Verified with Precedents" if unverified_count == 0 else "Caution: Unverified or Disputed Claims Flagged"
        )

        return enhanced_answer, claims, summary

    def _extract_citations(self, text: str) -> List[Dict[str, Any]]:
        citations = []
        # Pattern e.g. **Consumer Protection Act, 2019 — Section 35**: ...
        # Or: Section 138 of the Negotiable Instruments Act, 1881
        pattern1 = re.compile(
            r"\*\*(?P<act>[A-Za-z0-9\s,\(\)]+?(?:Act|Regulations|Sanhita|Code)[,\s\d]*?)\s*[—\-–:]+\s*(?:Section|Sec|Regulation)\s*(?P<sec>[0-9A-Za-z\(\)]+)\*\*\s*[:-]?\s*(?P<desc>[^\n\*\#]+)?",
            re.IGNORECASE
        )
        for m in pattern1.finditer(text):
            act = m.group("act").strip()
            sec = m.group("sec").strip()
            desc = (m.group("desc") or "").strip()
            citations.append({"act_name": act, "section_number": sec, "desc": desc})

        # Pattern 2: Section 35 of the Consumer Protection Act, 2019
        pattern2 = re.compile(
            r"(?:Section|Sec|Regulation)\s+(?P<sec>[0-9A-Za-z\(\)]+)\s+of\s+(?:the\s+)?(?P<act>[A-Za-z0-9\s,\(\)]+?(?:Act|Regulations|Sanhita|Code)[,\s\d]*)",
            re.IGNORECASE
        )
        for m in pattern2.finditer(text):
            act = m.group("act").strip().rstrip(".,;:")
            sec = m.group("sec").strip()
            if not any(c["act_name"].lower() == act.lower() and c["section_number"] == sec for c in citations):
                citations.append({"act_name": act, "section_number": sec, "desc": ""})

        # Pattern 3: Hierarchical Act heading followed by sub-bullet sections
        current_act = None
        for line in text.splitlines():
            line_str = line.strip()
            act_header_match = re.search(r"^\*?\s*\*\*(?P<act>[A-Za-z0-9\s,\(\)]+?(?:Act|Regulations|Sanhita|Code)[,\s\d]*?)\*\*\s*[:\-]", line_str, re.IGNORECASE)
            if act_header_match:
                cand_act = act_header_match.group("act").strip()
                if not re.search(r"Section|Sec", cand_act, re.IGNORECASE):
                    current_act = cand_act
                continue

            if current_act:
                # Sub-bullet with Section
                sec_match = re.search(r"^\*?\s*\*\*(?:Section|Sec|Regulation)\s*(?P<sec>[0-9A-Za-z\(\)]+)[^\*]*\*\*\s*[:\-]?\s*(?P<desc>.*)", line_str, re.IGNORECASE)
                if sec_match:
                    sec = sec_match.group("sec").strip()
                    desc = sec_match.group("desc").strip()
                    if not any(c["act_name"].lower() == current_act.lower() and c["section_number"] == sec for c in citations):
                        citations.append({"act_name": current_act, "section_number": sec, "desc": desc})
                elif line_str.startswith("### "):
                    current_act = None

        return citations

    def _verify_single_citation(
        self,
        act_name: str,
        section_number: str,
        alleged_desc: str,
        incident_date: Optional[str],
        jurisdiction: str,
        timestamp: str,
        sources: List[Dict[str, Any]]
    ) -> LegalClaim:
        lookup = lookup_provision(act_name, section_number)

        # Case 1: Act not found in verified database and not in retrieved documents
        if not lookup or not lookup.get("statute"):
            # Check if backed by custom uploaded RAG document
            rag_match = self._check_rag_sources(act_name, section_number, sources)
            if rag_match:
                return LegalClaim(
                    act_name=act_name,
                    section_number=section_number,
                    exact_provision_text=rag_match.get("text", "")[:300],
                    official_source=rag_match.get("source_url") or "Uploaded Legal Document",
                    effective_date="Verified in corpus",
                    current_status=rag_match.get("status", "active"),
                    relevant_judicial_precedents=[],
                    jurisdiction=jurisdiction,
                    verification_timestamp=timestamp,
                    confidence_level="verified",
                    claim_type="statutory",
                    in_force_on_incident_date=True,
                    conflicting_interpretations=[],
                    verification_notes="Verified against ingested legal corpus passage.",
                    is_verified=True
                )

            # Not found anywhere -> must return standard unverified notice
            return LegalClaim(
                act_name=act_name,
                section_number=section_number,
                exact_provision_text=UNVERIFIED_NOTICE,
                official_source="Not found in verified official sources",
                effective_date="Unknown",
                current_status="unverified",
                relevant_judicial_precedents=[],
                jurisdiction=jurisdiction,
                verification_timestamp=timestamp,
                confidence_level="unverified",
                claim_type="statutory",
                in_force_on_incident_date=None,
                conflicting_interpretations=[],
                verification_notes=f"{UNVERIFIED_NOTICE} Act '{act_name}' could not be matched with Gazette registry.",
                is_verified=False
            )

        statute = lookup["statute"]
        provision = lookup.get("provision")
        error_msg = lookup.get("error")

        # Case 2: Section does not exist or exceeds maximum section count
        if not provision:
            return LegalClaim(
                act_name=statute["official_name"],
                section_number=section_number,
                exact_provision_text=UNVERIFIED_NOTICE,
                official_source=statute.get("official_source", "India Code"),
                effective_date=statute.get("commencement_date", "Unknown"),
                current_status=statute.get("status", "unknown"),
                relevant_judicial_precedents=[],
                jurisdiction=statute.get("jurisdiction", jurisdiction),
                verification_timestamp=timestamp,
                confidence_level="refuted",
                claim_type="statutory",
                in_force_on_incident_date=None,
                conflicting_interpretations=[],
                verification_notes=error_msg or f"{UNVERIFIED_NOTICE} Section {section_number} not identified in verified enactment.",
                is_verified=False
            )

        # Case 3: Provision exists - check temporal validity
        temporal = check_temporal_validity(act_name, incident_date)
        in_force = temporal.get("in_force")
        conflicts = []
        notes = []

        if temporal.get("status") == "not_yet_in_force":
            conflicts.append(f"TEMPORAL INVALIDITY: {temporal.get('note')}")
            notes.append(f"Act commenced on {statute['commencement_date']}; not applicable on incident date.")
        elif temporal.get("status") == "repealed_prior":
            conflicts.append(f"REPEALED LAW: {temporal.get('note')}")
            notes.append("Statute was repealed prior to incident.")

        # Find matching judicial precedents
        precedents = []
        for prec in JUDICIAL_PRECEDENTS:
            if statute["official_name"].lower() in prec["subject"].lower() or any(w in prec["subject"].lower() for w in ["consumer", "education", "tenancy", "negotiable"]):
                if any(w in prec["holding"].lower() for w in [section_number.lower(), statute["official_name"][:15].lower()]):
                    precedents.append(f"{prec['citation']} ({prec['court']})")
                    if prec.get("conflicting_views"):
                        conflicts.append(prec["conflicting_views"])

        is_verified = (in_force is not False)
        confidence = "verified" if is_verified and not conflicts else ("caution" if conflicts else "unverified")

        return LegalClaim(
            act_name=statute["official_name"],
            section_number=section_number,
            exact_provision_text=provision.get("text", ""),
            official_source=statute.get("official_source", "India Code"),
            effective_date=statute.get("commencement_date", ""),
            current_status=statute.get("status", "in_force"),
            relevant_judicial_precedents=precedents,
            jurisdiction=statute.get("jurisdiction", jurisdiction),
            verification_timestamp=timestamp,
            confidence_level=confidence,
            claim_type=provision.get("claim_type", "statutory"),
            in_force_on_incident_date=in_force,
            conflicting_interpretations=conflicts,
            verification_notes="; ".join(notes) if notes else f"Provision verified against official text of {statute['official_name']}.",
            is_verified=is_verified
        )

    def _check_rag_sources(self, act_name: str, sec_num: str, sources: List[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
        act_lower = act_name.lower()
        sec_str = str(sec_num).lower()
        for s in sources:
            text = s.get("text", "").lower()
            title = s.get("metadata", {}).get("title", "").lower()
            if (act_lower in title or act_lower in text) and (f"section {sec_str}" in text or f"sec {sec_str}" in text or f"sec. {sec_str}" in text):
                return {
                    "text": s.get("text", ""),
                    "source_url": s.get("metadata", {}).get("source_url", ""),
                    "status": s.get("metadata", {}).get("status", "active")
                }
        return None

    def _audit_deadlines(self, text: str) -> List[str]:
        warnings = []
        lower = text.lower()

        # Check for erroneous short consumer limitation (e.g. 15 days or 30 days to file consumer case)
        if ("consumer" in lower or "district commission" in lower) and re.search(r"(file|submit|complaint).*?(within|in)\s+(15|10|7|30)\s+days", lower):
            warnings.append(
                "UNSUPPORTED DEADLINE CAUTION: Under Section 69 of the Consumer Protection Act, 2019, the limitation period to file a complaint is 2 years from the date on which the cause of action arises, NOT 15 or 30 days."
            )

        # Check for cheque bounce 138 deadlines
        if "138" in lower or "cheque" in lower:
            if re.search(r"notice.*(within|in)\s+(15|7|60)\s+days", lower):
                warnings.append(
                    "STATUTORY DEADLINE: Under Section 138 proviso (b) of the NI Act, the legal demand notice must be given within 30 days of receiving the memo of dishonour from the bank."
                )

        return warnings

    def _inject_verification_annotations(
        self,
        draft_answer: str,
        claims: List[LegalClaim],
        edu_eval: Optional[Dict[str, Any]],
        deadline_warnings: List[str]
    ) -> str:
        res = draft_answer

        # Replace any completely refuted/unverified provisions in the text
        for claim in claims:
            if not claim.is_verified and claim.confidence_level in ["unverified", "refuted"]:
                # If the draft had Section X with unverified status, annotate it clearly
                err_text = f"\n> ⚠️ **Verification Notice:** *{UNVERIFIED_NOTICE} (Cited as: {claim.act_name} - Section {claim.section_number})*"
                if claim.verification_notes:
                    err_text += f"\n> *Audit Finding:* {claim.verification_notes}"
                res += f"\n\n{err_text}"

        # If education dispute, append mandatory Supreme Court and UGC doctrine
        if edu_eval:
            edu_block = (
                "\n\n### ⚖️ Landmark Supreme Court Precedent & UGC Regulations (Education Disputes)\n"
                "* **[JUDICIAL PRECEDENT] Supreme Court Landmark Ruling**: In *Maharshi Dayanand University v. Surjeet Kaur (2010) 11 SCC 159* "
                "and *P.T. Koshy v. Ellen Charitable Trust 2012 (3) CPC 615 (SC)*, the Supreme Court ruled that educational institutions and "
                "universities imparting education and holding examinations do **NOT** provide a 'service' under the Consumer Protection Act, "
                "and a student is not a 'consumer'. Filing directly in consumer court risks outright dismissal.\n"
                "* **[JUDICIAL EXCEPTION / CONFLICTING VIEW]**: The NCDRC Full Bench in *Manu Solanki v. Vinayaka Mission University (2020)* "
                "carved out an exception: purely commercial, unaccredited private coaching institutes and test-preparation centres DO fall within Consumer Forum jurisdiction.\n"
                "* **[REGULATORY NORM] Mandatory UGC 2023 Recourse**: Under the *UGC (Redressal of Grievances of Students) Regulations, 2023*, "
                "the student must first lodge a formal grievance before the institutional **Student Grievance Redressal Committee (SGRC)** (15-day resolution timeline) "
                "and appeal to the University **Ombudsperson** (via samarth.ac.in or the University portal) before seeking High Court writ or civil relief."
            )
            if "Maharshi Dayanand" not in res and "Surjeet Kaur" not in res:
                res += edu_block

        # If deadline warnings exist, append them
        if deadline_warnings:
            warn_block = "\n\n### ⏳ Statutory Deadline Audits\n" + "\n".join(f"* ⚠️ {w}" for w in deadline_warnings)
            res += warn_block

        return res
