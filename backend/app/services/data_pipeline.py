"""
NyayaAI Medallion Data Engineering Pipeline (Bronze -> Silver -> Gold)
& Structured JSON Observability.

Design Guarantees:
1. Analytics failures NEVER block or crash user legal queries (graceful degradation).
2. Idempotent ingestion via unique event_id & source_event_id.
3. Dead-letter queue (DLQ) for malformed events.
4. Incremental Gold aggregation over touched UTC dates only.
5. Privacy separation: operational logs never store private user questions.
"""

import hashlib
import json
import logging
import threading
import time
import uuid
from datetime import datetime, timedelta, timezone
from typing import Any, Dict, List, Optional

from app.services.database import db_read, db_transaction

logger = logging.getLogger("nyaya.pipeline")

APP_START_TIME = time.time()
VALID_EVENT_TYPES = {
    "user_login",
    "user_login_failed",
    "user_logout",
    "ai_request",
    "ai_response",
    "cache_hit",
    "cache_miss",
    "api_error",
    "admin_action",
}

# Gemini 2.5 Flash reference pricing (USD per 1M tokens)
GEMINI_INPUT_PRICE_PER_1M = 0.15
GEMINI_OUTPUT_PRICE_PER_1M = 0.60


def log_json(level: str, event: str, **fields: Any) -> None:
    """Emit structured JSON log line."""
    record = {
        "ts": datetime.now(timezone.utc).isoformat(),
        "level": level.upper(),
        "event": event,
        **fields,
    }
    msg = json.dumps(record, default=str)
    if level.lower() == "error":
        logger.error(msg)
    elif level.lower() == "warning":
        logger.warning(msg)
    else:
        logger.info(msg)


def estimate_tokens(text: str) -> int:
    """Fast deterministic token estimator (~4 chars per token) when provider omits usage."""
    if not text:
        return 0
    return max(1, len(text) // 4)


def estimate_cost_usd(model: str, input_tokens: int, output_tokens: int) -> float:
    m = (model or "").lower()
    if "ollama" in m or "offline" in m or "cache" in m:
        return 0.0
    if "gpt-4o-mini" in m:
        return round((input_tokens * 0.15 + output_tokens * 0.60) / 1_000_000, 8)
    # Default Gemini 2.5 Flash pricing
    return round(
        (input_tokens * GEMINI_INPUT_PRICE_PER_1M + output_tokens * GEMINI_OUTPUT_PRICE_PER_1M)
        / 1_000_000,
        8,
    )


# ── BRONZE LAYER: Raw Event Ingestion ─────────────────────────────────────────

def ingest_bronze_event(
    event_type: str,
    user_id: Optional[str] = None,
    session_id: Optional[str] = None,
    status: str = "ok",
    payload: Optional[Dict[str, Any]] = None,
    event_id: Optional[str] = None,
    schema_version: str = "1.0",
) -> Optional[str]:
    """
    Idempotently appends a raw event into the Bronze table (`activity_events`).
    Never raises exceptions to callers — degrades gracefully on failure.
    """
    eid = event_id or str(uuid.uuid4())
    now_utc = datetime.now(timezone.utc).isoformat()
    safe_payload = dict(payload or {})
    # Strip any accidental sensitive keys
    for forbidden in ("password", "token", "access_token", "refresh_token", "question", "answer"):
        safe_payload.pop(forbidden, None)

    try:
        with db_transaction() as conn:
            conn.execute(
                """
                INSERT OR IGNORE INTO activity_events
                (event_id, event_type, schema_version, user_id, session_id, status, payload_json, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    eid,
                    str(event_type or "").strip(),
                    schema_version,
                    user_id,
                    session_id,
                    status,
                    json.dumps(safe_payload, default=str),
                    now_utc,
                ),
            )
        return eid
    except Exception as exc:
        log_json("warning", "bronze_ingest_degraded", error=str(exc), event_type=event_type)
        return None


def ingest_bronze_event_async(**kwargs: Any) -> None:
    """Fire-and-forget background thread ingestion so API latency is unaffected."""
    t = threading.Thread(target=ingest_bronze_event, kwargs=kwargs, daemon=True)
    t.start()


# ── SILVER LAYER: Cleaning, Validation & Deduplication ────────────────────────

def _normalize_utc_date(ts_str: str) -> Optional[str]:
    try:
        dt = datetime.fromisoformat(ts_str.replace("Z", "+00:00"))
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        return dt.astimezone(timezone.utc).strftime("%Y-%m-%d")
    except Exception:
        return None


def process_bronze_to_silver(batch_limit: int = 1000) -> Dict[str, int]:
    """
    Validates unprocessed Bronze events, removes duplicates, normalizes UTC dates,
    validates durations, and quarantines invalid records to `dead_letter_events`.
    """
    processed = 0
    quarantined = 0
    duplicates_skipped = 0
    now_utc = datetime.now(timezone.utc).isoformat()

    with db_transaction() as conn:
        rows = conn.execute(
            """
            SELECT a.*
            FROM activity_events a
            LEFT JOIN silver_events s ON s.source_event_id = a.event_id
            LEFT JOIN dead_letter_events d ON d.source_event_id = a.event_id
            WHERE s.source_event_id IS NULL AND d.source_event_id IS NULL
            ORDER BY a.created_at ASC
            LIMIT ?
            """,
            (batch_limit,),
        ).fetchall()

        for row in rows:
            eid = row["event_id"]
            etype = (row["event_type"] or "").strip().lower()
            created_at = row["created_at"] or ""
            status = (row["status"] or "ok").strip().lower()

            # Parse payload
            try:
                payload = json.loads(row["payload_json"] or "{}")
                if not isinstance(payload, dict):
                    raise ValueError("payload_json must be a JSON object")
            except Exception as exc:
                conn.execute(
                    """
                    INSERT OR IGNORE INTO dead_letter_events
                    (dlq_id, source_event_id, raw_payload_json, error_reason, quarantined_at)
                    VALUES (?, ?, ?, ?, ?)
                    """,
                    (str(uuid.uuid4()), eid, row["payload_json"] or "", f"Invalid JSON: {exc}", now_utc),
                )
                quarantined += 1
                continue

            # Validate event_type & timestamp
            date_utc = _normalize_utc_date(created_at)
            if etype not in VALID_EVENT_TYPES or not date_utc:
                conn.execute(
                    """
                    INSERT OR IGNORE INTO dead_letter_events
                    (dlq_id, source_event_id, raw_payload_json, error_reason, quarantined_at)
                    VALUES (?, ?, ?, ?, ?)
                    """,
                    (
                        str(uuid.uuid4()),
                        eid,
                        row["payload_json"] or "{}",
                        f"Invalid event_type={etype} or timestamp={created_at}",
                        now_utc,
                    ),
                )
                quarantined += 1
                continue

            # Validate duration
            raw_dur = payload.get("duration_ms", 0.0)
            try:
                dur_ms = max(0.0, float(raw_dur))
            except (TypeError, ValueError):
                dur_ms = 0.0

            is_success = 0 if (status in ("error", "failed", "failure") or etype in ("api_error", "user_login_failed")) else 1

            cur = conn.execute(
                """
                INSERT OR IGNORE INTO silver_events
                (event_id, source_event_id, event_type, user_id, session_id, status, duration_ms, is_success, event_date_utc, normalized_at, gold_processed)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 0)
                """,
                (
                    str(uuid.uuid4()),
                    eid,
                    etype,
                    row["user_id"],
                    row["session_id"],
                    status,
                    dur_ms,
                    is_success,
                    date_utc,
                    now_utc,
                ),
            )
            if cur.rowcount == 0:
                duplicates_skipped += 1
            else:
                processed += 1

    return {
        "silver_processed": processed,
        "quarantined": quarantined,
        "duplicates_removed": duplicates_skipped,
    }


# ── GOLD LAYER: Incremental Aggregations ──────────────────────────────────────

def aggregate_silver_to_gold() -> Dict[str, Any]:
    """
    Incrementally aggregates newly processed Silver events into:
    - `daily_user_analytics`
    - `daily_ai_analytics`
    Only recomputes UTC dates touched by `gold_processed = 0` rows.
    """
    now_utc = datetime.now(timezone.utc).isoformat()
    touched_dates: List[str] = []

    with db_transaction() as conn:
        date_rows = conn.execute(
            "SELECT DISTINCT event_date_utc FROM silver_events WHERE gold_processed = 0"
        ).fetchall()
        touched_dates = [r["event_date_utc"] for r in date_rows]

        # Also ensure today's UTC date is kept fresh if there were direct log writes
        today_utc = datetime.now(timezone.utc).strftime("%Y-%m-%d")
        if today_utc not in touched_dates:
            touched_dates.append(today_utc)

        total_users = conn.execute("SELECT COUNT(*) FROM user_profiles").fetchone()[0]
        active_sessions_now = conn.execute("SELECT COUNT(*) FROM user_sessions WHERE is_active = 1").fetchone()[0]

        for d in touched_dates:
            # 1. Daily User Analytics
            dau = conn.execute(
                """
                SELECT COUNT(DISTINCT user_id) FROM silver_events
                WHERE event_date_utc = ? AND user_id IS NOT NULL
                """,
                (d,),
            ).fetchone()[0]

            total_logins = conn.execute(
                "SELECT COUNT(*) FROM silver_events WHERE event_date_utc = ? AND event_type = 'user_login'",
                (d,),
            ).fetchone()[0]

            failed_logins = conn.execute(
                "SELECT COUNT(*) FROM silver_events WHERE event_date_utc = ? AND event_type = 'user_login_failed'",
                (d,),
            ).fetchone()[0]

            avg_sess = conn.execute(
                """
                SELECT COALESCE(AVG(session_duration_sec), 0.0)
                FROM user_sessions
                WHERE substr(login_timestamp, 1, 10) = ? AND session_duration_sec > 0
                """,
                (d,),
            ).fetchone()[0]

            conn.execute(
                """
                INSERT INTO daily_user_analytics
                (date_utc, total_registered_users, dau, active_sessions, total_logins, failed_logins, avg_session_duration_sec, updated_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT(date_utc) DO UPDATE SET
                    total_registered_users = excluded.total_registered_users,
                    dau = excluded.dau,
                    active_sessions = excluded.active_sessions,
                    total_logins = excluded.total_logins,
                    failed_logins = excluded.failed_logins,
                    avg_session_duration_sec = excluded.avg_session_duration_sec,
                    updated_at = excluded.updated_at
                """,
                (d, total_users, dau, active_sessions_now, total_logins, failed_logins, round(float(avg_sess), 2), now_utc),
            )

            # 2. Daily AI Analytics
            ai_row = conn.execute(
                """
                SELECT
                    COUNT(*) AS total_req,
                    SUM(CASE WHEN status = 'success' THEN 1 ELSE 0 END) AS ok_req,
                    SUM(CASE WHEN status != 'success' THEN 1 ELSE 0 END) AS fail_req,
                    SUM(CASE WHEN cache_status = 'hit_exact' THEN 1 ELSE 0 END) AS exact_hits,
                    SUM(CASE WHEN cache_status = 'hit_semantic' THEN 1 ELSE 0 END) AS sem_hits,
                    SUM(CASE WHEN cache_status = 'miss' THEN 1 ELSE 0 END) AS misses,
                    COALESCE(AVG(processing_duration_ms), 0.0) AS avg_ms,
                    COALESCE(SUM(input_tokens), 0) AS in_tok,
                    COALESCE(SUM(output_tokens), 0) AS out_tok,
                    COALESCE(SUM(estimated_cost_usd), 0.0) AS cost_usd
                FROM ai_request_logs
                WHERE substr(created_at, 1, 10) = ?
                """,
                (d,),
            ).fetchone()

            saved_row = conn.execute(
                """
                SELECT COALESCE(SUM(estimated_cost_saved_usd), 0.0) AS saved_usd
                FROM ai_usage_metrics
                WHERE substr(created_at, 1, 10) = ?
                """,
                (d,),
            ).fetchone()

            conn.execute(
                """
                INSERT INTO daily_ai_analytics
                (date_utc, total_requests, successful_requests, failed_requests, exact_cache_hits,
                 semantic_cache_hits, cache_misses, avg_response_ms, total_input_tokens,
                 total_output_tokens, estimated_cost_usd, estimated_cost_saved_usd, updated_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT(date_utc) DO UPDATE SET
                    total_requests = excluded.total_requests,
                    successful_requests = excluded.successful_requests,
                    failed_requests = excluded.failed_requests,
                    exact_cache_hits = excluded.exact_cache_hits,
                    semantic_cache_hits = excluded.semantic_cache_hits,
                    cache_misses = excluded.cache_misses,
                    avg_response_ms = excluded.avg_response_ms,
                    total_input_tokens = excluded.total_input_tokens,
                    total_output_tokens = excluded.total_output_tokens,
                    estimated_cost_usd = excluded.estimated_cost_usd,
                    estimated_cost_saved_usd = excluded.estimated_cost_saved_usd,
                    updated_at = excluded.updated_at
                """,
                (
                    d,
                    ai_row["total_req"] or 0,
                    ai_row["ok_req"] or 0,
                    ai_row["fail_req"] or 0,
                    ai_row["exact_hits"] or 0,
                    ai_row["sem_hits"] or 0,
                    ai_row["misses"] or 0,
                    round(float(ai_row["avg_ms"] or 0.0), 2),
                    ai_row["in_tok"] or 0,
                    ai_row["out_tok"] or 0,
                    round(float(ai_row["cost_usd"] or 0.0), 6),
                    round(float(saved_row["saved_usd"] or 0.0), 6),
                    now_utc,
                ),
            )

        # Mark silver rows as gold_processed = 1
        conn.execute("UPDATE silver_events SET gold_processed = 1 WHERE gold_processed = 0")

    return {"dates_updated": touched_dates}


def run_etl_pipeline() -> Dict[str, Any]:
    """Executes Bronze -> Silver -> Gold ETL and records pipeline execution telemetry."""
    t0 = time.perf_counter()
    silver_stats = process_bronze_to_silver()
    gold_stats = aggregate_silver_to_gold()
    exec_ms = round((time.perf_counter() - t0) * 1000, 2)
    now_utc = datetime.now(timezone.utc).isoformat()

    try:
        with db_transaction() as conn:
            conn.execute(
                """
                INSERT INTO pipeline_metadata (key, value, updated_at)
                VALUES ('last_etl_run', ?, ?)
                ON CONFLICT(key) DO UPDATE SET value = excluded.value, updated_at = excluded.updated_at
                """,
                (json.dumps({**silver_stats, **gold_stats, "execution_ms": exec_ms}), now_utc),
            )
    except Exception as exc:
        log_json("warning", "pipeline_metadata_update_failed", error=str(exc))

    return {
        "status": "success",
        "execution_ms": exec_ms,
        "last_run_at": now_utc,
        **silver_stats,
        **gold_stats,
    }


# ── AI Request Telemetry & Private Chat History Recording ─────────────────────

def record_ai_request_telemetry(
    *,
    request_id: str,
    idempotency_key: Optional[str],
    user_id: Optional[str],
    session_id: Optional[str],
    question: str,
    answer: str,
    legal_domain: str,
    jurisdiction: str,
    request_timestamp: str,
    response_timestamp: str,
    processing_duration_ms: float,
    rag_duration_ms: float,
    llm_duration_ms: float,
    status: str,
    http_status_code: int,
    model_used: str,
    input_tokens: int,
    output_tokens: int,
    estimated_cost_usd: float,
    estimated_cost_saved_usd: float,
    cache_status: str,
    retrieval_doc_count: int,
    error_details: Optional[str] = None,
) -> None:
    """
    Records AI telemetry cleanly without storing raw private questions in operational logs.
    Stores the actual Q&A only in access-controlled `user_chat_history` when user_id is present.
    Never raises into caller.
    """
    q_hash = hashlib.sha256((question or "").encode("utf-8")).hexdigest()
    now_utc = datetime.now(timezone.utc).isoformat()

    try:
        with db_transaction() as conn:
            conn.execute(
                """
                INSERT OR IGNORE INTO ai_request_logs
                (request_id, idempotency_key, user_id, session_id, question_hash, legal_domain, jurisdiction,
                 request_timestamp, response_timestamp, processing_duration_ms, rag_duration_ms, llm_duration_ms,
                 status, http_status_code, model_used, input_tokens, output_tokens, estimated_cost_usd,
                 cache_status, retrieval_doc_count, error_details, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    request_id,
                    idempotency_key,
                    user_id,
                    session_id,
                    q_hash,
                    legal_domain,
                    jurisdiction,
                    request_timestamp,
                    response_timestamp,
                    round(processing_duration_ms, 2),
                    round(rag_duration_ms, 2),
                    round(llm_duration_ms, 2),
                    status,
                    http_status_code,
                    model_used,
                    input_tokens,
                    output_tokens,
                    estimated_cost_usd,
                    cache_status,
                    retrieval_doc_count,
                    error_details,
                    now_utc,
                ),
            )

            is_hit = 1 if cache_status in ("hit_exact", "hit_semantic") else 0
            conn.execute(
                """
                INSERT INTO ai_usage_metrics
                (id, request_id, model_name, input_tokens, output_tokens, total_tokens,
                 estimated_cost_usd, estimated_cost_saved_usd, latency_ms, cache_hit, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    str(uuid.uuid4()),
                    request_id,
                    model_used,
                    input_tokens,
                    output_tokens,
                    input_tokens + output_tokens,
                    estimated_cost_usd,
                    estimated_cost_saved_usd,
                    round(processing_duration_ms, 2),
                    is_hit,
                    now_utc,
                ),
            )

            # Save private Q&A only to access-controlled user_chat_history
            if user_id and status == "success" and answer:
                # Ensure user profile exists to satisfy FK
                conn.execute(
                    """
                    INSERT OR IGNORE INTO user_profiles (user_id, email, full_name, role, created_at, updated_at)
                    VALUES (?, ?, ?, 'citizen', ?, ?)
                    """,
                    (user_id, f"{user_id}@nyaya.local", "User", now_utc, now_utc),
                )
                conn.execute(
                    """
                    INSERT INTO user_chat_history
                    (id, user_id, request_id, question, answer, legal_domain, jurisdiction, created_at)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    (str(uuid.uuid4()), user_id, request_id, question, answer, legal_domain, jurisdiction, now_utc),
                )

            if status != "success" and error_details:
                conn.execute(
                    """
                    INSERT INTO system_error_logs (id, error_type, endpoint, user_id, message, created_at)
                    VALUES (?, 'ai_request_error', '/api/chat', ?, ?, ?)
                    """,
                    (str(uuid.uuid4()), user_id, error_details[:500], now_utc),
                )

        # Emit Bronze events
        ingest_bronze_event(
            event_type="ai_request",
            user_id=user_id,
            session_id=session_id,
            status="ok",
            payload={"request_id": request_id, "domain": legal_domain, "jurisdiction": jurisdiction},
        )
        if cache_status in ("hit_exact", "hit_semantic"):
            ingest_bronze_event(
                event_type="cache_hit",
                user_id=user_id,
                session_id=session_id,
                status="ok",
                payload={"request_id": request_id, "cache_type": cache_status, "duration_ms": processing_duration_ms},
            )
        else:
            ingest_bronze_event(
                event_type="cache_miss",
                user_id=user_id,
                session_id=session_id,
                status="ok",
                payload={"request_id": request_id, "duration_ms": processing_duration_ms},
            )
        ingest_bronze_event(
            event_type="ai_response" if status == "success" else "api_error",
            user_id=user_id,
            session_id=session_id,
            status=status,
            payload={"request_id": request_id, "duration_ms": processing_duration_ms, "http_status": http_status_code},
        )
    except Exception as exc:
        log_json("warning", "telemetry_record_degraded", error=str(exc), request_id=request_id)


# ── Admin Analytics Queries ───────────────────────────────────────────────────

def get_admin_analytics_summary(
    date_range: str = "30d",
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Returns comprehensive user, AI, cache, and Medallion pipeline metrics
    for the requested date range without exposing private user questions.
    """
    # Ensure Gold tables reflect latest events
    run_etl_pipeline()

    now = datetime.now(timezone.utc)
    today_str = now.strftime("%Y-%m-%d")

    if date_range == "today":
        s_date = today_str
        e_date = today_str
    elif date_range == "7d":
        s_date = (now - timedelta(days=6)).strftime("%Y-%m-%d")
        e_date = today_str
    elif date_range == "custom" and start_date and end_date:
        s_date = start_date[:10]
        e_date = end_date[:10]
    else:
        s_date = (now - timedelta(days=29)).strftime("%Y-%m-%d")
        e_date = today_str

    with db_read() as conn:
        total_users = conn.execute("SELECT COUNT(*) FROM user_profiles").fetchone()[0]
        active_sessions = conn.execute(
            "SELECT COUNT(*) FROM user_sessions WHERE is_active = 1 AND expires_at > ?",
            (now.isoformat(),),
        ).fetchone()[0]

        dau = conn.execute(
            """
            SELECT COUNT(DISTINCT user_id) FROM silver_events
            WHERE event_date_utc = ? AND user_id IS NOT NULL
            """,
            (today_str,),
        ).fetchone()[0]

        mau_start = (now - timedelta(days=29)).strftime("%Y-%m-%d")
        mau = conn.execute(
            """
            SELECT COUNT(DISTINCT user_id) FROM silver_events
            WHERE event_date_utc >= ? AND user_id IS NOT NULL
            """,
            (mau_start,),
        ).fetchone()[0]

        login_stats = conn.execute(
            """
            SELECT
                COUNT(*) AS total_logins,
                SUM(CASE WHEN event_type = 'user_login_failed' THEN 1 ELSE 0 END) AS failed_logins
            FROM silver_events
            WHERE event_date_utc BETWEEN ? AND ? AND event_type IN ('user_login', 'user_login_failed')
            """,
            (s_date, e_date),
        ).fetchone()

        avg_sess = conn.execute(
            """
            SELECT COALESCE(AVG(session_duration_sec), 0.0)
            FROM user_sessions
            WHERE substr(login_timestamp, 1, 10) BETWEEN ? AND ? AND session_duration_sec > 0
            """,
            (s_date, e_date),
        ).fetchone()[0]

        # AI Metrics from Gold + Logs
        ai_agg = conn.execute(
            """
            SELECT
                COALESCE(SUM(total_requests), 0) AS total_requests,
                COALESCE(SUM(successful_requests), 0) AS successful_requests,
                COALESCE(SUM(failed_requests), 0) AS failed_requests,
                COALESCE(SUM(exact_cache_hits), 0) AS exact_hits,
                COALESCE(SUM(semantic_cache_hits), 0) AS semantic_hits,
                COALESCE(SUM(cache_misses), 0) AS cache_misses,
                COALESCE(AVG(NULLIF(avg_response_ms, 0)), 0.0) AS avg_response_ms,
                COALESCE(SUM(total_input_tokens), 0) AS total_input_tokens,
                COALESCE(SUM(total_output_tokens), 0) AS total_output_tokens,
                COALESCE(SUM(estimated_cost_usd), 0.0) AS estimated_cost_usd,
                COALESCE(SUM(estimated_cost_saved_usd), 0.0) AS estimated_cost_saved_usd
            FROM daily_ai_analytics
            WHERE date_utc BETWEEN ? AND ?
            """,
            (s_date, e_date),
        ).fetchone()

        daily_series = [
            dict(r)
            for r in conn.execute(
                """
                SELECT g.date_utc,
                       COALESCE(g.total_requests, 0) AS total_requests,
                       COALESCE(g.exact_cache_hits, 0) + COALESCE(g.semantic_cache_hits, 0) AS cache_hits,
                       COALESCE(g.cache_misses, 0) AS cache_misses,
                       COALESCE(g.estimated_cost_usd, 0.0) AS estimated_cost_usd,
                       COALESCE(u.dau, 0) AS dau
                FROM daily_ai_analytics g
                LEFT JOIN daily_user_analytics u ON u.date_utc = g.date_utc
                WHERE g.date_utc BETWEEN ? AND ?
                ORDER BY g.date_utc ASC
                """,
                (s_date, e_date),
            ).fetchall()
        ]

        model_breakdown = [
            dict(r)
            for r in conn.execute(
                """
                SELECT COALESCE(model_used, 'unknown') AS model_used,
                       COUNT(*) AS request_count,
                       COALESCE(SUM(input_tokens + output_tokens), 0) AS total_tokens,
                       COALESCE(SUM(estimated_cost_usd), 0.0) AS cost_usd
                FROM ai_request_logs
                WHERE substr(created_at, 1, 10) BETWEEN ? AND ?
                GROUP BY model_used
                """,
                (s_date, e_date),
            ).fetchall()
        ]

        # Pipeline counts
        bronze_count = conn.execute("SELECT COUNT(*) FROM activity_events").fetchone()[0]
        silver_count = conn.execute("SELECT COUNT(*) FROM silver_events").fetchone()[0]
        gold_count = conn.execute("SELECT COUNT(*) FROM daily_ai_analytics").fetchone()[0]
        dlq_count = conn.execute("SELECT COUNT(*) FROM dead_letter_events").fetchone()[0]
        cache_entries = conn.execute("SELECT COUNT(*) FROM cache_metadata WHERE invalidated = 0").fetchone()[0]

        pipe_meta_row = conn.execute(
            "SELECT value, updated_at FROM pipeline_metadata WHERE key = 'last_etl_run'"
        ).fetchone()
        last_etl = json.loads(pipe_meta_row["value"]) if pipe_meta_row else {}
        last_etl_at = pipe_meta_row["updated_at"] if pipe_meta_row else None

        # Recent login history (anonymized/safe — no passwords or tokens)
        login_history = [
            dict(r)
            for r in conn.execute(
                """
                SELECT s.session_id, u.email, u.role, s.login_timestamp, s.logout_timestamp,
                       s.session_duration_sec, s.is_active, s.browser_info
                FROM user_sessions s
                JOIN user_profiles u ON u.user_id = s.user_id
                ORDER BY s.login_timestamp DESC
                LIMIT 20
                """
            ).fetchall()
        ]

    total_req = ai_agg["total_requests"] or 0
    total_hits = (ai_agg["exact_hits"] or 0) + (ai_agg["semantic_hits"] or 0)
    cache_hit_ratio = round((total_hits / total_req) * 100, 1) if total_req > 0 else 0.0

    # Days span
    try:
        days_span = max(1, (datetime.fromisoformat(e_date) - datetime.fromisoformat(s_date)).days + 1)
    except Exception:
        days_span = 1

    requests_per_day = round(total_req / days_span, 2)
    requests_per_user = round(total_req / max(1, total_users), 2)

    return {
        "range": {"mode": date_range, "start_date": s_date, "end_date": e_date},
        "user_metrics": {
            "total_registered_users": total_users,
            "daily_active_users": dau,
            "monthly_active_users": mau,
            "active_sessions": active_sessions,
            "total_logins": login_stats["total_logins"] or 0,
            "failed_logins": login_stats["failed_logins"] or 0,
            "avg_session_duration_sec": round(float(avg_sess), 1),
        },
        "ai_metrics": {
            "total_requests": total_req,
            "successful_requests": ai_agg["successful_requests"] or 0,
            "failed_requests": ai_agg["failed_requests"] or 0,
            "requests_per_user": requests_per_user,
            "requests_per_day": requests_per_day,
            "avg_response_time_ms": round(float(ai_agg["avg_response_ms"] or 0.0), 1),
            "exact_cache_hits": ai_agg["exact_hits"] or 0,
            "semantic_cache_hits": ai_agg["semantic_hits"] or 0,
            "cache_misses": ai_agg["cache_misses"] or 0,
            "cache_hit_ratio_pct": cache_hit_ratio,
            "requests_saved_via_cache": total_hits,
            "total_input_tokens": ai_agg["total_input_tokens"] or 0,
            "total_output_tokens": ai_agg["total_output_tokens"] or 0,
            "estimated_cost_usd": round(float(ai_agg["estimated_cost_usd"] or 0.0), 6),
            "estimated_cost_saved_usd": round(float(ai_agg["estimated_cost_saved_usd"] or 0.0), 6),
        },
        "pipeline_metrics": {
            "bronze_records": bronze_count,
            "silver_processed_records": silver_count,
            "gold_aggregated_records": gold_count,
            "duplicates_removed": last_etl.get("duplicates_removed", 0),
            "failed_dlq_events": dlq_count,
            "pipeline_execution_ms": last_etl.get("execution_ms", 0.0),
            "last_successful_processing": last_etl_at,
            "active_cache_entries": cache_entries,
        },
        "system_health": {
            "api_uptime_sec": round(time.time() - APP_START_TIME, 1),
            "database_connected": True,
            "cache_available": True,
            "error_rate_pct": round(((ai_agg["failed_requests"] or 0) / max(1, total_req)) * 100, 2),
        },
        "daily_series": daily_series,
        "model_breakdown": model_breakdown,
        "recent_sessions": login_history,
    }

