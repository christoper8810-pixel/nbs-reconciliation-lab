"""GL_MAPPING adapter: the bank's GL mapping workbook (migration reference), read as data only.

Sheets used:
- GL Report : DKBGL report lines and their T24 criteria (category, sector, balance type, PL fields). Named ranges
              such as *CASH, *RETAIL or *PRINCIPAL2 are defined inline (RANGE name / field / start-end or list).
- CATEGORY  : T24 category codes and ranges with descriptions, module, range group and GL parameter.
- SEGMENT   : T24 sector codes with customer type, GL classification and segment.
- GL Mapping: Ethix GL account (old GL number + currency) -> Transact GL, T24 category, DKBGL line.
The workbook name marks it as a migration reference; the tool labels every use of it accordingly.
"""
from __future__ import annotations
import json
import re

from . import ooxml
from .rebuild_store import register_source

DATASET = 'GL_MAPPING'
IMPORT_VERSION = 'gl-mapping-1'
USE_NOTE = 'Bank GL mapping workbook (marked for migration use); used as a reference for T24 category, sector and GL-line definitions'

SCHEMA = """
CREATE TABLE IF NOT EXISTS gl_lines(source_sha256 TEXT, line TEXT, type TEXT, description TEXT, seq INTEGER, row_no INTEGER,
  PRIMARY KEY(source_sha256, line));
CREATE TABLE IF NOT EXISTS gl_criteria(source_sha256 TEXT, line TEXT, seq INTEGER, row_no INTEGER, app TEXT, market TEXT, currency TEXT,
  category TEXT, plcategory TEXT, plproduct TEXT, sector TEXT, plsector TEXT, pldepartment TEXT, balance TEXT, note TEXT,
  PRIMARY KEY(source_sha256, line, seq));
CREATE TABLE IF NOT EXISTS gl_named(source_sha256 TEXT, name TEXT, field TEXT, start TEXT, finish TEXT, items TEXT, row_no INTEGER,
  PRIMARY KEY(source_sha256, name));
CREATE TABLE IF NOT EXISTS t24_categories(source_sha256 TEXT, code TEXT, code_to TEXT, description TEXT, module TEXT, range_group TEXT,
  gl_param TEXT, transact_gl TEXT, row_no INTEGER);
CREATE TABLE IF NOT EXISTS t24_sectors(source_sha256 TEXT, code TEXT, name TEXT, customer_type TEXT, gl_class TEXT, segment TEXT, row_no INTEGER);
CREATE TABLE IF NOT EXISTS gl_accounts(source_sha256 TEXT, old_gl TEXT, gl10 TEXT, currency TEXT, description TEXT, transact_gl TEXT,
  category TEXT, dkbgl TEXT, classification TEXT, row_no INTEGER);
CREATE INDEX IF NOT EXISTS gl_accounts_gl ON gl_accounts(source_sha256, gl10);
"""


class GLMappingError(ValueError):
    pass


def _v(cells, col):
    v = cells.get(col, (None,))[0]
    if v is None:
        return None
    v = ooxml.identifier(v).strip()
    return v or None


def import_gl_mapping(c, path):
    c.executescript(SCHEMA)
    digest, existing = register_source(c, path, DATASET, IMPORT_VERSION)
    if existing and c.execute('SELECT 1 FROM gl_lines WHERE source_sha256=? LIMIT 1', (digest,)).fetchone():
        return {'source_sha256': digest, 'already_imported': True, **json.loads(c.execute('SELECT summary FROM sources WHERE source_sha256=?', (digest,)).fetchone()[0] or '{}')}
    sheets = dict(ooxml.sheets(path))
    for need in ('GL Report', 'CATEGORY'):
        if need not in sheets:
            raise GLMappingError(f'GL mapping workbook has no "{need}" sheet')
    try:
        summary = {'dataset': DATASET, 'use_note': USE_NOTE}
        summary.update(_gl_report(c, path, sheets['GL Report'], digest))
        summary['categories'] = _categories(c, path, sheets['CATEGORY'], digest)
        if 'SEGMENT' in sheets:
            summary['sectors'] = _sectors(c, path, sheets['SEGMENT'], digest)
        if 'GL Mapping' in sheets:
            summary['gl_accounts'] = _accounts(c, path, sheets['GL Mapping'], digest)
    except Exception:
        c.rollback()
        raise
    c.execute('UPDATE sources SET summary=? WHERE source_sha256=?', (json.dumps(summary), digest))
    c.commit()
    return {'source_sha256': digest, 'already_imported': False, **summary}


def _gl_report(c, path, part, digest):
    lines = crit = named = 0
    current = None
    seq = 0
    header = None
    for row_no, cells in ooxml.raw_rows(path, part):
        if header is None:
            header = {k: v[0] for k, v in cells.items()}
            if header.get('A') != 'LINE':
                raise GLMappingError('GL Report header must start with LINE')
            continue
        line = _v(cells, 'A')
        if line and line.startswith('DKBGL'):
            current = line
            seq = 0
            lines += 1
            c.execute('INSERT OR REPLACE INTO gl_lines VALUES(?,?,?,?,?,?)', (digest, line, _v(cells, 'B'), _v(cells, 'C'), lines, row_no))
        name, field = _v(cells, 'O'), _v(cells, 'P')
        if name and field:
            c.execute('INSERT OR REPLACE INTO gl_named VALUES(?,?,?,?,?,?,?)',
                      (digest, name.upper(), field.upper().replace('CATEEGORY', 'CATEGORY'), _v(cells, 'Q'), _v(cells, 'R'),
                       json.dumps(_items(_v(cells, 'Q'))) if _v(cells, 'Q') and not _v(cells, 'R') else None, row_no))
            named += 1
        if current and any(_v(cells, k) for k in ('G', 'H', 'J', 'M')):
            seq += 1
            crit += 1
            c.execute('INSERT INTO gl_criteria VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)',
                      (digest, current, seq, row_no, _v(cells, 'D'), _v(cells, 'E'), _v(cells, 'F'), _v(cells, 'G'), _v(cells, 'H'),
                       _v(cells, 'I'), _v(cells, 'J'), _v(cells, 'K'), _v(cells, 'L'), _v(cells, 'M'), _v(cells, 'N')))
    return {'gl_lines': lines, 'gl_criteria': crit, 'named_ranges': named}


def _items(text):
    return [x for x in re.split(r'[\s,;]+', text or '') if x]


def _categories(c, path, part, digest):
    n = 0
    group = None
    for row_no, cells in ooxml.raw_rows(path, part):
        if row_no == 1:
            continue
        if _v(cells, 'A'):
            group = _v(cells, 'A')
        code = _v(cells, 'E') or _v(cells, 'B')
        if not code or not re.fullmatch(r'\d+', code):
            continue
        c.execute('INSERT INTO t24_categories VALUES(?,?,?,?,?,?,?,?,?)',
                  (digest, code, _v(cells, 'C') if _v(cells, 'A') else None, _v(cells, 'F'), _v(cells, 'D'), _v(cells, 'K') or group,
                   _v(cells, 'G'), _v(cells, 'H'), row_no))
        n += 1
    return n


def _sectors(c, path, part, digest):
    n = 0
    ctype = gl = None
    for row_no, cells in ooxml.raw_rows(path, part):
        if row_no == 1:
            continue
        ctype = _v(cells, 'A') or ctype
        gl = _v(cells, 'B') or gl
        sec = _v(cells, 'C')
        m = re.match(r'\s*(\d{4})\s*-\s*(.+)', sec or '')
        if not m:
            continue
        c.execute('INSERT INTO t24_sectors VALUES(?,?,?,?,?,?,?)', (digest, m.group(1), m.group(2).strip(), ctype, gl, _v(cells, 'D'), row_no))
        n += 1
    return n


def _accounts(c, path, part, digest):
    n = 0
    batch = []
    for row_no, cells in ooxml.raw_rows(path, part):
        if row_no == 1:
            continue
        old = _v(cells, 'A')
        if not old:
            continue
        gl10 = old.split('-')[-1] if re.search(r'-\d{10}$', old) else None
        batch.append((digest, old, gl10, _v(cells, 'B'), _v(cells, 'C'), _v(cells, 'E'), _v(cells, 'L'), _v(cells, 'W'), _v(cells, 'H'), row_no))
        n += 1
        if len(batch) >= 5000:
            c.executemany('INSERT INTO gl_accounts VALUES(?,?,?,?,?,?,?,?,?,?)', batch)
            batch = []
    if batch:
        c.executemany('INSERT INTO gl_accounts VALUES(?,?,?,?,?,?,?,?,?,?)', batch)
    return n


def latest(c):
    c.executescript(SCHEMA)
    r = c.execute("SELECT source_sha256 FROM sources WHERE dataset=? ORDER BY imported_at DESC LIMIT 1", (DATASET,)).fetchone()
    return r[0] if r else None


def named_ranges(c, digest):
    return {n: {'field': f, 'start': s, 'end': e, 'items': json.loads(i) if i else None}
            for n, f, s, e, i in c.execute('SELECT name, field, start, finish, items FROM gl_named WHERE source_sha256=?', (digest,))}


def _token_filter(token, field, named):
    """'*NAME' -> named range; '5001' -> exact code; '6001, 7001' -> list; '1000-1999, 6001' -> inclusive range OR list.

    Fixed: inline ranges were previously kept as the literal text '1000-1999' and never matched a category."""
    if not token:
        return None, None
    token = token.strip()
    if token.startswith('*'):
        nr = named.get(token[1:].upper())
        if not nr:
            return None, f'named range {token} not defined in the GL Report'
        if nr['items']:
            return {'field': field, 'op': 'in', 'values': nr['items']}, None
        if nr['start'] and nr['end'] and nr['start'].isdigit() and nr['end'].isdigit():
            return {'field': field, 'op': 'range', 'values': [int(nr['start']), int(nr['end'])]}, None
        if nr['start']:
            return {'field': field, 'op': 'in', 'values': _items(nr['start'])}, None
        return None, f'named range {token} has no values'
    from .tbrecon import criteria
    text = re.sub(r'\s*-\s*', '-', token)
    text = re.sub(r'\s+', ',', text)
    try:
        crit = criteria.parse(text)
    except criteria.CriteriaError as exc:
        return None, f'{field} criterion {token!r}: {exc}'
    if crit.kind != 'SET':
        return None, None
    parts = []
    if crit.exact:
        parts.append({'field': field, 'op': 'in', 'values': sorted(crit.exact)})
    parts += [{'field': field, 'op': 'range', 'values': [lo, hi]} for lo, hi in crit.ranges]
    if crit.prefixes:
        parts.append({'field': field, 'op': 'prefix', 'values': list(crit.prefixes)})
    return (parts[0] if len(parts) == 1 else {'any': parts}), None


def _balance_types(token, named):
    """Fixed: a listed cell such as 'CURACCOUNT, DUEACCOUNT' was previously one (non-existent) balance type."""
    if not token:
        return [], 'no balance type'
    if token.startswith('*'):
        nr = named.get(token[1:].upper())
        if not nr:
            return [], f'balance group {token} not defined'
        return [x.upper() for x in (nr['items'] or _items(nr['start']))], None
    types = [x.upper() for x in _items(token)]
    bad = [x for x in types if not re.fullmatch(r'[A-Z][A-Z0-9_]*', x)]
    if bad:
        return [], f'balance type(s) {", ".join(bad)} are not atomic identifiers'
    return types, None


def line_parts(c, digest, line):
    """Translate one DKBGL line into engine parts over ECB balances. P&L criteria are returned as unsupported."""
    named = named_ranges(c, digest)
    parts, notes = [], []
    for seq, cat, plcat, sector, bal, app in c.execute(
            'SELECT seq, category, plcategory, sector, balance, app FROM gl_criteria WHERE source_sha256=? AND line=? ORDER BY seq', (digest, line)):
        if plcat and not cat:
            notes.append(f'criteria {seq}: P&L category {plcat} (P&L line, not an ECB balance)')
            continue
        f_cat, e1 = _token_filter(cat, 'category', named)
        f_sec, e2 = _token_filter(sector, 'sector', named)
        types, e3 = _balance_types(bal, named)
        errs = [e for e in (e1, e2, e3) if e]
        if errs or not f_cat:
            notes.append(f'criteria {seq}: ' + '; '.join(errs or ['no category']))
            continue
        flt = {'all': [x for x in (f_cat, f_sec) if x]} if f_sec else f_cat
        parts.append({'kind': 'STOCK', 'source': 'ECB', 'measure': 'components', 'components': types, 'filter': flt, 'factor': 1,
                      'enabled': True, 'label': f'{line} criteria {seq}: category {cat} sector {sector or "any"} balance {bal}'})
    return parts, notes
