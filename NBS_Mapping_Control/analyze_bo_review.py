"""Diagnostic comparisons, never an approved automatic mapping."""
from __future__ import annotations

import json
import re
from collections import Counter, defaultdict
from decimal import Decimal
from pathlib import Path
from audit_rebuild_sources import OUT, ROOT, DOWNLOADS, rows, sheets, save_csv, save_json


def clean(s):
    s = re.sub(r'^\.*\s*\d+\s*', '', s).strip().lower()
    return re.sub(r'[^a-z0-9]+', '', s)


def main():
    bo = json.loads((OUT / 'bo_normalized_rows.json').read_text())
    old = json.loads((ROOT / 'exports/NBS_generated_review.json').read_text())['rows']
    bytable = defaultdict(list)
    for r in bo:
        bytable[r['table']].append(r)
    oldtable = defaultdict(list)
    for r in old:
        tab = str(r['table']).zfill(3) if r['table'] is not None else {'Assets': '100', 'Liabilities': '200', 'Contra Items': '300', 'Income': '400', 'Expenses': '500'}[r['base']]
        oldtable[tab].append(r)
    proposals = []
    comparisons = []
    for table, records in bytable.items():
        idx = {r['item_code'].split('-')[-1]: r for r in records}
        for r in records:
            suffix = r['item_code'].split('-')[-1]
            ancestors = sorted((k for k in idx if suffix.startswith(k) and len(k) < len(suffix)), key=len)
            # Base report root captions are not part of the old row hierarchy.
            parents = [idx[k]['description'] for k in ancestors if not (table in ('100', '200', '300', '400', '500') and len(k) == 1)]
            bp = [clean(s) for s in parents + [r['description']]]
            candidates = []
            for x in oldtable[table]:
                op = [clean(s) for s in x['path'].split(' > ') if not s.lower().startswith('dukhan bank')]
                if op == bp:
                    candidates.append(x)
            proposals.append({'table': table, 'bo_sheet': r['sheet'], 'bo_row': r['row'], 'bo_item_code': r['item_code'], 'bo_description': r['description'], 'bo_hierarchy': ' > '.join(parents + [r['description']]), 'candidate_count': len(candidates), 'candidate_ids': '|'.join(x['id'] for x in candidates), 'candidate_old_rows': '|'.join(str(x['row']) for x in candidates), 'status': 'UNREVIEWED_EXACT_PATH_CANDIDATE' if len(candidates) == 1 else 'UNRESOLVED', 'approval': ''})
            if table not in ('100', '200') or len(candidates) != 1:
                continue
            x = candidates[0]
            for name, col in [('In Lc Amount', 'B'), ('In Fc Amount', 'C'), ('Out Lc Amount', 'E'), ('Out Fc Amount', 'F')]:
                if name not in r['measures'] or col not in x['reference']:
                    continue
                bv, ov = Decimal(r['measures'][name]), Decimal(str(x['reference'][col]))
                if bv != ov:
                    comparisons.append({'table': table, 'item_code': r['item_code'], 'description': r['description'], 'measure': name, 'bo_source_cell': f"{r['sheet']}!{r['source_cells'][name]}", 'bo_value': str(bv), 'earlier_reference_cell': f"All Reports By Report ID_Templa!{col}{x['row']}", 'earlier_value': str(ov), 'bo_less_earlier': str(bv - ov), 'basis': 'Diagnostic exact normalized hierarchy match; not an approved generation mapping'})
    save_csv('bo_to_current_mapping_candidates.csv', proposals)
    save_csv('bo_vs_earlier_reference_base_differences.csv', comparisons)
    hierarchy_checks = []
    for table in ('100', '200', '300', '400', '500'):
        records = bytable[table]
        idx = {r['item_code'].split('-')[-1]: r for r in records}
        for suffix, parent in idx.items():
            children = [c for k, c in idx.items() if k.startswith(suffix) and k != suffix and not any(k.startswith(m) and len(suffix) < len(m) < len(k) for m in idx)]
            if not children:
                continue
            for name in list(parent['measures'])[:4]:
                vals = [Decimal(c['measures'][name]) for c in children]
                actual = Decimal(parent['measures'][name])
                expected = sum(vals, Decimal(0))
                if actual != expected:
                    hierarchy_checks.append({'table': table, 'item_code': parent['item_code'], 'description': parent['description'], 'measure': name, 'parent_cell': f"{parent['sheet']}!{parent['source_cells'][name]}", 'parent_value': str(actual), 'immediate_child_sum': str(expected), 'parent_less_children': str(actual - expected), 'child_codes': '|'.join(c['item_code'] for c in children), 'status': 'DIAGNOSTIC_DIFFERENCE_REQUIRES_FORMULA_REVIEW'})
    save_csv('bo_hierarchy_diagnostics.csv', hierarchy_checks)
    keyrows = {x['item_code']: x for x in bo}
    intangible = keyrows['1-100-10902']
    cost = sum(Decimal(keyrows[c]['measures']['Orig Cost In Qatar']) for c in ('1-018-1090201', '1-018-1090202', '1-018-1090203'))
    amort = sum(Decimal(keyrows[c]['measures']['Amor Impair In Qatar']) for c in ('1-018-1090201', '1-018-1090202', '1-018-1090203'))
    assetroot = keyrows['1-100-1']
    liabilityroot = keyrows['2-200-2']
    four = ('In Lc Amount', 'In Fc Amount', 'Out Lc Amount', 'Out Fc Amount')
    at = sum(Decimal(assetroot['measures'][m]) for m in four)
    lt = sum(Decimal(liabilityroot['measures'][m]) for m in four)
    scope = [{'table': t, 'bo_rows': len(bytable[t]), 'current_rows': len(oldtable[t]), 'difference': len(bytable[t]) - len(oldtable[t])} for t in sorted(set(bytable) | set(oldtable))]
    save_csv('bo_vs_current_scope.csv', scope)
    special_rows = list(rows(DOWNLOADS / 'BO_QCB_NBS_Report.xlsx', dict(sheets(DOWNLOADS / 'BO_QCB_NBS_Report.xlsx'))['Table-020']))
    save_json('bo_relationship_findings.json', {
        'crosswalk_candidates': dict(Counter(p['status'] for p in proposals)),
        'base_comparison_changed_cells': len(comparisons),
        'hierarchy_differences': len(hierarchy_checks),
        'hierarchy_differences_over_one_display_unit': sum(abs(Decimal(x['parent_less_children'])) > 1 for x in hierarchy_checks),
        'intangible': {'bo_asset_gross': intangible['measures']['In Lc Amount'], 'detail_gross_top_level_only': str(cost), 'detail_signed_amortization': str(amort), 'detail_net': str(cost + amort), 'asset_gross_less_detail_net': str(Decimal(intangible['measures']['In Lc Amount']) - cost - amort), 'caveat': 'Gross and net are different measures. Do not force equality without confirming intended NBS presentation.'},
        'bo_root_four_primary_columns': {'assets': str(at), 'liabilities_capital': str(lt), 'assets_less_liabilities_capital': str(at - lt), 'caveat': 'Source control difference; investigate inclusion/formulas/adjustments before treating either total as correct.'},
        'special_table_020': special_rows,
        'scope': scope,
    })
    print(json.dumps(json.loads((OUT / 'bo_relationship_findings.json').read_text()), indent=2)[:5500])


if __name__ == '__main__':
    main()
