"""Owner decision store (SQLite, standard library).

Decisions are append-only events keyed by stable subject IDs (business mapping
IDs, section IDs, finding-queue item IDs). Each event records the evidence
fingerprint it was made against, so a refreshed import that changes the
evidence makes the decision STALE until the owner reviews it again. Rollback
appends a new event copying an earlier version; history is never rewritten.
"""

from __future__ import annotations

import json
import sqlite3
from contextlib import contextmanager
from datetime import date, datetime, timezone
from pathlib import Path
from typing import Any, Iterator

from . import DATA_DIR

SUBJECT_KINDS = ("MAPPING", "SECTION", "FINDING")
ACTIONS = {
    "MAPPING": ("APPROVE_PROPOSAL", "APPROVE_OVERRIDE", "REJECT", "NOT_APPLICABLE", "DEFER", "RECORD_REVIEW_NOTE"),
    "SECTION": ("APPROVE_JOIN", "OUT_OF_SCOPE", "REJECT", "DEFER"),
    "FINDING": ("CORRECTION_APPROVED", "POLICY_DECIDED", "ACCEPT_LEGACY", "NOT_A_DEFECT", "DEFER"),
}
APPROVING = {"APPROVE_PROPOSAL", "APPROVE_OVERRIDE", "APPROVE_JOIN", "CORRECTION_APPROVED", "POLICY_DECIDED",
             "ACCEPT_LEGACY", "NOT_A_DEFECT", "OUT_OF_SCOPE", "NOT_APPLICABLE", "REJECT"}
SCHEMA = """
CREATE TABLE IF NOT EXISTS catalog_versions (
    version_id INTEGER PRIMARY KEY AUTOINCREMENT,
    imported_at TEXT NOT NULL,
    catalog_path TEXT NOT NULL,
    sources_json TEXT NOT NULL,
    config_hashes_json TEXT NOT NULL,
    note TEXT
);
CREATE TABLE IF NOT EXISTS decision_events (
    event_id INTEGER PRIMARY KEY AUTOINCREMENT,
    subject_kind TEXT NOT NULL,
    subject_id TEXT NOT NULL,
    version INTEGER NOT NULL,
    action TEXT NOT NULL,
    payload_json TEXT NOT NULL,
    evidence_fingerprint TEXT,
    catalog_version INTEGER,
    actor TEXT NOT NULL,
    approved_on TEXT,
    reason TEXT NOT NULL,
    approval_evidence TEXT,
    origin TEXT NOT NULL,
    rollback_of_version INTEGER,
    recorded_at TEXT NOT NULL,
    UNIQUE(subject_kind, subject_id, version)
);
CREATE INDEX IF NOT EXISTS idx_decisions_subject ON decision_events(subject_kind, subject_id);
"""


class DecisionError(ValueError):
    """A decision is incomplete or malformed."""


def _now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


class Store:
    def __init__(self, data_dir: str | Path = DATA_DIR):
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(parents=True, exist_ok=True)
        (self.data_dir / "catalogs").mkdir(exist_ok=True)
        self.db_path = self.data_dir / "control.db"
        with self._connect() as db:
            db.executescript(SCHEMA)
        self._catalog_cache: tuple[int, dict[str, Any]] | None = None

    @contextmanager
    def _connect(self) -> Iterator[sqlite3.Connection]:
        """Commit on success, roll back on error, and always close the connection."""
        connection = sqlite3.connect(self.db_path)
        connection.row_factory = sqlite3.Row
        try:
            with connection:
                yield connection
        finally:
            connection.close()

    # ---- catalog versions -------------------------------------------------
    def save_catalog(self, catalog: dict[str, Any], config_hashes: dict[str, str], note: str = "") -> int:
        with self._connect() as db:
            cursor = db.execute(
                "INSERT INTO catalog_versions(imported_at, catalog_path, sources_json, config_hashes_json, note) "
                "VALUES (?, '', ?, ?, ?)",
                (_now(), json.dumps(catalog["sources"]), json.dumps(config_hashes), note))
            version = cursor.lastrowid
            path = self.data_dir / "catalogs" / f"catalog-{version:04d}.json"
            path.write_text(json.dumps({**catalog, "catalog_version": version}, ensure_ascii=False), encoding="utf-8")
            db.execute("UPDATE catalog_versions SET catalog_path=? WHERE version_id=?", (str(path.name), version))
        self._catalog_cache = None
        return version

    def catalog_versions(self) -> list[dict[str, Any]]:
        with self._connect() as db:
            rows = db.execute("SELECT * FROM catalog_versions ORDER BY version_id").fetchall()
        return [{**dict(r), "sources": json.loads(r["sources_json"]),
                 "config_hashes": json.loads(r["config_hashes_json"])} for r in rows]

    def current_catalog(self) -> dict[str, Any] | None:
        with self._connect() as db:
            row = db.execute("SELECT * FROM catalog_versions ORDER BY version_id DESC LIMIT 1").fetchone()
        if row is None:
            return None
        if self._catalog_cache and self._catalog_cache[0] == row["version_id"]:
            return self._catalog_cache[1]
        catalog = json.loads((self.data_dir / "catalogs" / row["catalog_path"]).read_text(encoding="utf-8"))
        self._catalog_cache = (row["version_id"], catalog)
        return catalog

    # ---- decisions --------------------------------------------------------
    def record(self, subject_kind: str, subject_id: str, action: str, *, actor: str, reason: str,
               evidence_fingerprint: str | None, catalog_version: int | None, payload: dict[str, Any] | None = None,
               approved_on: str | None = None, approval_evidence: str | None = None, origin: str = "UI",
               rollback_of_version: int | None = None) -> dict[str, Any]:
        if subject_kind not in SUBJECT_KINDS:
            raise DecisionError(f"Unknown subject kind {subject_kind}")
        if action not in ACTIONS[subject_kind] and action != "CLEARED":
            raise DecisionError(f"Action {action} is not valid for {subject_kind}")
        if not isinstance(actor, str) or not actor.strip():
            raise DecisionError("Decision requires the owner's name (actor)")
        if not isinstance(reason, str) or not reason.strip():
            raise DecisionError("Decision requires an owner reason")
        if action in APPROVING:
            if not approved_on:
                raise DecisionError("Approving decisions require approved_on (YYYY-MM-DD)")
            try:
                if date.fromisoformat(approved_on).isoformat() != approved_on:
                    raise ValueError
            except ValueError as exc:
                raise DecisionError("approved_on must be YYYY-MM-DD") from exc
            if not approval_evidence or not approval_evidence.strip():
                raise DecisionError("Approving decisions require approval evidence (reference, minute, email id)")
        with self._connect() as db:
            row = db.execute("SELECT MAX(version) AS v FROM decision_events WHERE subject_kind=? AND subject_id=?",
                             (subject_kind, subject_id)).fetchone()
            version = (row["v"] or 0) + 1
            db.execute(
                "INSERT INTO decision_events(subject_kind, subject_id, version, action, payload_json, evidence_fingerprint,"
                " catalog_version, actor, approved_on, reason, approval_evidence, origin, rollback_of_version, recorded_at)"
                " VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
                (subject_kind, subject_id, version, action, json.dumps(payload or {}, ensure_ascii=False),
                 evidence_fingerprint, catalog_version, actor.strip(), approved_on, reason.strip(),
                 (approval_evidence or "").strip() or None, origin, rollback_of_version, _now()))
        return self.current(subject_kind, subject_id)

    @staticmethod
    def _event(row: sqlite3.Row) -> dict[str, Any]:
        event = dict(row)
        event["payload"] = json.loads(event.pop("payload_json"))
        return event

    def current(self, subject_kind: str, subject_id: str) -> dict[str, Any] | None:
        with self._connect() as db:
            row = db.execute("SELECT * FROM decision_events WHERE subject_kind=? AND subject_id=? "
                             "ORDER BY version DESC LIMIT 1", (subject_kind, subject_id)).fetchone()
        if row is None or row["action"] == "CLEARED":
            return None
        return self._event(row)

    def current_all(self, subject_kind: str) -> dict[str, dict[str, Any]]:
        with self._connect() as db:
            rows = db.execute(
                "SELECT e.* FROM decision_events e JOIN (SELECT subject_id, MAX(version) AS v FROM decision_events "
                "WHERE subject_kind=? GROUP BY subject_id) m ON e.subject_id=m.subject_id AND e.version=m.v "
                "WHERE e.subject_kind=?", (subject_kind, subject_kind)).fetchall()
        return {row["subject_id"]: self._event(row) for row in rows if row["action"] != "CLEARED"}

    def history(self, subject_kind: str | None = None, subject_id: str | None = None, limit: int = 500) -> list[dict[str, Any]]:
        query = "SELECT * FROM decision_events"
        clauses, params = [], []
        if subject_kind:
            clauses.append("subject_kind=?"); params.append(subject_kind)
        if subject_id:
            clauses.append("subject_id=?"); params.append(subject_id)
        if clauses:
            query += " WHERE " + " AND ".join(clauses)
        query += " ORDER BY event_id DESC LIMIT ?"
        params.append(limit)
        with self._connect() as db:
            return [self._event(row) for row in db.execute(query, params).fetchall()]

    def rollback(self, subject_kind: str, subject_id: str, to_version: int, actor: str, reason: str) -> dict[str, Any] | None:
        """Append a new event equal to an earlier version (0 clears the decision)."""
        if to_version == 0:
            self.record(subject_kind, subject_id, "CLEARED", actor=actor, reason=f"Rollback to no decision: {reason}",
                        evidence_fingerprint=None, catalog_version=None, origin="ROLLBACK", rollback_of_version=0)
            return None
        with self._connect() as db:
            row = db.execute("SELECT * FROM decision_events WHERE subject_kind=? AND subject_id=? AND version=?",
                             (subject_kind, subject_id, to_version)).fetchone()
        if row is None:
            raise DecisionError(f"No version {to_version} for {subject_id}")
        target = self._event(row)
        if target["action"] == "CLEARED":
            return self.rollback(subject_kind, subject_id, 0, actor, reason)
        return self.record(subject_kind, subject_id, target["action"], actor=actor,
                           reason=f"Rollback to v{to_version}: {reason}",
                           evidence_fingerprint=target["evidence_fingerprint"],
                           catalog_version=target["catalog_version"], payload=target["payload"],
                           approved_on=target["approved_on"], approval_evidence=target["approval_evidence"],
                           origin="ROLLBACK", rollback_of_version=to_version)
