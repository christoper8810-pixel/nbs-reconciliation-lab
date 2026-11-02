"""ETHIX_BO_NBS adapter: the BO QCB NBS workbook as a *reference*, never a generation input.

Measures are identified by validated header names per table (not column letters), table codes
stay zero-padded text, report-date columns are dates (never money), and Table-020's distinct
acquisition schema is retained separately. Duplicate table/item/date/measure keys fail.
"""
from __future__ import annotations
import json
import re
from pathlib import Path

from . import ooxml
from .money import parse_decimal, to_micro
from .rebuild_store import register_source, now

DATASET = 'ETHIX_BO_NBS'
IMPORT_VERSION = 'bo-adapter-1'
ITEM_HEADERS = ('Qcb Item Code',)
DESC_HEADERS = ('Qcb Item Description', 'Qcb Item Desc')
DATE_HEADERS = ('Report Date', 'Rep Date')
SPECIAL_TABLES = {'020': ('Acquistion No', 'Provision Amount', 'Net Value')}
SUBSET_PREFIXES = ('gcc', 'saudi', 'uae', 'oman', 'kuw', 'bah', 'blocked')
COUNTRY = {'saudi': 'SA', 'uae': 'AE', 'oman': 'OM', 'kuw': 'KW', 'bah': 'BH'}


class BOImportError(ValueError):
    pass


def norm(h):
    return re.sub(r'\s+', ' ', str(h)).strip()


def classify(table, header):
    """Semantic measure definition for one validated header. Owner-editable via the catalogue file."""
    h = norm(header)
    low = h.lower()
    d = {'header': h, 'kind': 'money', 'unit': 'QAR_THOUSANDS_ASSUMED', 'additive': True, 'primary': True, 'semantic': None}
    cur = 'FC' if re.search(r'\bfc\b', low) else 'LC' if re.search(r'\blc\b', low) else None
    if low.startswith(SUBSET_PREFIXES):
        key = low.split()[0]
        d.update(primary=False, semantic=('SUBSET_' + (COUNTRY.get(key, key.upper())) + ('_' + cur if cur else '')),
                 note='Subset/view of primary geography; never added to primary totals')
        if key == 'blocked':
            d['semantic'] = 'BLOCKED_AMOUNT'
        return d
    m = re.fullmatch(r'(in|out)\s+(lc|fc)\s+amount', low) or re.fullmatch(r'(in|out)\s+amount\s+(lc|fc)', low)
    if m:
        d['semantic'] = f'{m.group(1).upper()}_{m.group(2).upper()}'
        return d
    if table in ('012', '025'):
        d['semantic'] = 'BAND_' + re.sub(r'\W+', '_', low.replace(' amt', '')).upper()
        if not low.endswith('amt'):
            d.update(kind='count', unit='COUNT', semantic=d['semantic'] + '_COUNT', note='Count: never divided by 1000')
        else:
            d['semantic'] += '_AMOUNT'
        return d
    if 'rate' in low:
        d.update(kind='rate', unit='RATE', additive=False, semantic='RATE_' + re.sub(r'\W+', '_', low).upper(),
                 note='Rate: never summed as money')
        return d
    if table == '038':
        if low.startswith('nat'):
            d.update(kind='notional', semantic='NOTIONAL_' + re.sub(r'\W+', '_', low).upper())
        elif 'fair value' in low:
            d.update(kind='fair_value_positive' if low.startswith('pive') else 'fair_value_negative',
                     semantic='FV_' + ('POSITIVE' if low.startswith('pive') else 'NEGATIVE'))
        return d
    mat = {
        'no maturity': 'MAT_NONE', 'one week': 'MAT_1W', 'week to 1 month': 'MAT_1M', 'one to 3 month': 'MAT_3M',
        'three to 6 month': 'MAT_6M', 'six to 12 month': 'MAT_12M', 'one to 2 year': 'MAT_2Y', 'two to 5 year': 'MAT_5Y',
        'five to 10 year': 'MAT_10Y', 'ten to 20 year': 'MAT_20Y', 'greater 20 year': 'MAT_GT20Y',
        'greater 5 year': 'MAT_GT5Y', 'one to 5 year': 'MAT_1Y_5Y', 'greater 10 year': 'MAT_GT10Y',
        'greater 2 year': 'MAT_GT2Y', 'current and call': 'DEP_CURRENT_CALL', 'saving': 'DEP_SAVING',
    }
    if low in mat:
        d['semantic'] = mat[low]
        return d
    if low in ('total lc', 'total fc', 'total'):
        d.update(semantic='TOTAL' + ('_' + low.split()[1].upper() if ' ' in low else ''), subtotal=True)
        return d
    if table == '011':
        cls = {'good low': 'GOOD', 'spec ment': 'WATCH', 'substand': 'SUBSTANDARD', 'doubtful': 'DOUBTFUL', 'bad debt': 'BAD'}
        for k, v in cls.items():
            if low.startswith(k):
                d['semantic'] = v + ('_INDIRECT' if low.endswith('indir') else '_DIRECT')
                return d
    if table in ('044', '045'):
        sec = {'non bank fin inst': 'NBFI', 'govt inst': 'GOV', 'semi govt inst': 'SEMI_GOV', 'priv sect corp': 'PRIVATE', 'personal': 'PERSONAL'}
        for k, v in sec.items():
            if low.startswith(k):
                d['semantic'] = f'SECTOR_{v}_{cur}'
                return d
    d['semantic'] = re.sub(r'\W+', '_', low).strip('_').upper()
    if re.search(r'amor|depre|prov|neg|loss', low):
        d['sign_note'] = 'Contra/negative measure: raw sign preserved; presentation rule applied once downstream'
    return d


def build_catalogue(path, catalogue_path):
    """Create the measure catalogue from a BO workbook's validated headers (kept if it already exists)."""
    catalogue_path = Path(catalogue_path)
    if catalogue_path.exists():
        return json.loads(catalogue_path.read_text(encoding='utf-8'))
    out = {'schema_version': 1, 'version': 1, 'source': 'Generated from BO headers; owner-editable',
           'tables': {}}
    for sheet, part in ooxml.sheets(path):
        table, title, header_row, headers = _headers(path, sheet, part)
        if table in SPECIAL_TABLES:
            out['tables'][table] = {'sheet': sheet, 'title': title, 'special_schema': list(SPECIAL_TABLES[table]), 'measures': {}}
            continue
        measures = {}
        for col, h in headers.items():
            if h in ('Table Code',) + ITEM_HEADERS + DESC_HEADERS + DATE_HEADERS:
                continue
            measures[norm(h)] = classify(table, h)
        out['tables'][table] = {'sheet': sheet, 'title': title, 'measures': measures}
    catalogue_path.parent.mkdir(parents=True, exist_ok=True)
    catalogue_path.write_text(json.dumps(out, indent=1) + '\n', encoding='utf-8')
    return out


def _headers(path, sheet, part):
    m = re.fullmatch(r'Table-(\d{3})', sheet)
    if not m:
        raise BOImportError(f'Unexpected BO sheet name {sheet!r}')
    title = ''
    for row_no, cells in ooxml.raw_rows(path, part):
        vals = {k: norm(v[0]) for k, v in cells.items()}
        if 'Table Code' in vals.values():
            return m.group(1), title, row_no, vals
        if vals and not title:
            title = next(iter(vals.values()))
        if row_no > 20:
            break
    raise BOImportError(f'{sheet}: header row with Table Code not found')


def import_bo(c, path, catalogue, ref_version=None):
    digest, existing = register_source(c, path, DATASET, IMPORT_VERSION)
    ref_version = ref_version or 'BO_' + digest[:12]
    if existing and c.execute('SELECT 1 FROM ref_versions WHERE ref_version=?', (ref_version,)).fetchone():
        return {'ref_version': ref_version, 'source_sha256': digest, 'already_imported': True,
                **json.loads(c.execute('SELECT summary FROM sources WHERE source_sha256=?', (digest,)).fetchone()[0])}
    try:
        summary = _import(c, path, catalogue, ref_version, digest)
    except Exception:
        c.rollback()
        raise
    c.execute('UPDATE sources SET summary=? WHERE source_sha256=?', (json.dumps(summary), digest))
    c.commit()
    return {'ref_version': ref_version, 'source_sha256': digest, 'already_imported': False, **summary}


def _import(c, path, catalogue, ref_version, digest):
    package = ooxml.inspect_package(path)
    dates = set()
    standard = special = cells_n = 0
    tables = []
    for sheet, part in ooxml.sheets(path):
        table, title, header_row, headers = _headers(path, sheet, part)
        tables.append(table)
        by_name = {}
        for col, h in headers.items():
            if h in by_name:
                raise BOImportError(f'{sheet}: duplicate header {h!r}')
            by_name[h] = col
        c.execute('INSERT INTO bo_headers VALUES(?,?,?,?,?,?)', (ref_version, table, sheet, title, header_row, json.dumps(headers)))
        date_col = next((by_name[h] for h in DATE_HEADERS if h in by_name), None)
        if date_col is None:
            raise BOImportError(f'{sheet}: no Report Date / Rep Date column')
        if table in SPECIAL_TABLES:
            for name in SPECIAL_TABLES[table]:
                if name not in by_name:
                    raise BOImportError(f'{sheet}: special schema field {name!r} missing')
            for row_no, cells in ooxml.raw_rows(path, part):
                if row_no <= header_row or not cells:
                    continue
                rd = _date(cells, date_col, sheet, row_no)
                dates.add(rd)
                fields = {n: {'cell': by_name[n] + str(row_no), 'raw': cells.get(by_name[n], (None,))[0]} for n in SPECIAL_TABLES[table]}
                c.execute('INSERT INTO bo_special VALUES(?,?,?,?,?,?)', (ref_version, table, sheet, row_no, rd, json.dumps(fields)))
                special += 1
            continue
        item_col = by_name.get('Qcb Item Code')
        desc_col = next((by_name[h] for h in DESC_HEADERS if h in by_name), None)
        if not item_col or not desc_col:
            raise BOImportError(f'{sheet}: item code / description header missing')
        measures = catalogue['tables'].get(table, {}).get('measures', {})
        meas_cols = {h: col for h, col in by_name.items() if h not in ('Table Code', 'Qcb Item Code', *DESC_HEADERS, *DATE_HEADERS)}
        unknown = [h for h in meas_cols if h not in measures]
        if unknown:
            raise BOImportError(f'{sheet}: headers not in measure catalogue: {unknown}')
        for row_no, cells in ooxml.raw_rows(path, part):
            if row_no <= header_row or not cells:
                continue
            tc = cells.get(by_name['Table Code'], ('',))[0].strip()
            if tc != table:
                raise BOImportError(f'{sheet}!{by_name["Table Code"]}{row_no}: table code {tc!r} does not match {table!r} (leading zeroes are required)')
            item = cells.get(item_col, ('',))[0].strip()
            if not item:
                raise BOImportError(f'{sheet} row {row_no}: blank Qcb Item Code')
            rd = _date(cells, date_col, sheet, row_no)
            dates.add(rd)
            if c.execute('SELECT 1 FROM bo_items WHERE ref_version=? AND table_code=? AND item_code=? AND report_date=?', (ref_version, table, item, rd)).fetchone():
                raise BOImportError(f'Duplicate BO key table {table} item {item} date {rd} ({sheet} row {row_no})')
            c.execute('INSERT INTO bo_items VALUES(?,?,?,?,?,?,?,?,?)',
                      (ref_version, table, item, cells.get(desc_col, ('',))[0].strip(), None, None, sheet, row_no, rd))
            standard += 1
            for h, col in meas_cols.items():
                m = measures[h]
                raw = cells.get(col, (None,))[0]
                try:
                    val = to_micro(raw)
                except ValueError as exc:
                    raise BOImportError(f'{sheet}!{col}{row_no}: {exc}') from exc
                if m['kind'] in ('money', 'count', 'notional', 'fair_value_positive', 'fair_value_negative', 'rate') and raw is not None:
                    pass
                c.execute('INSERT INTO bo_cells VALUES(?,?,?,?,?,?,?,?,?,?,?,?)',
                          (ref_version, table, item, rd, h, h, m['semantic'], m['kind'], m['unit'], f'{sheet}!{col}{row_no}', raw, val))
                cells_n += 1
    _hierarchy(c, ref_version)
    if len(dates) != 1:
        raise BOImportError(f'BO workbook mixes report dates: {sorted(dates)}')
    report_date = dates.pop()
    c.execute('INSERT INTO ref_versions VALUES(?,?,?,?,?,?,?,?)',
              (ref_version, DATASET, digest, Path(path).name, report_date, 'QAR thousands (assumed; counts and rates separate)', now(),
               'Cash 417,680 LC / 76,581 FC agree with the earlier live QAR-thousand report; unit not stated in BO headers'))
    return {'dataset': DATASET, 'ref_version': ref_version, 'sheets': len(tables), 'tables': tables,
            'standard_item_rows': standard, 'special_records': special, 'reference_cells': cells_n,
            'report_date': report_date, 'package': package}


def _date(cells, col, sheet, row_no):
    raw = cells.get(col, (None,))[0]
    d = ooxml.excel_serial_date(raw)
    if d is None:
        raise BOImportError(f'{sheet}!{col}{row_no}: report date {raw!r} is not a valid date')
    return d


def _hierarchy(c, ref_version):
    """Parent = longest other code in the same table that prefixes this one (code identity, not row order)."""
    items = c.execute('SELECT table_code, item_code, report_date FROM bo_items WHERE ref_version=?', (ref_version,)).fetchall()
    by_table = {}
    for t, i, d in items:
        by_table.setdefault((t, d), []).append(i)
    for (t, d), codes in by_table.items():
        s = set(codes)
        parents = {code: next((code[:k] for k in range(len(code) - 1, 0, -1) if code[:k] in s), None) for code in codes}
        for code in codes:
            parent = parents[code]
            depth, p = 0, parent
            while p:
                depth += 1
                p = parents[p]
            c.execute('UPDATE bo_items SET parent_code=?, depth=? WHERE ref_version=? AND table_code=? AND item_code=? AND report_date=?',
                      (parent, depth, ref_version, t, code, d))


def reference_values(c, ref_version):
    """{(table, item, measure): micro} for comparison only."""
    return {(t, i, m): v for t, i, m, v in c.execute(
        'SELECT table_code, item_code, measure, value_micro FROM bo_cells WHERE ref_version=?', (ref_version,))}


def import_live_reference(c, template_path, ref_version='LIVE_NBS01_2026-09'):
    """The earlier live NBS report (template layout), stored as a separate named reference version."""
    digest, _ = register_source(c, template_path, 'LIVE_NBS_REFERENCE', 'live-ref-1')
    if c.execute('SELECT 1 FROM ref_versions WHERE ref_version=?', (ref_version,)).fetchone():
        return {'ref_version': ref_version, 'already_imported': True}
    n = 0
    part = ooxml.sheets(template_path)[0][1]
    for row_no, cells in ooxml.raw_rows(template_path, part):
        label = cells.get('A', ('',))[0]
        for col, (raw, kind) in cells.items():
            if col == 'A' or kind == 's':
                continue
            try:
                v = to_micro(raw)
            except ValueError:
                continue
            c.execute('INSERT INTO live_cells VALUES(?,?,?,?,?,?)', (ref_version, row_no, col, raw, v, label))
            n += 1
    c.execute('INSERT INTO ref_versions VALUES(?,?,?,?,?,?,?,?)', (ref_version, 'LIVE_NBS_REFERENCE', digest, Path(template_path).name,
              '2026-09-30', 'QAR thousands', now(), 'Earlier live NBS01 report; template-row layout'))
    c.execute("UPDATE sources SET summary=? WHERE source_sha256=?", (json.dumps({'ref_version': ref_version, 'numeric_cells': n}), digest))
    c.commit()
    return {'ref_version': ref_version, 'numeric_cells': n}
