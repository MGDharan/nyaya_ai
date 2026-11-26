"""
NyayaAI Mandatory Authentication, Session Management, RBAC & Rate Limiting Service.

Features:
1. Verifies Supabase Auth JWTs via `/auth/v1/user` (cached briefly in memory).
2. Issues & verifies signed HMAC-SHA256 `nyaya_session` tokens for HttpOnly cookies & Bearer headers.
3. Tracks `user_profiles` and `user_sessions` (login, logout, duration, active sessions, expiration).
4. Emits Bronze `user_login`, `user_login_failed`, `user_logout`, and `admin_action` events.
5. Enforces RBAC (`citizen`, `advocate`, `admin`) and per-user rate limiting.
6. Provides DPDPA 2023 user data export and deletion workflows.
"""

import base64
import hashlib
import hmac
import json
import os
import threading
import time
import uuid
from collections import defaultdict, deque
from datetime import datetime, timedelta, timezone
from typing import Any, Dict, Optional

import requests
from fastapi import Cookie, Header, HTTPException, Request

from app.config import settings
from app.services.data_pipeline import ingest_bronze_event, log_json
from app.services.database import db_read, db_transaction

SUPABASE_URL = os.getenv("SUPABASE_URL", "")
SUPABASE_ANON_KEY = os.getenv("SUPABASE_ANON_KEY", "")

# Server-side HMAC secret for signed session cookies (never exposed to frontend)
_SESSION_SECRET = (
    os.getenv("SESSION_SECRET")
    or settings.admin_api_key
    or os.getenv("SUPABASE_SERVICE_ROLE_KEY")
    or "nyaya-dev-session-secret-change-in-prod"
).encode("utf-8")

SESSION_TTL_HOURS = 12
ADMIN_EMAILS = {"mgdharan7@gmail.com"}

# Short-lived in-memory cache for Supabase JWT verification {token_hash: (user_dict, expires_ts)}
_jwt_cache: Dict[str, tuple[Dict[str, Any], float]] = {}
_jwt_cache_lock = threading.Lock()

# Per-user sliding-window rate limiter {user_id: deque[timestamps]}
_rate_buckets: Dict[str, deque] = defaultdict(deque)
_rate_lock = threading.Lock()
RATE_LIMIT_MAX_REQUESTS = 30
RATE_LIMIT_WINDOW_SEC = 60

# Short-TTL in-flight / duplicate-click idempotency lock {key: timestamp}
_idempotency_locks: Dict[str, float] = {}
_idempotency_lock = threading.Lock()


def _sign_payload(payload: Dict[str, Any]) -> str:
    raw = json.dumps(payload, separators=(",", ":"), sort_keys=True).encode("utf-8")
    b64 = base64.urlsafe_b64encode(raw).decode("ascii").rstrip("=")
    sig = hmac.new(_SESSION_SECRET, b64.encode("ascii"), hashlib.sha256).hexdigest()
    return f"{b64}.{sig}"


def verify_session_token(token: str) -> Optional[Dict[str, Any]]:
    """Verifies HMAC-signed session token and checks expiry + active DB session."""
    if not token or "." not in token:
        return None
    try:
        b64, sig = token.split(".", 1)
        expected = hmac.new(_SESSION_SECRET, b64.encode("ascii"), hashlib.sha256).hexdigest()
        if not hmac.compare_digest(sig, expected):
            return None
        padded = b64 + "=" * (-len(b64) % 4)
        payload = json.loads(base64.urlsafe_b64decode(padded).decode("utf-8"))
        if payload.get("exp", 0) < time.time():
            return None

        session_id = payload.get("session_id")
        if session_id:
            with db_read() as conn:
                row = conn.execute(
                    "SELECT is_active, expires_at FROM user_sessions WHERE session_id = ?",
                    (session_id,),
                ).fetchone()
                if not row or row["is_active"] != 1:
                    return None
                if row["expires_at"] <= datetime.now(timezone.utc).isoformat():
                    return None
        return payload
    except Exception:
        return None


def verify_supabase_jwt(access_token: str) -> Optional[Dict[str, Any]]:
    """Verifies a Supabase Auth access_token against `/auth/v1/user` with 60s caching."""
    if not access_token or not SUPABASE_URL or not SUPABASE_ANON_KEY:
        return None

    thash = hashlib.sha256(access_token.encode("utf-8")).hexdigest()
    now = time.time()
    with _jwt_cache_lock:
        cached = _jwt_cache.get(thash)
        if cached and cached[1] > now:
            return cached[0]

    try:
        resp = requests.get(
            f"{SUPABASE_URL.rstrip('/')}/auth/v1/user",
            headers={
                "apikey": SUPABASE_ANON_KEY,
                "Authorization": f"Bearer {access_token}",
            },
            timeout=5,
        )
        if resp.status_code == 200:
            user = resp.json()
            with _jwt_cache_lock:
                _jwt_cache[thash] = (user, now + 60.0)
            return user
    except Exception as exc:
        log_json("warning", "supabase_jwt_verify_failed", error=str(exc))
    return None


def _resolve_role(email: str, requested_role: str) -> str:
    e = (email or "").strip().lower()
    r = (requested_role or "citizen").strip().lower()
    if e in ADMIN_EMAILS or r == "admin":
        return "admin"
    if r == "advocate":
        return "advocate"
    return "citizen"


def create_user_session(
    *,
    email: str,
    full_name: str,
    role: str = "citizen",
    bar_council_no: Optional[str] = None,
    supabase_access_token: Optional[str] = None,
    supabase_user_id: Optional[str] = None,
    device_info: Optional[str] = None,
    browser_info: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Validates credentials (via Supabase JWT when provided), upserts `user_profiles`,
    creates an active `user_sessions` row, emits `user_login` Bronze event,
    and returns signed session token + user profile.
    """
    verified_email = (email or "").strip().lower()
    user_id = supabase_user_id

    if supabase_access_token:
        sb_user = verify_supabase_jwt(supabase_access_token)
        if sb_user:
            verified_email = (sb_user.get("email") or verified_email).strip().lower()
            user_id = sb_user.get("id") or user_id
            meta = sb_user.get("user_metadata") or {}
            full_name = meta.get("full_name") or full_name
            role = meta.get("role") or role
            bar_council_no = meta.get("bar_council_no") or bar_council_no
        elif settings.environment.lower() == "production":
            ingest_bronze_event(
                event_type="user_login_failed",
                status="failed",
                payload={"reason": "invalid_supabase_jwt"},
            )
            raise HTTPException(status_code=401, detail="Invalid or expired authentication token.")

    if not verified_email:
        raise HTTPException(status_code=400, detail="Email is required.")

    if not user_id:
        user_id = str(uuid.uuid5(uuid.NAMESPACE_DNS, verified_email))

    resolved_role = _resolve_role(verified_email, role)
    now = datetime.now(timezone.utc)
    now_iso = now.isoformat()
    expires_at = (now + timedelta(hours=SESSION_TTL_HOURS)).isoformat()
    session_id = str(uuid.uuid4())

    with db_transaction() as conn:
        existing_by_email = conn.execute(
            "SELECT user_id, role, full_name, bar_council_no FROM user_profiles WHERE email = ?",
            (verified_email,),
        ).fetchone()
        if existing_by_email:
            user_id = existing_by_email["user_id"]
            if existing_by_email["role"] == "admin" or resolved_role == "admin":
                resolved_role = "admin"
            conn.execute(
                """
                UPDATE user_profiles
                SET full_name = ?, role = ?, bar_council_no = COALESCE(?, bar_council_no), updated_at = ?
                WHERE user_id = ?
                """,
                (full_name or existing_by_email["full_name"], resolved_role, bar_council_no, now_iso, user_id),
            )
        else:
            conn.execute(
                """
                INSERT INTO user_profiles (user_id, email, full_name, role, bar_council_no, is_active, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?, 1, ?, ?)
                """,
                (user_id, verified_email, full_name or verified_email.split("@")[0], resolved_role, bar_council_no, now_iso, now_iso),
            )

        eff_row = conn.execute("SELECT role, full_name, bar_council_no FROM user_profiles WHERE user_id = ?", (user_id,)).fetchone()
        effective_role = eff_row["role"] if eff_row else resolved_role
        effective_name = eff_row["full_name"] if eff_row else full_name

        conn.execute(
            """
            INSERT INTO user_sessions
            (session_id, user_id, login_timestamp, last_active_timestamp, session_duration_sec,
             device_info, browser_info, is_active, expires_at, created_at, updated_at)
            VALUES (?, ?, ?, ?, 0.0, ?, ?, 1, ?, ?, ?)
            """,
            (
                session_id,
                user_id,
                now_iso,
                now_iso,
                (device_info or "Desktop")[:120],
                (browser_info or "WebBrowser")[:120],
                expires_at,
                now_iso,
                now_iso,
            ),
        )

    ingest_bronze_event(
        event_type="user_login",
        user_id=user_id,
        session_id=session_id,
        status="ok",
        payload={"role": effective_role, "browser": (browser_info or "")[:60]},
    )

    token_payload = {
        "user_id": user_id,
        "email": verified_email,
        "name": effective_name,
        "role": effective_role,
        "bar_council_no": bar_council_no,
        "session_id": session_id,
        "exp": int((now + timedelta(hours=SESSION_TTL_HOURS)).timestamp()),
    }
    session_token = _sign_payload(token_payload)

    return {
        "session_id": session_id,
        "session_token": session_token,
        "expires_at": expires_at,
        "user": {
            "user_id": user_id,
            "email": verified_email,
            "name": effective_name,
            "role": effective_role,
            "bar_council_no": bar_council_no,
        },
    }


def invalidate_user_session(session_id: Optional[str], user_id: Optional[str] = None) -> None:
    """Marks session inactive, computes duration, and emits `user_logout` Bronze event."""
    if not session_id:
        return
    now = datetime.now(timezone.utc)
    now_iso = now.isoformat()
    duration_sec = 0.0
    resolved_uid = user_id

    try:
        with db_transaction() as conn:
            row = conn.execute(
                "SELECT user_id, login_timestamp FROM user_sessions WHERE session_id = ?",
                (session_id,),
            ).fetchone()
            if row:
                resolved_uid = resolved_uid or row["user_id"]
                try:
                    login_dt = datetime.fromisoformat(row["login_timestamp"].replace("Z", "+00:00"))
                    duration_sec = max(0.0, (now - login_dt).total_seconds())
                except Exception:
                    duration_sec = 0.0
            conn.execute(
                """
                UPDATE user_sessions
                SET is_active = 0, logout_timestamp = ?, last_active_timestamp = ?,
                    session_duration_sec = ?, updated_at = ?
                WHERE session_id = ?
                """,
                (now_iso, now_iso, round(duration_sec, 2), now_iso, session_id),
            )
    except Exception as exc:
        log_json("warning", "logout_session_update_failed", error=str(exc))

    ingest_bronze_event(
        event_type="user_logout",
        user_id=resolved_uid,
        session_id=session_id,
        status="ok",
        payload={"duration_ms": round(duration_sec * 1000, 2)},
    )


def _touch_session(session_id: Optional[str]) -> None:
    if not session_id:
        return
    try:
        now = datetime.now(timezone.utc)
        with db_transaction() as conn:
            row = conn.execute(
                "SELECT login_timestamp FROM user_sessions WHERE session_id = ? AND is_active = 1",
                (session_id,),
            ).fetchone()
            if row:
                try:
                    login_dt = datetime.fromisoformat(row["login_timestamp"].replace("Z", "+00:00"))
                    dur = max(0.0, (now - login_dt).total_seconds())
                except Exception:
                    dur = 0.0
                conn.execute(
                    "UPDATE user_sessions SET last_active_timestamp = ?, session_duration_sec = ?, updated_at = ? WHERE session_id = ?",
                    (now.isoformat(), round(dur, 2), now.isoformat(), session_id),
                )
    except Exception:
        pass


def get_optional_user(
    request: Request,
    authorization: Optional[str] = Header(default=None),
    nyaya_session: Optional[str] = Cookie(default=None),
) -> Optional[Dict[str, Any]]:
    """Extracts and verifies authenticated user from Bearer header or HttpOnly cookie."""
    token = None
    if authorization and authorization.lower().startswith("bearer "):
        token = authorization[7:].strip()
    elif nyaya_session:
        token = nyaya_session.strip()

    if not token:
        return None

    # 1. Try signed nyaya_session token
    payload = verify_session_token(token)
    if payload:
        _touch_session(payload.get("session_id"))
        return payload

    # 2. Try Supabase JWT directly
    sb_user = verify_supabase_jwt(token)
    if sb_user:
        email = (sb_user.get("email") or "").lower()
        meta = sb_user.get("user_metadata") or {}
        role = _resolve_role(email, meta.get("role", "citizen"))
        return {
            "user_id": sb_user.get("id"),
            "email": email,
            "name": meta.get("full_name") or email.split("@")[0],
            "role": role,
            "bar_council_no": meta.get("bar_council_no"),
            "session_id": None,
        }

    return None


def require_authenticated_user(
    request: Request,
    authorization: Optional[str] = Header(default=None),
    nyaya_session: Optional[str] = Cookie(default=None),
) -> Dict[str, Any]:
    user = get_optional_user(request, authorization, nyaya_session)
    if not user:
        raise HTTPException(status_code=401, detail="Authentication required. Please sign in at /login.")
    return user


def require_advocate_or_admin(
    request: Request,
    authorization: Optional[str] = Header(default=None),
    nyaya_session: Optional[str] = Cookie(default=None),
) -> Dict[str, Any]:
    user = require_authenticated_user(request, authorization, nyaya_session)
    if user.get("role") not in ("advocate", "admin"):
        raise HTTPException(status_code=403, detail="Advocate or Administrator privileges required.")
    return user


def require_admin_user(
    request: Request,
    authorization: Optional[str] = Header(default=None),
    nyaya_session: Optional[str] = Cookie(default=None),
    x_admin_key: Optional[str] = Header(default=None),
) -> Dict[str, Any]:
    if settings.admin_api_key and x_admin_key and hmac.compare_digest(x_admin_key, settings.admin_api_key):
        return {"user_id": "admin-key", "email": "admin@nyaya.ai", "role": "admin", "name": "System Admin"}
    user = require_authenticated_user(request, authorization, nyaya_session)
    if user.get("role") != "admin":
        raise HTTPException(status_code=403, detail="Administrator access required.")
    return user


# ── Rate Limiting & Idempotency Guards (Module 6) ─────────────────────────────

def enforce_rate_limit(user_id: str) -> None:
    """Sliding-window per-user rate limit (30 req / 60s)."""
    now = time.time()
    with _rate_lock:
        q = _rate_buckets[user_id]
        while q and q[0] < now - RATE_LIMIT_WINDOW_SEC:
            q.popleft()
        if len(q) >= RATE_LIMIT_MAX_REQUESTS:
            raise HTTPException(
                status_code=429,
                detail="Rate limit exceeded. Please wait a few seconds before submitting another legal query.",
            )
        q.append(now)


def acquire_idempotency_guard(key: str, window_sec: float = 4.0) -> bool:
    """Returns True if this request is fresh; False if duplicate double-click within `window_sec`."""
    now = time.time()
    with _idempotency_lock:
        # Clean stale locks
        stale = [k for k, ts in _idempotency_locks.items() if ts < now - window_sec]
        for k in stale:
            del _idempotency_locks[k]
        if key in _idempotency_locks:
            return False
        _idempotency_locks[key] = now
        return True


# ── DPDPA 2023 User Data Export & Deletion (Module 9) ─────────────────────────

def export_user_data(user_id: str) -> Dict[str, Any]:
    with db_read() as conn:
        profile = conn.execute("SELECT * FROM user_profiles WHERE user_id = ?", (user_id,)).fetchone()
        sessions = conn.execute(
            "SELECT session_id, login_timestamp, logout_timestamp, session_duration_sec, device_info, browser_info FROM user_sessions WHERE user_id = ? ORDER BY login_timestamp DESC",
            (user_id,),
        ).fetchall()
        chats = conn.execute(
            "SELECT id, request_id, question, answer, legal_domain, jurisdiction, created_at FROM user_chat_history WHERE user_id = ? ORDER BY created_at DESC",
            (user_id,),
        ).fetchall()

    return {
        "exported_at": datetime.now(timezone.utc).isoformat(),
        "profile": dict(profile) if profile else None,
        "sessions": [dict(s) for s in sessions],
        "chat_history": [dict(c) for c in chats],
    }


def delete_user_data(user_id: str) -> Dict[str, int]:
    with db_transaction() as conn:
        c1 = conn.execute("DELETE FROM user_chat_history WHERE user_id = ?", (user_id,)).rowcount
        c2 = conn.execute("DELETE FROM user_sessions WHERE user_id = ?", (user_id,)).rowcount
        return {"deleted_chats": c1, "deleted_sessions": c2}


def record_admin_audit(admin_user_id: str, action: str, target_resource: str = "", details: str = "") -> None:
    now_iso = datetime.now(timezone.utc).isoformat()
    try:
        with db_transaction() as conn:
            conn.execute(
                """
                INSERT INTO admin_audit_logs (id, admin_user_id, action, target_resource, details, created_at)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (str(uuid.uuid4()), admin_user_id, action, target_resource, details, now_iso),
            )
        ingest_bronze_event(
            event_type="admin_action",
            user_id=admin_user_id,
            status="ok",
            payload={"action": action, "target": target_resource},
        )
    except Exception as exc:
        log_json("warning", "admin_audit_failed", error=str(exc))

