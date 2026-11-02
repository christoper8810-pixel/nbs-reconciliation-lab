"""CATEG_ENTRY adapter: T24 category accounting events, kept at their own grain.

Ingestion identity is (source hash, sheet, row). The exported ID is stored separately; it is
not unique and no row is deleted, deduplicated or chosen by position here. Unheaded populated
columns are preserved under neutral names. The PL CONSOL.KEY is parsed with its own layout and
only the five tokens validated against explicit fields are named.
"""
from __future__ import annotations
import hashlib
import json
from collections import Counter, defaultdict
from decimal import Decimal

from . import ooxml
from .money import parse_decimal, to_micro, text as micro_text
from .rebuild_store import register_source

DATASET = 'CATEG_ENTRY'
IMPORT_VERSION = 'categ-adapter-1'

FIELDS = {
    'ID': 'source_id', 'COMPANY.CODE': 'company', 'AMOUNT.LCY': 'amount_raw', 'TRANSACTION.CODE': 'transaction_code',
    'PL.CATEGORY': 'pl_category', 'CUSTOMER.ID': 'customer_id', 'ACCOUNT.OFFICER': 'account_officer',
    'PRODUCT.CATEGORY': 'product_category', 'VALUE.DATE': 'value_date', 'CURRENCY': 'currency',
    'POSITION.TYPE': 'position_type', 'OUR.REFERENCE': 'our_reference', 'EXPOSURE.DATE': 'exposure_date',
    'CURRENCY.MARKET': 'currency_market', 'TRANS.REFERENCE': 'trans_reference', 'SYSTEM.ID': 'system_id',
    'BOOKING.DATE': 'booking_date', 'CONSOL.KEY': 'consol_key', 'PROCESSING.DATE': 'processing_date',
    'SOFT.ACCTNG.DTLS': 'soft_acctng_dtls',
}
REQUIRED = {'ID', 'COMPANY.CODE', 'AMOUNT.LCY', 'PL.CATEGORY', 'CURRENCY', 'BOOKING.DATE',
            'PROCESSING.DATE', 'VALUE.DATE', 'CONSOL.KEY', 'SYSTEM.ID'}
DATE_FIELDS = ('value_date', 'exposure_date', 'booking_date', 'processing_date')
# Validated PL CONSOL.KEY positions. Other tokens are kept but deliberately unnamed.
KEY_TOKENS = {1: 'pl_category', 2: 'currency', 3: 'product_category', 4: 'account_officer', -1: 'company'}
KEY_LENGTH = 14
# Filterable fields for typed mappings; PL.CATEGORY and PRODUCT.CATEGORY stay distinct namespaces.
FILTER_FIELDS = {'pl_category', 'product_category', 'transaction_code', 'system_id', 'company', 'currency',
                 'soft_acctng_dtls', 'unheaded_u', 'event_type', 'position_type', 'account_officer'}


class CategImportError(ValueError):
    pass


def fingerprint(cells: dict) -> str:
    """Hash of every populated exported cell value. Diagnostic only, not a posting identity."""
    payload = json.dumps(sorted((k, v[0]) for k, v in cells.items()), separators=(',', ':'))
    return hashlib.sha256(payload.encode('utf-8')).hexdigest()


def event_type(rec) -> str:
    if rec['system_id'] == 'DC' and not rec['soft_acctng_dtls']:
        return 'DC_WITHOUT_SOFT_DETAILS'
    return (rec['soft_acctng_dtls'] or 'NO_SOFT_DETAILS') + ' / ' + (rec['unheaded_u'] or '-')


def import_categ(c, path, sheet_name=None):
    """Import one category workbook. A byte-identical copy is recognised and not reloaded."""
    digest, existing = register_source(c, path, DATASET, IMPORT_VERSION)
    if existing:
        return {'source_sha256': digest, 'already_imported': True,
                **json.loads(c.execute('SELECT summary FROM sources WHERE source_sha256=?', (digest,)).fetchone()[0])}
    try:
        summary = _import(c, path, digest, sheet_name)
    except Exception:
        c.rollback()
        raise
    c.execute('UPDATE sources SET summary=? WHERE source_sha256=?', (json.dumps(summary), digest))
    c.commit()
    return {'source_sha256': digest, 'already_imported': False, **summary}


def _import(c, path, digest, sheet_name):
    package = ooxml.inspect_package(path)
    sheets = ooxml.sheets(path)
    if sheet_name:
        sheets = [s for s in sheets if s[0] == sheet_name]
        if not sheets:
            raise CategImportError(f'Sheet {sheet_name} not found')
    name, part = sheets[0]
    headers = None
    unheaded = {}
    rows = 0
    issues = Counter()
    raw_batch, ev_batch = [], []
    for row_no, cells in ooxml.raw_rows(path, part):
        if not cells:
            continue
        if headers is None:
            headers = {col: v[0].strip() for col, v in cells.items()}
            missing = REQUIRED - set(headers.values())
            if missing:
                raise CategImportError('Category workbook is missing required headers: ' + ', '.join(sorted(missing)))
            dup = [h for h, n in Counter(headers.values()).items() if n > 1]
            if dup:
                raise CategImportError('Duplicate category headers: ' + ', '.join(dup))
            for col, h in headers.items():
                c.execute('INSERT INTO categ_schema VALUES(?,?,?,?,?)', (digest, col, h, FIELDS.get(h), None if h in FIELDS else 'UNMAPPED_HEADER'))
            last = max(ooxml.col_index(k) for k in headers)
            continue
        for col in cells:
            if col not in headers and col not in unheaded:
                if ooxml.col_index(col) <= last:
                    raise CategImportError(f'Populated cell {col}{row_no} lies inside the header range but has no header')
                unheaded[col] = 'UNHEADED_' + col
        rec = {f: None for f in FIELDS.values()}
        for col, (val, _kind) in cells.items():
            field = FIELDS.get(headers.get(col))
            if field:
                rec[field] = val
        rec['unheaded_u'] = cells.get('U', (None,))[0]
        for f in ('source_id', 'company', 'transaction_code', 'pl_category', 'customer_id', 'account_officer',
                  'product_category', 'currency', 'position_type', 'our_reference', 'currency_market',
                  'trans_reference', 'system_id', 'consol_key', 'soft_acctng_dtls'):
            rec[f] = ooxml.identifier(rec[f]) if rec[f] is not None else None
            if rec[f] == '':
                rec[f] = None
        if not rec['source_id']:
            raise CategImportError(f'Row {row_no} has no ID')
        try:
            amount = parse_decimal(rec['amount_raw'])
        except ValueError as exc:
            raise CategImportError(f'Row {row_no}: {exc}') from exc
        if amount is None:
            raise CategImportError(f'Row {row_no} has a blank AMOUNT.LCY')
        for f in DATE_FIELDS:
            try:
                rec[f] = ooxml.yyyymmdd(rec[f])
            except ValueError as exc:
                raise CategImportError(f'Row {row_no} {f}: {exc}') from exc
        tokens = (rec['consol_key'] or '').split('.')
        conflicts = []
        if len(tokens) != KEY_LENGTH or tokens[0] != 'PL':
            conflicts.append(f'PL CONSOL.KEY has {len(tokens)} tokens / prefix {tokens[0]!r}')
        else:
            for pos, field in KEY_TOKENS.items():
                if (tokens[pos] or None) != rec[field]:
                    conflicts.append(f'token{pos}={tokens[pos]!r} vs {field}={rec[field]!r}')
        if conflicts:
            issues['consol_key_conflict'] += 1
        rec['event_type'] = event_type(rec)
        fp = fingerprint(cells)
        raw_batch.append((digest, name, row_no, json.dumps({k: v[0] for k, v in cells.items()}, separators=(',', ':'))))
        ev_batch.append((digest, name, row_no, rec['source_id'], None, rec['company'], rec['amount_raw'], to_micro(amount),
                         rec['transaction_code'], rec['pl_category'], rec['customer_id'], rec['account_officer'],
                         rec['product_category'], rec['value_date'], rec['currency'], rec['position_type'],
                         rec['our_reference'], rec['exposure_date'], rec['currency_market'], rec['trans_reference'],
                         rec['system_id'], rec['booking_date'], rec['consol_key'], rec['processing_date'],
                         rec['soft_acctng_dtls'], rec['unheaded_u'], json.dumps(tokens), json.dumps(conflicts) if conflicts else None,
                         rec['event_type'], fp))
        rows += 1
        if len(ev_batch) >= 5000:
            _flush(c, raw_batch, ev_batch)
    if headers is None or rows == 0:
        raise CategImportError('Category workbook contains no data rows')
    _flush(c, raw_batch, ev_batch)
    for col, neutral in unheaded.items():
        c.execute('INSERT INTO categ_schema VALUES(?,?,?,?,?)', (digest, col, None, neutral.lower(), 'MISSING_HEADER_POPULATED_COLUMN'))
    return {'dataset': DATASET, 'sheet': name, 'rows': rows, 'headers': headers, 'unheaded_columns': unheaded,
            'package': package, 'issues': dict(issues)}


def _flush(c, raw_batch, ev_batch):
    c.executemany('INSERT INTO categ_raw VALUES(?,?,?,?)', raw_batch)
    c.executemany('INSERT INTO categ_events VALUES(' + ','.join('?' * 30) + ')', ev_batch)
    raw_batch.clear()
    ev_batch.clear()


def source_controls(c, digest):
    """Independent controls straight from the raw layer (re-parsed text), not the normalized amount."""
    total = Decimal(0)
    pos = Decimal(0)
    neg = Decimal(0)
    n = 0
    for (cells,) in c.execute('SELECT cells FROM categ_raw WHERE source_sha256=?', (digest,)):
        d = json.loads(cells)
        hdr = _amount_column(c, digest)
        a = parse_decimal(d.get(hdr))
        total += a
        n += 1
        if a > 0:
            pos += a
        elif a < 0:
            neg += a
    out = {'rows': n, 'net_lcy': str(total), 'positive_lcy': str(pos), 'negative_lcy': str(neg)}
    for dim in ('booking_date', 'processing_date', 'company', 'currency', 'pl_category', 'event_type', 'system_id'):
        out['by_' + dim] = {str(k): {'rows': r, 'net_lcy': micro_text(s)} for k, r, s in c.execute(
            f'SELECT {dim}, count(*), sum(amount_micro) FROM categ_events WHERE source_sha256=? GROUP BY {dim} ORDER BY {dim}', (digest,))}
    out['value_date_profile'] = dict(c.execute(
        """SELECT CASE WHEN value_date IS NULL THEN 'blank' WHEN value_date<=booking_date AND value_date<'2026-10-01' THEN 'on_or_before_2026-09-30'
           ELSE 'october_or_later' END k, count(*) FROM categ_events WHERE source_sha256=? GROUP BY k""", (digest,)))
    out['distinct_ids'] = c.execute('SELECT count(DISTINCT source_id) FROM categ_events WHERE source_sha256=?', (digest,)).fetchone()[0]
    out['ids_with_multiple_rows'] = c.execute(
        'SELECT count(*) FROM (SELECT source_id FROM categ_events WHERE source_sha256=? GROUP BY source_id HAVING count(*)>1)', (digest,)).fetchone()[0]
    out['ids_with_multiple_variants'] = c.execute(
        'SELECT count(*) FROM (SELECT source_id FROM categ_events WHERE source_sha256=? GROUP BY source_id HAVING count(DISTINCT fingerprint)>1)', (digest,)).fetchone()[0]
    out['blank_reference_rows'] = c.execute('SELECT count(*) FROM categ_events WHERE source_sha256=? AND our_reference IS NULL', (digest,)).fetchone()[0]
    out['unheaded_u_rows'] = c.execute('SELECT count(*) FROM categ_events WHERE source_sha256=? AND unheaded_u IS NOT NULL', (digest,)).fetchone()[0]
    out['consol_key_conflicts'] = c.execute('SELECT count(*) FROM categ_events WHERE source_sha256=? AND key_conflicts IS NOT NULL', (digest,)).fetchone()[0]
    return out


_amount_cache = {}


def _amount_column(c, digest):
    if digest not in _amount_cache:
        _amount_cache[digest] = c.execute("SELECT column FROM categ_schema WHERE source_sha256=? AND header='AMOUNT.LCY'", (digest,)).fetchone()[0]
    return _amount_cache[digest]


def repeated_groups(c, digest):
    """Identical exported observations, grouped by value fingerprint (never by row order)."""
    out = []
    for fp, n, rows, amount, sid in c.execute(
            """SELECT fingerprint, count(*), group_concat(row_no, '|'), max(amount_micro), max(source_id)
               FROM categ_events WHERE source_sha256=? GROUP BY fingerprint HAVING count(*)>1 ORDER BY fingerprint""", (digest,)):
        out.append({'fingerprint': fp, 'occurrences': n, 'excess': n - 1, 'source_id': sid,
                    'rows': sorted(int(x) for x in rows.split('|')), 'amount_each_micro': amount,
                    'excess_micro': amount * (n - 1)})
    return out


def account_links(c, digest, bank, currency_field='currency'):
    """Event-to-ECB relationship profile at account grain. Never sums repeated ECB balances."""
    refs = defaultdict(lambda: [0, 0])
    for ref, cur, n, amt in c.execute(
            'SELECT our_reference, currency, count(*), sum(amount_micro) FROM categ_events WHERE source_sha256=? GROUP BY our_reference, currency', (digest,)):
        refs[(ref, cur)] = [n, amt]
    matched_rows = matched_accounts = ambiguous = 0
    unmatched_rows = 0
    for (ref, cur), (n, _amt) in refs.items():
        if ref is None:
            unmatched_rows += n
            continue
        hits = bank.execute("SELECT count(*), count(DISTINCT currency) FROM unique_records WHERE source='ECB' AND account=?", (ref,)).fetchone()
        same = bank.execute("SELECT count(*) FROM unique_records WHERE source='ECB' AND account=? AND currency=?", (ref, cur)).fetchone()[0]
        if same == 1:
            matched_rows += n
            matched_accounts += 1
        elif same > 1 or (hits[0] and not same):
            ambiguous += n
        else:
            unmatched_rows += n
    return {'matched_rows': matched_rows, 'matched_distinct_accounts': matched_accounts,
            'ambiguous_or_conflicting_rows': ambiguous, 'unmatched_or_blank_reference_rows': unmatched_rows}
