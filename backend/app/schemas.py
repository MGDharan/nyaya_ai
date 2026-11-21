from pydantic import BaseModel, Field
from typing import Optional, List

class ChatRequest(BaseModel):
    question: str = Field(min_length=8, max_length=8000)
    language: str = "English"
    jurisdiction: str = "India"
    date_of_incident: Optional[str] = None
    context: Optional[str] = Field(default=None, max_length=4000)

class LegalClaim(BaseModel):
    act_name: str
    section_number: str
    exact_provision_text: str
    official_source: str
    effective_date: str
    current_status: str  # in_force, repealed, amended, not_yet_in_force
    relevant_judicial_precedents: List[str] = []
    jurisdiction: str = "India"
    verification_timestamp: str
    confidence_level: str  # verified, caution, unverified, refuted
    claim_type: str = "statutory"  # statutory, judicial_precedent, regulatory_norm, practical_recommendation
    in_force_on_incident_date: Optional[bool] = None
    conflicting_interpretations: List[str] = []
    verification_notes: Optional[str] = None
    is_verified: bool = False

class VerificationSummary(BaseModel):
    total_claims_detected: int = 0
    verified_claims_count: int = 0
    unverified_claims_count: int = 0
    caution_flags_count: int = 0
    temporal_validity_checked: bool = False
    education_dispute_evaluated: bool = False
    audit_verdict: str = "Passed"

class ChatResponse(BaseModel):
    answer: str
    agents: List[dict]
    sources: List[dict]
    confidence: str
    disclaimer: str
    claims: List[LegalClaim] = []
    verification_summary: Optional[VerificationSummary] = None

class DocumentInfo(BaseModel):
    id: str
    title: str
    jurisdiction: str
    document_type: str
    status: str
    source_url: str
    ingested_at: str
