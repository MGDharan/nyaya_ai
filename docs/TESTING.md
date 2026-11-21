# NyayaAI – Automated Testing & Benchmark Evaluation Guide

## 1. Test Suite Structure

The platform incorporates comprehensive automated test suites covering core chunking, pure-Python BM25, multi-agent pipeline execution, independent citation verification, and a 15-scenario real-world benchmark suite.

```
backend/tests/
  ├── test_core.py                  # Chunking & fallback verification
  ├── test_hybrid_and_agents.py     # BM25, Section Chunker, 10-Agent Pipeline, Complaint Generator
  └── test_verification.py          # Citation verifier (out-of-range sections, repealed laws, temporal checks)
```

---

## 2. Test Execution

To execute the full test suite via `pytest`:
```bash
cd backend
.\.venv\Scripts\python.exe -m pytest tests -v
```

### Current Test Suite Results (14 / 14 Passed):
- `tests/test_core.py::test_chunk_text_returns_content` **PASSED**
- `tests/test_core.py::test_no_source_fallback_does_not_invent_law` **PASSED**
- `tests/test_hybrid_and_agents.py::test_bm25_tokenize_and_search` **PASSED**
- `tests/test_hybrid_and_agents.py::test_section_aware_chunker` **PASSED**
- `tests/test_hybrid_and_agents.py::test_complaint_generator_college_grievance` **PASSED**
- `tests/test_hybrid_and_agents.py::test_benchmark_scenarios_structure` **PASSED**
- `tests/test_hybrid_and_agents.py::test_multi_agent_pipeline_execution` **PASSED**
- `tests/test_verification.py::TestCitationVerification::test_incorrect_section_numbers_rejected` **PASSED**
- `tests/test_verification.py::TestCitationVerification::test_repealed_laws_detected` **PASSED**
- `tests/test_verification.py::TestCitationVerification::test_commencement_dates_checked` **PASSED**
- `tests/test_verification.py::TestCitationVerification::test_unsupported_deadlines_flagged` **PASSED**
- `tests/test_verification.py::TestCitationVerification::test_education_dispute_evaluates_ugc_and_sc_precedents` **PASSED**
- `tests/test_verification.py::TestCitationVerification::test_hallucinated_citation_rejected_with_standard_notice` **PASSED**
- `tests/test_verification.py::TestCitationVerification::test_mandatory_metadata_attributes_present` **PASSED**

---

## 3. 15-Scenario Legal Evaluation Benchmark

The benchmark harness (`backend/app/services/legal_benchmark.py`) tests the system against 15 complex, real-world Indian legal disputes across diverse domains:

| ID | Legal Domain | Scenario Title | Pass Status | Score |
|---|---|---|---|---|
| `scenario_01` | Education Law | College examination fee UPI debit discrepancy | **PASS** | 90% |
| `scenario_02` | Education Law | Withholding of original degree certificates | **PASS** | 100% |
| `scenario_03` | Administrative Law | Government office delay in issuing driving license | **PASS** | 90% |
| `scenario_04` | Labour Law | Unpaid salary after resignation | **PASS** | 90% |
| `scenario_05` | Labour Law | Maternity leave termination of employment | **PASS** | 90% |
| `scenario_06` | Criminal Law | Police refusal to register FIR for phone snatching | **PASS** | 100% |
| `scenario_07` | Cybercrime | Morphed obscene photographs sent on social media | **PASS** | 100% |
| `scenario_08` | Consumer Law | Defective laptop delivered by e-commerce marketplace | **PASS** | 100% |
| `scenario_09` | Banking Law | Unauthorized bank debit via fraudulent UPI request | **PASS** | 100% |
| `scenario_10` | Cybercrime | Fraudulent job offer letter charging security deposit | **PASS** | 100% |
| `scenario_11` | Tenancy Law | Landlord refusing to return rental security deposit | **PASS** | 100% |
| `scenario_12` | Family Law | Interim maintenance for deserted wife and minor child | **PASS** | 100% |
| `scenario_13` | Criminal Law | Pre-July 2024 crime: Old (IPC) vs new (BNS) law | **PASS** | 85% |
| `scenario_14` | Financial Law | Cheque bounce: Demand notice requirement before case | **PASS** | 70% |
| `scenario_15` | Civil Recovery | Ambiguous monetary dispute requiring fact extraction | **PASS** | 100% |

**Overall Benchmark Pass Rate: 100.0% (15 / 15 Scenarios Passed)**

To execute the benchmark script:
```bash
cd backend
.\.venv\Scripts\python.exe scripts/run_benchmark.py
```

