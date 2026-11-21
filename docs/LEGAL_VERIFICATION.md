# NyayaAI – Legal Citation Verification & Audit Agent

## 1. Zero-Hallucination Mandate

In legal applications, a plausible-sounding hallucinated section or limitation deadline can cause a citizen to forfeit their statutory cause of action or file in the wrong forum.

**NyayaAI strictly forbids unverified AI generation.** An answer is never marked "verified" merely because an LLM generated a convincing paragraph. Every cited Act, section, and procedural claim must pass an independent citation audit against authoritative primary sources.

If an Act or section cannot be verified against the official statutory registry, the system returns:
> *"Unable to verify this legal provision from the available official sources."*

---

## 2. Verification Rules & Logic

The **Legal Citation Verification Agent** (`backend/app/agents/citation_verifier.py`) enforces 6 independent verification gates:

### Gate 1: Out-of-Range & Non-Existent Section Numbers
- Validates cited section numbers against the total section count of the Act in `STATUTES_REGISTRY`.
- Example: The Consumer Protection Act, 2019 only has 107 sections. If an LLM cites "Section 138 of the Consumer Protection Act", it is immediately detected as out of bounds, refuted, and replaced with an unverified notice.

### Gate 2: Temporal Validity & Ex-Post Facto Bar (Constitution Art. 20(1))
- Evaluates the date of the incident against the commencement date of the Act.
- Example: The Bharatiya Nyaya Sanhita, 2023 (BNS) came into force on **1 July 2024**. For an offence committed on 10 March 2024, BNS cannot be applied prospectively pursuant to Article 20(1) of the Constitution of India. Substantive charges must be filed under the Indian Penal Code, 1860 (IPC).

### Gate 3: Repealed Laws Detection
- Detects citations to repealed statutes for incidents occurring after the repeal date.
- Example: The Consumer Protection Act, 1986 was repealed in July 2020 by the Consumer Protection Act, 2019. Citing the 1986 Act for a 2024 dispute triggers a warning alert with the successor Act mapping.

### Gate 4: Unsupported Procedural Deadlines
- Audits generated procedural time limits against statutory limitation periods.
- Rejects hallucinated limitation deadlines (e.g., claiming a consumer complaint must be filed within 15 days) and injects the statutory rule (Section 69 CPA mandates a 2-year limitation period).

### Gate 5: Education Dispute Gate (UGC Regulations vs. Consumer Forums)
- College, university, degree, and examination fee disputes trigger mandatory statutory evaluation:
  1. **Supreme Court Precedent**: *Maharshi Dayanand University v. Surjeet Kaur (2010) 11 SCC 159* and *P.T. Koshy (2012) 3 SCC 797* hold that education is not a "service" and students are not "consumers" under the Consumer Protection Act.
  2. **Primary Recourse**: Student Grievance Redressal Committee (SGRC) and University Ombudsperson under the **UGC (Redressal of Grievances of Students) Regulations, 2023** (mandatory 15-day timeline).
  3. **Judicial Exception**: Private coaching centers fall under consumer forums pursuant to *Manu Solanki (2020) NCDRC*.

### Gate 6: Mandatory Output Metadata
Every single verified legal claim carries structured metadata:
- **Act Name**
- **Section Number**
- **Exact Provision Text**
- **Official Source URL / Gazette Citation**
- **Effective Date**
- **Current Status** (`in_force`)
- **Relevant Judicial Precedents**
- **Jurisdiction**
- **Verification Timestamp**
- **Confidence Level** (`verified`, `caution`, `unverified`, `refuted`)

---

## 3. Verification State & Summary Structure

```json
{
  "total_claims_detected": 3,
  "verified_claims_count": 3,
  "unverified_claims_count": 0,
  "education_dispute_evaluated": true,
  "audit_verdict": "Passed",
  "claims": [
    {
      "act_name": "UGC (Redressal of Grievances of Students) Regulations, 2023",
      "section_number": "5",
      "exact_provision_text": "Regulation 5. Student Grievance Redressal Committees (SGRC)...",
      "official_source": "https://www.ugc.gov.in/pdfnews/9152473_ugc-regulations-2023.pdf",
      "effective_date": "2023-04-11",
      "current_status": "in_force",
      "relevant_judicial_precedents": [
        "MDU v. Surjeet Kaur (2010) 11 SCC 159",
        "P.T. Koshy v. Ellen Charitable Trust (2012) 3 SCC 797"
      ],
      "jurisdiction": "India",
      "verification_timestamp": "2026-11-20T13:30:00Z",
      "confidence_level": "verified",
      "claim_type": "regulatory_norm"
    }
  ]
}
```

