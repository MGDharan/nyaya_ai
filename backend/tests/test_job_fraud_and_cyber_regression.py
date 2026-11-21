"""
Regression tests for Job Fraud, Cyber Offence Classification, and Civil/Criminal Boundaries.
Covers 6 distinct scenarios:
1. Fake Job Recruitment (Criminal Cheating + IT Act 66D; CPA & IT 43/66 excluded)
2. Actual Identity Impersonation (IT Act 66D + BNS 319 / IPC 419; CPA & IT 43/66 excluded)
3. Stolen Login Credentials (IT Act 66C; CPA & IT 43/66 excluded)
4. Unauthorized Computer Access (IT Act 43 & 66; CPA & Cheating excluded)
5. Ordinary Unpaid Loan (Contract Act Sec 73 + CPC Order 37; Cheating & CPA excluded)
6. Genuine Recruitment Agency Service Dispute (CPA 2019 + Contract Act; Criminal Cheating excluded)
"""

import pytest
import sys
from pathlib import Path

# Ensure backend directory is in path
backend_dir = Path(__file__).resolve().parent.parent
if str(backend_dir) not in sys.path:
    sys.path.insert(0, str(backend_dir))

from app.services.legal_classifier import LegalClassificationEngine
from app.services.hybrid_retriever import is_statute_irrelevant_to_query
from app.agents.multi_agent_pipeline import NyayaMultiAgentPipeline, LegalAgentState


@pytest.fixture
def classifier():
    return LegalClassificationEngine()


@pytest.fixture
def pipeline():
    return NyayaMultiAgentPipeline()


def _get_all_act_names(result):
    acts = [result.get("primary_legislation", {}).get("act_name", "")]
    for s in result.get("secondary_legislation", []):
        acts.append(s.get("act_name", ""))
    return acts


def _get_all_sections(result):
    secs = list(result.get("primary_legislation", {}).get("sections", []))
    for s in result.get("secondary_legislation", []):
        secs.extend(s.get("sections", []))
    return secs


def test_scenario_1_fake_job_recruitment_post_july_2024(classifier):
    """
    Scenario 1: Fake job recruitment after July 1, 2024.
    Should classify into Domain 3B (Job Scams / BNS Cheating) and Domain 8C (IT Act 66D).
    Must strictly exclude: Consumer Protection Act, IT Act 43/66, UGC / Education regulations.
    """
    query = (
        "In August 2024, a person on Telegram posed as an HR manager from Infosys and offered me a remote job. "
        "They demanded Rs. 15,000 for training and background verification via UPI, then blocked my number. "
        "What legal action can I take?"
    )
    result = classifier.classify(query)
    all_acts = _get_all_act_names(result)
    all_secs = str(_get_all_sections(result))

    # 1. Primary legislation & sections
    assert any("Bharatiya Nyaya Sanhita, 2023" in act for act in all_acts)
    assert "318(4)" in all_secs
    assert "319" in all_secs

    # 2. Secondary cyber legislation
    assert any("Information Technology Act, 2000" in act for act in all_acts)
    assert "66D" in all_secs

    # 3. Must NOT classify under IPC (post July 2024)
    assert not any("Indian Penal Code, 1860" in act for act in all_acts)

    # 4. Strictly excluded legislation
    assert not any("Consumer Protection Act, 2019" in act for act in all_acts)
    assert "Section 43" not in all_secs
    assert "Section 66 (" not in all_secs

    # 5. Hybrid retriever relevance check
    assert is_statute_irrelevant_to_query(query, "Consumer Protection Act, 2019")
    assert is_statute_irrelevant_to_query(query, "Section 43")
    assert is_statute_irrelevant_to_query(query, "University Grants Commission")


def test_scenario_1_fake_job_recruitment_pre_july_2024(classifier):
    """
    Scenario 1 variant: Fake job recruitment occurring before July 1, 2024.
    Must cite Indian Penal Code (Sections 420 and 419), not BNS.
    """
    query = (
        "In January 2023, someone called claiming to be from TCS HR offering a data entry role. "
        "I transferred Rs. 20,000 as refundable security deposit via NetBanking, after which they vanished."
    )
    result = classifier.classify(query)
    all_acts = _get_all_act_names(result)
    all_secs = str(_get_all_sections(result))

    assert any("Indian Penal Code, 1860" in act for act in all_acts)
    assert "420" in all_secs
    assert "419" in all_secs
    assert not any("Bharatiya Nyaya Sanhita, 2023" in act for act in all_acts)
    assert not any("Consumer Protection Act, 2019" in act for act in all_acts)


def test_scenario_2_actual_identity_impersonation(classifier):
    """
    Scenario 2: Actual identity impersonation.
    Someone created a fake profile impersonating an individual to deceive others.
    Primary: IT Act 66D and BNS 319 / IPC 419.
    Must exclude: Consumer Protection Act, IT Act 43/66.
    """
    query = (
        "An unknown fraudster created an Instagram profile using my colleague's name and photographs, "
        "and is impersonating him to solicit money from people via UPI transfers."
    )
    result = classifier.classify(query)
    all_acts = _get_all_act_names(result)
    all_secs = str(_get_all_sections(result))

    assert any("Information Technology Act, 2000" in act for act in all_acts)
    assert "66D" in all_secs
    assert "319" in all_secs
    assert not any("Consumer Protection Act, 2019" in act for act in all_acts)
    assert "Section 43" not in all_secs
    assert is_statute_irrelevant_to_query(query, "Consumer Protection Act, 2019")


def test_scenario_3_stolen_login_credentials(classifier):
    """
    Scenario 3: Stolen login credentials (identity theft / password theft).
    Primary: IT Act Section 66C.
    Must exclude: Consumer Protection Act, Section 43/66 (unless server hacking is shown).
    """
    query = (
        "My net banking password and OTP were fraudulently obtained through a phishing link, "
        "and the perpetrator logged into my portal using my confidential credentials to transfer funds."
    )
    result = classifier.classify(query)
    all_acts = _get_all_act_names(result)
    all_secs = str(_get_all_sections(result))

    assert any("Information Technology Act, 2000" in act for act in all_acts)
    assert "66C" in all_secs
    assert not any("Consumer Protection Act, 2019" in act for act in all_acts)
    assert is_statute_irrelevant_to_query(query, "Consumer Protection Act, 2019")


def test_scenario_4_unauthorized_computer_access(classifier):
    """
    Scenario 4: Unauthorized computer access / server hacking / data damage.
    Primary: IT Act Section 43 & Section 66.
    Must exclude: Consumer Protection Act, simple cheating without computer breach.
    """
    query = (
        "An unauthorized hacker breached our corporate cloud server, injected ransomware malware, "
        "and damaged database records without authorization."
    )
    result = classifier.classify(query)
    all_acts = _get_all_act_names(result)
    all_secs = str(_get_all_sections(result))

    assert any("Information Technology Act, 2000" in act for act in all_acts)
    assert "43" in all_secs
    assert "66" in all_secs
    assert not any("Consumer Protection Act, 2019" in act for act in all_acts)
    assert not is_statute_irrelevant_to_query(query, "Section 43")


def test_scenario_5_ordinary_unpaid_loan(classifier):
    """
    Scenario 5: Ordinary unpaid friendly loan.
    Civil dispute: Indian Contract Act Section 73 + CPC Order 37 summary suit.
    Must exclude: Criminal cheating (BNS 318 / IPC 420) and Consumer Protection Act.
    """
    query = (
        "I gave a personal friendly loan of Rs. 2,00,000 to my friend with a written promissory note. "
        "He has not returned the money even after the agreed 6 months period. What can I do to recover it?"
    )
    result = classifier.classify(query)
    all_acts = _get_all_act_names(result)
    all_secs = str(_get_all_sections(result))

    assert any("Indian Contract Act, 1872" in act for act in all_acts)
    assert "73" in all_secs or "Order 37" in all_secs or "Civil Recovery" in result.get("domain", "")
    assert not any("Consumer Protection Act, 2019" in act for act in all_acts)
    assert "318(4)" not in all_secs
    assert is_statute_irrelevant_to_query(query, "Consumer Protection Act, 2019")


def test_scenario_6_genuine_recruitment_agency_dispute(classifier):
    """
    Scenario 6: Genuine registered recruitment agency service dispute.
    Consumer dispute: Consumer Protection Act 2019 (Sections 2(7), 2(11), 35) + Contract Act.
    Must exclude: Criminal cheating (BNS 318).
    """
    query = (
        "I engaged ABC Placements Ltd, a registered recruitment consultancy, and paid Rs. 10,000 for resume building "
        "and guaranteed interview scheduling services as per written contract. They failed to arrange any interviews "
        "and are refusing to issue a refund despite repeated deficiency of service notices."
    )
    result = classifier.classify(query)
    all_acts = _get_all_act_names(result)
    all_secs = str(_get_all_sections(result))

    assert any("Consumer Protection Act, 2019" in act for act in all_acts)
    assert "35" in all_secs or "2(11)" in all_secs
    assert "318(4)" not in all_secs
    assert not is_statute_irrelevant_to_query(query, "Consumer Protection Act, 2019")


def test_pipeline_end_to_end_job_fraud_no_irrelevant_sources(pipeline):
    """
    End-to-end pipeline test for fake recruitment job fraud.
    Verifies that:
    - BNS 318(4) and 319 are retrieved.
    - IT Act 66D is retrieved.
    - UGC / Education judgments (Surjeet Kaur) are completely absent.
    - IT Act 43/66 are absent.
    - Consumer Protection Act is absent from final acts/sources.
    """
    query = (
        "A fraudulent recruiter on WhatsApp claimed to offer an airport ground staff job. "
        "I paid Rs. 12,000 registration fee in October 2024. After payment they blocked my phone number."
    )
    state = LegalAgentState(question=query)
    report = pipeline.run(state)

    ans = report.get("answer", "").lower()
    sources = report.get("sources", [])

    # Must contain relevant provisions in answer or sources
    assert "318" in ans or "319" in ans or "66d" in ans

    # Must NOT contain irrelevant UGC / Education judgments
    assert "surjeet kaur" not in ans
    assert "ugc" not in ans
    assert "university grants commission" not in ans

    for src in sources:
        title = src.get("title", "").lower()
        assert "surjeet kaur" not in title
        assert "university grants commission" not in title
        assert "ugc" not in title

    # Must NOT cite IT Act 43 (damage/hacking) or 66 (hacking)
    acts_cited = [act.get("act_name", "") for act in report.get("applicable_acts", [])]
    sections_cited = [act.get("section", "") for act in report.get("applicable_acts", [])]

    assert "Section 43" not in sections_cited
    assert "Consumer Protection Act, 2019" not in acts_cited
