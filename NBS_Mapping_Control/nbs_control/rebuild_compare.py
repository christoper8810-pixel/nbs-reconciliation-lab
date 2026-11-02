"""Compare generated results with named reference versions. Reads references; never feeds them back.

Pre-round generated values are compared with display-rounded references using a declared per-kind
tolerance. Differences are categorized; anything not explained by evidence stays UNKNOWN.
"""
from __future__ import annotations
from decimal import Decimal

from .maturity import TEMPLATE_T10, TEMPLATE_T24
from .rebuild_engine import SIZE_BANDS

TOLERANCE = {'money': Decimal('0.5'), 'notional': Decimal('0.5'), 'fair_value_positive': Decimal('0.5'),
             'fair_value_negative': Decimal('0.5'), 'count': Decimal(0), 'rate': Decimal('0.0001')}
TOLERANCE_NOTE = ('money/notional/fair value: 0.5 display unit (QAR thousand) for BO integer rounding; '
                  'counts exact; rates 0.0001')


def display(value, kind):
    """Generated value in reference display units, pre-round."""
    if value is None:
        return None
    if kind == 'count':
        return Decimal(value)
    return Decimal(value) / Decimal(10 ** 9)


def ref_display(micro, kind):
    if micro is None:
        return None
    return Decimal(micro) / Decimal(10 ** 6)


def categorize(gen, ref, kind, cell, target, row_cells=None):
    diff = gen - ref
    if abs(diff) <= TOLERANCE.get(kind, Decimal('0.5')):
        return 'WITHIN_TOLERANCE' if diff == 0 or kind == 'count' else 'ROUNDING'
    issues = ' '.join(cell.get('issues', []))
    if ref != 0 and abs(gen + ref) <= TOLERANCE.get(kind, Decimal('0.5')):
        return 'SIGN'
    if cell['status'] == 'DRAFT_CANDIDATE_PREVIEW':
        return 'POPULATION_OR_MAPPING_UNREVIEWED'
    if 'Absent balance columns' in issues or 'Owner group columns absent' in issues:
        return 'COMPONENT'
    if 'HYBRID' in issues:
        return 'FEE'
    if 'UNRESOLVED' in cell['status']:
        return 'PERIOD_OR_DUPLICATE_BASIS'
    if row_cells:
        return row_cells
    return 'UNKNOWN'


def _split_category(gen_row, ref_row, pairs):
    """If a split differs but the combined total agrees, the difference is geography or currency."""
    for label, a, b in pairs:
        if all(x in gen_row and x in ref_row for x in (a, b)):
            if abs((gen_row[a] + gen_row[b]) - (ref_row[a] + ref_row[b])) <= 1 and abs(gen_row[a] - ref_row[a]) > 1:
                return label
    return None


def compare_bo(results, catalogue, bo_values, ref_version):
    out = []
    for tid, r in results.items():
        t = r['target']
        measures = catalogue['tables'].get(t['table'], {}).get('measures', {})
        gen_row = {m['semantic']: display(r['cells'][h]['value'], m['kind']) for h, m in measures.items()
                   if h in r['cells'] and r['cells'][h]['value'] is not None}
        ref_row = {m['semantic']: ref_display(bo_values.get((t['table'], t['item_code'], h)), m['kind']) for h, m in measures.items()
                   if bo_values.get((t['table'], t['item_code'], h)) is not None}
        split = _split_category(gen_row, ref_row, [('CURRENCY', 'IN_LC', 'IN_FC'), ('CURRENCY', 'OUT_LC', 'OUT_FC'),
                                                    ('GEOGRAPHY', 'IN_LC', 'OUT_LC'), ('GEOGRAPHY', 'IN_FC', 'OUT_FC')])
        for h, m in measures.items():
            cell = r['cells'].get(h)
            if cell is None:
                continue
            ref = ref_display(bo_values.get((t['table'], t['item_code'], h)), m['kind'])
            gen = display(cell['value'], m['kind'])
            rec = {'reference_version': ref_version, 'target_id': tid, 'table': t['table'], 'item_code': t['item_code'],
                   'description': t['description'], 'measure': h, 'semantic': m['semantic'], 'kind': m['kind'],
                   'primary': m.get('primary', True), 'generated': gen, 'reference': ref, 'status': cell['status'],
                   'mapping_status': t['status'], 'source_kind': cell.get('source_kind')}
            if gen is None and ref is None:
                rec.update(difference=None, category='NO_VALUES')
            elif gen is None:
                rec.update(difference=None, category='GENERATED_UNAVAILABLE' if ref == 0 else 'MISSING_FEED_OR_MAPPING')
            elif ref is None:
                rec.update(difference=None, category='REFERENCE_ABSENT')
            else:
                rec['difference'] = gen - ref
                rec['category'] = categorize(gen, ref, m['kind'], cell, t, split)
            out.append(rec)
    return out


def template_columns(layout, sem):
    """Semantic results -> earlier live template columns, including the template's presentation totals."""
    if sem is None:
        return {}
    v = {k: Decimal(x) / Decimal(10 ** 9) for k, x in sem.items() if not k.endswith('_COUNT')}
    counts = {k: Decimal(x) for k, x in sem.items() if k.endswith('_COUNT')}
    out = {}
    if layout == 'geo':
        for s, col in (('IN_LC', 'B'), ('IN_FC', 'C'), ('OUT_LC', 'E'), ('OUT_FC', 'F')):
            if s in v:
                out[col] = v[s]
        for col, a, b in (('D', 'B', 'C'), ('G', 'E', 'F'), ('H', 'B', 'E'), ('I', 'C', 'F'), ('J', 'H', 'I')):
            if a in out and b in out:
                out[col] = out[a] + out[b]
    elif layout == 'tb':
        if 'ALL_GEO_LC' in v:
            out['H'] = v['ALL_GEO_LC']
        if 'ALL_GEO_FC' in v:
            out['I'] = v['ALL_GEO_FC']
        if 'H' in out and 'I' in out:
            out['J'] = out['H'] + out['I']
    elif layout in ('maturity_loan', 'maturity_deposit'):
        cmap = TEMPLATE_T10 if layout == 'maturity_loan' else TEMPLATE_T24
        out = {col: v[s] for s, col in cmap.items() if s in v}
    elif layout == 'size':
        for i, b in enumerate(SIZE_BANDS):
            out[chr(66 + 2 * i)] = counts.get(b + '_COUNT', Decimal(0))
            out[chr(67 + 2 * i)] = v.get(b + '_AMOUNT', Decimal(0))
        out['T'] = sum(out[chr(66 + 2 * i)] for i in range(9))
        out['U'] = sum(out[chr(67 + 2 * i)] for i in range(9))
    elif layout == 'risk':
        for s, col in (('GOOD_DIRECT', 'B'), ('WATCH_DIRECT', 'D'), ('SUBSTANDARD_DIRECT', 'H'), ('DOUBTFUL_DIRECT', 'J'), ('BAD_DIRECT', 'L')):
            if s in v:
                out[col] = v[s]
        if 'B' in out and 'D' in out:
            out['F'] = out['B'] + out['D']
        if all(c in out for c in 'HJL'):
            out['N'] = out['H'] + out['J'] + out['L']
        if 'F' in out and 'N' in out:
            out['P'] = out['F'] + out['N']
    elif layout == 'sector_columns':
        for i, s in enumerate(('NBFI', 'GOV', 'SEMI_GOV', 'PRIVATE', 'PERSONAL')):
            for j, cur in enumerate(('LC', 'FC')):
                k = f'SECTOR_{s}_{cur}'
                if k in v:
                    out[chr(66 + 2 * i + j)] = v[k]
        for col, s in (('L', 'TOTAL_LC'), ('M', 'TOTAL_FC'), ('N', 'TOTAL')):
            if s in v:
                out[col] = v[s]
    return out


def compare_live(results, rules, live_cells, ref_version):
    """Earlier live NBS01 report: compare by the legacy rule's template row and validated layout columns."""
    out = []
    seen = set()
    cols_by_row = {}
    for (row, col) in live_cells:
        cols_by_row.setdefault(row, set()).add(col)
    for tid, r in results.items():
        t = r['target']
        if t['method'] != 'LEGACY_RULE' or r['semantic'] is None:
            continue
        spec = rules['rules'].get(t['legacy_rule_id'])
        if not spec or spec['row'] in seen:
            continue
        seen.add(spec['row'])
        gen = template_columns(r['layout'], r['semantic'])
        for col in sorted(set(gen) | cols_by_row.get(spec['row'], set()), key=lambda x: (len(x), x)):
            ref = live_cells.get((spec['row'], col))
            ref = None if ref is None else Decimal(ref) / Decimal(10 ** 6)
            g = gen.get(col)
            kind = 'count' if r['layout'] == 'size' and (ord(col) - 66) % 2 == 0 and col <= 'T' else 'money'
            rec = {'reference_version': ref_version, 'target_id': tid, 'legacy_rule_id': t['legacy_rule_id'], 'template_row': spec['row'],
                   'cell': f'{col}{spec["row"]}', 'description': spec['description'], 'layout': r['layout'], 'generated': g,
                   'reference': ref, 'mapping_status': t['status']}
            if g is None or ref is None:
                rec.update(difference=None, category='GENERATED_UNAVAILABLE' if g is None else 'REFERENCE_ABSENT')
            else:
                rec['difference'] = g - ref
                cell = next(iter(r['cells'].values()), {'status': '', 'issues': r['issues']})
                rec['category'] = categorize(g, ref, kind, {'status': cell['status'], 'issues': r['issues']}, t)
            out.append(rec)
    return out


def materiality(rows):
    """Financial materiality summary: nonzero amounts available/unavailable, not a zero-dominated hit rate."""
    s = {'reference_cells': 0, 'nonzero_reference_cells': 0, 'nonzero_reference_abs': Decimal(0),
         'nonzero_reference_generated': 0, 'nonzero_reference_generated_abs': Decimal(0),
         'nonzero_reference_unavailable_abs': Decimal(0), 'abs_difference_on_comparable': Decimal(0),
         'within_tolerance_nonzero': 0, 'categories': {}}
    for r in rows:
        if not r.get('primary', True) or r.get('kind') not in (None, 'money'):
            continue
        if r['reference'] is None:
            continue
        s['reference_cells'] += 1
        if r['reference'] != 0:
            s['nonzero_reference_cells'] += 1
            s['nonzero_reference_abs'] += abs(r['reference'])
            if r['generated'] is not None:
                s['nonzero_reference_generated'] += 1
                s['nonzero_reference_generated_abs'] += abs(r['reference'])
                if r['category'] in ('WITHIN_TOLERANCE', 'ROUNDING'):
                    s['within_tolerance_nonzero'] += 1
            else:
                s['nonzero_reference_unavailable_abs'] += abs(r['reference'])
        if r.get('difference') is not None:
            s['abs_difference_on_comparable'] += abs(r['difference'])
        s['categories'][r['category']] = s['categories'].get(r['category'], 0) + 1
    return {k: (str(v) if isinstance(v, Decimal) else v) for k, v in s.items()}
