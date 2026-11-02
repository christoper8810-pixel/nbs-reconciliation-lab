"""Read-only examination of supplied NBS rebuild evidence; never runs source SQL."""
from __future__ import annotations

import csv
import hashlib
import json
import re
import sqlite3
from collections import Counter, defaultdict
from datetime import datetime, timedelta
from decimal import Decimal, InvalidOperation, getcontext
from pathlib import Path
from zipfile import ZipFile

from lxml import etree as ET

ROOT = Path(__file__).resolve().parent
OUT = ROOT / 'exports' / 'rebuild_review_20261017'
DOWNLOADS = Path(r'C:\Users\Test\Downloads')
MAIN = '{http://schemas.openxmlformats.org/spreadsheetml/2006/main}'
WORD = '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}'
REL = '{http://schemas.openxmlformats.org/officeDocument/2006/relationships}'
getcontext().prec = 50


def digest(path):
    h = hashlib.sha256()
    with path.open('rb') as f:
        for block in iter(lambda: f.read(1024 * 1024), b''):
            h.update(block)
    return h.hexdigest()


def sheets(path):
    with ZipFile(path) as z:
        targets = {x.get('Id'): x.get('Target') for x in ET.fromstring(z.read('xl/_rels/workbook.xml.rels'))}
        wb = ET.fromstring(z.read('xl/workbook.xml'))
        return [(s.get('name'), 'xl/' + targets[s.get(REL + 'id')].lstrip('/') if not targets[s.get(REL + 'id')].startswith('/') else targets[s.get(REL + 'id')][1:]) for s in wb.find(MAIN + 'sheets')]


def rows(path, sheet):
    """Return cached cells as exact strings, retaining Excel coordinates and type."""
    with ZipFile(path) as z:
        strings = []
        if 'xl/sharedStrings.xml' in z.namelist():
            with z.open('xl/sharedStrings.xml') as f:
                for _, el in ET.iterparse(f, events=('end',), tag=MAIN + 'si'):
                    strings.append(''.join(t.text or '' for t in el.iter(MAIN + 't')))
                    el.clear()
                    while el.getprevious() is not None:
                        del el.getparent()[0]
        with z.open(sheet) as f:
            for _, el in ET.iterparse(f, events=('end',), tag=MAIN + 'row'):
                data = {}
                for c in el:
                    if c.tag != MAIN + 'c':
                        continue
                    typ = c.get('t', 'n')
                    v = c.find(MAIN + 'v')
                    if typ == 'inlineStr':
                        text = ''.join(t.text or '' for t in c.iter(MAIN + 't'))
                    elif v is None or v.text is None:
                        continue
                    elif typ == 's':
                        text = strings[int(v.text)]
                    else:
                        text = v.text
                    data[re.sub(r'\d', '', c.get('r'))] = text
                yield int(el.get('r')), data
                el.clear()
                while el.getprevious() is not None:
                    del el.getparent()[0]


def dec(text):
    try:
        return Decimal(text.replace(',', ''))
    except (InvalidOperation, AttributeError):
        return None


def save_json(name, data):
    (OUT / name).write_text(json.dumps(data, indent=2, ensure_ascii=False, default=str), encoding='utf-8')


def save_csv(name, data):
    if not data:
        return
    with (OUT / name).open('w', encoding='utf-8-sig', newline='') as f:
        w = csv.DictWriter(f, fieldnames=list(data[0]))
        w.writeheader()
        w.writerows(data)


def extract_sql():
    path = DOWNLOADS / 'bs.docx'
    with ZipFile(path) as z:
        root = ET.fromstring(z.read('word/document.xml'))
        lines = []
        for p in root.iter(WORD + 'p'):
            parts = []
            for node in p.iter():
                if node.tag == WORD + 't':
                    parts.append(node.text or '')
                elif node.tag == WORD + 'tab':
                    parts.append('\t')
                elif node.tag in (WORD + 'br', WORD + 'cr'):
                    parts.append('\n')
            lines.append(''.join(parts))
        text = '\n'.join(lines)
    (OUT / 'bs_source_extracted.sql').write_text(text, encoding='utf-8')
    cases = re.findall(r'When\s+(.*?)\s+Then\s+\x27([^\x27]+)\x27', text, re.I | re.S)
    save_csv('balance_sheet_case_rules.csv', [{'case_order': i + 1, 'condition_as_supplied': re.sub(r'\s+', ' ', c), 'label': label} for i, (c, label) in enumerate(cases)])
    outputs = []
    for match in re.finditer(r"Select\s+(\d+)\s+As\s+No,\s*'([^']*)'\s+Description,\s*(.*?)(?=\nUnion|\nOrder By No)", text, re.I | re.S):
        groups = re.search(r'Where\s+Sr\s+In\s*\(([^)]+)\)', match[3], re.I)
        outputs.append({'output_number': int(match[1]), 'description': match[2], 'group_numbers': groups[1] if groups else '', 'value_mode': 'GROUP_SUM' if groups else 'LITERAL_ZERO'})
    save_csv('balance_sheet_output_lines.csv', outputs)
    return {'path': str(path), 'sha256': digest(path), 'characters': len(text), 'case_rules': len(cases), 'sql_executed': False}


def profile_categories():
    path = DOWNLOADS / 'Mock3_UAT3 Categ Entry Extract (1).xlsx'
    duplicate_path = DOWNLOADS / 'Mock3_UAT3 Categ Entry Extract.xlsx'
    names = sheets(path)
    dates = {k: Counter() for k in ('I', 'M', 'Q', 'S')}
    domains = {k: Counter() for k in ('B', 'D', 'E', 'H', 'J', 'K', 'P', 'T', 'U', 'V')}
    width = Counter()
    missing = Counter()
    signatures = Counter()
    ids = Counter()
    id_versions = defaultdict(set)
    reference_counts = Counter()
    signature_amounts = {}
    signature_rows = defaultdict(list)
    sample_by_id = defaultdict(list)
    events = defaultdict(lambda: {'rows': 0, 'net_lcy': Decimal(0), 'references': set()})
    key_lengths = Counter()
    key_mismatch = Counter()
    totals = defaultdict(Decimal)
    category_totals = defaultdict(lambda: {'rows': 0, 'net_lcy': Decimal(0), 'positive_lcy': Decimal(0), 'negative_lcy': Decimal(0)})
    invalid_amounts = []
    overflow = []
    extrema = [None, None]
    counts = Counter()
    with sqlite3.connect((ROOT / 'data/bank_20260930.sqlite').as_uri() + '?mode=ro', uri=True) as c:
        ecb_accounts = {r[0] for r in c.execute("select distinct account from records where source='ECB'")}
        ecb_pairs = {(r[0], r[1]) for r in c.execute("select account,currency from unique_records where source='ECB'")}
    matched_accounts = set()
    for rownum, r in rows(path, names[0][1]):
        if rownum == 1:
            header = r
            continue
        if not r:
            continue
        counts['rows'] += 1
        width[str(max(r, key=lambda v: (len(v), v)))] += 1
        for col in header:
            if col not in r or r[col] == '':
                missing[header[col]] += 1
        for col in dates:
            dates[col][r.get(col, '<blank>')] += 1
        for col in domains:
            domains[col][r.get(col, '<blank>')] += 1
        extra = {k: v for k, v in r.items() if k not in header}
        if extra and len(overflow) < 8:
            overflow.append({'row': rownum, 'header_last': 'T', 'extra': extra})
        ids[r.get('A', '')] += 1
        signature = hashlib.sha256(json.dumps(r, sort_keys=True).encode()).hexdigest()
        signatures[signature] += 1
        signature_rows[signature].append(rownum)
        if len(sample_by_id[r.get('A', '')]) < 3:
            sample_by_id[r.get('A', '')].append({'row': rownum, 'amount_lcy': r.get('C'), 'pl_category': r.get('E'), 'value_date': r.get('I'), 'soft_accounting_details': r.get('T'), 'unheaded_u': r.get('U')})
        id_versions[r.get('A', '')].add(signature)
        ref = r.get('L', '')
        reference_counts[ref] += 1
        if ref in ecb_accounts:
            counts['ecb_account_reference_matched_rows'] += 1
            matched_accounts.add(ref)
        if (ref, r.get('J')) in ecb_pairs:
            counts['ecb_account_currency_reference_matched_rows'] += 1
        amount = dec(r.get('C'))
        if amount is None:
            invalid_amounts.append(rownum)
            continue
        if not amount.is_finite():
            invalid_amounts.append(rownum)
            continue
        signature_amounts[signature] = amount
        event = events[(r.get('P', ''), r.get('T', ''), r.get('U', ''))]
        event['rows'] += 1
        event['net_lcy'] += amount
        if ref:
            event['references'].add(ref)
        counts['positive_rows' if amount > 0 else 'negative_rows' if amount < 0 else 'zero_rows'] += 1
        totals[r.get('J', '<blank>')] += amount
        cat = category_totals[r.get('E', '<blank>')]
        cat['rows'] += 1
        cat['net_lcy'] += amount
        cat['positive_lcy' if amount >= 0 else 'negative_lcy'] += amount
        extrema[0] = amount if extrema[0] is None else min(extrema[0], amount)
        extrema[1] = amount if extrema[1] is None else max(extrema[1], amount)
        for col in ('I', 'M', 'Q', 'S'):
            val = r.get(col, '')
            if re.fullmatch(r'\d{8}', val) and val <= '20260930':
                counts['on_or_before_sep30_' + header[col]] += 1
        if r.get('I') != r.get('Q'):
            counts['value_booking_date_differ'] += 1
        parts = r.get('R', '').split('.')
        key_lengths[str(len(parts))] += 1
        for idx, col in ((1, 'E'), (2, 'J'), (3, 'H'), (4, 'G')):
            if len(parts) <= idx or parts[idx] != r.get(col, ''):
                key_mismatch[header[col]] += 1
        if parts[-1] != r.get('B', ''):
            key_mismatch['COMPANY.CODE'] += 1
        if parts[0] != 'PL':
            key_mismatch['prefix_not_PL'] += 1
    details = [{
        'pl_category': cat, 'rows': v['rows'], 'net_lcy': str(v['net_lcy']),
        'positive_lcy': str(v['positive_lcy']), 'negative_lcy': str(v['negative_lcy'])
    } for cat, v in sorted(category_totals.items())]
    save_csv('category_totals.csv', details)
    save_csv('category_repeated_export_groups.csv', [
        {'raw_value_fingerprint': key, 'occurrences': count, 'excess_occurrences': count - 1,
         'source_rows': '|'.join(map(str, signature_rows[key])), 'amount_lcy_each': str(signature_amounts[key]),
         'excess_net_lcy': str((count - 1) * signature_amounts[key]),
         'treatment': 'UNRESOLVED Do not delete solely from identical exported fields'}
        for key, count in signatures.items() if count > 1
    ])
    result = {
        'path': str(path), 'sha256': digest(path), 'bytes': path.stat().st_size,
        'duplicate_file': str(duplicate_path), 'duplicate_file_identical': digest(path) == digest(duplicate_path),
        'sheets': names, 'headers': header, 'counts': dict(counts), 'missing_by_header': dict(missing),
        'dates': {header[k]: dict(v) for k, v in dates.items()},
        'domains': {header.get(k, 'UNHEADED_' + k): dict(v) for k, v in domains.items()},
        'last_populated_column_counts': dict(width), 'extra_column_examples': overflow,
        'amount_lcy_net': str(sum(totals.values(), Decimal(0))),
        'amount_lcy_by_original_currency': dict(totals), 'amount_lcy_min_max': extrema,
        'invalid_amount_rows': invalid_amounts, 'id_unique': len(ids),
        'duplicate_id_keys': sum(v > 1 for v in ids.values()),
        'duplicate_id_extra_rows': sum(v - 1 for v in ids.values()),
        'conflicting_id_keys': sum(len(v) > 1 for v in id_versions.values()),
        'identical_extra_rows': sum(v - 1 for v in signatures.values()),
        'identical_extra_rows_net_lcy': str(sum(((n - 1) * signature_amounts[k] for k, n in signatures.items()), Decimal(0))),
        'identical_extra_rows_absolute_lcy': str(sum(((n - 1) * abs(signature_amounts[k]) for k, n in signatures.items()), Decimal(0))),
        'repeated_id_examples': [{'id': key, 'occurrences': n, 'first_three_rows': sample_by_id[key]} for key, n in ids.most_common(4)],
        'our_reference_unique': len(reference_counts),
        'our_reference_repeated_keys': sum(v > 1 for v in reference_counts.values()),
        'our_reference_largest_multiplicity': max(reference_counts.values()),
        'ecb_reference_matched_distinct_accounts': len(matched_accounts),
        'consol_key_lengths': dict(key_lengths), 'consol_key_header_conflicts': dict(key_mismatch),
        'pl_categories': details,
        'events': [{'system': key[0], 'soft_accounting_details': key[1], 'unheaded_u': key[2], 'rows': val['rows'], 'net_lcy': str(val['net_lcy']), 'distinct_nonblank_references': len(val['references'])} for key, val in events.items()],
    }
    save_json('category_profile.json', result)
    return result


def profile_bo():
    path = DOWNLOADS / 'BO_QCB_NBS_Report.xlsx'
    all_rows = []
    profiles = []
    problems = []
    row_keys = Counter()
    date_values = Counter()
    for sheet, part in sheets(path):
        rr = list(rows(path, part))
        hdr = next((r for n, r in rr if any(v.strip().lower() == 'qcb item code' for v in r.values())), {})
        title = ' '.join(v for n, r in rr if n == 2 for v in r.values())
        keys = {v.strip().lower(): k for k, v in hdr.items()}
        itemcol, tablecol = keys.get('qcb item code'), keys.get('table code')
        desccol = keys.get('qcb item description', keys.get('qcb item desc'))
        datecol = keys.get('report date', keys.get('rep date'))
        measure_cols = {k: v.strip() for k, v in hdr.items() if k not in (itemcol, tablecol, desccol, datecol)}
        valid = []
        for n, r in rr:
            if n <= 4 or not r.get(itemcol):
                continue
            item = r[itemcol]
            if not re.fullmatch(r'\d+-\d{3}-\d+', item):
                problems.append({'sheet': sheet, 'row': n, 'problem': 'NONSTANDARD_ITEM_CODE', 'value': item})
                continue
            val = r.get(datecol, '')
            dt = (datetime(1899, 12, 30) + timedelta(days=float(val))).date().isoformat() if dec(val) is not None else val
            date_values[dt] += 1
            table = r.get(tablecol, '')
            row_keys[(table, item, dt)] += 1
            if table != item.split('-')[1]:
                problems.append({'sheet': sheet, 'row': n, 'problem': 'TABLE_CODE_CONFLICT', 'value': item})
            values = {measure_cols[k]: str(dec(r[k])) if dec(r.get(k)) is not None else r.get(k) for k in measure_cols}
            valid.append({'sheet': sheet, 'row': n, 'table': table, 'item_code': item, 'description': r.get(desccol), 'report_date': dt, 'measures': values, 'source_cells': {measure_cols[k]: f'{k}{n}' for k in measure_cols}})
        with ZipFile(path) as z:
            root = ET.fromstring(z.read(part))
            formulas = len(list(root.iter(MAIN + 'f')))
            errors = [c.get('r') for c in root.iter(MAIN + 'c') if c.get('t') == 'e']
        profiles.append({'sheet': sheet, 'title': title, 'rows': len(valid), 'headers': hdr, 'measures': measure_cols, 'formula_cells': formulas, 'error_cells': errors})
        all_rows.extend(valid)
    save_json('bo_normalized_rows.json', all_rows)
    save_csv('bo_table_inventory.csv', [{'sheet': x['sheet'], 'title': x['title'], 'data_rows': x['rows'], 'measure_count': len(x['measures']), 'formula_cells': x['formula_cells']} for x in profiles])
    flat = []
    for r in all_rows:
        for measure, value in r['measures'].items():
            flat.append({k: r[k] for k in ('sheet', 'row', 'table', 'item_code', 'description', 'report_date')} | {'measure': measure, 'value': value, 'cell': r['source_cells'][measure]})
    save_csv('bo_reference_cells.csv', flat)
    result = {'path': str(path), 'sha256': digest(path), 'sheets': len(profiles), 'data_rows': len(all_rows), 'report_dates': dict(date_values), 'duplicate_table_item_date_keys': sum(v > 1 for v in row_keys.values()), 'duplicate_key_excess_rows': sum(v - 1 for v in row_keys.values()), 'problems': problems, 'table_profiles': profiles}
    save_json('bo_profile.json', result)
    return result


if __name__ == '__main__':
    OUT.mkdir(exist_ok=True)
    sql = extract_sql()
    bo = profile_bo()
    print('SQL', sql, flush=True)
    print('BO', {k: v for k, v in bo.items() if k != 'table_profiles'}, flush=True)
    category = profile_categories()
    print('CATEGORY', {k: category[k] for k in ('counts', 'last_populated_column_counts', 'amount_lcy_net', 'id_unique', 'duplicate_id_keys', 'conflicting_id_keys', 'our_reference_unique', 'our_reference_largest_multiplicity', 'ecb_reference_matched_distinct_accounts', 'consol_key_header_conflicts')}, flush=True)
    save_json('audit_manifest.json', {'review_date': '2026-10-17', 'sources': [sql, {k: bo[k] for k in ('path', 'sha256')}, {k: category[k] for k in ('path', 'sha256')}], 'method': 'Read cached OOXML cells and document text only. Source SQL was never executed. Existing bank database opened read-only. Original files unchanged.'})
