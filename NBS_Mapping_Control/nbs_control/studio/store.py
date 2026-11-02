"""Mapping Studio persistence (data/studio/studio.sqlite): projects, runs, proposal decisions and the audit trail.

Additive schema with a version table; existing application databases are never touched.
"""
from __future__ import annotations

import datetime as dt
import json
import sqlite3
from contextlib import contextmanager
from pathlib import Path

SCHEMA_VERSION = 1
SCHEMA = """
CREATE TABLE IF NOT EXISTS schema_version(component TEXT PRIMARY KEY, version INTEGER, applied TEXT);
CREATE TABLE IF NOT EXISTS projects(id TEXT PRIMARY KEY, created TEXT, label TEXT, folder TEXT, files TEXT, config TEXT);
CREATE TABLE IF NOT EXISTS runs(id TEXT PRIMARY KEY, project_id TEXT, created TEXT, kind TEXT, parent_run TEXT,
  workbook_sha256 TEXT, folder TEXT, summary TEXT);
CREATE TABLE IF NOT EXISTS proposals(run_id TEXT, proposal_id TEXT, confidence TEXT, status TEXT, decided_by TEXT, decided_at TEXT,
  decision_reason TEXT, body TEXT, PRIMARY KEY(run_id, proposal_id));
CREATE TABLE IF NOT EXISTS audit(id INTEGER PRIMARY KEY AUTOINCREMENT, ts TEXT, run_id TEXT, proposal_id TEXT, actor TEXT, action TEXT,
  cell TEXT, before TEXT, after TEXT, evidence TEXT);
"""


def now():
    return dt.datetime.now().isoformat(timespec='seconds')


class Store:
    def __init__(self, data_root):
        self.path = Path(data_root) / 'studio' / 'studio.sqlite'
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with self.c() as c:
            c.executescript(SCHEMA)
            c.execute('INSERT OR IGNORE INTO schema_version VALUES(?,?,?)', ('studio', SCHEMA_VERSION, now()))

    @contextmanager
    def c(self):
        c = sqlite3.connect(self.path)
        c.row_factory = sqlite3.Row
        try:
            with c:
                yield c
        finally:
            c.close()

    def add_project(self, pid, label, folder, files, config):
        with self.c() as c:
            c.execute('INSERT INTO projects VALUES(?,?,?,?,?,?)', (pid, now(), label, str(folder), json.dumps(files), json.dumps(config or {})))

    def project(self, pid):
        with self.c() as c:
            r = c.execute('SELECT * FROM projects WHERE id=?', (pid,)).fetchone()
        return {**dict(r), 'files': json.loads(r['files']), 'config': json.loads(r['config'])} if r else None

    def projects(self):
        with self.c() as c:
            return [dict(r) for r in c.execute('SELECT * FROM projects ORDER BY created DESC, rowid DESC')]

    def add_run(self, rid, pid, kind, parent, sha, folder, summary, proposals):
        with self.c() as c:
            c.execute('INSERT INTO runs VALUES(?,?,?,?,?,?,?,?)', (rid, pid, now(), kind, parent, sha, str(folder), json.dumps(summary, default=str)))
            for p in proposals:
                c.execute('INSERT INTO proposals VALUES(?,?,?,?,?,?,?,?)', (rid, p['id'], p['confidence'], 'PROPOSED', None, None, None,
                                                                         json.dumps(p, default=str)))
            c.execute('INSERT INTO audit(ts, run_id, actor, action, evidence) VALUES(?,?,?,?,?)',
                      (now(), rid, 'system', f'{kind}_RUN', f'{len(proposals)} proposals generated'))

    def runs(self, pid=None):
        with self.c() as c:
            q = 'SELECT * FROM runs' + (' WHERE project_id=?' if pid else '') + ' ORDER BY created DESC, rowid DESC'
            return [{**dict(r), 'summary': json.loads(r['summary'])} for r in c.execute(q, (pid,) if pid else ())]

    def run(self, rid):
        with self.c() as c:
            r = c.execute('SELECT * FROM runs WHERE id=?', (rid,)).fetchone()
        return {**dict(r), 'summary': json.loads(r['summary'])} if r else None

    def proposals(self, rid):
        with self.c() as c:
            return [{**json.loads(r['body']), 'status': r['status'], 'decided_by': r['decided_by'], 'decided_at': r['decided_at'],
                     'decision_reason': r['decision_reason']} for r in c.execute('SELECT * FROM proposals WHERE run_id=? ORDER BY proposal_id', (rid,))]

    def decide(self, rid, pids, status, actor, reason):
        if status not in ('APPROVED', 'REJECTED', 'PROPOSED'):
            raise ValueError('status must be APPROVED, REJECTED or PROPOSED')
        if not actor or not reason:
            raise ValueError('Name and reason are required for every decision')
        n = 0
        with self.c() as c:
            for pid in pids:
                r = c.execute('SELECT status, body FROM proposals WHERE run_id=? AND proposal_id=?', (rid, pid)).fetchone()
                if not r:
                    continue
                body = json.loads(r['body'])
                if status == 'APPROVED' and body['confidence'] == 'UNRESOLVED':
                    raise ValueError(f'{pid} is UNRESOLVED: there is no evidence-backed value to approve')
                c.execute('UPDATE proposals SET status=?, decided_by=?, decided_at=?, decision_reason=? WHERE run_id=? AND proposal_id=?',
                          (status, actor, now(), reason, rid, pid))
                for e in body['edits']:
                    c.execute('INSERT INTO audit(ts, run_id, proposal_id, actor, action, cell, before, after, evidence) VALUES(?,?,?,?,?,?,?,?,?)',
                              (now(), rid, pid, actor, status, e['cell'], str(e['existing']), str(e['proposed']), reason))
                n += 1
        return n

    def log(self, rid, actor, action, evidence, cell=None, before=None, after=None):
        with self.c() as c:
            c.execute('INSERT INTO audit(ts, run_id, actor, action, cell, before, after, evidence) VALUES(?,?,?,?,?,?,?,?)',
                      (now(), rid, actor, action, cell, before, after, evidence))

    def audit(self, rid=None):
        with self.c() as c:
            q = 'SELECT * FROM audit' + (' WHERE run_id=?' if rid else '') + ' ORDER BY id'
            return [dict(r) for r in c.execute(q, (rid,) if rid else ())]
