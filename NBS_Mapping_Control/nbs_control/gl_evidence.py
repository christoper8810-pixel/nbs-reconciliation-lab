"""Evidence that NBS cannot be produced by mapping GL accounts to report lines.

A GL mapping assigns each GL's whole balance to one report cell. NBS cells split the same balances by
counterparty and contract attributes (residency, currency, economic sector, remaining maturity, facility
size, risk class) and also require counts. This module measures, from the bank's own account files, how
much balance every GL-only mapping must misplace: for each GL and each breakdown, even the best single
cell for that GL leaves the rest of its balance in the wrong cell. The figures are lower bounds.
It also classifies every BO cell by the attribute it needs and summarises the QCB rules that tie
different breakdowns of the same population together.
"""
from __future__ import annotations
from collections import Counter, defaultdict
from contextlib import closing
from decimal import Decimal

from . import maturity as mat
from .rebuild_engine import SIZE_BANDS, SIZE_BOUNDS_THOUSANDS
from .rebuild_store import open_bank_readonly


def _sector(r):
    ind, pers = r['industry'] or '', r['personal'] or ''
    if pers == 'Personal':
        return 'PERSONAL'
    if pers != 'NonPersonal':
        return 'UNKNOWN'
    if ind.startswith('441'):
        return 'NBFI'
    if ind.startswith('2'):
        return 'GOV'
    if ind.startswith('3'):
        return 'SEMI_GOV'
    if ind.startswith('4'):
        return 'PRIVATE'
    return 'UNKNOWN'


def _band(amount):
    t = abs(Decimal(repr(amount))) / 1000
    if t == 0:
        return 'ZERO'
    for b, lo, hi in zip(SIZE_BANDS, SIZE_BOUNDS_THOUSANDS, SIZE_BOUNDS_THOUSANDS[1:]):
        if t > lo and (hi is None or t <= hi):
            return b


DIMENSIONS = {
    'residency (Inside/Outside Qatar)': lambda r, d: r['residency'] or 'UNKNOWN',
    'currency (LC/FC)': lambda r, d: 'LC' if r['currency'] == 'QAR' else 'FC',
    'economic sector (Tables 044/045 columns)': lambda r, d: _sector(r),
    'industry code (Table 044 rows)': lambda r, d: (r['industry'] or 'UNKNOWN')[:5],
    'remaining maturity (Tables 010/024)': lambda r, d: mat.bucket(r['maturity'] or None, d, mat.LOAN_BANDS, 'DAY_COUNT'),
    'facility size band (Tables 012/025)': lambda r, d: _band(r['amount']),
    'product / account type': lambda r, d: r['product'] or 'UNKNOWN',
}
COMBINED = ('residency (Inside/Outside Qatar)', 'currency (LC/FC)', 'economic sector (Tables 044/045 columns)', 'remaining maturity (Tables 010/024)')


def account_dispersion(bank_path, report_date='2026-09-30'):
    out = {}
    with closing(open_bank_readonly(bank_path)) as c:
        for source in ('LOAN', 'DEPOSIT'):
            rows = [dict(zip(('gl', 'residency', 'currency', 'industry', 'personal', 'maturity', 'product', 'amount', 'rim'), x)) for x in c.execute(
                'SELECT gl, residency, currency, industry, personal, maturity, product, amount, rim FROM unique_records WHERE source=? AND amount IS NOT NULL', (source,))]
            total = sum(abs(Decimal(repr(r['amount']))) for r in rows)
            gls = {r['gl'] for r in rows}
            dims = {}
            for name, fn in list(DIMENSIONS.items()) + [('combined: residency x currency x sector x maturity', None)]:
                by_gl = defaultdict(lambda: defaultdict(Decimal))
                for r in rows:
                    key = tuple(DIMENSIONS[d](r, report_date) for d in COMBINED) if fn is None else fn(r, report_date)
                    by_gl[r['gl']][key] += abs(Decimal(repr(r['amount'])))
                misplaced = sum((sum(v.values()) - max(v.values()) for v in by_gl.values()), Decimal(0))
                mixed = [g for g, v in by_gl.items() if len([x for x in v.values() if x]) > 1]
                mixed_amt = sum((sum(by_gl[g].values()) for g in mixed), Decimal(0))
                worst = sorted(((g, sum(v.values()) - max(v.values()), len(v)) for g, v in by_gl.items()), key=lambda x: -x[1])[:5]
                dims[name] = {'gls': len(by_gl), 'gls_spanning_several_cells': len(mixed),
                              'balance_in_mixed_gls_qar': str(mixed_amt.quantize(Decimal('0.01'))),
                              'minimum_misplaced_by_any_gl_mapping_qar': str(misplaced.quantize(Decimal('0.01'))),
                              'minimum_misplaced_pct': float(round(misplaced / total * 100, 2)) if total else None,
                              'largest_gls': [{'gl': g, 'misplaced_qar': str(m.quantize(Decimal('0.01'))), 'cells': n} for g, m, n in worst]}
            customers = len({r['rim'] for r in rows if r['rim']})
            out[source] = {'accounts': len(rows), 'gls': len(gls), 'customers': customers, 'absolute_balance_qar': str(total.quantize(Decimal('0.01'))),
                           'by_breakdown': dims}
        tb_cols = [x[1] for x in c.execute('PRAGMA table_info(records)')]
        tb_populated = {col: c.execute(f"SELECT count(*) FROM records WHERE source='TB' AND {col} IS NOT NULL AND {col}!=''").fetchone()[0]
                        for col in ('residency', 'country', 'industry', 'maturity', 'rim', 'risk', 'currency', 'gl')}
        out['TRIAL_BALANCE_ATTRIBUTES'] = {'populated_fields': tb_populated,
                                           'note': 'The GL trial balance carries GL, currency and amount only: no residency, sector, maturity, customer or risk attribute'}
    return out


NEEDS = [
    ('count', 'Customer/facility counts', lambda t, h, m: m['kind'] == 'count'),
    ('maturity', 'Remaining maturity per contract', lambda t, h, m: (m.get('semantic') or '').startswith('MAT_') or (m.get('semantic') or '').startswith('NOTIONAL_NAT')),
    ('size', 'Facility/customer amount band', lambda t, h, m: (m.get('semantic') or '').startswith('BAND_')),
    ('sector', 'Counterparty economic sector', lambda t, h, m: (m.get('semantic') or '').startswith('SECTOR_') or t in ('044', '045')),
    ('risk', 'Credit classification / risk grade', lambda t, h, m: t == '011'),
    ('collateral', 'Collateral type per facility', lambda t, h, m: t == '013'),
    ('listing', 'Listed / unlisted instrument', lambda t, h, m: t in ('004', '005', '042')),
    ('country', 'Counterparty country (GCC subsets)', lambda t, h, m: (m.get('semantic') or '').startswith('SUBSET_')),
    ('derivative', 'Derivative notional / fair value per contract', lambda t, h, m: t == '038'),
    ('residency', 'Counterparty residency (Inside/Outside Qatar)', lambda t, h, m: (m.get('semantic') or '')[:3] in ('IN_', 'OUT') or 'In Qatar' in h or 'Out Qatar' in h or 'Inside' in h or 'Outside' in h or ' In ' in f' {h} ' or ' Out ' in f' {h} '),
]


def cell_requirements(catalogue, store, ref_version):
    """Classify every BO reference cell by the first contract/counterparty attribute it requires."""
    cells = store.execute('SELECT table_code, measure, count(*), sum(CASE WHEN value_micro!=0 THEN 1 ELSE 0 END), sum(abs(value_micro)) FROM bo_cells WHERE ref_version=? GROUP BY table_code, measure', (ref_version,)).fetchall()
    by_need = defaultdict(lambda: {'cells': 0, 'nonzero_cells': 0, 'abs_amount_thousands': Decimal(0), 'tables': set()})
    total = {'cells': 0, 'nonzero_cells': 0}
    for t, h, n, nz, amt in cells:
        m = catalogue['tables'][t]['measures'][h]
        need = next((k for k, _, f in NEEDS if f(t, h, m)), 'gl_structure_only')
        x = by_need[need]
        x['cells'] += n
        x['nonzero_cells'] += nz
        if m['kind'] != 'count':
            x['abs_amount_thousands'] += Decimal(amt or 0) / 10 ** 6
        x['tables'].add(t)
        total['cells'] += n
        total['nonzero_cells'] += nz
    labels = {k: lbl for k, lbl, _ in NEEDS}
    labels['gl_structure_only'] = 'No counterparty/contract attribute (GL-derivable if the GL chart is granular enough)'
    out = []
    for k, v in sorted(by_need.items(), key=lambda x: -x[1]['cells']):
        out.append({'requirement': k, 'meaning': labels[k], 'cells': v['cells'], 'nonzero_cells': v['nonzero_cells'],
                    'share_of_cells_pct': round(v['cells'] / total['cells'] * 100, 1), 'abs_amount_thousands': str(v['abs_amount_thousands']),
                    'tables': sorted(v['tables'])})
    return {'total': total, 'by_requirement': out}


def qcb_rule_evidence(qrules):
    kinds = Counter(r['kind'] for r in qrules)
    examples = [r for r in qrules if r['kind'] == 'CROSS_DIMENSION_SAME_POPULATION'][:6]
    return {'rules': len(qrules), 'by_kind': dict(kinds),
            'cross_dimension_examples': [{'qcb_code': r['qcb_code'], 'rule': f"{r['left']} {r['operator']} {r['right']}"[:300]} for r in examples],
            'note': ('CROSS_DIMENSION_SAME_POPULATION rules require one population to add up identically when split by different '
                     'contract attributes (e.g. Table 009 by product = Table 012 by size band = Table 013 by collateral = Table 044 by sector). '
                     'A GL mapping can satisfy them only if every GL lies wholly inside one cell of every breakdown.')}


def build(bank_path, catalogue, store, ref_version, qrules, legacy_case_rules=None):
    out = {'accounts': account_dispersion(bank_path), 'cells': cell_requirements(catalogue, store, ref_version),
           'qcb_rules': qcb_rule_evidence(qrules)}
    if legacy_case_rules:
        out['legacy_gl_sql'] = {'classification_groups': len(legacy_case_rules), 'bo_items': store.execute(
            'SELECT count(*) FROM bo_items WHERE ref_version=?', (ref_version,)).fetchone()[0],
            'note': 'The supplied Ethix balance-sheet SQL maps GLs into 37 groups / 37 output lines; it contains no residency, sector, maturity, size, count or risk logic.'}
    return out
