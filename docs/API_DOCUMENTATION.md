# NyayaAI – REST API Documentation

Base URL: `http://localhost:8000`

---

## 1. Core Endpoints

### `POST /api/chat`
Processes citizen legal inquiries through the 10-Agent verification workflow.

#### Request Body
```json
{
  "question": "I paid ₹200 for my college exam fee through UPI, but the college refuses my hall ticket. What can I do?",
  "language": "English",
  "jurisdiction": "India",
  "date_of_incident": "2026-11-10",
  "context": "Payment receipt available with SBI reference number."
}
```

#### Response (`200 OK`)
```json
{
  "answer": "### 📌 Quick Summary\n...",
  "sources": [
    {
      "title": "UGC (Redressal of Grievances of Students) Regulations, 2023",
      "jurisdiction": "India",
      "document_type": "regulation",
      "status": "in_force",
      "source_url": "https://www.ugc.gov.in/...",
      "chunk_excerpt": "Regulation 5. Student Grievance Redressal Committees..."
    }
  ],
  "agents": [
    {"agent": "Legal Intent & Domain Classifier", "status": "completed", "note": "Domain identified..."},
    {"agent": "Independent Citation Verification Agent", "status": "completed", "note": "Audited 3 legal claims..."}
  ],
  "confidence": "10-Agent Verified RAG · Citation Audit: Passed",
  "disclaimer": "NyayaAI provides legal intelligence based on official Indian statutes...",
  "claims": [
    {
      "act_name": "UGC (Redressal of Grievances of Students) Regulations, 2023",
      "section_number": "5",
      "exact_provision_text": "Regulation 5...",
      "official_source": "https://www.ugc.gov.in/...",
      "effective_date": "2023-04-11",
      "current_status": "in_force",
      "relevant_judicial_precedents": ["MDU v. Surjeet Kaur (2010) 11 SCC 159"],
      "jurisdiction": "India",
      "confidence_level": "verified",
      "claim_type": "regulatory_norm"
    }
  ],
  "verification_summary": {
    "total_claims_detected": 3,
    "verified_claims_count": 3,
    "unverified_claims_count": 0,
    "education_dispute_evaluated": true,
    "audit_verdict": "Passed"
  }
}
```

---

### `POST /api/generate-complaint`
Generates a structured, legally sound formal notice or grievance complaint letter ready for signing and dispatch.

#### Supported Template Types:
- `college_exam`: UGC Student Grievance Redressal Notice
- `cheque_bounce`: Section 138 Negotiable Instruments Act Statutory Demand Notice
- `consumer_cpa`: Section 35 Consumer Protection Act Complaint Notice
- `cyber_fraud`: National Cyber Crime Reporting Portal & Bank Incident Notice
- `rent_deposit`: Section 10(2) Tenancy Security Deposit Refund Demand Notice
- `unpaid_salary`: Section 15 Payment of Wages Act Formal Demand Letter
- `rti_application`: Section 6(1) Right to Information Formal Application

#### Request Body
```json
{
  "template_type": "college_exam",
  "user_name": "Rahul Sharma",
  "user_address": "123 Anna Nagar, Chennai",
  "user_contact": "rahul@example.com",
  "opposite_party_name": "ABC Engineering College",
  "opposite_party_address": "GST Road, Chennai",
  "incident_date": "2026-11-10",
  "amount": "₹200",
  "transaction_ref": "UPI/1234567890/SBI",
  "facts_summary": "Fee debited via UPI, but college refused hall ticket.",
  "relief_sought": "Grant hall ticket and admit to examination."
}
```

#### Response (`200 OK`)
```json
{
  "template_type": "college_exam",
  "title": "Grievance Representation to SGRC under UGC Regulations, 2023",
  "statutory_act": "UGC (Redressal of Grievances of Students) Regulations, 2023",
  "governing_section": "Regulation 5 & 6",
  "prescribed_timeline": "15 days for SGRC recommendations",
  "recipient_authority": "Student Grievance Redressal Committee (SGRC) / Principal",
  "escalation_forum": "University Ombudsperson / UGC e-Samadhaan Portal",
  "text_content": "To,\nThe Convener, Student Grievance Redressal Committee (SGRC)...\n\nSUBJECT: URGENT GRIEVANCE..."
}
```

---

### `GET /api/eval/benchmark`
Retrieves the list of 15 standard Indian legal evaluation scenarios.

---

### `POST /api/eval/run`
Executes automated benchmark evaluation over registered test scenarios and returns scores, matched provisions, and violation checks.

---

### `GET /api/documents`
Lists all indexed primary statutes, Gazette notifications, and court precedent digests.

---

### `GET /api/health`
System health check endpoint returning service status, corpus document count, and architecture metadata.

