"""Separate, versioned store for the rebuild model.

The legacy bank database (data/bank_20260930.sqlite) is only ever opened read-only. This store
keeps three layers apart: raw source rows, normalized source facts and BO/live reference cells.
Generated results live in per-run databases, never in the reference tables.
"""
from __future__ import annotations
import hashlib
import json
import shutil
import sqlite3
from datetime import datetime, timezone
from pathlib import Path

SCHEMA_VERSION = 1

SCHEMA = """
CREATE TABLE IF NOT EXISTS meta(key TEXT PRIMARY KEY, value TEXT);
CREATE TABLE IF NOT EXISTS sources(
  source_sha256 TEXT PRIMARY KEY, dataset TEXT NOT NULL, filename TEXT, original_path TEXT,
  bytes INTEGER, imported_at TEXT, import_version TEXT, aliases TEXT, summary TEXT);
CREATE TABLE IF NOT EXISTS categ_raw(
  source_sha256 TEXT, sheet TEXT, row_no INTEGER, cells TEXT,
  PRIMARY KEY(source_sha256, sheet, row_no));
CREATE TABLE IF NOT EXISTS categ_schema(
  source_sha256 TEXT, column TEXT, header TEXT, field TEXT, issue TEXT,
  PRIMARY KEY(source_sha256, column));
CREATE TABLE IF NOT EXISTS categ_events(
  source_sha256 TEXT, sheet TEXT, row_no INTEGER,
  source_id TEXT, subentry_seq TEXT, company TEXT, amount_raw TEXT, amount_micro INTEGER,
  transaction_code TEXT, pl_category TEXT, customer_id TEXT, account_officer TEXT, product_category TEXT,
  value_date TEXT, currency TEXT, position_type TEXT, our_reference TEXT, exposure_date TEXT,
  currency_market TEXT, trans_reference TEXT, system_id TEXT, booking_date TEXT, consol_key TEXT,
  processing_date TEXT, soft_acctng_dtls TEXT, unheaded_u TEXT, key_tokens TEXT, key_conflicts TEXT,
  event_type TEXT, fingerprint TEXT,
  PRIMARY KEY(source_sha256, sheet, row_no));
CREATE INDEX IF NOT EXISTS categ_fp ON categ_events(source_sha256, fingerprint);
CREATE INDEX IF NOT EXISTS categ_id ON categ_events(source_sha256, source_id);
CREATE INDEX IF NOT EXISTS categ_ref ON categ_events(source_sha256, our_reference);
CREATE TABLE IF NOT EXISTS ref_versions(
  ref_version TEXT PRIMARY KEY, kind TEXT, source_sha256 TEXT, filename TEXT, report_date TEXT,
  unit TEXT, imported_at TEXT, notes TEXT);
CREATE TABLE IF NOT EXISTS bo_items(
  ref_version TEXT, table_code TEXT, item_code TEXT, description TEXT, parent_code TEXT,
  depth INTEGER, sheet TEXT, row_no INTEGER, report_date TEXT,
  PRIMARY KEY(ref_version, table_code, item_code, report_date));
CREATE TABLE IF NOT EXISTS bo_cells(
  ref_version TEXT, table_code TEXT, item_code TEXT, report_date TEXT, measure TEXT,
  header TEXT, semantic TEXT, kind TEXT, unit TEXT, cell TEXT, raw TEXT, value_micro INTEGER,
  PRIMARY KEY(ref_version, table_code, item_code, report_date, measure));
CREATE TABLE IF NOT EXISTS bo_special(
  ref_version TEXT, table_code TEXT, sheet TEXT, row_no INTEGER, report_date TEXT, fields TEXT,
  PRIMARY KEY(ref_version, table_code, row_no));
CREATE TABLE IF NOT EXISTS bo_headers(
  ref_version TEXT, table_code TEXT, sheet TEXT, title TEXT, header_row INTEGER, headers TEXT,
  PRIMARY KEY(ref_version, table_code));
CREATE TABLE IF NOT EXISTS qcb_rules(
  rule_id TEXT PRIMARY KEY, qcb_code TEXT, kind TEXT, operator TEXT, left_text TEXT, right_text TEXT, rule TEXT);
CREATE TABLE IF NOT EXISTS live_cells(
  ref_version TEXT, row_no INTEGER, col TEXT, raw TEXT, value_micro INTEGER, label TEXT,
  PRIMARY KEY(ref_version, row_no, col));
"""


def sha256(path) -> str:
    h = hashlib.sha256()
    with Path(path).open('rb') as f:
        for b in iter(lambda: f.read(1 << 20), b''):
            h.update(b)
    return h.hexdigest()


def now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec='seconds')


def connect(path) -> sqlite3.Connection:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    c = sqlite3.connect(path)
    c.executescript(SCHEMA)
    row = c.execute("SELECT value FROM meta WHERE key='schema_version'").fetchone()
    if row is None:
        c.execute("INSERT INTO meta VALUES('schema_version',?)", (str(SCHEMA_VERSION),))
        c.commit()
    elif int(row[0]) > SCHEMA_VERSION:
        raise ValueError('Rebuild store was written by a newer schema version')
    return c


def safe_migrate_copy(path) -> Path:
    """Before any schema migration, keep a byte copy of the existing store."""
    path = Path(path)
    if not path.exists():
        return path
    backup = path.with_name(path.stem + '.' + datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S') + '.bak.sqlite')
    shutil.copy2(path, backup)
    return backup


def open_bank_readonly(database, shared=False) -> sqlite3.Connection:
    """Legacy bank evidence is immutable: open with SQLite's read-only URI mode."""
    uri = Path(database).resolve().as_uri().replace('file:', 'file:', 1) + '?mode=ro'
    return sqlite3.connect(uri, uri=True, check_same_thread=not shared)  # shared connections are serialised by their owner's lock


def register_source(c, path, dataset, import_version) -> tuple[str, bool]:
    """Register a whole upload by content hash. Returns (sha256, already_imported)."""
    digest = sha256(path)
    row = c.execute('SELECT dataset, aliases FROM sources WHERE source_sha256=?', (digest,)).fetchone()
    name = Path(path).name
    if row:
        if row[0] != dataset:
            raise ValueError(f'File {name} was already imported as {row[0]}, not {dataset}')
        aliases = json.loads(row[1] or '[]')
        if name not in aliases:
            aliases.append(name)
            c.execute('UPDATE sources SET aliases=? WHERE source_sha256=?', (json.dumps(aliases), digest))
            c.commit()
        return digest, True
    c.execute('INSERT INTO sources VALUES(?,?,?,?,?,?,?,?,?)',
              (digest, dataset, name, str(Path(path).resolve()), Path(path).stat().st_size, now(),
               import_version, json.dumps([name]), None))
    return digest, False


def sources(c):
    cols = ['source_sha256', 'dataset', 'filename', 'original_path', 'bytes', 'imported_at', 'import_version', 'aliases', 'summary']
    out = []
    for r in c.execute('SELECT * FROM sources ORDER BY imported_at'):
        d = dict(zip(cols, r))
        d['aliases'] = json.loads(d['aliases'] or '[]')
        d['summary'] = json.loads(d['summary']) if d['summary'] else None
        out.append(d)
    return out
