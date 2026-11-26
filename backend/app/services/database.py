"""
NyayaAI Enterprise Database Layer
- Thread-safe SQLite Connection Pool with WAL mode & Foreign Keys
- Versioned Schema Migrations (Bronze / Silver / Gold + Auth + Cache + Governance)
- Configurable Data Retention Cleanup
"""

import queue
import sqlite3
import threading
from contextlib import contextmanager
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Generator, Optional

from app.config import settings

DB_PATH = Path(settings.data_dir) / "nyaya_enterprise.db"
DB_PATH.parent.mkdir(parents=True, exist_ok=True)


class SQLiteConnectionPool:
    """Thread-safe SQLite connection pool with WAL journaling."""

    def __init__(self, db_path: Path, pool_size: int = 8):
        self.db_path = db_path
        self.pool_size = pool_size
        self._pool: queue.Queue[sqlite3.Connection] = queue.Queue(maxsize=pool_size)
        self._lock = threading.Lock()
        self._initialized = False

    def _create_connection(self) -> sqlite3.Connection:
        conn = sqlite3.connect(
            str(self.db_path),
            check_same_thread=False,
            timeout=15.0,
            isolation_level=None,  # explicit transaction control
        )
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA journal_mode=WAL;")
        conn.execute("PRAGMA synchronous=NORMAL;")
        conn.execute("PRAGMA foreign_keys=ON;")
        conn.execute("PRAGMA busy_timeout=5000;")
        return conn

    def acquire(self) -> sqlite3.Connection:
        try:
            return self._pool.get_nowait()
        except queue.Empty:
            return self._create_connection()

    def release(self, conn: sqlite3.Connection) -> None:
        try:
            self._pool.put_nowait(conn)
        except queue.Full:
            try:
                conn.close()
            except Exception:
                pass

    def health_check(self) -> bool:
        try:
            with self.transaction() as conn:
                conn.execute("SELECT 1").fetchone()
            return True
        except Exception:
            return False

    @contextmanager
    def transaction(self) -> Generator[sqlite3.Connection, None, None]:
        conn = self.acquire()
        try:
            conn.execute("BEGIN")
            yield conn
            conn.execute("COMMIT")
        except Exception:
            try:
                conn.execute("ROLLBACK")
            except Exception:
                pass
            raise
        finally:
            self.release(conn)

    @contextmanager
    def read_conn(self) -> Generator[sqlite3.Connection, None, None]:
        conn = self.acquire()
        try:
            yield conn
        finally:
            self.release(conn)


_pool = SQLiteConnectionPool(DB_PATH, pool_size=10)


def get_pool() -> SQLiteConnectionPool:
    return _pool


@contextmanager
def db_transaction() -> Generator[sqlite3.Connection, None, None]:
    with _pool.transaction() as conn:
        yield conn


@contextmanager
def db_read() -> Generator[sqlite3.Connection, None, None]:
    with _pool.read_conn() as conn:
        yield conn


MIGRATIONS: list[tuple[str, str]] = [
    (
        "001_initial_enterprise_schema",
        """
        -- 1. User Profiles
        CREATE TABLE IF NOT EXISTS user_profiles (
            user_id TEXT PRIMARY KEY,
            email TEXT NOT NULL UNIQUE,
            full_name TEXT NOT NULL DEFAULT 'User',
            role TEXT NOT NULL DEFAULT 'citizen' CHECK(role IN ('citizen', 'advocate', 'admin')),
            bar_council_no TEXT,
            is_active INTEGER NOT NULL DEFAULT 1,
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL
        );
        CREATE INDEX IF NOT EXISTS idx_user_profiles_email ON user_profiles(email);
        CREATE INDEX IF NOT EXISTS idx_user_profiles_role ON user_profiles(role);

        -- 2. User Sessions
        CREATE TABLE IF NOT EXISTS user_sessions (
            session_id TEXT PRIMARY KEY,
            user_id TEXT NOT NULL,
            login_timestamp TEXT NOT NULL,
            logout_timestamp TEXT,
            last_active_timestamp TEXT NOT NULL,
            session_duration_sec REAL DEFAULT 0.0,
            device_info TEXT,
            browser_info TEXT,
            is_active INTEGER NOT NULL DEFAULT 1,
            expires_at TEXT NOT NULL,
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL,
            FOREIGN KEY (user_id) REFERENCES user_profiles(user_id) ON DELETE CASCADE
        );
        CREATE INDEX IF NOT EXISTS idx_user_sessions_user ON user_sessions(user_id);
        CREATE INDEX IF NOT EXISTS idx_user_sessions_active ON user_sessions(is_active, expires_at);

        -- 3. Bronze Layer: Raw Activity Events
        CREATE TABLE IF NOT EXISTS activity_events (
            event_id TEXT PRIMARY KEY,
            event_type TEXT NOT NULL,
            schema_version TEXT NOT NULL DEFAULT '1.0',
            user_id TEXT,
            session_id TEXT,
            status TEXT NOT NULL DEFAULT 'ok',
            payload_json TEXT NOT NULL DEFAULT '{}',
            created_at TEXT NOT NULL
        );
        CREATE INDEX IF NOT EXISTS idx_activity_events_type ON activity_events(event_type, created_at);
        CREATE INDEX IF NOT EXISTS idx_activity_events_user ON activity_events(user_id, created_at);

        -- 3b. Silver Layer: Cleaned & Validated Events
        CREATE TABLE IF NOT EXISTS silver_events (
            event_id TEXT PRIMARY KEY,
            source_event_id TEXT NOT NULL UNIQUE,
            event_type TEXT NOT NULL,
            user_id TEXT,
            session_id TEXT,
            status TEXT NOT NULL,
            duration_ms REAL DEFAULT 0.0,
            is_success INTEGER NOT NULL DEFAULT 1,
            event_date_utc TEXT NOT NULL,
            normalized_at TEXT NOT NULL,
            gold_processed INTEGER NOT NULL DEFAULT 0
        );
        CREATE INDEX IF NOT EXISTS idx_silver_events_date ON silver_events(event_date_utc, event_type);
        CREATE INDEX IF NOT EXISTS idx_silver_events_gold ON silver_events(gold_processed);

        -- 3c. Dead Letter Queue for Malformed Events
        CREATE TABLE IF NOT EXISTS dead_letter_events (
            dlq_id TEXT PRIMARY KEY,
            source_event_id TEXT,
            raw_payload_json TEXT NOT NULL,
            error_reason TEXT NOT NULL,
            quarantined_at TEXT NOT NULL
        );

        -- 4. AI Request Logs (Operational Telemetry — No raw private question text)
        CREATE TABLE IF NOT EXISTS ai_request_logs (
            request_id TEXT PRIMARY KEY,
            idempotency_key TEXT UNIQUE,
            user_id TEXT,
            session_id TEXT,
            question_hash TEXT NOT NULL,
            legal_domain TEXT,
            jurisdiction TEXT DEFAULT 'India',
            request_timestamp TEXT NOT NULL,
            response_timestamp TEXT,
            processing_duration_ms REAL DEFAULT 0.0,
            rag_duration_ms REAL DEFAULT 0.0,
            llm_duration_ms REAL DEFAULT 0.0,
            status TEXT NOT NULL DEFAULT 'success',
            http_status_code INTEGER NOT NULL DEFAULT 200,
            model_used TEXT,
            input_tokens INTEGER DEFAULT 0,
            output_tokens INTEGER DEFAULT 0,
            estimated_cost_usd REAL DEFAULT 0.0,
            cache_status TEXT NOT NULL DEFAULT 'miss',
            retrieval_doc_count INTEGER DEFAULT 0,
            error_details TEXT,
            created_at TEXT NOT NULL
        );
        CREATE INDEX IF NOT EXISTS idx_ai_req_user_time ON ai_request_logs(user_id, created_at);
        CREATE INDEX IF NOT EXISTS idx_ai_req_status ON ai_request_logs(status, created_at);
        CREATE INDEX IF NOT EXISTS idx_ai_req_cache ON ai_request_logs(cache_status, created_at);

        -- 4b. Dedicated Access-Controlled User Chat History (Separated from operational analytics)
        CREATE TABLE IF NOT EXISTS user_chat_history (
            id TEXT PRIMARY KEY,
            user_id TEXT NOT NULL,
            request_id TEXT NOT NULL,
            question TEXT NOT NULL,
            answer TEXT NOT NULL,
            legal_domain TEXT,
            jurisdiction TEXT DEFAULT 'India',
            created_at TEXT NOT NULL,
            FOREIGN KEY (user_id) REFERENCES user_profiles(user_id) ON DELETE CASCADE
        );
        CREATE INDEX IF NOT EXISTS idx_chat_history_user ON user_chat_history(user_id, created_at DESC);

        -- 5. AI Usage Metrics
        CREATE TABLE IF NOT EXISTS ai_usage_metrics (
            id TEXT PRIMARY KEY,
            request_id TEXT NOT NULL,
            model_name TEXT NOT NULL,
            input_tokens INTEGER NOT NULL DEFAULT 0,
            output_tokens INTEGER NOT NULL DEFAULT 0,
            total_tokens INTEGER NOT NULL DEFAULT 0,
            estimated_cost_usd REAL NOT NULL DEFAULT 0.0,
            estimated_cost_saved_usd REAL NOT NULL DEFAULT 0.0,
            latency_ms REAL NOT NULL DEFAULT 0.0,
            cache_hit INTEGER NOT NULL DEFAULT 0,
            created_at TEXT NOT NULL,
            FOREIGN KEY (request_id) REFERENCES ai_request_logs(request_id) ON DELETE CASCADE
        );
        CREATE INDEX IF NOT EXISTS idx_ai_usage_created ON ai_usage_metrics(created_at);

        -- 6. Cache Metadata (Exact + Semantic Cache)
        CREATE TABLE IF NOT EXISTS cache_metadata (
            cache_key TEXT PRIMARY KEY,
            original_question TEXT NOT NULL,
            normalized_question TEXT NOT NULL,
            question_embedding_json TEXT,
            jurisdiction TEXT NOT NULL DEFAULT 'India',
            language TEXT NOT NULL DEFAULT 'English',
            legal_domain TEXT NOT NULL DEFAULT 'General',
            applicable_provisions_json TEXT NOT NULL DEFAULT '[]',
            source_version TEXT NOT NULL DEFAULT 'v1',
            model_version TEXT NOT NULL,
            prompt_version TEXT NOT NULL DEFAULT 'v1',
            embedding_model_version TEXT NOT NULL,
            response_json TEXT NOT NULL,
            hit_count INTEGER NOT NULL DEFAULT 0,
            created_at TEXT NOT NULL,
            expires_at TEXT NOT NULL,
            invalidated INTEGER NOT NULL DEFAULT 0,
            invalidation_reason TEXT
        );
        CREATE INDEX IF NOT EXISTS idx_cache_norm ON cache_metadata(normalized_question, jurisdiction, language);
        CREATE INDEX IF NOT EXISTS idx_cache_valid ON cache_metadata(invalidated, expires_at);

        -- 7. Gold Layer: Daily User Analytics
        CREATE TABLE IF NOT EXISTS daily_user_analytics (
            date_utc TEXT PRIMARY KEY,
            total_registered_users INTEGER NOT NULL DEFAULT 0,
            dau INTEGER NOT NULL DEFAULT 0,
            active_sessions INTEGER NOT NULL DEFAULT 0,
            total_logins INTEGER NOT NULL DEFAULT 0,
            failed_logins INTEGER NOT NULL DEFAULT 0,
            avg_session_duration_sec REAL NOT NULL DEFAULT 0.0,
            updated_at TEXT NOT NULL
        );

        -- 8. Gold Layer: Daily AI Analytics
        CREATE TABLE IF NOT EXISTS daily_ai_analytics (
            date_utc TEXT PRIMARY KEY,
            total_requests INTEGER NOT NULL DEFAULT 0,
            successful_requests INTEGER NOT NULL DEFAULT 0,
            failed_requests INTEGER NOT NULL DEFAULT 0,
            exact_cache_hits INTEGER NOT NULL DEFAULT 0,
            semantic_cache_hits INTEGER NOT NULL DEFAULT 0,
            cache_misses INTEGER NOT NULL DEFAULT 0,
            avg_response_ms REAL NOT NULL DEFAULT 0.0,
            total_input_tokens INTEGER NOT NULL DEFAULT 0,
            total_output_tokens INTEGER NOT NULL DEFAULT 0,
            estimated_cost_usd REAL NOT NULL DEFAULT 0.0,
            estimated_cost_saved_usd REAL NOT NULL DEFAULT 0.0,
            updated_at TEXT NOT NULL
        );

        -- 9. System Error Logs
        CREATE TABLE IF NOT EXISTS system_error_logs (
            id TEXT PRIMARY KEY,
            error_type TEXT NOT NULL,
            endpoint TEXT,
            user_id TEXT,
            message TEXT NOT NULL,
            stack_trace TEXT,
            created_at TEXT NOT NULL
        );
        CREATE INDEX IF NOT EXISTS idx_sys_err_created ON system_error_logs(created_at);

        -- 10. Admin Audit Logs
        CREATE TABLE IF NOT EXISTS admin_audit_logs (
            id TEXT PRIMARY KEY,
            admin_user_id TEXT NOT NULL,
            action TEXT NOT NULL,
            target_resource TEXT,
            details TEXT,
            created_at TEXT NOT NULL
        );
        CREATE INDEX IF NOT EXISTS idx_admin_audit_created ON admin_audit_logs(created_at);

        -- 11. Pipeline State Metadata
        CREATE TABLE IF NOT EXISTS pipeline_metadata (
            key TEXT PRIMARY KEY,
            value TEXT NOT NULL,
            updated_at TEXT NOT NULL
        );
        """,
    )
]


def run_migrations() -> None:
    """Apply pending schema migrations idempotently without destroying existing data."""
    with db_transaction() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS schema_migrations (
                version TEXT PRIMARY KEY,
                applied_at TEXT NOT NULL
            )
            """
        )
        applied = {
            row["version"]
            for row in conn.execute("SELECT version FROM schema_migrations").fetchall()
        }
        now = datetime.now(timezone.utc).isoformat()
        for version, sql in MIGRATIONS:
            if version not in applied:
                for stmt in sql.split(";"):
                    s = stmt.strip()
                    if s:
                        conn.execute(s)
                conn.execute(
                    "INSERT INTO schema_migrations (version, applied_at) VALUES (?, ?)",
                    (version, now),
                )


def apply_retention_policy(
    raw_event_days: int = 90,
    error_log_days: int = 60,
    expired_cache_days: int = 7,
) -> dict:
    """Purge expired cache and aged operational logs per configurable retention policy."""
    now = datetime.now(timezone.utc)
    cutoff_events = (now - timedelta(days=raw_event_days)).isoformat()
    cutoff_errors = (now - timedelta(days=error_log_days)).isoformat()
    cutoff_cache = (now - timedelta(days=expired_cache_days)).isoformat()

    deleted = {"activity_events": 0, "system_error_logs": 0, "cache_metadata": 0}
    with db_transaction() as conn:
        cur = conn.execute("DELETE FROM activity_events WHERE created_at < ?", (cutoff_events,))
        deleted["activity_events"] = cur.rowcount
        cur = conn.execute("DELETE FROM system_error_logs WHERE created_at < ?", (cutoff_errors,))
        deleted["system_error_logs"] = cur.rowcount
        cur = conn.execute(
            "DELETE FROM cache_metadata WHERE (invalidated = 1 OR expires_at < ?) AND created_at < ?",
            (now.isoformat(), cutoff_cache),
        )
        deleted["cache_metadata"] = cur.rowcount
    return deleted


# Initialize schema on module import
run_migrations()

