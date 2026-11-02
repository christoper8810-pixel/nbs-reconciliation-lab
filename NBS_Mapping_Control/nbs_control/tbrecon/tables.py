"""Read CSV / XLSX input tables as data, with normalised headers, row numbers and SHA-256."""
from __future__ import annotations

import csv
import hashlib
import re
from decimal import Decimal, InvalidOperation
from pathlib import Path

EXTENSIONS = ('.csv', '.xlsx', '.xlsm')

# Canonical column -> accepted (normalised) aliases, per input kind. Unknown columns are kept as-is.
ALIASES = {
    'LEGACY_GL': ('LEGACY_GL', 'OLD_GL', 'GL_ACCOUNT', 'ACCOUNT_NO_GL', 'LEDGER_NO', 'ETHIX_GL'),
    'TARGET_GL': ('TARGET_GL', 'DKB_GL', 'DKBGL', 'TRANSACT_GL', 'T24_GL', 'NEW_GL'),
    'CURRENCY': ('CURRENCY', 'CCY', 'CUR', 'ACCOUNT_CURRENCY', 'ISO_CODE'),
    'BALANCE': ('BALANCE', 'BALANCE_LCY', 'AMOUNT', 'AMOUNT_LCY', 'EQUIV_CUR_BAL', 'BALANCE_QAR', 'CLOSING_BALANCE'),
    'ACCOUNT_NO': ('ACCOUNT_NO', 'ACCOUNT', 'ACCOUNT_NUMBER', 'SOURCE_ACCOUNT', 'INTERNAL_ACCOUNT', 'LEGACY_ACCOUNT'),
    'TARGET_ACCOUNT': ('TARGET_ACCOUNT', 'NEW_ACCOUNT', 'T24_ACCOUNT', 'TRANSACT_ACCOUNT'),
    'CONSOL_KEY': ('CONSOL_KEY', 'CONSOLKEY'),
    'BUSINESS_DATE': ('BUSINESS_DATE', 'DATE', 'AS_OF', 'BOOKING_DATE', 'VALUE_DATE'),
    'CLASS': ('CLASS', 'GL_CLASS', 'BS_PL_OBS', 'TYPE_CLASS'),
    'CUSTOMER_ACCOUNT_REF': ('CUSTOMER_ACCOUNT_REF', 'CUSTOMER_ACCOUNT', 'CUS_ACC_REF', 'CUSTOMER_ACC'),
    'RULE_ID': ('RULE_ID', 'LINE', 'RULE'),
}


class TableError(ValueError):
    pass


def norm_header(h) -> str:
    s = re.sub(r'[^0-9A-Za-z]+', '_', str(h or '').strip()).strip('_').upper()
    return s


def sha256(path) -> str:
    h = hashlib.sha256()
    with Path(path).open('rb') as f:
        for b in iter(lambda: f.read(1 << 20), b''):
            h.update(b)
    return h.hexdigest()


def text(v) -> str:
    if v is None:
        return ''
    if isinstance(v, float) and v.is_integer():
        return str(int(v))
    return str(v).strip()


def amount(v) -> Decimal | None:
    """Blank -> None (missing, never zero)."""
    if v is None:
        return None
    if isinstance(v, (int, Decimal)):
        return Decimal(v)
    if isinstance(v, float):
        return Decimal(repr(v))
    s = str(v).strip().replace(',', '')
    if s in ('', '-', 'N/A'):
        return None
    neg = s.startswith('(') and s.endswith(')')
    try:
        d = Decimal(s.strip('()'))
    except InvalidOperation as exc:
        raise TableError(f'Amount is not numeric: {v!r}') from exc
    if not d.is_finite():
        raise TableError(f'Amount is not finite: {v!r}')
    return -d if neg else d


def _canon(headers):
    """Map normalised headers onto canonical names where an alias matches; keep first occurrence."""
    out, seen = [], set()
    normed = {norm_header(h) for h in headers}
    for h in headers:
        n = norm_header(h)
        for canon, al in ALIASES.items():
            if n in al and canon not in seen and (n == canon or canon not in normed):
                n = canon
                break
        if n in seen and n:
            raise TableError(f'Duplicate column after normalisation: {n}')
        seen.add(n)
        out.append(n)
    return out


def read_table(path, sheet=None):
    """Return (rows, meta). Each row is a dict of canonical headers plus _row (1-based source row)."""
    path = Path(path)
    if not path.exists():
        raise TableError(f'File not found: {path}')
    ext = path.suffix.lower()
    if ext == '.csv':
        with path.open(encoding='utf-8-sig', newline='') as f:
            reader = csv.reader(f)
            raw = list(reader)
        header_idx = next((i for i, r in enumerate(raw) if any(c.strip() for c in r)), None)
        if header_idx is None:
            raise TableError(f'{path.name}: no header row')
        headers = _canon(raw[header_idx])
        rows = []
        for i, r in enumerate(raw[header_idx + 1:], start=header_idx + 2):
            if not any(c.strip() for c in r):
                continue
            if len(r) > len(headers) and any(c.strip() for c in r[len(headers):]):
                raise TableError(f'{path.name} row {i}: populated cell outside the header range')
            d = {h: (r[j] if j < len(r) else '') for j, h in enumerate(headers) if h}
            d['_row'] = i
            rows.append(d)
    elif ext in ('.xlsx', '.xlsm'):
        import openpyxl
        wb = openpyxl.load_workbook(path, read_only=True, data_only=True)
        try:
            ws = wb[sheet] if sheet else wb.worksheets[0]
            it = ws.iter_rows(values_only=True)
            headers, rows = None, []
            for i, r in enumerate(it, start=1):
                if headers is None:
                    if r and any(text(c) for c in r):
                        headers = _canon([text(c) for c in r])
                    continue
                if not r or not any(text(c) for c in r):
                    continue
                d = {h: r[j] if j < len(r) else None for j, h in enumerate(headers) if h}
                d['_row'] = i
                rows.append(d)
            if headers is None:
                raise TableError(f'{path.name}: no header row')
        finally:
            wb.close()
    else:
        raise TableError(f'Unsupported file type {ext}; use CSV or XLSX')
    meta = {'path': str(path.resolve()), 'name': path.name, 'sha256': sha256(path), 'rows': len(rows),
            'headers': [h for h in headers if h]}
    return rows, meta


def require(meta, kind, columns):
    missing = [c for c in columns if c not in meta['headers']]
    if missing:
        raise TableError(f'{kind} ({meta["name"]}) is missing required columns: {", ".join(missing)}')
