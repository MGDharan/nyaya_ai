# NyayaAI — Deep Learning + Agentic RAG Indian Legal Intelligence Platform

[![Python](https://img.shields.io/badge/Python-3.10%20%7C%203.11%20%7C%203.12%20%7C%203.15-blue.svg)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115+-009688.svg)](https://fastapi.tiangolo.com)
[![Tests](https://img.shields.io/badge/Tests-14%2F14%20Passed%20(100%25)-brightgreen.svg)]()
[![Benchmark](https://img.shields.io/badge/Legal%20Benchmark-15%2F15%20Passed%20(100%25)-success.svg)]()
[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](LICENSE)

NyayaAI is a production-oriented, modular, and scalable Indian Legal Intelligence and Citizen Assistance Platform built on **Deep-Learning Semantic Retrieval**, **Section-Aware Statutory Ingestion**, and a **10-Agent LangGraph-Style Deliberation Pipeline** with **Deterministic Legal Citation Verification**.

---

## 🌟 Key Capabilities

1. **Multilingual Legal Assistance**:
   Supports citizen inquiries in English, Hindi (हिन्दी), Tamil (தமிழ்), Telugu (తెలుగు), Malayalam (മലയാളം), and Kannada (ಕನ್ನಡ).
2. **Hybrid RAG Retrieval Engine**:
   - Pure-Python **Okapi BM25** Lexical Retrieval ($k_1=1.5, b=0.75$).
   - Normalized 768-dimensional **Dense Vector Embeddings** (Google Gemini).
   - **Reciprocal Rank Fusion (RRF, $k=60$)** combining lexical & dense vector candidates.
   - **Cross-Encoder Legal Heuristic Reranker** prioritizing in-force statutes and exact section numbers.
3. **Section-Aware Hierarchical Statute Chunking**:
   Preserves legislative context (Act title, Chapter, Section, Subsection, Provisos, and Explanations). Zero arbitrary text chunking.
4. **10-Agent Deliberation Pipeline**:
   - Agent 1: Legal Intent & Domain Classifier (15 priority legal domains)
   - Agent 2: Hybrid Legal Research Agent (Top-7 hierarchical statute excerpts)
   - Agent 3: Legislative Status Agent (Gazette `in_force` validation)
   - Agent 4: Judicial Precedent Agent (Binding Supreme Court / High Court holdings)
   - Agent 5: Jurisdictional Applicability Agent (Forums & financial limits)
   - Agent 6: Evidence Identification Agent (Paper trails, UTRs, bank stamps)
   - Agent 7: Action Planning Agent (Graduated escalation roadmap)
   - Agent 8: Statutory Deadline Auditor (Limitation period checks)
   - Agent 9: Independent Citation Verifier (Rejection of non-existent sections)
   - Agent 10: Citizen Response Synthesizer (Visual cards, badges, steppers)
5. **Independent Legal Citation Verification**:
   - Rejection of out-of-bounds section numbers (e.g. CPA 2019 Section 138).
   - Enforces Article 20(1) constitutional bar against retroactive criminal penalties (IPC 1860 vs. BNS 2023).
   - Rejection of repealed statutes (CPA 1986 -> CPA 2019).
   - Mandatory evaluation of UGC Regulations 2023 and Supreme Court precedents (*MDU v. Surjeet Kaur (2010)*, *P.T. Koshy (2012)*) before consumer litigation in educational disputes.
6. **Formal Statutory Complaint Letter Generator (7 Templates)**:
   - College Examination & Fee Grievance (UGC 2023)
   - Cheque Bounce Statutory Demand Notice (Section 138 NI Act)
   - Consumer Forum Formal Complaint (Section 35 CPA)
   - Cybercrime & UPI Fraud Bank Notice
   - Tenancy Security Deposit Refund Notice (TNRRLTA Section 10(2))
   - Unpaid Salary Recovery Notice (Payment of Wages Act Section 15)
   - RTI Formal Application (Section 6(1) RTI Act)
7. **Citizen-Friendly Interactive UI**:
   Visual summary cards, badges (`[STATUTE]`, `[JUDICIAL PRECEDENT]`, `[REGULATORY NORM]`), interactive evidence checklists, Do's & Don'ts grid, and print/PDF export.

---

## 🚀 Quick Start (Local Development)

### 1. Prerequisites
- Python 3.10+ (Fully compatible with Python 3.15 on Windows, macOS, and Linux).
- Google Gemini API Key.

### 2. Setup Virtual Environment
```powershell
cd backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1   # On Windows
# source .venv/bin/activate    # On Linux/macOS

# Install dependencies (zero C++ compiler dependencies required)
pip install -r requirements-local.txt
```

### 3. Configure Environment
Create or edit `backend/.env`:
```env
APP_NAME=NyayaAI
LLM_PROVIDER=gemini
GEMINI_API_KEY=your_gemini_api_key_here
GEMINI_MODEL=gemini-2.5-flash
DATA_DIR=./data
TOP_K=7
```

### 4. Index Legislation Corpus & Run Tests
```powershell
# Index 40 statutory section chunks across all 15 legal domains
python scripts/reingest_all.py

# Run all 14 automated unit tests
python -m pytest tests -v

# Run the 15-scenario legal evaluation benchmark
python scripts/run_benchmark.py
```

### 5. Launch the Web Application
```powershell
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```
Open your browser at: **`http://localhost:8000`**

---

## 🐳 Docker Deployment (Production)

To deploy the full containerized stack with PostgreSQL and pgvector:
```bash
docker compose up --build -d
```

---

## 📊 Benchmark & Evaluation Results

NyayaAI is evaluated against a 15-scenario benchmark covering real-world Indian legal disputes:
- **Total Scenarios Evaluated**: 15
- **Passed Scenarios**: 15
- **Pass Rate**: **100.0%**
- **Test Suite Pass Rate**: **14 / 14 (100.0%)**

---

## 📚 Documentation Suite

Complete technical and operational manuals are available in the [`docs/`](file:///d:/sanddisk/projects/WORK OUT PROJECT/NyayaAI_Project/nyayaai/docs/) directory:
- [System Architecture](file:///d:/sanddisk/projects/WORK OUT PROJECT/NyayaAI_Project/nyayaai/docs/ARCHITECTURE.md)
- [Database Schema & Models](file:///d:/sanddisk/projects/WORK OUT PROJECT/NyayaAI_Project/nyayaai/docs/DATABASE_SCHEMA.md)
- [Data Ingestion & Section Chunker](file:///d:/sanddisk/projects/WORK OUT PROJECT/NyayaAI_Project/nyayaai/docs/DATA_INGESTION.md)
- [Legal Citation Verification Agent](file:///d:/sanddisk/projects/WORK OUT PROJECT/NyayaAI_Project/nyayaai/docs/LEGAL_VERIFICATION.md)
- [Automated Testing & Benchmark](file:///d:/sanddisk/projects/WORK OUT PROJECT/NyayaAI_Project/nyayaai/docs/TESTING.md)
- [REST API Documentation](file:///d:/sanddisk/projects/WORK OUT PROJECT/NyayaAI_Project/nyayaai/docs/API_DOCUMENTATION.md)
- [Deployment Guide](file:///d:/sanddisk/projects/WORK OUT PROJECT/NyayaAI_Project/nyayaai/docs/DEPLOYMENT.md)
- [Citizen & Practitioner User Guide](file:///d:/sanddisk/projects/WORK OUT PROJECT/NyayaAI_Project/nyayaai/docs/USER_GUIDE.md)

---

## ⚖️ Legal Disclaimer

NyayaAI provides legal information and intelligence based on official Indian statutes, Gazette notifications, and reported judicial precedents. It is designed to assist citizens and legal researchers. It does not constitute formal legal representation or create an attorney-client relationship. Users should consult an enrolled advocate for contentious litigation.
