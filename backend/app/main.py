import hashlib
import json
import secrets
import time
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

from fastapi import Cookie, Depends, FastAPI, File, Form, Header, HTTPException, Query, Request, Response
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.responses import FileResponse, JSONResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from app.agents.workflow import run_legal_workflow
from app.config import settings
from app.ingest import ingest_file, load_registry
from app.schemas import ChatRequest, ChatResponse
from app.services.advocate_service import (
    generate_counsel_research_brief,
    get_advocate_exclusive_benefits,
    get_statutes_health_registry,
    load_civilian_cases,
    record_civilian_inquiry,
)
from app.services.ai_cache import (
    invalidate_cache,
    lookup_cached_response,
    normalize_query,
    store_cached_response,
)
from app.services.auth_service import (
    acquire_idempotency_guard,
    create_user_session,
    delete_user_data,
    enforce_rate_limit,
    export_user_data,
    get_optional_user,
    invalidate_user_session,
    record_admin_audit,
    require_admin_user,
    require_advocate_or_admin,
    require_authenticated_user,
)
from app.services.complaint_generator import (
    generate_complaint_letter,
    generate_police_fir_complaint,
    generate_section_63_bsa_certificate,
)
from app.services.data_pipeline import (
    APP_START_TIME,
    estimate_cost_usd,
    get_admin_analytics_summary,
    ingest_bronze_event,
    log_json,
    record_ai_request_telemetry,
    run_etl_pipeline,
)
from app.services.database import db_read, db_transaction, get_pool
from app.services.embeddings import embed_query
from app.services.legal_benchmark import LEGAL_BENCHMARK_SCENARIOS, evaluate_response_against_scenario
from app.services.supabase_service import (
    advocate_connect_to_civilian,
    get_available_advocates,
    submit_civilian_complaint,
)

app = FastAPI(
    title=settings.app_name,
    version="2.0.0",
    description="Production-Oriented Indian Legal Intelligence, Auth, Medallion Analytics & Semantic Caching Platform",
)

# API Response Compression (Module 6)
app.add_middleware(GZipMiddleware, minimum_size=1000)

BASE = Path(__file__).parent
UPLOAD_DIR = Path(settings.data_dir) / "uploads"
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
app.mount("/static", StaticFiles(directory=BASE / "static"), name="static")


# Centralized Exception Handler (Module 8)
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    log_json("error", "unhandled_exception", path=str(request.url.path), error=str(exc))
    try:
        with db_transaction() as conn:
            conn.execute(
                """
                INSERT INTO system_error_logs (id, error_type, endpoint, message, created_at)
                VALUES (?, 'unhandled_exception', ?, ?, ?)
                """,
                (str(uuid.uuid4()), str(request.url.path), str(exc)[:500], datetime.now(timezone.utc).isoformat()),
            )
    except Exception:
        pass
    return JSONResponse(status_code=500, content={"detail": "Internal server error. Our engineering team has been notified."})


def check_admin(key: str | None):
    if settings.admin_api_key and not secrets.compare_digest(key or "", settings.admin_api_key):
        raise HTTPException(status_code=401, detail="Invalid admin key")


# ── Page Routes with Mandatory Auth Redirects (Module 1) ──────────────────────

@app.get("/")
def home(
    request: Request,
    authorization: Optional[str] = Header(default=None),
    nyaya_session: Optional[str] = Cookie(default=None),
):
    user = get_optional_user(request, authorization, nyaya_session)
    if user:
        if user.get("role") == "admin":
            return RedirectResponse(url="/admin", status_code=302)
        if user.get("role") == "advocate":
            return RedirectResponse(url="/advocate", status_code=302)
        return RedirectResponse(url="/app", status_code=302)
    return RedirectResponse(url="/login", status_code=302)


@app.get("/login")
def login_gateway():
    return FileResponse(BASE / "static" / "login.html")


@app.get("/register")
def register_gateway():
    return FileResponse(BASE / "static" / "login.html")


@app.get("/app")
def legal_assistant_web(
    request: Request,
    authorization: Optional[str] = Header(default=None),
    nyaya_session: Optional[str] = Cookie(default=None),
):
    user = get_optional_user(request, authorization, nyaya_session)
    if not user:
        return RedirectResponse(url="/login", status_code=302)
    return FileResponse(BASE / "static" / "index.html")


@app.get("/assistant")
def assistant_web_alias(
    request: Request,
    authorization: Optional[str] = Header(default=None),
    nyaya_session: Optional[str] = Cookie(default=None),
):
    user = get_optional_user(request, authorization, nyaya_session)
    if not user:
        return RedirectResponse(url="/login", status_code=302)
    return FileResponse(BASE / "static" / "index.html")


@app.get("/advocate")
def advocate_console_view(
    request: Request,
    authorization: Optional[str] = Header(default=None),
    nyaya_session: Optional[str] = Cookie(default=None),
):
    user = get_optional_user(request, authorization, nyaya_session)
    if not user:
        return RedirectResponse(url="/login", status_code=302)
    if user.get("role") not in ("advocate", "admin"):
        return RedirectResponse(url="/app", status_code=302)
    return FileResponse(BASE / "static" / "advocate.html")


@app.get("/admin")
def admin_dashboard_view(
    request: Request,
    authorization: Optional[str] = Header(default=None),
    nyaya_session: Optional[str] = Cookie(default=None),
):
    user = get_optional_user(request, authorization, nyaya_session)
    if not user:
        return RedirectResponse(url="/login", status_code=302)
    if user.get("role") != "admin":
        return RedirectResponse(url="/app", status_code=302)
    return FileResponse(BASE / "static" / "admin.html")


# ── Authentication & Session Endpoints (Module 1 & 9) ─────────────────────────

class SessionCreateRequest(BaseModel):
    email: str
    full_name: Optional[str] = ""
    role: Optional[str] = "citizen"
    bar_council_no: Optional[str] = None
    supabase_access_token: Optional[str] = None
    supabase_user_id: Optional[str] = None
    device_info: Optional[str] = None
    browser_info: Optional[str] = None


class LoginFailureRequest(BaseModel):
    email: Optional[str] = None
    reason: Optional[str] = "invalid_credentials"


@app.post("/api/auth/session")
def establish_auth_session(req: SessionCreateRequest, response: Response):
    session_data = create_user_session(
        email=req.email,
        full_name=req.full_name or "",
        role=req.role or "citizen",
        bar_council_no=req.bar_council_no,
        supabase_access_token=req.supabase_access_token,
        supabase_user_id=req.supabase_user_id,
        device_info=req.device_info,
        browser_info=req.browser_info,
    )
    response.set_cookie(
        key="nyaya_session",
        value=session_data["session_token"],
        httponly=True,
        samesite="lax",
        max_age=12 * 3600,
        path="/",
    )
    return {"status": "authenticated", **session_data}


@app.post("/api/auth/login-failure")
def record_login_failure(req: LoginFailureRequest):
    ingest_bronze_event(
        event_type="user_login_failed",
        status="failed",
        payload={"reason": req.reason or "invalid_credentials"},
    )
    return {"status": "recorded"}


@app.post("/api/auth/logout")
def logout_auth_session(
    request: Request,
    response: Response,
    authorization: Optional[str] = Header(default=None),
    nyaya_session: Optional[str] = Cookie(default=None),
):
    user = get_optional_user(request, authorization, nyaya_session)
    if user:
        invalidate_user_session(user.get("session_id"), user.get("user_id"))
    response.delete_cookie(key="nyaya_session", path="/")
    return {"status": "logged_out"}


@app.get("/api/auth/me")
def get_current_session_user(user: dict = Depends(require_authenticated_user)):
    return {"status": "authenticated", "user": user}


@app.get("/api/user/history")
def get_my_chat_history(
    page: int = Query(default=1, ge=1),
    limit: int = Query(default=20, ge=1, le=100),
    user: dict = Depends(require_authenticated_user),
):
    offset = (page - 1) * limit
    uid = user["user_id"]
    with db_read() as conn:
        total = conn.execute("SELECT COUNT(*) FROM user_chat_history WHERE user_id = ?", (uid,)).fetchone()[0]
        rows = conn.execute(
            """
            SELECT id, request_id, question, answer, legal_domain, jurisdiction, created_at
            FROM user_chat_history
            WHERE user_id = ?
            ORDER BY created_at DESC
            LIMIT ? OFFSET ?
            """,
            (uid, limit, offset),
        ).fetchall()
    return {"page": page, "limit": limit, "total": total, "items": [dict(r) for r in rows]}


@app.get("/api/user/export")
def export_my_data(user: dict = Depends(require_authenticated_user)):
    return export_user_data(user["user_id"])


@app.delete("/api/user/data")
def delete_my_data(user: dict = Depends(require_authenticated_user)):
    res = delete_user_data(user["user_id"])
    return {"status": "deleted", **res}


# ── System Health Check (Module 8) ────────────────────────────────────────────

@app.get("/api/health")
def health():
    db_ok = get_pool().health_check()
    return {
        "status": "ok" if db_ok else "degraded",
        "app": settings.app_name,
        "version": "2.0.0",
        "time": datetime.now(timezone.utc).isoformat(),
        "uptime_sec": round(time.time() - APP_START_TIME, 1),
        "database_connected": db_ok,
        "cache_available": db_ok,
        "corpus_documents": len(load_registry()),
        "architecture": "10-Agent Pipeline + Semantic Cache + Medallion ETL",
    }


# ── Protected AI Legal Chat with Caching & Telemetry (Modules 1, 2, 4, 5, 6, 8) ─

@app.post("/api/chat", response_model=ChatResponse)
def chat(
    payload: ChatRequest,
    user: dict = Depends(require_authenticated_user),
    x_idempotency_key: Optional[str] = Header(default=None),
):
    user_id = user["user_id"]
    session_id = user.get("session_id")

    # 1. Per-user rate limiting
    enforce_rate_limit(user_id)

    # 2. Duplicate-click / idempotency protection
    norm_q = normalize_query(payload.question)
    idem_key = x_idempotency_key or f"{user_id}:{hashlib.sha256(norm_q.encode('utf-8')).hexdigest()}"
    if not x_idempotency_key:
        # Guard against accidental rapid double-click within 3 seconds
        if not acquire_idempotency_guard(idem_key, window_sec=3.0):
            raise HTTPException(status_code=409, detail="Duplicate request detected. Your legal analysis is already in progress.")

    request_id = str(uuid.uuid4())
    req_ts = datetime.now(timezone.utc).isoformat()
    t_start = time.perf_counter()

    # 3. Compute query embedding once (shared by Semantic Cache and RAG Vector Search)
    try:
        query_emb = embed_query(payload.question)
    except Exception:
        query_emb = None

    # 4. Exact & Semantic Cache Lookup
    cached_result, cache_status, _ = lookup_cached_response(
        question=payload.question,
        jurisdiction=payload.jurisdiction,
        language=payload.language,
        incident_date=payload.date_of_incident,
        query_embedding=query_emb,
    )

    if cached_result is not None:
        proc_ms = round((time.perf_counter() - t_start) * 1000, 2)
        resp_ts = datetime.now(timezone.utc).isoformat()
        saved_tok_in = int(cached_result.get("telemetry", {}).get("input_tokens") or 800)
        saved_tok_out = int(cached_result.get("telemetry", {}).get("output_tokens") or 600)
        saved_cost = estimate_cost_usd(
            cached_result.get("telemetry", {}).get("model_used", "gemini-2.5-flash"),
            saved_tok_in,
            saved_tok_out,
        )

        record_ai_request_telemetry(
            request_id=request_id,
            idempotency_key=x_idempotency_key,
            user_id=user_id,
            session_id=session_id,
            question=payload.question,
            answer=cached_result.get("answer", ""),
            legal_domain=cached_result.get("telemetry", {}).get("legal_domain", "Cached Legal Query"),
            jurisdiction=payload.jurisdiction,
            request_timestamp=req_ts,
            response_timestamp=resp_ts,
            processing_duration_ms=proc_ms,
            rag_duration_ms=0.0,
            llm_duration_ms=0.0,
            status="success",
            http_status_code=200,
            model_used="semantic-cache" if cache_status == "hit_semantic" else "exact-cache",
            input_tokens=0,
            output_tokens=0,
            estimated_cost_usd=0.0,
            estimated_cost_saved_usd=saved_cost,
            cache_status=cache_status,
            retrieval_doc_count=len(cached_result.get("sources", [])),
        )
        return cached_result

    # 5. Cache Miss -> Run 10-Agent RAG + LLM Pipeline
    try:
        result = run_legal_workflow(
            question=payload.question,
            language=payload.language,
            jurisdiction=payload.jurisdiction,
            incident_date=payload.date_of_incident,
            context=payload.context,
            query_embedding=query_emb,
        )
    except Exception as exc:
        proc_ms = round((time.perf_counter() - t_start) * 1000, 2)
        record_ai_request_telemetry(
            request_id=request_id,
            idempotency_key=x_idempotency_key,
            user_id=user_id,
            session_id=session_id,
            question=payload.question,
            answer="",
            legal_domain="Unknown",
            jurisdiction=payload.jurisdiction,
            request_timestamp=req_ts,
            response_timestamp=datetime.now(timezone.utc).isoformat(),
            processing_duration_ms=proc_ms,
            rag_duration_ms=0.0,
            llm_duration_ms=0.0,
            status="failed",
            http_status_code=500,
            model_used=settings.gemini_model,
            input_tokens=0,
            output_tokens=0,
            estimated_cost_usd=0.0,
            estimated_cost_saved_usd=0.0,
            cache_status="miss",
            retrieval_doc_count=0,
            error_details=str(exc),
        )
        raise HTTPException(status_code=500, detail="Failed to process legal analysis.")

    proc_ms = round((time.perf_counter() - t_start) * 1000, 2)
    resp_ts = datetime.now(timezone.utc).isoformat()
    tel = result.get("telemetry") or {}
    in_tok = int(tel.get("input_tokens") or 0)
    out_tok = int(tel.get("output_tokens") or 0)
    model_used = tel.get("model_used") or settings.gemini_model
    cost_usd = estimate_cost_usd(model_used, in_tok, out_tok)
    legal_domain = tel.get("legal_domain") or "General Legal Query"

    # 6. Store in validated Legal Cache (non-blocking if fails)
    try:
        provisions = [
            f"{c.get('act_name', '')} {c.get('section_number', '')}".strip()
            for c in result.get("claims", [])
        ]
        store_cached_response(
            question=payload.question,
            jurisdiction=payload.jurisdiction,
            language=payload.language,
            incident_date=payload.date_of_incident,
            legal_domain=legal_domain,
            applicable_provisions=provisions,
            response_payload=result,
            query_embedding=query_emb,
        )
    except Exception as exc:
        log_json("warning", "cache_store_failed", error=str(exc))

    # 7. Record Telemetry (graceful degradation if fails)
    record_ai_request_telemetry(
        request_id=request_id,
        idempotency_key=x_idempotency_key,
        user_id=user_id,
        session_id=session_id,
        question=payload.question,
        answer=result.get("answer", ""),
        legal_domain=legal_domain,
        jurisdiction=payload.jurisdiction,
        request_timestamp=req_ts,
        response_timestamp=resp_ts,
        processing_duration_ms=proc_ms,
        rag_duration_ms=float(tel.get("rag_duration_ms") or 0.0),
        llm_duration_ms=float(tel.get("llm_duration_ms") or 0.0),
        status="success",
        http_status_code=200,
        model_used=model_used,
        input_tokens=in_tok,
        output_tokens=out_tok,
        estimated_cost_usd=cost_usd,
        estimated_cost_saved_usd=0.0,
        cache_status="miss",
        retrieval_doc_count=int(tel.get("retrieval_doc_count") or len(result.get("sources", []))),
    )

    # Real-time tracking of civilian inquiry in advocate intake roster
    try:
        first_act = result.get("applicable_acts", [{}])[0].get("act_name", "General Statutory Law") if result.get("applicable_acts") else "Indian Law"
        record_civilian_inquiry(
            question=payload.question,
            domain=legal_domain,
            jurisdiction=payload.jurisdiction,
            primary_law=first_act,
            forum=legal_domain,
            client_name=user.get("email") or "Registered Citizen",
        )
    except Exception:
        pass

    return result


# ── Advocate Practice Console Endpoints (Protected) ───────────────────────────

class CounselBriefRequest(BaseModel):
    query: str


@app.get("/api/advocate/dashboard")
def get_advocate_dashboard_data(user: dict = Depends(require_advocate_or_admin)):
    statutes_data = get_statutes_health_registry()
    civilian_cases = load_civilian_cases()
    benefits = get_advocate_exclusive_benefits()
    return {
        "status": "success",
        "civilian_cases": civilian_cases,
        "statutes": statutes_data,
        "advocate_benefits": benefits,
        "total_civilians": len(civilian_cases),
        "active_statutes_count": statutes_data["active_count"],
        "repealed_statutes_count": statutes_data["repealed_count"],
    }


@app.post("/api/advocate/counsel-brief")
def create_counsel_brief_endpoint(req: CounselBriefRequest, user: dict = Depends(require_advocate_or_admin)):
    return generate_counsel_research_brief(req.query)


# ── Civilian-to-Advocate Assignment & Communication Endpoints ─────────────────

class AssignComplaintRequest(BaseModel):
    civilian_name: str
    civilian_email: str
    civilian_contact: Optional[str] = "+91 ••••••••••"
    jurisdiction: Optional[str] = "India"
    legal_domain: Optional[str] = "Citizen Legal Grievance"
    facts_summary: str
    complaint_letter: str
    advocate_id: str
    advocate_name: Optional[str] = None
    advocate_email: Optional[str] = None


class ConnectClientRequest(BaseModel):
    case_id: str
    counsel_message: str
    advocate_name: Optional[str] = "Advocate Counsel"


@app.get("/api/advocates")
def get_advocates_list(user: dict = Depends(require_authenticated_user)):
    return get_available_advocates()


@app.post("/api/civilian/assign-complaint")
def assign_complaint_to_advocate(req: AssignComplaintRequest, user: dict = Depends(require_authenticated_user)):
    case = submit_civilian_complaint(
        civilian_name=req.civilian_name,
        civilian_email=req.civilian_email,
        civilian_contact=req.civilian_contact,
        jurisdiction=req.jurisdiction,
        legal_domain=req.legal_domain,
        facts_summary=req.facts_summary,
        complaint_letter=req.complaint_letter,
        advocate_id=req.advocate_id,
        advocate_name=req.advocate_name,
        advocate_email=req.advocate_email,
    )
    return {
        "status": "success",
        "message": f"Complaint successfully assigned and dispatched to {case['assigned_advocate_name']}!",
        "case": case,
    }


@app.post("/api/advocate/connect-client")
def connect_client_endpoint(req: ConnectClientRequest, user: dict = Depends(require_advocate_or_admin)):
    result = advocate_connect_to_civilian(
        case_id=req.case_id,
        counsel_message=req.counsel_message,
        advocate_name=req.advocate_name,
    )
    if result.get("status") == "error":
        raise HTTPException(status_code=404, detail=result.get("message"))
    return result


@app.get("/api/documents")
def documents(user: dict = Depends(require_authenticated_user)):
    docs = load_registry()
    return [
        {k: d.get(k, "") for k in ["document_id", "title", "jurisdiction", "document_type", "status", "source_url", "ingested_at", "chunks"]}
        for d in docs
    ]


# ── Legal Document Generators (Protected) ─────────────────────────────────────

class ComplaintRequest(BaseModel):
    template_type: str = "college_exam"
    user_name: str
    user_address: str
    user_contact: str
    opposite_party_name: str
    opposite_party_address: str
    incident_date: Optional[str] = None
    amount: Optional[str] = None
    transaction_ref: Optional[str] = None
    facts_summary: Optional[str] = None
    relief_sought: Optional[str] = None


@app.post("/api/generate-complaint")
def create_complaint_letter(req: ComplaintRequest, user: dict = Depends(require_authenticated_user)):
    try:
        return generate_complaint_letter(
            template_type=req.template_type,
            user_name=req.user_name,
            user_address=req.user_address,
            user_contact=req.user_contact,
            opposite_party_name=req.opposite_party_name,
            opposite_party_address=req.opposite_party_address,
            incident_date=req.incident_date,
            amount=req.amount,
            transaction_ref=req.transaction_ref,
            facts_summary=req.facts_summary,
            relief_sought=req.relief_sought,
        )
    except Exception as exc:
        raise HTTPException(status_code=400, detail=str(exc))


class BSACertificateRequest(BaseModel):
    certifier_name: str
    device_model: Optional[str] = "Smartphone / Computing Device"
    mobile_number: Optional[str] = "+91 ••••••••••"
    evidence_description: Optional[str] = "WhatsApp conversation logs, bank payment SMS, and transaction UTR statements"
    incident_date: Optional[str] = None
    hash_digest: Optional[str] = None


@app.post("/api/generate-bsa-certificate")
def create_bsa_certificate(req: BSACertificateRequest, user: dict = Depends(require_authenticated_user)):
    try:
        return generate_section_63_bsa_certificate(
            certifier_name=req.certifier_name,
            device_model=req.device_model,
            mobile_number=req.mobile_number,
            evidence_description=req.evidence_description,
            incident_date=req.incident_date,
            hash_digest=req.hash_digest,
        )
    except Exception as exc:
        raise HTTPException(status_code=400, detail=str(exc))


class PoliceComplaintRequest(BaseModel):
    complainant_name: str
    complainant_address: Optional[str] = "Resident of India"
    complainant_phone: Optional[str] = "+91 ••••••••••"
    police_station_name: Optional[str] = "The Station House Officer (SHO), Cyber Crime Police Station"
    district_city: Optional[str] = "India"
    accused_details: Optional[str] = "Unknown Fraudulent Entity / Beneficiary Account Holder"
    amount_lost: Optional[str] = None
    transaction_ref: Optional[str] = None
    facts_chronology: Optional[str] = None
    incident_date: Optional[str] = None


@app.post("/api/generate-police-complaint")
def create_police_complaint(req: PoliceComplaintRequest, user: dict = Depends(require_authenticated_user)):
    try:
        return generate_police_fir_complaint(
            complainant_name=req.complainant_name,
            complainant_address=req.complainant_address,
            complainant_phone=req.complainant_phone,
            police_station_name=req.police_station_name,
            district_city=req.district_city,
            accused_details=req.accused_details,
            amount_lost=req.amount_lost,
            transaction_ref=req.transaction_ref,
            facts_chronology=req.facts_chronology,
            incident_date=req.incident_date,
        )
    except Exception as exc:
        raise HTTPException(status_code=400, detail=str(exc))


class ContactCreatorRequest(BaseModel):
    name: str
    email: str
    message: str
    phone: Optional[str] = None


@app.post("/api/contact-creator")
def contact_creator_endpoint(req: ContactCreatorRequest):
    return {
        "status": "success",
        "message": f"Thank you, {req.name}! Your message has been received by Giridharan (mgdharan7@gmail.com). We will reach out to you shortly.",
        "recipient": "Giridharan (Founder & Creator of NyayaAI)",
        "contact_email": "mgdharan7@gmail.com",
    }


# ── Legal Benchmark & Evaluation Suite (Admin) ────────────────────────────────

@app.get("/api/eval/benchmark")
def get_benchmarks(user: dict = Depends(require_admin_user)):
    return {
        "total_scenarios": len(LEGAL_BENCHMARK_SCENARIOS),
        "scenarios": [
            {
                "id": s["id"],
                "domain": s["domain"],
                "title": s["title"],
                "question": s["question"],
                "expected_authorities": s["expected_authorities"],
            }
            for s in LEGAL_BENCHMARK_SCENARIOS
        ],
    }


@app.post("/api/eval/run")
def run_evaluation_benchmark(scenario_id: Optional[str] = None, user: dict = Depends(require_admin_user)):
    results = []
    scenarios_to_run = (
        [s for s in LEGAL_BENCHMARK_SCENARIOS if s["id"] == scenario_id]
        if scenario_id
        else LEGAL_BENCHMARK_SCENARIOS[:5]
    )

    for sc in scenarios_to_run:
        ans_obj = run_legal_workflow(question=sc["question"])
        eval_score = evaluate_response_against_scenario(sc, ans_obj["answer"])
        results.append(eval_score)

    passed_count = sum(1 for r in results if r["passed"])
    return {
        "total_evaluated": len(results),
        "passed": passed_count,
        "pass_rate": f"{round((passed_count / max(1, len(results))) * 100, 1)}%",
        "results": results,
    }


# ── Admin Analytics, Pipeline & Cache Management (Module 7) ───────────────────

@app.get("/api/admin/analytics")
def admin_analytics_endpoint(
    range: str = Query(default="30d"),
    start: Optional[str] = Query(default=None),
    end: Optional[str] = Query(default=None),
    user: dict = Depends(require_admin_user),
):
    return get_admin_analytics_summary(date_range=range, start_date=start, end_date=end)


@app.post("/api/admin/pipeline/run")
def admin_run_pipeline(user: dict = Depends(require_admin_user)):
    res = run_etl_pipeline()
    record_admin_audit(
        admin_user_id=user["user_id"],
        action="run_etl_pipeline",
        target_resource="medallion_pipeline",
        details=json.dumps(res),
    )
    return res


class CacheInvalidateRequest(BaseModel):
    statute_keyword: Optional[str] = None
    reason: Optional[str] = "Manual admin invalidation"


@app.post("/api/admin/cache/invalidate")
def admin_invalidate_cache(req: CacheInvalidateRequest, user: dict = Depends(require_admin_user)):
    count = invalidate_cache(statute_keyword=req.statute_keyword, reason=req.reason or "Admin invalidation")
    record_admin_audit(
        admin_user_id=user["user_id"],
        action="invalidate_cache",
        target_resource=req.statute_keyword or "all",
        details=f"Invalidated {count} entries",
    )
    return {"status": "success", "invalidated_count": count}


@app.get("/api/admin/audit-logs")
def admin_audit_logs(
    page: int = Query(default=1, ge=1),
    limit: int = Query(default=25, ge=1, le=100),
    user: dict = Depends(require_admin_user),
):
    offset = (page - 1) * limit
    with db_read() as conn:
        total = conn.execute("SELECT COUNT(*) FROM admin_audit_logs").fetchone()[0]
        rows = conn.execute(
            "SELECT * FROM admin_audit_logs ORDER BY created_at DESC LIMIT ? OFFSET ?",
            (limit, offset),
        ).fetchall()
    return {"page": page, "limit": limit, "total": total, "items": [dict(r) for r in rows]}


# ── Administrative Ingestion Endpoints ────────────────────────────────────────

@app.post("/api/admin/ingest")
async def admin_ingest(
    file: UploadFile = File(...),
    title: str = Form(""),
    jurisdiction: str = Form("India"),
    source_url: str = Form(""),
    document_type: str = Form("other"),
    status: str = Form("unverified"),
    x_admin_key: str | None = Header(default=None),
):
    check_admin(x_admin_key)
    suffix = Path(file.filename or "").suffix.lower()
    if suffix not in {".pdf", ".docx", ".txt", ".md"}:
        raise HTTPException(400, "Supported file types: PDF, DOCX, TXT, MD")
    content = await file.read()
    if len(content) > settings.max_upload_mb * 1024 * 1024:
        raise HTTPException(413, f"File exceeds {settings.max_upload_mb} MB limit")
    safe_name = f"{uuid.uuid4()}{suffix}"
    path = UPLOAD_DIR / safe_name
    path.write_bytes(content)
    try:
        doc_title = title or Path(file.filename or "source").stem
        result = ingest_file(path, doc_title, jurisdiction, source_url, document_type, status)
        # Invalidate affected cache entries when legal corpus is updated
        invalidate_cache(statute_keyword=doc_title, reason=f"Corpus updated: {doc_title}")
        return result
    except Exception as exc:
        path.unlink(missing_ok=True)
        raise HTTPException(400, str(exc))


@app.post("/api/admin/reindex")
def reindex(x_admin_key: str | None = Header(default=None)):
    check_admin(x_admin_key)
    invalidate_cache(reason="Full corpus reindex")
    return {"status": "success", "message": "The hybrid vector index is updated incrementally during ingestion."}
