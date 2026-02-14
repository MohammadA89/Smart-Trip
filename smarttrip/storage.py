from __future__ import annotations

import json
import os
import sqlite3
import time
from typing import Any, Dict, List, Optional, Tuple


def connect(db_path: str) -> sqlite3.Connection:
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON;")
    conn.execute("PRAGMA journal_mode = WAL;")
    init_db(conn)
    return conn


def init_db(conn: sqlite3.Connection) -> None:
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS weights_global (
            feature TEXT PRIMARY KEY,
            weight REAL NOT NULL,
            updated_ts REAL NOT NULL
        )
        """
    )
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS weights_user (
            session_id TEXT NOT NULL,
            feature TEXT NOT NULL,
            weight REAL NOT NULL,
            updated_ts REAL NOT NULL,
            PRIMARY KEY (session_id, feature)
        )
        """
    )
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS recommendations (
            request_id TEXT PRIMARY KEY,
            created_ts REAL NOT NULL,
            session_id TEXT,
            context_json TEXT NOT NULL,
            search_mode TEXT,
            city TEXT
        )
        """
    )
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS recommendation_items (
            request_id TEXT NOT NULL,
            place_id TEXT NOT NULL,
            place_json TEXT NOT NULL,
            PRIMARY KEY (request_id, place_id),
            FOREIGN KEY (request_id) REFERENCES recommendations(request_id) ON DELETE CASCADE
        )
        """
    )
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            created_ts REAL NOT NULL,
            session_id TEXT,
            request_id TEXT,
            action TEXT NOT NULL,
            place_id TEXT,
            payload_json TEXT
        )
        """
    )
    conn.commit()


def ensure_seed_global_weights(conn: sqlite3.Connection, seed: Dict[str, float]) -> None:
    rows = conn.execute("SELECT feature FROM weights_global LIMIT 1").fetchall()
    if not rows:
        now = time.time()
        conn.executemany(
            "INSERT INTO weights_global(feature, weight, updated_ts) VALUES(?, ?, ?)",
            [(f, float(w), now) for f, w in seed.items()],
        )
        conn.commit()
        return

    existing = {r["feature"] for r in conn.execute("SELECT feature FROM weights_global").fetchall()}
    missing = [(f, float(w), time.time()) for f, w in seed.items() if f not in existing]
    if missing:
        conn.executemany(
            "INSERT INTO weights_global(feature, weight, updated_ts) VALUES(?, ?, ?)",
            missing,
        )
        conn.commit()


def load_global_weights(conn: sqlite3.Connection) -> Dict[str, float]:
    rows = conn.execute("SELECT feature, weight FROM weights_global").fetchall()
    return {r["feature"]: float(r["weight"]) for r in rows}


def load_user_weights(conn: sqlite3.Connection, session_id: str) -> Dict[str, float]:
    rows = conn.execute(
        "SELECT feature, weight FROM weights_user WHERE session_id = ?", (session_id,)
    ).fetchall()
    return {r["feature"]: float(r["weight"]) for r in rows}


def upsert_global_weights(conn: sqlite3.Connection, updates: Dict[str, float]) -> None:
    now = time.time()
    conn.executemany(
        """
        INSERT INTO weights_global(feature, weight, updated_ts)
        VALUES(?, ?, ?)
        ON CONFLICT(feature) DO UPDATE SET weight=excluded.weight, updated_ts=excluded.updated_ts
        """,
        [(f, float(w), now) for f, w in updates.items()],
    )
    conn.commit()


def upsert_user_weights(conn: sqlite3.Connection, session_id: str, updates: Dict[str, float]) -> None:
    now = time.time()
    conn.executemany(
        """
        INSERT INTO weights_user(session_id, feature, weight, updated_ts)
        VALUES(?, ?, ?, ?)
        ON CONFLICT(session_id, feature) DO UPDATE SET weight=excluded.weight, updated_ts=excluded.updated_ts
        """,
        [(session_id, f, float(w), now) for f, w in updates.items()],
    )
    conn.commit()


def log_recommendation(
    conn: sqlite3.Connection,
    *,
    request_id: str,
    session_id: Optional[str],
    context: Dict[str, Any],
    search_mode: str,
    city: Optional[str],
    recommendations: List[Dict[str, Any]],
) -> None:
    now = time.time()
    conn.execute(
        """
        INSERT INTO recommendations(request_id, created_ts, session_id, context_json, search_mode, city)
        VALUES(?, ?, ?, ?, ?, ?)
        """,
        (
            request_id,
            now,
            session_id,
            json.dumps(context, ensure_ascii=False),
            search_mode,
            city,
        ),
    )
    conn.executemany(
        """
        INSERT INTO recommendation_items(request_id, place_id, place_json)
        VALUES(?, ?, ?)
        """,
        [
            (request_id, str(p.get("place_id") or ""), json.dumps(p, ensure_ascii=False))
            for p in recommendations
        ],
    )
    conn.commit()


def get_recommendation(
    conn: sqlite3.Connection, request_id: str
) -> Tuple[Optional[Dict[str, Any]], List[Dict[str, Any]]]:
    row = conn.execute(
        "SELECT context_json FROM recommendations WHERE request_id = ?", (request_id,)
    ).fetchone()
    if row is None:
        return None, []

    try:
        context = json.loads(row["context_json"])
    except Exception:
        context = None

    items = conn.execute(
        "SELECT place_json FROM recommendation_items WHERE request_id = ?", (request_id,)
    ).fetchall()
    places: List[Dict[str, Any]] = []
    for r in items:
        try:
            places.append(json.loads(r["place_json"]))
        except Exception:
            continue

    if not isinstance(context, dict):
        return None, places
    return context, places


def log_event(
    conn: sqlite3.Connection,
    *,
    session_id: Optional[str],
    request_id: Optional[str],
    action: str,
    place_id: Optional[str] = None,
    payload: Optional[Dict[str, Any]] = None,
) -> None:
    conn.execute(
        """
        INSERT INTO events(created_ts, session_id, request_id, action, place_id, payload_json)
        VALUES(?, ?, ?, ?, ?, ?)
        """,
        (
            time.time(),
            session_id,
            request_id,
            action,
            place_id,
            json.dumps(payload or {}, ensure_ascii=False) if payload is not None else None,
        ),
    )
    conn.commit()

