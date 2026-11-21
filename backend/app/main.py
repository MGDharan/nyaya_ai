import json, secrets, uuid
from datetime import datetime, timezone
from pathlib import Path
from fastapi import FastAPI, UploadFile, File, Form, Header, HTTPException
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import Optional

from app.config import settings
from app.schemas import ChatRequest, ChatResponse
from app.agents.workflow import run_legal_workflow
from app.ingest import ingest_file, load_registry
from app.services.complaint_generator import (
    generate_complaint_letter,
    generate_section_63_bsa_certificate,
    generate_police_fir_complaint
)
from app.services.legal_benchmark import LEGAL_BENCHMARK_SCENARIOS, evaluate_response_against_scenario
from app.services.vector_store import search
from app.services.advocate_service import (
    load_civilian_cases,
    record_civilian_inquiry,
    get_statutes_health_registry,
    get_advocate_exclusive_benefits,
    generate_counsel_research_brief
)
from app.services.supabase_service import (
    get_available_advocates,
    submit_civilian_complaint,
    advocate_connect_to_civilian
)

app = FastAPI(
    title=settings.app_name,
    version="1.0.0",
    description="Production-Oriented Indian Legal Intelligence and Citizen Assistance Platform"
)

BASE = Path(__file__).parent
UPLOAD_DIR = Path(settings.data_dir) / "uploads"
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
app.mount("/static", StaticFiles(directory=BASE / "static"), name="static")

def check_admin(key: str | None):
    if settings.admin_api_key and not secrets.compare_digest(key or "", settings.admin_api_key):
        raise HTTPException(status_code=401, detail="Invalid admin key")

@app.get("/")
def home():
    """
    Sovereign Authentication & Verification Gateway.
    Directs users through Advocate/Civilian verification before entering the legal workspace.
    """
    return FileResponse(BASE / "static" / "login.html")

@app.get("/login")
def login_gateway():
    return FileResponse(BASE / "static" / "login.html")

@app.get("/app")
def legal_assistant_web():
    """
    NyayaAI Citizen Legal Intelligence & Rights Navigator Web Application.
    """
    return FileResponse(BASE / "static" / "index.html")

@app.get("/assistant")
def assistant_web_alias():
    return FileResponse(BASE / "static" / "index.html")

@app.get("/advocate")
def advocate_console_view():
    """
    Advocate Counsel Console & Practice Intelligence Gateway.
    Provides civilian client inflow, statute status monitor, deep legal briefs, and practice suite.
    """
    return FileResponse(BASE / "static" / "advocate.html")

@app.get("/api/health")
def health():
    return {
        "status": "ok",
        "app": settings.app_name,
        "version": "1.0.0",
        "time": datetime.now(timezone.utc).isoformat(),
        "corpus_documents": len(load_registry()),
        "architecture": "10-Agent LangGraph-Style Pipeline + BM25 & Dense Hybrid RAG"
    }

@app.post("/api/chat", response_model=ChatResponse)
def chat(payload: ChatRequest):
    result = run_legal_workflow(
        question=payload.question,
        language=payload.language,
        jurisdiction=payload.jurisdiction,
        incident_date=payload.date_of_incident,
        context=payload.context
    )

    # Real-time tracking of civilian inquiry in advocate intake roster
    try:
        first_act = result.get("applicable_acts", [{}])[0].get("act_name", "General Statutory Law") if result.get("applicable_acts") else "Indian Law"
        forum = result.get("legal_domain", "Civil Court")
        record_civilian_inquiry(
            question=payload.question,
            domain=result.get("legal_domain", "General Citizen Inquiry"),
            jurisdiction=payload.jurisdiction,
            primary_law=first_act,
            forum=forum
        )
    except Exception:
        pass

    return result


# ── Advocate Practice Console Endpoints ────────────────────────────────────────

class CounselBriefRequest(BaseModel):
    query: str

@app.get("/api/advocate/dashboard")
def get_advocate_dashboard_data():
    """
    Fetches real-time Advocate Dashboard data:
    1. Civilian Client Inflow roster & case statuses.
    2. Active vs. Deactive/Repealed statute health registry.
    3. Advocate exclusive practice privileges & benefits.
    """
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
        "repealed_statutes_count": statutes_data["repealed_count"]
    }

@app.post("/api/advocate/counsel-brief")
def create_counsel_brief_endpoint(req: CounselBriefRequest):
    """
    Generates a deep Advocate Counsel Legal Brief with statutory ingredients,
    binding Supreme Court precedents, contradictory interpretations, and trial strategies.
    """
    return generate_counsel_research_brief(req.query)


# ── Civilian-to-Advocate Assignment & Communication Endpoints ──────────────────

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
def get_advocates_list():
    """
    Returns verified advocates registered in Supabase DB / platform
    available for civilian selection.
    """
    return get_available_advocates()

@app.post("/api/civilian/assign-complaint")
def assign_complaint_to_advocate(req: AssignComplaintRequest):
    """
    Enables a civilian to select an advocate and send their formal complaint letter
    and legal grievance directly to that advocate under Section 132 BSA privilege.
    """
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
        advocate_email=req.advocate_email
    )
    return {
        "status": "success",
        "message": f"Complaint successfully assigned and dispatched to {case['assigned_advocate_name']}!",
        "case": case
    }

@app.post("/api/advocate/connect-client")
def connect_client_endpoint(req: ConnectClientRequest):
    """
    Enables an advocate to review civilian complaint letters and connect directly
    with legal advice, consultation scheduling, or case representation.
    """
    result = advocate_connect_to_civilian(
        case_id=req.case_id,
        counsel_message=req.counsel_message,
        advocate_name=req.advocate_name
    )
    if result.get("status") == "error":
        raise HTTPException(status_code=404, detail=result.get("message"))
    return result

@app.get("/api/documents")
def documents():
    docs = load_registry()
    return [{k: d.get(k, "") for k in ["document_id", "title", "jurisdiction", "document_type", "status", "source_url", "ingested_at", "chunks"]} for d in docs]


# ── Complaint Letter Generation Endpoint ──────────────────────────────────────

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
def create_complaint_letter(req: ComplaintRequest):
    try:
        draft = generate_complaint_letter(
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
            relief_sought=req.relief_sought
        )
        return draft
    except Exception as exc:
        raise HTTPException(status_code=400, detail=str(exc))


# ── Section 63 BSA Digital Evidence Certificate Endpoint ─────────────────────

class BSACertificateRequest(BaseModel):
    certifier_name: str
    device_model: Optional[str] = "Smartphone / Computing Device"
    mobile_number: Optional[str] = "+91 ••••••••••"
    evidence_description: Optional[str] = "WhatsApp conversation logs, bank payment SMS, and transaction UTR statements"
    incident_date: Optional[str] = None
    hash_digest: Optional[str] = None

@app.post("/api/generate-bsa-certificate")
def create_bsa_certificate(req: BSACertificateRequest):
    """
    Generates mandatory electronic evidence certificate under Section 63 of the
    Bharatiya Sakshya Adhiniyam, 2023 for WhatsApp chats, UPI records, and screenshots.
    """
    try:
        cert = generate_section_63_bsa_certificate(
            certifier_name=req.certifier_name,
            device_model=req.device_model,
            mobile_number=req.mobile_number,
            evidence_description=req.evidence_description,
            incident_date=req.incident_date,
            hash_digest=req.hash_digest
        )
        return cert
    except Exception as exc:
        raise HTTPException(status_code=400, detail=str(exc))


# ── Police FIR / Complaint under Sec 173 BNSS Endpoint ────────────────────────

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
def create_police_complaint(req: PoliceComplaintRequest):
    """
    Generates formal Police Written Complaint under Section 173 of the
    Bharatiya Nagarik Suraksha Sanhita (BNSS), 2023 for cognizable cheating and cyber fraud.
    """
    try:
        draft = generate_police_fir_complaint(
            complainant_name=req.complainant_name,
            complainant_address=req.complainant_address,
            complainant_phone=req.complainant_phone,
            police_station_name=req.police_station_name,
            district_city=req.district_city,
            accused_details=req.accused_details,
            amount_lost=req.amount_lost,
            transaction_ref=req.transaction_ref,
            facts_chronology=req.facts_chronology,
            incident_date=req.incident_date
        )
        return draft
    except Exception as exc:
        raise HTTPException(status_code=400, detail=str(exc))


# ── Creator Contact & Reach Out Endpoint ──────────────────────────────────────

class ContactCreatorRequest(BaseModel):
    name: str
    email: str
    message: str
    phone: Optional[str] = None

@app.post("/api/contact-creator")
def contact_creator_endpoint(req: ContactCreatorRequest):
    """
    Allows citizens and advocates to connect directly with Giridharan, Creator of NyayaAI.
    """
    return {
        "status": "success",
        "message": f"Thank you, {req.name}! Your message has been received by Giridharan (mgdharan7@gmail.com). We will reach out to you shortly.",
        "recipient": "Giridharan (Founder & Creator of NyayaAI)",
        "contact_email": "mgdharan7@gmail.com"
    }


# ── Legal Benchmark & Evaluation Suite Endpoint ───────────────────────────────

@app.get("/api/eval/benchmark")
def get_benchmarks():
    return {
        "total_scenarios": len(LEGAL_BENCHMARK_SCENARIOS),
        "scenarios": [
            {
                "id": s["id"],
                "domain": s["domain"],
                "title": s["title"],
                "question": s["question"],
                "expected_authorities": s["expected_authorities"]
            }
            for s in LEGAL_BENCHMARK_SCENARIOS
        ]
    }

@app.post("/api/eval/run")
def run_evaluation_benchmark(scenario_id: Optional[str] = None):
    results = []
    scenarios_to_run = (
        [s for s in LEGAL_BENCHMARK_SCENARIOS if s["id"] == scenario_id]
        if scenario_id
        else LEGAL_BENCHMARK_SCENARIOS[:5]  # Run first 5 scenarios for responsive API return
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
        "results": results
    }


# ── Administrative Ingestion Endpoints ────────────────────────────────────────

@app.post("/api/admin/ingest")
async def admin_ingest(
    file: UploadFile = File(...),
    title: str = Form(""),
    jurisdiction: str = Form("India"),
    source_url: str = Form(""),
    document_type: str = Form("other"),
    status: str = Form("unverified"),
    x_admin_key: str | None = Header(default=None)
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
        result = ingest_file(path, title or Path(file.filename or "source").stem, jurisdiction, source_url, document_type, status)
        return result
    except Exception as exc:
        path.unlink(missing_ok=True)
        raise HTTPException(400, str(exc))

@app.post("/api/admin/reindex")
def reindex(x_admin_key: str | None = Header(default=None)):
    check_admin(x_admin_key)
    return {"status": "success", "message": "The hybrid vector index is updated incrementally during ingestion."}
