"""
Comprehensive Test Suite for Hybrid Search, Section Chunker, and Multi-Agent Pipeline.
"""

import pytest
from app.services.hybrid_retriever import BM25Retriever, reciprocal_rank_fusion, legal_rerank, tokenize
from app.services.section_chunker import chunk_legal_statute_section_aware
from app.services.complaint_generator import generate_complaint_letter
from app.services.legal_benchmark import LEGAL_BENCHMARK_SCENARIOS, evaluate_response_against_scenario
from app.agents.multi_agent_pipeline import NyayaMultiAgentPipeline, LegalAgentState


def test_bm25_tokenize_and_search():
    docs = [
        {"text": "Section 138 of Negotiable Instruments Act deals with dishonour of cheque."},
        {"text": "Section 35 of Consumer Protection Act relates to filing complaints before District Commission."},
        {"text": "UGC Regulations 2023 provide Student Grievance Redressal Committee."}
    ]
    bm25 = BM25Retriever()
    bm25.fit(docs)
    assert bm25.total_docs == 3

    results = bm25.search("cheque bounce dishonour 138", top_k=2)
    assert len(results) > 0
    assert "Negotiable Instruments" in results[0]["text"]
    assert results[0]["bm25_score"] > 0


def test_section_aware_chunker():
    sample_statute = """
THE CONSUMER PROTECTION ACT, 2019
CHAPTER I: PRELIMINARY
Section 2. Definitions.
(7) "consumer" means any person who buys any goods or avails services.
Section 35. Manner in which complaint shall be made.
A complaint may be filed with District Commission by consumer.
Provided that complaint must contain verified facts.
    """
    chunks = chunk_legal_statute_section_aware(sample_statute, default_act_title="Consumer Protection Act, 2019")
    assert len(chunks) >= 2
    sec_numbers = [c["section_number"] for c in chunks]
    assert "2" in sec_numbers or "35" in sec_numbers
    # Check proviso extraction
    c35 = next((c for c in chunks if c["section_number"] == "35"), None)
    if c35:
        assert len(c35["provisos"]) > 0 or "Provided that" in c35["text"]


def test_complaint_generator_college_grievance():
    letter = generate_complaint_letter(
        template_type="college_exam",
        user_name="Rahul Sharma",
        user_address="123 Anna Nagar, Chennai",
        user_contact="rahul@example.com",
        opposite_party_name="ABC Engineering College",
        opposite_party_address="GST Road, Chennai",
        incident_date="2026-11-10",
        amount="₹200",
        transaction_ref="UPI/1234567890/SBI",
        facts_summary="Fee debited from SBI account via UPI, but college refused hall ticket.",
        relief_sought="Grant hall ticket and admit to university examination."
    )
    assert letter["template_type"] == "college_exam"
    assert "UGC (Redressal of Grievances of Students) Regulations, 2023" in letter["text_content"]
    assert "Rahul Sharma" in letter["text_content"]
    assert "UPI/1234567890/SBI" in letter["text_content"]
    assert "15 days" in letter["text_content"]


def test_benchmark_scenarios_structure():
    assert len(LEGAL_BENCHMARK_SCENARIOS) == 15
    sc1 = LEGAL_BENCHMARK_SCENARIOS[0]
    assert sc1["id"] == "scenario_01"
    assert "examination fee" in sc1["question"]
    assert len(sc1["expected_provisions"]) >= 2
    assert len(sc1["prohibited_conclusions"]) >= 1

    # Test scoring helper
    test_ans = "Under UGC Regulations 2023, you must approach SGRC. In MDU v. Surjeet Kaur, SC held education is not a service under CPA."
    res = evaluate_response_against_scenario(sc1, test_ans)
    assert res["passed"] is True
    assert len(res["prohibited_violations"]) == 0


def test_multi_agent_pipeline_execution():
    pipeline = NyayaMultiAgentPipeline()
    state = LegalAgentState(
        question="My cheque of ₹50,000 bounced due to insufficient funds. What notice should I send?",
        language="English",
        jurisdiction="India"
    )
    result = pipeline.run(state)
    assert "answer" in result
    assert len(result["agents"]) == 10
    assert result["verification_summary"] is not None
    # Check that Agent 1 recognized Financial/Negotiable Instruments
    assert any("Negotiable Instruments" in log["note"] or "Financial" in log["note"] for log in result["agents"])

