"""
Comprehensive Test Suite for NYAYA AI Enterprise Architecture (Module 10):
- Mandatory Authentication, Session Lifecycle, Expiration & Admin RBAC
- Medallion Data Engineering Pipeline (Bronze -> Silver -> Gold + DLQ + Idempotency)
- Exact & Semantic AI Caching + Legal Context Safety Guard + Statute Invalidation
- Performance, Idempotency & Graceful Analytics Degradation
- DPDPA 2023 User Data Export & Deletion Scoping
"""

import time
import uuid
from unittest.mock import patch

import pytest
from fastapi import HTTPException, Response
from starlette.requests import Request

from app.main import (
    SessionCreateRequest,
    admin_analytics_endpoint,
    chat,
    delete_my_data,
    establish_auth_session,
    export_my_data,
    home,
    legal_assistant_web,
    admin_dashboard_view,
    advocate_console_view,
)
from app.schemas import ChatRequest
from app.services.ai_cache import (
    invalidate_cache,
    lookup_cached_response,
    normalize_query,
    store_cached_response,
)
from app.services.auth_service import (
    _sign_payload,
    invalidate_user_session,
    require_admin_user,
    require_authenticated_user,
    verify_session_token,
)
from app.services.data_pipeline import ingest_bronze_event, run_etl_pipeline
from app.services.database import db_read, db_transaction
from app.services.legal_classifier import LegalClassificationEngine


def _dummy_request(path: str = "/") -> Request:
    return Request({"type": "http", "method": "GET", "path": path, "headers": []})


# ── 1. Authentication, Redirects, Session Lifecycle & RBAC Tests ──────────────

def test_unauthenticated_redirects_to_login():
    req = _dummy_request("/")
    for fn in (home, legal_assistant_web, advocate_console_view, admin_dashboard_view):
        resp = fn(request=req, authorization=None, nyaya_session=None)
        assert resp.status_code == 302
        assert resp.headers["location"] == "/login"


def test_unauthenticated_api_raises_401():
    req = _dummy_request("/api/auth/me")
    with pytest.raises(HTTPException) as exc_info:
        require_authenticated_user(request=req, authorization=None, nyaya_session=None)
    assert exc_info.value.status_code == 401


def test_session_lifecycle_login_refresh_logout_and_rbac():
    email = f"citizen_{uuid.uuid4().hex[:8]}@example.com"
    resp = Response()
    sess = establish_auth_session(
        SessionCreateRequest(email=email, full_name="Test Citizen", role="citizen"),
        response=resp,
    )
    token = sess["session_token"]
    user = sess["user"]
    assert user["role"] == "citizen"

    # Session persists & validates
    verified = verify_session_token(token)
    assert verified is not None and verified["email"] == email

    # Citizen can access /app
    req = _dummy_request("/app")
    app_resp = legal_assistant_web(request=req, authorization=f"Bearer {token}", nyaya_session=None)
    assert app_resp.status_code == 200

    # Citizen rejected from /admin (302) and admin API (403)
    admin_page_resp = admin_dashboard_view(request=_dummy_request("/admin"), authorization=f"Bearer {token}", nyaya_session=None)
    assert admin_page_resp.status_code == 302
    with pytest.raises(HTTPException) as exc_admin:
        require_admin_user(request=_dummy_request("/api/admin/analytics"), authorization=f"Bearer {token}", nyaya_session=None, x_admin_key=None)
    assert exc_admin.value.status_code == 403

    # Logout invalidates session
    invalidate_user_session(sess["session_id"], user["user_id"])
    assert verify_session_token(token) is None
    assert legal_assistant_web(request=req, authorization=f"Bearer {token}", nyaya_session=None).status_code == 302


def test_expired_session_rejected():
    expired_token = _sign_payload({
        "user_id": "expired-user",
        "email": "exp@example.com",
        "role": "citizen",
        "session_id": "nonexistent",
        "exp": int(time.time()) - 100,
    })
    assert verify_session_token(expired_token) is None


def test_admin_access_granted_for_founder():
    resp = Response()
    sess = establish_auth_session(
        SessionCreateRequest(email="mgdharan7@gmail.com", full_name="Giridharan", role="advocate"),
        response=resp,
    )
    assert sess["user"]["role"] == "admin"
    token = sess["session_token"]
    assert admin_dashboard_view(request=_dummy_request("/admin"), authorization=f"Bearer {token}", nyaya_session=None).status_code == 200
    analytics = admin_analytics_endpoint(range="30d", start=None, end=None, user=sess["user"])
    assert "user_metrics" in analytics
    assert "ai_metrics" in analytics
    assert "pipeline_metrics" in analytics
    assert "system_health" in analytics


# ── 2. Data Engineering Medallion Pipeline Tests ──────────────────────────────

def test_medallion_pipeline_idempotency_and_dlq():
    unique_eid = f"evt-{uuid.uuid4().hex}"
    ingest_bronze_event(
        event_type="user_login",
        user_id="pipe-user-1",
        session_id="sess-1",
        status="ok",
        payload={"duration_ms": 120},
        event_id=unique_eid,
    )
    ingest_bronze_event(
        event_type="user_login",
        user_id="pipe-user-1",
        session_id="sess-1",
        status="ok",
        payload={"duration_ms": 120},
        event_id=unique_eid,
    )

    bad_eid = f"bad-evt-{uuid.uuid4().hex}"
    with db_transaction() as conn:
        conn.execute(
            """
            INSERT INTO activity_events (event_id, event_type, schema_version, user_id, session_id, status, payload_json, created_at)
            VALUES (?, 'unknown_garbage_type', '1.0', 'u1', 's1', 'ok', '{}', '2026-11-26T00:00:00+00:00')
            """,
            (bad_eid,),
        )

    etl_res = run_etl_pipeline()
    assert etl_res["status"] == "success"

    with db_read() as conn:
        silver_matches = conn.execute(
            "SELECT COUNT(*) FROM silver_events WHERE source_event_id = ?",
            (unique_eid,),
        ).fetchone()[0]
        dlq_matches = conn.execute(
            "SELECT COUNT(*) FROM dead_letter_events WHERE source_event_id = ?",
            (bad_eid,),
        ).fetchone()[0]

    assert silver_matches == 1
    assert dlq_matches == 1


# ── 3. AI Caching, Semantic Safety & Invalidation Tests ───────────────────────

def test_exact_and_semantic_cache_with_legal_safety_and_invalidation():
    invalidate_cache(reason="Test isolation reset")
    cls_engine = LegalClassificationEngine()
    q1 = "Someone gave me a cheque of Rs 50,000 that bounced due to insufficient funds"
    q2 = "A cheque issued to me for Rs 75,000 was dishonoured by bank for insufficient funds"
    q_different_domain = "My landlord is refusing to return my security deposit of 50000"

    assert normalize_query("F.I.R. for U.P.I. scam!!") == "fir for upi scam"

    domain_q1 = cls_engine.classify(query=q1)["domain"]
    emb_cheque_1 = [0.9, 0.4, 0.1, 0.0]
    emb_cheque_2 = [0.89, 0.44, 0.1, 0.0]
    emb_different_domain = [0.9, 0.4, 0.1, 0.0]

    store_cached_response(
        question=q1,
        jurisdiction="India",
        language="English",
        incident_date=None,
        legal_domain=domain_q1,
        applicable_provisions=["Negotiable Instruments Act, 1881 Section 138"],
        response_payload={
            "answer": "### 📌 Quick Summary\nCheque dishonour is an offence under Section 138 NI Act.",
            "agents": [],
            "sources": [],
            "confidence": "Verified",
            "disclaimer": "General info",
            "claims": [],
            "verification_summary": {},
        },
        query_embedding=emb_cheque_1,
    )

    hit1, status1, _ = lookup_cached_response(
        question="someone gave me a cheque of rs 50 000 that bounced due to insufficient funds",
        jurisdiction="India",
        language="English",
    )
    assert status1 == "hit_exact"
    assert hit1 is not None and "Section 138 NI Act" in hit1["answer"]

    hit2, status2, _ = lookup_cached_response(
        question=q2,
        jurisdiction="India",
        language="English",
        query_embedding=emb_cheque_2,
    )
    assert status2 == "hit_semantic"
    assert hit2 is not None

    hit3, status3, _ = lookup_cached_response(
        question=q_different_domain,
        jurisdiction="India",
        language="English",
        query_embedding=emb_different_domain,
    )
    assert status3 == "miss"
    assert hit3 is None

    inv_count = invalidate_cache(statute_keyword="Negotiable Instruments", reason="Amendment test")
    assert inv_count >= 1
    hit_after, status_after, _ = lookup_cached_response(question=q1, jurisdiction="India", language="English")
    assert status_after == "miss"
    assert hit_after is None


# ── 4. Chat Endpoint Performance, Idempotency & Graceful Degradation ──────────

def test_chat_caching_speedup_idempotency_and_analytics_degradation():
    invalidate_cache(reason="Chat test reset")
    email = f"perf_{uuid.uuid4().hex[:8]}@example.com"
    sess = establish_auth_session(
        SessionCreateRequest(email=email, full_name="Perf User", role="citizen"),
        response=Response(),
    )
    user = {**sess["user"], "session_id": sess["session_id"]}

    fake_result = {
        "answer": "### 📌 Quick Summary\nTest legal answer under Section 138 NI Act.",
        "agents": [{"agent": "Test", "status": "completed", "note": "ok"}],
        "sources": [],
        "confidence": "10-Agent Verified RAG",
        "disclaimer": "General legal information only.",
        "claims": [],
        "verification_summary": {
            "total_claims_detected": 0,
            "verified_claims_count": 0,
            "unverified_claims_count": 0,
            "caution_flags_count": 0,
            "temporal_validity_checked": False,
            "education_dispute_evaluated": False,
            "audit_verdict": "Passed",
        },
        "telemetry": {
            "legal_domain": "Negotiable Instruments / Financial Law",
            "rag_duration_ms": 12.0,
            "llm_duration_ms": 150.0,
            "input_tokens": 500,
            "output_tokens": 300,
            "model_used": "gemini-2.5-flash",
            "retrieval_doc_count": 2,
        },
    }

    q = f"My cheque of Rs 50000 bounced due to insufficient funds {uuid.uuid4().hex[:6]}"

    with patch("app.main.embed_query", return_value=[0.1, 0.2, 0.3, 0.4]), \
         patch("app.main.run_legal_workflow", return_value=fake_result) as mock_wf:
        t0 = time.perf_counter()
        r1 = chat(ChatRequest(question=q), user=user, x_idempotency_key=f"k1-{uuid.uuid4()}")
        t_miss = time.perf_counter() - t0
        assert "Section 138 NI Act" in r1["answer"]
        assert mock_wf.call_count == 1

        t1 = time.perf_counter()
        r2 = chat(ChatRequest(question=q), user=user, x_idempotency_key=f"k2-{uuid.uuid4()}")
        t_hit = time.perf_counter() - t1
        assert "Section 138 NI Act" in r2["answer"]
        assert mock_wf.call_count == 1
        assert t_hit <= t_miss + 0.2

    # Rapid double-click without explicit idempotency key raises 409
    q_dup = f"Duplicate click protection test query {uuid.uuid4().hex[:6]}"
    with patch("app.main.embed_query", return_value=[0.2, 0.3, 0.4, 0.5]), \
         patch("app.main.run_legal_workflow", return_value=fake_result):
        chat(ChatRequest(question=q_dup), user=user, x_idempotency_key=None)
        with pytest.raises(HTTPException) as dup_exc:
            chat(ChatRequest(question=q_dup), user=user, x_idempotency_key=None)
        assert dup_exc.value.status_code == 409

    # Analytics failure must NOT interrupt AI response
    q_deg = f"Graceful degradation test query {uuid.uuid4().hex[:6]}"
    with patch("app.main.embed_query", return_value=[0.3, 0.4, 0.5, 0.6]), \
         patch("app.main.run_legal_workflow", return_value=fake_result), \
         patch("app.services.data_pipeline.db_transaction", side_effect=RuntimeError("DB down")):
        res_deg = chat(ChatRequest(question=q_deg), user=user, x_idempotency_key=f"k3-{uuid.uuid4()}")
        assert "Section 138 NI Act" in res_deg["answer"]

    # DPDPA user export & deletion scoped to user
    exp = export_my_data(user=user)
    assert len(exp["chat_history"]) >= 1
    del_res = delete_my_data(user=user)
    assert del_res["deleted_chats"] >= 1
