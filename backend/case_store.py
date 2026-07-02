"""
Purpose: SQLite-backed persistence for case investigation state (AI results, analyst
dispositions, manager decisions) so a case escalated by one role is visible to every
other role, across logins and app restarts.
"""

import json
import sqlite3
from contextlib import contextmanager
from datetime import datetime
from pathlib import Path
from typing import Iterator

DB_PATH = Path(__file__).resolve().parent.parent / "case_store.db"

@contextmanager
def _connect() -> Iterator[sqlite3.Connection]:
    conn = sqlite3.connect(DB_PATH, timeout=10)
    conn.execute("PRAGMA journal_mode=WAL")
    try:
        yield conn
        conn.commit()
    finally:
        conn.close()

def init_db() -> None:
    with _connect() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS case_activity (
                case_id TEXT NOT NULL,
                kind TEXT NOT NULL,
                data TEXT NOT NULL,
                updated_at TEXT NOT NULL,
                PRIMARY KEY (case_id, kind)
            )
        """)

def _upsert(case_id: str, kind: str, data: dict) -> None:
    with _connect() as conn:
        conn.execute(
            "INSERT INTO case_activity (case_id, kind, data, updated_at) VALUES (?, ?, ?, ?) "
            "ON CONFLICT(case_id, kind) DO UPDATE SET data = excluded.data, updated_at = excluded.updated_at",
            (case_id, kind, json.dumps(data), datetime.now().strftime("%Y-%m-%d %H:%M")),
        )

def _delete(case_id: str, kind: str) -> None:
    with _connect() as conn:
        conn.execute("DELETE FROM case_activity WHERE case_id = ? AND kind = ?", (case_id, kind))

def load_all() -> dict:
    """Loads every case's state in one pass, shaped like the four lookups the UI needs:
    case_results, disposition_records, manager_decisions, and case_last_updated (the
    investigation run timestamp, used as a status's last-updated fallback)."""
    case_results, disposition_records, manager_decisions, case_last_updated = {}, {}, {}, {}
    with _connect() as conn:
        rows = conn.execute("SELECT case_id, kind, data, updated_at FROM case_activity")
        for case_id, kind, data, updated_at in rows:
            record = json.loads(data)
            if kind == "result":
                case_results[case_id] = record
                case_last_updated[case_id] = updated_at
            elif kind == "disposition":
                disposition_records[case_id] = record
            elif kind == "manager_decision":
                manager_decisions[case_id] = record
    return {
        "case_results": case_results,
        "disposition_records": disposition_records,
        "manager_decisions": manager_decisions,
        "case_last_updated": case_last_updated,
    }

def save_result(case_id: str, result: dict) -> None:
    _upsert(case_id, "result", result)

def save_disposition(case_id: str, disposition: dict) -> None:
    _upsert(case_id, "disposition", disposition)

def clear_disposition(case_id: str) -> None:
    _delete(case_id, "disposition")

def save_manager_decision(case_id: str, decision: dict) -> None:
    _upsert(case_id, "manager_decision", decision)

def clear_manager_decision(case_id: str) -> None:
    _delete(case_id, "manager_decision")

init_db()
