"""
Intelligent Legal AI Caching Engine (Exact + Semantic Cache with Legal Safety Validation)

Guarantees:
1. Query normalization before exact cache lookup.
2. Semantic cache via embeddings with configurable similarity threshold.
3. Legal Safety Guard: Never mixes criminal, civil, constitutional, consumer, or education contexts,
   and checks jurisdiction + incident_date + applicable provisions before reusing an answer.
4. TTL expiration & statute-based invalidation (never caches legal answers indefinitely).
"""

import hashlib
import json
import math
import re
from datetime import datetime, timedelta, timezone
from typing import Any, Dict, List, Optional, Tuple

from app.config import settings
from app.services.database import db_read, db_transaction
from app.services.legal_classifier import LegalClassificationEngine

PROMPT_VERSION = "nyaya-prompt-v2.0"
SOURCE_VERSION = "indian-statutes-2026.1"
DEFAULT_CACHE_TTL_HOURS = 168  # 7 days max TTL
SEMANTIC_SIMILARITY_THRESHOLD = 0.88

_classifier = LegalClassificationEngine()


def normalize_query(question: str) -> str:
    """Normalize legal question for consistent exact cache matching."""
    q = (question or "").strip().lower()
    # Expand common Indian legal abbreviations
    q = re.sub(r"\bf\.?i\.?r\.?\b", "fir", q)
    q = re.sub(r"\bu\.?p\.?i\.?\b", "upi", q)
    q = re.sub(r"\br\.?t\.?i\.?\b", "rti", q)
    q = re.sub(r"\bb\.?n\.?s\.?\b", "bns", q)
    q = re.sub(r"\bi\.?p\.?c\.?\b", "ipc", q)
    q = re.sub(r"[^\w\s]", " ", q)
    q = re.sub(r"\s+", " ", q).strip()
    return q


def build_exact_cache_key(
    normalized_question: str,
    jurisdiction: str,
    language: str,
    incident_date: Optional[str] = None,
) -> str:
    raw = f"{normalized_question}|{jurisdiction.lower()}|{language.lower()}|{incident_date or ''}|{PROMPT_VERSION}|{SOURCE_VERSION}"
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()


def _cosine_similarity(a: List[float], b: List[float]) -> float:
    if not a or not b or len(a) != len(b):
        return 0.0
    dot = sum(x * y for x, y in zip(a, b))
    na = math.sqrt(sum(x * x for x in a))
    nb = math.sqrt(sum(y * y for y in b))
    if na == 0.0 or nb == 0.0:
        return 0.0
    return dot / (na * nb)


def lookup_cached_response(
    *,
    question: str,
    jurisdiction: str = "India",
    language: str = "English",
    incident_date: Optional[str] = None,
    query_embedding: Optional[List[float]] = None,
    semantic_threshold: float = SEMANTIC_SIMILARITY_THRESHOLD,
) -> Tuple[Optional[Dict[str, Any]], str, Optional[str]]:
    """
    Attempts:
    1. Exact cache lookup by normalized key.
    2. Semantic cache lookup (only if legal domain, jurisdiction, and provisions match safely).

    Returns: (cached_response_dict | None, cache_status ['hit_exact'|'hit_semantic'|'miss'], matched_key | None)
    """
    norm_q = normalize_query(question)
    exact_key = build_exact_cache_key(norm_q, jurisdiction, language, incident_date)
    now_iso = datetime.now(timezone.utc).isoformat()

    # 1. Exact Cache Check
    with db_read() as conn:
        row = conn.execute(
            """
            SELECT * FROM cache_metadata
            WHERE cache_key = ? AND invalidated = 0 AND expires_at > ?
            """,
            (exact_key, now_iso),
        ).fetchone()

    if row:
        try:
            payload = json.loads(row["response_json"])
            with db_transaction() as conn:
                conn.execute(
                    "UPDATE cache_metadata SET hit_count = hit_count + 1 WHERE cache_key = ?",
                    (exact_key,),
                )
            return payload, "hit_exact", exact_key
        except Exception:
            pass

    # 2. Semantic Cache Check (skip if incident_date is specified for temporal safety, or if no embedding)
    if not query_embedding or all(v == 0.0 for v in query_embedding[:8]):
        return None, "miss", None

    # Classify incoming question's legal domain & statutory context
    cls_res = _classifier.classify(query=question, incident_date=incident_date, jurisdiction=jurisdiction)
    target_domain = (cls_res.get("domain") or "General").lower()

    with db_read() as conn:
        candidates = conn.execute(
            """
            SELECT cache_key, original_question, normalized_question, question_embedding_json,
                   jurisdiction, language, legal_domain, applicable_provisions_json, response_json
            FROM cache_metadata
            WHERE invalidated = 0
              AND expires_at > ?
              AND lower(jurisdiction) = lower(?)
              AND lower(language) = lower(?)
              AND question_embedding_json IS NOT NULL
            ORDER BY hit_count DESC, created_at DESC
            LIMIT 100
            """,
            (now_iso, jurisdiction, language),
        ).fetchall()

    best_score = 0.0
    best_row = None

    for cand in candidates:
        # Legal Safety Guard 1: Never mix legal domains (criminal vs civil vs consumer vs education)
        cand_domain = (cand["legal_domain"] or "General").lower()
        if cand_domain != target_domain:
            continue

        try:
            cand_emb = json.loads(cand["question_embedding_json"])
        except Exception:
            continue

        sim = _cosine_similarity(query_embedding, cand_emb)
        if sim >= semantic_threshold and sim > best_score:
            best_score = sim
            best_row = cand

    if best_row:
        try:
            payload = json.loads(best_row["response_json"])
            # Legal Safety Guard 2: Verify cached answer has valid non-empty provisions/claims
            if not payload.get("answer"):
                return None, "miss", None
            with db_transaction() as conn:
                conn.execute(
                    "UPDATE cache_metadata SET hit_count = hit_count + 1 WHERE cache_key = ?",
                    (best_row["cache_key"],),
                )
            return payload, "hit_semantic", best_row["cache_key"]
        except Exception:
            pass

    return None, "miss", None


def store_cached_response(
    *,
    question: str,
    jurisdiction: str,
    language: str,
    incident_date: Optional[str],
    legal_domain: str,
    applicable_provisions: List[str],
    response_payload: Dict[str, Any],
    query_embedding: Optional[List[float]] = None,
    ttl_hours: int = DEFAULT_CACHE_TTL_HOURS,
) -> str:
    """Stores a validated legal AI response in `cache_metadata` with strict versioning & TTL."""
    norm_q = normalize_query(question)
    cache_key = build_exact_cache_key(norm_q, jurisdiction, language, incident_date)
    now = datetime.now(timezone.utc)
    expires = now + timedelta(hours=ttl_hours)

    model_ver = settings.gemini_model if settings.llm_provider == "gemini" else settings.ollama_model
    emb_ver = "gemini-embedding-001" if settings.llm_provider == "gemini" else settings.embedding_model

    with db_transaction() as conn:
        conn.execute(
            """
            INSERT INTO cache_metadata
            (cache_key, original_question, normalized_question, question_embedding_json,
             jurisdiction, language, legal_domain, applicable_provisions_json,
             source_version, model_version, prompt_version, embedding_model_version,
             response_json, hit_count, created_at, expires_at, invalidated)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 0, ?, ?, 0)
            ON CONFLICT(cache_key) DO UPDATE SET
                response_json = excluded.response_json,
                question_embedding_json = excluded.question_embedding_json,
                applicable_provisions_json = excluded.applicable_provisions_json,
                expires_at = excluded.expires_at,
                invalidated = 0,
                invalidation_reason = NULL
            """,
            (
                cache_key,
                question,
                norm_q,
                json.dumps(query_embedding) if query_embedding else None,
                jurisdiction,
                language,
                legal_domain or "General",
                json.dumps(applicable_provisions),
                SOURCE_VERSION,
                model_ver,
                PROMPT_VERSION,
                emb_ver,
                json.dumps(response_payload),
                now.isoformat(),
                expires.isoformat(),
            ),
        )
    return cache_key


def invalidate_cache(
    *,
    statute_keyword: Optional[str] = None,
    reason: str = "Legislative / corpus update",
) -> int:
    """
    Invalidates cached legal answers either globally or matching a specific statute/domain keyword.
    Called automatically when new statutes are ingested or manually by Admin.
    """
    with db_transaction() as conn:
        if statute_keyword:
            kw = f"%{statute_keyword.lower()}%"
            cur = conn.execute(
                """
                UPDATE cache_metadata
                SET invalidated = 1, invalidation_reason = ?
                WHERE invalidated = 0
                  AND (lower(applicable_provisions_json) LIKE ?
                       OR lower(legal_domain) LIKE ?
                       OR lower(original_question) LIKE ?)
                """,
                (reason, kw, kw, kw),
            )
        else:
            cur = conn.execute(
                """
                UPDATE cache_metadata
                SET invalidated = 1, invalidation_reason = ?
                WHERE invalidated = 0
                """,
                (reason,),
            )
        return cur.rowcount

