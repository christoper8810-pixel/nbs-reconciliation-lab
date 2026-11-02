"""Independent spot checks and arithmetic controls for the NBS evidence review."""
import csv
import json
from collections import Counter
from decimal import Decimal, getcontext
from pathlib import Path
import re

import openpyxl

from audit_rebuild_sources import OUT, ROOT, DOWNLOADS, digest

getcontext().prec = 50
checks = []


def check(name, condition):
    checks.append({'check': name, 'passed': bool(condition)})
    if not condition:
        raise AssertionError(name)


category = json.loads((OUT / 'category_profile.json').read_text())
bo = json.loads((OUT / 'bo_profile.json').read_text())
relationships = json.loads((OUT / 'bo_relationship_findings.json').read_text())
manifest = json.loads((OUT / 'audit_manifest.json').read_text())
check('All new original file hashes unchanged', all(digest(Path(x['path'])) == x['sha256'] for x in manifest['sources']))
check('Duplicate category filename is identical', category['duplicate_file_identical'])
check('Category count from independent worksheet dimension', openpyxl.load_workbook(category['path'], read_only=True, data_only=True).active.max_row == category['counts']['rows'] + 1 == 81723)
check('Category date domain totals reconcile', all(sum(v.values()) == 81722 for v in category['dates'].values()))
check('All booking and processing dates are October 1', category['dates']['BOOKING.DATE'] == category['dates']['PROCESSING.DATE'] == {'20261001': 81722})
check('Value date range checked', min(x for x in category['dates']['VALUE.DATE'] if x != '<blank>') == '20111117' and max(x for x in category['dates']['VALUE.DATE'] if x != '<blank>') == '20261001')
check('Positive negative counts reconcile', category['counts']['positive_rows'] + category['counts']['negative_rows'] == 81722)
check('Event counts reconcile', sum(x['rows'] for x in category['events']) == 81722)
check('Event amounts reconcile exactly to raw decimal total', sum((Decimal(x['net_lcy']) for x in category['events']), Decimal(0)) == Decimal(category['amount_lcy_net']))
check('Category subtotal counts reconcile', sum(x['rows'] for x in category['pl_categories']) == 81722 and len(category['pl_categories']) == 237)
check('Category subtotal amounts reconcile exactly', sum((Decimal(x['net_lcy']) for x in category['pl_categories']), Decimal(0)) == Decimal(category['amount_lcy_net']))
check('Repeat ID excess count reconciles', category['duplicate_id_extra_rows'] == 81722 - category['id_unique'] == 80011)
with (OUT / 'category_repeated_export_groups.csv').open(encoding='utf-8-sig') as f:
    dup = list(csv.DictReader(f))
check('Repeated-export group excess counts reconcile', sum(int(x['excess_occurrences']) for x in dup) == category['identical_extra_rows'] == 24515)
check('Repeated-export amount sensitivity reconciles', sum((Decimal(x['excess_net_lcy']) for x in dup), Decimal(0)) == Decimal(category['identical_extra_rows_net_lcy']))
check('Raw rows retained rather than deduplicated', sum(len(x['source_rows'].split('|')) - 1 for x in dup) == 24515)
check('BO table catalogue has all 50 tables', bo['sheets'] == 50 and {x['sheet'] for x in bo['table_profiles']} == {f'Table-{x:03d}' for x in list(range(1, 46)) + [100, 200, 300, 400, 500]})
check('BO standard item dates reconcile', bo['data_rows'] == 1648 and bo['report_dates'] == {'2026-09-30': 1648})
check('BO item keys unique', bo['duplicate_table_item_date_keys'] == 0)
check('BO output is a value-only reference', sum(x['formula_cells'] for x in bo['table_profiles']) == 0)

bw = openpyxl.load_workbook(DOWNLOADS / 'BO_QCB_NBS_Report.xlsx', read_only=True, data_only=True)
cw = openpyxl.load_workbook(DOWNLOADS / 'Mock3_UAT3 Categ Entry Extract (1).xlsx', read_only=True, data_only=True)
check('Independent read confirms unheaded U and first event', cw.active['T1'].value == 'SOFT.ACCTNG.DTLS' and cw.active['U1'].value is None and cw.active['U2'].value == 'SDB-CHARGE' and cw.active['Q2'].value == 20261001)
check('Independent read confirms Table 20 record', list(bw['Table-020'].iter_rows(min_row=5, max_row=5, min_col=2, max_col=6, values_only=True))[0][:4] == ('020', 0, 0, 0))
check('Independent read confirms header variations', bw['Table-009']['M4'].value == 'Uae Fc' and bw['Table-009']['N4'].value == 'Uae Lc' and bw['Table-022']['M4'].value == 'Rep Date' and bw['Table-031']['D4'].value == 'Qcb Item Desc')
check('Independent read confirms gross versus net control', bw['Table-100']['E50'].value == 896109 and bw['Table-018']['E5'].value + bw['Table-018']['E6'].value + bw['Table-018']['E7'].value == 896109 and bw['Table-018']['F5'].value + bw['Table-018']['F6'].value + bw['Table-018']['F7'].value == -603699 and 896109 - 603699 == 292410)
asset_total = sum(Decimal(str(c.value)) for c in list(bw['Table-100'].iter_rows(min_row=5, max_row=5, min_col=5, max_col=8))[0])
liab_total = sum(Decimal(str(c.value)) for c in list(bw['Table-200'].iter_rows(min_row=5, max_row=5, min_col=5, max_col=8))[0])
check('Independent root total difference', asset_total - liab_total == Decimal('5747560'))
bw.close()
cw.close()
with (OUT / 'bo_to_current_mapping_candidates.csv').open(encoding='utf-8-sig') as f:
    crosswalk = list(csv.DictReader(f))
check('Crosswalk covers all standard BO rows without activation', len(crosswalk) == 1648 and Counter(x['status'] for x in crosswalk) == {'UNREVIEWED_EXACT_PATH_CANDIDATE': 1037, 'UNRESOLVED': 611} and all(not x['approval'] for x in crosswalk))
with (OUT / 'balance_sheet_output_lines.csv').open(encoding='utf-8-sig') as f:
    sql_outputs = list(csv.DictReader(f))
check('SQL final line and literal zero counts', len(sql_outputs) == 37 and sum(x['value_mode'] == 'LITERAL_ZERO' for x in sql_outputs) == 16)
used = {int(n) for x in sql_outputs for n in x['group_numbers'].split(',') if n.strip()}
check('SQL omitted groups exposed', set(range(1, 39)) - used == {17, 38})
source_query = (OUT / 'bs_source_extracted.sql').read_text(encoding='utf-8')
check('SQL parameter and original field semantics retained', '{?DBdate}' in source_query and 'Equiv_cur_bal_Begin' in source_query and '\t' in source_query and 'Bo..Tbl_GL_Daily_Bo' in source_query)

old = json.loads((ROOT / 'exports/NBS_generated_review.json').read_text())
row770 = next(r for r in old['rows'] if r['row'] == 770)
check('Current maturity defect confirmed in saved result', 'J' in row770['values'] and 'M' not in row770['values'] and abs(row770['values']['J'] - 2110791.70457) < 0.00001)
ow = openpyxl.load_workbook(ROOT / 'data/bank_sources/NBS01 Sep 2026 English.xlsx', read_only=True, data_only=True)
header = list(ow.active.iter_rows(min_row=769, max_row=769, min_col=1, max_col=13, values_only=True))[0]
check('Current maturity headings independently confirm wrong columns', header[1] == 'Without Maturity' and header[9] == '>5 Years To 10 Years' and header[12] == 'Total Amount')
ow.close()
confirmation_path = OUT / 'reporting_basis_owner_confirmation.json'
if confirmation_path.exists():
    confirmation = json.loads(confirmation_path.read_text())
    check('Owner-confirmed September basis preserves original October dates and exact source scope',
          confirmation['status'] == 'OWNER_CONFIRMED'
          and confirmation['source']['sha256'] == category['sha256']
          and confirmation['raw_booking_date'] == '2026-10-01'
          and confirmation['effective_reporting_date'] == '2026-09-30'
          and confirmation['implementation']['preserve_raw_dates']
          and not confirmation['implementation']['automatically_apply_to_unrelated_uploads'])
validation = {'review_date': '2026-10-17', 'status': 'Passed evidence-review checks', 'checks_passed': len(checks), 'checks': checks, 'scope': 'Inspection evidence and arithmetic validation only. No production code fix or full NBS accounting reconciliation is claimed.', 'source_sql_executed': False, 'original_inputs_modified': False}
(OUT / 'review_validation.json').write_text(json.dumps(validation, indent=2), encoding='utf-8')
print(json.dumps({k: v for k, v in validation.items() if k != 'checks'}, indent=2))
