# NyayaAI – System Architecture & Multi-Agent RAG Design

## 1. Architectural Overview

NyayaAI is an enterprise-grade Indian Legal Intelligence and Citizen Assistance Platform built on **Deep Learning Semantic Retrieval**, **Section-Aware Statutory Chunking**, and a **10-Agent LangGraph-Style Pipeline** with **Deterministic Legal Citation Verification**.

The system is designed to provide ordinary Indian citizens, legal practitioners, and researchers with precise, hallucination-free legal guidance, statutory rights, limitation periods, evidence requirements, and ready-to-file complaint notices.

```
USER QUESTION (Multilingual: EN, HI, TA, TE, ML, KN)
   │
   ▼
[Language Processing & Entity Extraction]
   │
   ▼
[10-Agent Pipeline: Stage 1 — Domain & Entity Classification]
   │
   ▼
[Hybrid Retrieval Engine]
   ├──────────────────────────────┬──────────────────────────────┐
   ▼                              ▼                              ▼
[Okapi BM25 Lexical]    [Dense Vector Search]     [Legal Metadata Filtering]
   │ (k1=1.5, b=0.75)             │ (Gemini 768-d)               │ (Jurisdiction/Status)
   └──────────────────────────────┴──────────────────────────────┘
                                  │
                                  ▼
               [Reciprocal Rank Fusion (RRF, k=60)]
                                  │
                                  ▼
             [Cross-Encoder Legal Heuristic Reranker]
                                  │
                                  ▼
     [Top-K Hierarchical Statutory Chunks & Precedent Digests]
                                  │
                                  ▼
     [Multi-Agent Deliberation & Verification Chain (Agents 3–8)]
        ├─ Status Verification (Gazette in-force check)
        ├─ Judicial Precedents (SC/HC holdings, e.g., Surjeet Kaur)
        ├─ Jurisdictional Exceptions & Applicability
        ├─ Evidence Identification (UTRs, stamps, paper trail)
        ├─ Action Planning (Informal -> Statutory Authority -> Court)
        └─ Deadline Verification (Statutory limitation audits)
                                  │
                                  ▼
     [Agent 9: Independent Legal Citation Verification Agent]
        ├─ Max section boundary check (rejection of non-existent sections)
        ├─ Temporal validity & ex-post facto check (Art 20(1), BNS vs IPC)
        ├─ Repealed law detection (e.g., CPA 1986 -> CPA 2019)
        ├─ Education dispute gate (UGC 2023 Reg 5/6 & Surjeet Kaur)
        └─ Audit verdict: PASSED | CAUTION | REFUTED
                                  │
                                  ▼
     [Agent 10: Citizen Response Synthesis & Visual Formatting]
        ├─ Visual badging ([STATUTE], [JUDICIAL PRECEDENT], [REGULATORY NORM])
        ├─ Interactive Evidence Checklist
        ├─ Stepper Action Timeline
        ├─ Limitation Warning Alerts
        └─ Formal Notice & Complaint Letter Draft
```

---

## 2. Multi-Agent Pipeline Specifications

The deliberation pipeline consists of 10 specialized agent roles operating sequentially over a shared `LegalAgentState`:

| Agent # | Agent Name | Primary Responsibility | Output Artifact |
|---|---|---|---|
| **1** | **Legal Intent & Domain Classifier** | Classifies legal domain across 15 priority areas, user persona, and extracts critical dates. | Domain tag, user persona, incident date. |
| **2** | **Hybrid Legal Research Agent** | Queries Okapi BM25 index and dense vector space, fusing results with Reciprocal Rank Fusion (RRF). | Top-7 statutory excerpts & Gazette notifications. |
| **3** | **Legislative Status Agent** | Validates enactment commencement, amendment history, and repeal status against India Code registry. | Temporal validity confirmation (`in_force`). |
| **4** | **Judicial Precedent Agent** | Analyzes binding Supreme Court rulings, High Court exceptions, and statutory overrides. | Precedent holdings (e.g., *Surjeet Kaur*, *Lalita Kumari*, *Rajnesh v. Neha*). |
| **5** | **Jurisdictional Applicability Agent** | Distinguishes statutory rights from discretionary reliefs and consumer vs regulatory forums. | Forum identification & threshold checks. |
| **6** | **Evidence Identification Agent** | Compiles exhaustive digital and documentary evidence checklists required for complaint survival. | Evidence checklist (UTRs, statements, notices). |
| **7** | **Action Planning Agent** | Outlines graduated escalation steps from internal grievance to statutory commissions. | Stepper roadmap with escalation paths. |
| **8** | **Statutory Deadline Auditor** | Audits claims against Indian limitation statutes (CPA Sec 69, NI Act Sec 138, RTI Sec 7/19). | Limitation period warnings & cut-off dates. |
| **9** | **Independent Citation Verifier** | Performs deep verification of every cited Act, section, and deadline against primary sources. | Full audit verdict, claim table, rejection notices. |
| **10** | **Citizen Response Synthesizer** | Assembles citizen-friendly visual presentation with structured cards, quick tips, and printable notice. | Final structured HTML/Markdown response. |

---

## 3. Hybrid Retrieval Architecture

### A. Okapi BM25 Lexical Retrieval
- Custom zero-dependency pure-Python implementation (`app.services.hybrid_retriever.BM25Retriever`).
- Tuned parameters: `k1 = 1.5`, `b = 0.75`.
- Normalized Indian legal tokenization preserving section numbers (e.g., `138`, `35`, `66d`, `125`).

### B. Dense Vector Retrieval
- Embeddings: Google Gemini `gemini-embedding-001` (768 dimensions) with cosine distance metric.
- Dual storage engine:
  - **Primary Production**: PostgreSQL 16 + `pgvector` extension.
  - **Embedded / Local Dev**: Pure SQLite vector store (`SQLiteVectorStore` in `data/vectors.db`) with zero external C++ build dependencies.

### C. Reciprocal Rank Fusion (RRF)
Merges ranked lists from lexical and dense vector search without requiring score calibration:
$$RRF(d) = \sum_{m \in M} \frac{1}{60 + r_m(d)}$$

### D. Legal Cross-Encoder Heuristic Reranker
Re-scores candidates by evaluating:
- Exact section number matches (`+0.35` boost)
- In-force status (`+0.15` boost)
- Repealed statute penalty (`-0.50` penalty)
- Jurisdiction alignment (`+0.10` boost)

---

## 4. Fallback & Resilience Strategy

1. **Zero-Hallucination Fallback**: If no relevant primary statute is indexed for an obscure query, the system explicitly returns:
   > *"NyayaAI could not find a relevant source in the legal repository and will not guess. Please upload the relevant Act or consult a qualified advocate."*
2. **Offline Graceful Degradation**: When network access is restricted or LLM quota is exhausted, the system automatically transitions to the deterministic rule-based statutory synthesizer, ensuring 100% test passing and zero service downtime.

