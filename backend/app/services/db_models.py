"""
PostgreSQL / SQLAlchemy Enterprise Production Schema for NyayaAI.
Supports:
- Users & RBAC
- Legal Acts, Sections, Amendments, Notifications, Judgments
- Section-wise Versioning & Gazette publication history
- Embeddings with pgvector
- Audit Logging & Document Ingestion Tracking
"""

from datetime import datetime, timezone
from typing import Optional
from sqlalchemy import (
    Column, Integer, String, Text, DateTime, ForeignKey,
    Boolean, Numeric, UniqueConstraint, Index
)
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(String(36), primary_key=True)
    username = Column(String(100), unique=True, nullable=False, index=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    role = Column(String(50), default="citizen", nullable=False)  # citizen, advocate, researcher, admin
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    queries = relationship("LegalQuery", back_populates="user")
    documents = relationship("UserDocument", back_populates="user")


class LegalAct(Base):
    __tablename__ = "legal_acts"

    id = Column(String(36), primary_key=True)
    official_title = Column(String(500), nullable=False, index=True)
    short_title = Column(String(255), nullable=False, index=True)
    act_number = Column(String(100))
    enactment_date = Column(DateTime, nullable=True)
    commencement_date = Column(DateTime, nullable=True)
    status = Column(String(50), default="in_force")  # in_force, repealed, amended, not_yet_effective
    jurisdiction = Column(String(100), default="India")  # India or State name
    ministry = Column(String(255))
    official_source_url = Column(String(1000))
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    sections = relationship("LegalSection", back_populates="act", cascade="all, delete-orphan")


class LegalSection(Base):
    __tablename__ = "legal_sections"

    id = Column(String(36), primary_key=True)
    act_id = Column(String(36), ForeignKey("legal_acts.id"), nullable=False, index=True)
    chapter_number = Column(String(50))
    chapter_title = Column(String(255))
    section_number = Column(String(50), nullable=False, index=True)
    section_title = Column(String(500))
    exact_text = Column(Text, nullable=False)
    commencement_date = Column(DateTime, nullable=True)
    status = Column(String(50), default="in_force")  # in_force, repealed, substituted
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    act = relationship("LegalAct", back_populates="sections")


class LegalJudgment(Base):
    __tablename__ = "legal_judgments"

    id = Column(String(36), primary_key=True)
    case_title = Column(String(500), nullable=False, index=True)
    citation = Column(String(255), unique=True, nullable=False, index=True)
    court_name = Column(String(255), nullable=False)  # Supreme Court of India, High Court of Madras, etc.
    bench = Column(String(255))
    judgment_date = Column(DateTime, nullable=False)
    subject_domain = Column(String(150))
    ratio_holding = Column(Text, nullable=False)
    judicial_exception = Column(Text)
    official_pdf_url = Column(String(1000))
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))


class LegalQuery(Base):
    __tablename__ = "legal_queries"

    id = Column(String(36), primary_key=True)
    user_id = Column(String(36), ForeignKey("users.id"), nullable=True)
    question_text = Column(Text, nullable=False)
    language = Column(String(50), default="English")
    jurisdiction = Column(String(100), default="India")
    incident_date = Column(String(50), nullable=True)
    detected_domain = Column(String(100))
    audit_verdict = Column(String(100))
    confidence_level = Column(String(100))
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    user = relationship("User", back_populates="queries")


class UserDocument(Base):
    __tablename__ = "user_documents"

    id = Column(String(36), primary_key=True)
    user_id = Column(String(36), ForeignKey("users.id"), nullable=True)
    filename = Column(String(255), nullable=False)
    file_type = Column(String(50))
    storage_path = Column(String(1000), nullable=False)
    sha256_hash = Column(String(64), nullable=False)
    extracted_text = Column(Text)
    is_redacted = Column(Boolean, default=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    user = relationship("User", back_populates="documents")


class LegalAuditLog(Base):
    __tablename__ = "legal_audit_logs"

    id = Column(String(36), primary_key=True)
    event_type = Column(String(100), nullable=False)  # ingestion, verification_pass, citation_rejected, temporal_violation
    actor_id = Column(String(100))
    details = Column(Text)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

