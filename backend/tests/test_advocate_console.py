"""
Unit and Integration Tests for Advocate Counsel Practice Console.
Validates:
1. Civilian Client Inflow tracking & case roster attributes.
2. Authoritative Statute Health Monitor (Active vs. Deactive / Repealed laws).
3. Deep Advocate Research Brief generator (Statutory elements, Coram, Precedents, Conflicts, Strategy).
4. Advocate Exclusive Privileges & Practice Benefits.
"""

import pytest
import sys
from pathlib import Path

# Ensure backend directory is in path
backend_dir = Path(__file__).resolve().parent.parent
if str(backend_dir) not in sys.path:
    sys.path.insert(0, str(backend_dir))

from app.services.advocate_service import (
    load_civilian_cases,
    record_civilian_inquiry,
    get_statutes_health_registry,
    get_advocate_exclusive_benefits,
    generate_counsel_research_brief
)


def test_civilian_cases_roster():
    """Validates civilian inquiries roster structure and required fields."""
    cases = load_civilian_cases()
    assert len(cases) >= 1

    first = cases[0]
    required_fields = [
        "case_id", "civilian_name", "contact_redacted", "jurisdiction",
        "legal_domain", "facts_summary", "primary_law"
    ]
    for field in required_fields:
        assert field in first, f"Missing required field: {field}"


def test_record_new_civilian_inquiry():
    """Validates real-time addition of incoming civilian queries to roster."""
    initial_cases = load_civilian_cases()
    initial_count = len(initial_cases)

    new_case = record_civilian_inquiry(
        question="My employer hasn't paid my 3 months salary of Rs 1,50,000.",
        domain="Labour & Employment Law",
        jurisdiction="Karnataka",
        primary_law="Payment of Wages Act, 1936",
        forum="Labour Court / Payment of Wages Authority",
        client_name="Test Civilian"
    )

    updated_cases = load_civilian_cases()
    assert len(updated_cases) == initial_count + 1
    assert updated_cases[0]["case_id"] == new_case["case_id"]
    assert updated_cases[0]["civilian_name"] == "Test Civilian"
    assert "Salary" in updated_cases[0]["facts_summary"] or "salary" in updated_cases[0]["facts_summary"]


def test_statute_health_active_vs_deactive():
    """Validates Active (In Force) vs Deactive (Repealed) status detection."""
    registry = get_statutes_health_registry()

    assert registry["total_statutes"] >= 15
    assert registry["active_count"] >= 13
    assert registry["repealed_count"] >= 2

    active_keys = [s["key"] for s in registry["active_statutes"]]
    repealed_keys = [s["key"] for s in registry["repealed_statutes"]]

    # Active laws
    assert "bharatiya nyaya sanhita, 2023" in active_keys
    assert "consumer protection act, 2019" in active_keys
    assert "negotiable instruments act, 1881" in active_keys
    assert "information technology act, 2000" in active_keys

    # Repealed / Deactive laws
    assert "indian penal code, 1860" in repealed_keys
    assert "consumer protection act, 1986" in repealed_keys

    # Check transition metadata on repealed law
    ipc_entry = next(s for s in registry["repealed_statutes"] if s["key"] == "indian penal code, 1860")
    assert ipc_entry["is_active"] is False
    assert "Bharatiya Nyaya Sanhita, 2023" in ipc_entry["repealed_by"]
    assert "1 July 2024" in ipc_entry["repealed_by"]


def test_counsel_research_brief_cheque_bounce():
    """Validates in-depth counsel brief generation for Section 138 NI Act."""
    brief = generate_counsel_research_brief("Cheque bounce of Rs 75,000 for unpaid invoice")

    assert "Negotiable Instruments Act" in brief["primary_act"]
    assert any("138" in sec for sec in brief["applicable_sections"])
    assert len(brief["essential_elements"]) >= 4

    # Binding Precedents & Coram
    precedent_citations = [p["citation"] for p in brief["binding_precedents"]]
    assert any("Bir Singh" in c for c in precedent_citations)

    # Statutory limitation & strategy
    assert "30 days" in brief["limitation_period_rule"]
    assert "Section 139" in brief["counsel_prosecution_strategy"]
    assert "security" in brief["counsel_defense_strategy"].lower()
    assert "PRIVILEGE" in brief["privilege_notice"]


def test_counsel_research_brief_job_scam():
    """Validates in-depth counsel brief generation for Job Fraud."""
    brief = generate_counsel_research_brief("Bogus job recruiter on WhatsApp took interview fee BNS 318")

    assert "Bharatiya Nyaya Sanhita" in brief["primary_act"]
    assert any("318(4)" in sec for sec in brief["applicable_sections"])
    assert any("66D" in sec for sec in brief["applicable_sections"])

    precedent_citations = [p["citation"] for p in brief["binding_precedents"]]
    assert any("Hridaya Ranjan" in c for c in precedent_citations)


def test_advocate_exclusive_benefits():
    """Validates advocate-exclusive privileges and practice tools."""
    benefits = get_advocate_exclusive_benefits()
    assert len(benefits) >= 5

    benefit_ids = [b["id"] for b in benefits]
    assert "privilege_shield" in benefit_ids
    assert "court_pleadings" in benefit_ids
    assert "precedent_conflict_detector" in benefit_ids
    assert "temporal_code_converter" in benefit_ids
    assert "limitation_audit" in benefit_ids

    # Verify statutory basis
    privilege = next(b for b in benefits if b["id"] == "privilege_shield")
    assert "Section 132" in privilege["statutory_basis"]
    assert "Bharatiya Sakshya Adhiniyam" in privilege["statutory_basis"]


def test_get_available_advocates():
    """Validates advocate listing strictly from real Supabase registered counsel."""
    from app.services.supabase_service import get_available_advocates
    advocates = get_available_advocates()
    assert len(advocates) >= 1

    emails = [a["email"] for a in advocates]
    assert "mgdharan7@gmail.com" in emails
    # Ensure zero dummy or temporary advocates exist
    assert "advocate.sharma@delhibar.in" not in emails
    assert "priya.counsel@chennaibar.org" not in emails

    giridharan = next(a for a in advocates if a["email"] == "mgdharan7@gmail.com")
    assert "Giridharan" in giridharan["name"]
    assert "D/1847/2019" in giridharan["bar_council_no"]
    assert giridharan["verified"] is True


def test_civilian_assign_complaint_and_advocate_connect():
    """Validates civilian assigning complaint letter to advocate and advocate connecting."""
    from app.services.supabase_service import submit_civilian_complaint, advocate_connect_to_civilian, load_dynamic_civilian_cases

    # 1. Civilian submits complaint assigned to Advocate Giridharan
    new_case = submit_civilian_complaint(
        civilian_name="Test Civilian User",
        civilian_email="civilian.test@example.com",
        civilian_contact="+91 99999 •••••",
        jurisdiction="Delhi (NCT)",
        legal_domain="Cyber Fraud & Impersonation",
        facts_summary="Transferred ₹50,000 for a fake job offer on WhatsApp.",
        complaint_letter="FORMAL COMPLAINT\n\nI was deceived into paying ₹50,000 for fake interview clearance.\nPlease issue statutory notice under BNS 318(4).",
        advocate_id="adv-giridharan",
        advocate_name="Advocate Giridharan",
        advocate_email="mgdharan7@gmail.com"
    )

    assert new_case["assigned_advocate_name"] == "Advocate Giridharan"
    assert new_case["assigned_advocate_email"] == "mgdharan7@gmail.com"
    assert "FORMAL COMPLAINT" in new_case["complaint_letter"]
    assert new_case["advocate_connected"] is False

    # Verify presence in dynamic roster
    roster = load_dynamic_civilian_cases()
    found = next((c for c in roster if c["case_id"] == new_case["case_id"]), None)
    assert found is not None

    # 2. Advocate reviews case and connects with civilian
    res = advocate_connect_to_civilian(
        case_id=new_case["case_id"],
        counsel_message="I have reviewed your job fraud complaint. BNS 318(4) and IT Act 66D apply. Consultation scheduled for tomorrow at 4 PM.",
        advocate_name="Advocate Giridharan"
    )

    assert res["status"] == "success"
    assert res["case"]["advocate_connected"] is True
    assert "Counsel Connected" in res["case"]["status"]
    assert res["case"]["advocate_response"]["message"].startswith("I have reviewed")


def test_advocate_and_civilian_api_endpoints():
    """Validates FastAPI endpoints for advocate listing, complaint assignment, and client connection."""
    from app.main import (
        get_advocates_list,
        assign_complaint_to_advocate,
        get_advocate_dashboard_data,
        connect_client_endpoint,
        AssignComplaintRequest,
        ConnectClientRequest
    )

    # 1. GET /api/advocates
    adv_list = get_advocates_list()
    assert isinstance(adv_list, list)
    assert any(a["email"] == "mgdharan7@gmail.com" for a in adv_list)

    # 2. POST /api/civilian/assign-complaint
    req = AssignComplaintRequest(
        civilian_name="API Test Citizen",
        civilian_email="citizen.api@example.com",
        civilian_contact="+91 98111 •••••",
        jurisdiction="Tamil Nadu",
        legal_domain="Tenancy & Security Deposit Refund",
        facts_summary="Landlord withheld ₹80,000 security deposit without justification.",
        complaint_letter="STATUTORY NOTICE TO VACATE & REFUND\n\nPlease refund ₹80,000 security deposit within 15 days.",
        advocate_id="adv-giridharan",
        advocate_name="Advocate Giridharan",
        advocate_email="mgdharan7@gmail.com"
    )
    assign_data = assign_complaint_to_advocate(req)
    assert assign_data["status"] == "success"
    assigned_case_id = assign_data["case"]["case_id"]

    # 3. GET /api/advocate/dashboard
    dash_data = get_advocate_dashboard_data()
    assert dash_data["status"] == "success"
    assert dash_data["total_civilians"] >= 1
    assert any(c["case_id"] == assigned_case_id for c in dash_data["civilian_cases"])

    # 4. POST /api/advocate/connect-client
    connect_req = ConnectClientRequest(
        case_id=assigned_case_id,
        counsel_message="Consultation confirmed. Tenancy Act notice prepared.",
        advocate_name="Advocate Giridharan"
    )
    connect_data = connect_client_endpoint(connect_req)
    assert connect_data["status"] == "success"
    assert connect_data["case"]["advocate_connected"] is True

    # Clean up test cases so only real original civilian data remains
    from app.services.supabase_service import DYNAMIC_CASES_FILE
    import json
    clean_real_cases = [
        c for c in get_advocate_dashboard_data()["civilian_cases"]
        if "Test" not in c.get("civilian_name", "") and "API" not in c.get("civilian_name", "")
    ]
    if clean_real_cases:
        DYNAMIC_CASES_FILE.write_text(json.dumps(clean_real_cases, indent=2), encoding="utf-8")


