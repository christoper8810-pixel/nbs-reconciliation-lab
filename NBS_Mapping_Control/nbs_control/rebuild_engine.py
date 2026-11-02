"""Rebuild generator: source facts -> independent per-table measures -> contributions -> results.

Generation reads only source facts (ECB/LOAN/DEPOSIT/TB through the read-only legacy bank DB and
category events from the rebuild store) and mapping/policy snapshots. It never reads BO or live
reference values; comparison is a separate later stage (rebuild_compare).

Stocks and events are aggregated at their own grain. A category event is never joined to an ECB
balance in a way that repeats the balance; ECB facts are one row per account/currency.
"""
from __future__ import annotations
import json
import re
from collections import Counter, defaultdict
from decimal import Decimal

from . import maturity as mat
from .generation import prepare_facts, rebuild_settings
from .money import to_micro
from .report_mapping import compile_filter as legacy_compile, allof, term, validate_spec, CURRENT_TYPES, SAVING_TYPES
from .target_mappings import CALCULATING, compile_filter as categ_compile

GEO = {('IN', 'LC'): 'IN_LC', ('IN', 'FC'): 'IN_FC', ('OUT', 'LC'): 'OUT_LC', ('OUT', 'FC'): 'OUT_FC'}
SIZE_BANDS = ['BAND_UPTO_100TH', 'BAND_HUN_TO_1000TH', 'BAND_THOU_TO_2500TH', 'BAND_TFHUN_TO_10000TH', 'BAND_TEN_TO_50MI',
              'BAND_FIFTY_TO_100MI', 'BAND_HUN_TO_500MI', 'BAND_FHUN_TO_1000MI', 'BAND_GREATER1000MI']
SIZE_BOUNDS_THOUSANDS = [0, 100, 1000, 2500, 10000, 50000, 100000, 500000, 1000000, None]
RISK = [('GOOD_DIRECT', {'1', '2', '3', '4', '5', '6'}), ('WATCH_DIRECT', {'7'}), ('SUBSTANDARD_DIRECT', {'8'}),
        ('DOUBTFUL_DIRECT', {'9'}), ('BAD_DIRECT', {'10'})]
SECTORS = [('NBFI', lambda r: r['personal'] == 'NonPersonal' and (r['industry'] or '').startswith('441')),
           ('GOV', lambda r: r['personal'] == 'NonPersonal' and (r['industry'] or '').startswith('2')),
           ('SEMI_GOV', lambda r: r['personal'] == 'NonPersonal' and (r['industry'] or '').startswith('3')),
           ('PRIVATE', lambda r: r['personal'] == 'NonPersonal' and (r['industry'] or '').startswith('4') and not (r['industry'] or '').startswith('441')),
           ('PERSONAL', lambda r: r['personal'] == 'Personal')]
MONEY_KINDS = ('money', 'notional', 'fair_value_positive', 'fair_value_negative')


def micro_of_float(x):
    return None if x is None else to_micro(repr(float(x)))


class FactSource:
    """Per-account stock facts prepared once from the read-only legacy bank DB."""

    def __init__(self, bank_conn, balance_rules, manifest, report_date, product_policies):
        import threading
        self.c = bank_conn
        self.lock = threading.RLock()  # the web app shares one prepared connection across request threads
        self.manifest = manifest
        self.columns = manifest['ECB']['component_columns']
        self.checks = prepare_facts(bank_conn, balance_rules, manifest, report_date, product_policies)

    def rows(self, spec):
        with self.lock:
            return self._rows(spec)

    def _rows(self, spec):
        validate_spec(spec)
        params = [spec['source']]
        where = 'f.source=? AND ' + legacy_compile(spec.get('filter'), params)
        measure = spec['measure']
        missing = []
        if measure == 'components':
            ts = spec['components']
            missing = [t for t in ts if t not in self.columns]
            expr = '+'.join(f"COALESCE(json_extract(f.components,'$.{t}'),0)" for t in ts if t in self.columns) or 'NULL'
        elif measure in ('outstanding', 'earned', 'unearned', 'carrying', 'ethix_carrying', 'deposit', 'amount'):
            expr = 'f.' + measure
            groups = {'outstanding': ('OUTSTANDING',), 'earned': ('AMORTIZED_EARNED',),
                      'unearned': ('UNEARNED_PROFIT',), 'carrying': ('OUTSTANDING', 'AMORTIZED_EARNED'),
                      'ethix_carrying': ('OUTSTANDING', 'AMORTIZED_EARNED')}.get(measure, ())
            missing = sorted({t for g in groups for t in self.checks.get('missing_balance_columns', {}).get(g, [])})
            if measure == 'deposit':
                missing = [t for t in ('CREDIT', 'CURACCOUNT') if t not in self.columns]
        else:
            return [], ['Measure undefined'], missing
        if spec.get('negative_filter'):
            nparams = []
            neg = legacy_compile(spec['negative_filter'], nparams)
            expr = f'(CASE WHEN {neg} THEN -({expr}) ELSE ({expr}) END)'
            params = nparams + params
        sql = (f'SELECT f.rowid, f.source, f.account, f.currency, f.residency, f.country, f.maturity, f.product, f.risk, '
               f'f.personal, f.industry, f.unavailable, f.issue, ({expr}), f.rim FROM facts f WHERE {where}')
        out = []
        for r in self.c.execute(sql, params):
            out.append({'fid': r[0], 'source': r[1], 'account': r[2], 'currency': r[3], 'residency': r[4], 'country': r[5],
                        'maturity': r[6], 'product': r[7], 'risk': r[8], 'personal': r[9], 'industry': r[10],
                        'unavailable': r[11], 'issue': r[12], 'amount': r[13], 'rim': r[14]})
        return out, [], missing


def _fields(node, acc):
    if not node:
        return acc
    if 'field' in node:
        acc.add(node['field'])
    for k in ('all', 'any'):
        for x in node.get(k, []):
            _fields(x, acc)
    if 'not' in node:
        _fields(node['not'], acc)
    return acc


def _conjunct_fields(node, acc):
    """Fields fixed by top-level AND conditions only (a field inside OR/NOT does not constrain the population)."""
    if not node:
        return acc
    if 'field' in node:
        acc.add(node['field'])
    for x in node.get('all', []):
        _conjunct_fields(x, acc)
    return acc


def correct_namespaces(spec, cfg):
    """Legacy drafts sometimes put 4-digit T24 SECTOR codes (1000-series individuals, 2000-series corporates) on the
    5-digit SIC 'industry' field, where they can never match. Re-target exactly those conditions to 'sector'."""
    if not cfg or not cfg.get('namespace_corrections', {}).get('industry_4digit_to_sector'):
        return spec, []
    fixed = []

    def walk(node):
        if not node:
            return node
        if 'field' in node:
            vals = [str(v) for v in node.get('values', [])]
            if node['field'] == 'industry' and vals and all(re.fullmatch(r'\d{4}', v) for v in vals):
                fixed.append(f"{node['op']} {','.join(vals)}")
                return dict(node, field='sector')
            return node
        out = {}
        for k in ('all', 'any'):
            if k in node:
                out[k] = [walk(x) for x in node[k]]
        if 'not' in node:
            out['not'] = walk(node['not'])
        return out

    new = walk(spec.get('filter'))
    if not fixed:
        return spec, []
    return dict(spec, filter=new), ['4-digit T24 SECTOR codes moved from SIC field to ECB sector: ' + '; '.join(fixed)]


def correct_components(spec, corrections):
    """Apply the owner-reviewable component-name corrections (typos, non-type words). Owner group types are not touched."""
    if spec.get('preserve_original') or not corrections or not spec.get('components'):
        return spec, []
    typos = corrections.get('typos', {})
    words = set(corrections.get('not_balance_types', {}).get('words', []))
    out, notes = [], []
    for c in spec['components']:
        if c in typos:
            out.append(typos[c]['to'])
            notes.append(f'{c} -> {typos[c]["to"]} ({typos[c].get("status", "PROVISIONAL")} typo correction)')
        elif c in words:
            notes.append(f'"{c}" dropped (not a balance type)')
        else:
            out.append(c)
    if not notes:
        return spec, []
    return dict(spec, components=list(dict.fromkeys(out))), ['Component names corrected: ' + '; '.join(notes)]


def inherit_hierarchy(spec, cfg):
    """Add the dimension predicates of recognised ancestor levels that the row's own filter leaves open."""
    if spec.get('preserve_original'):
        return spec, []
    from .report_mapping import sector_filter
    spec, corrected = correct_namespaces(spec, cfg)
    if not cfg or not cfg.get('enabled'):
        return spec, corrected
    have = _conjunct_fields(spec.get('filter'), set())
    added, notes = [], []
    levels = spec['path'].split(' > ')
    for level in (levels if cfg.get('apply_to_leaf') else levels[:-1]):
        label = re.sub(r'^[\s.\d]+', '', level).strip().lower()
        entry = cfg['labels'].get(label)
        if not entry or not entry.get('enabled', True):
            continue
        if 'SECTOR' in entry and spec['source'] not in ('ECB_LOAN', 'ECB_DEPOSIT'):
            continue  # customer type / SIC exist only on the loan- and deposit-joined facts
        pred = sector_filter(entry['SECTOR']) if 'SECTOR' in entry else entry.get(spec['source'])
        if not pred:
            continue
        if entry.get('PROVISIONAL'):
            notes.append('PROVISIONAL rule: ' + entry['PROVISIONAL'])
        fields = _fields(pred, set())
        if fields & have and not entry.get('FORCE'):
            continue
        added.append(pred)
        have |= _conjunct_fields(pred, set())
        notes.append(f'inherited "{level.strip(". ")}" -> {", ".join(sorted(fields))}')
    if not added:
        return spec, corrected
    return dict(spec, filter=allof(spec.get('filter'), *added)), corrected + ['Parent-level dimensions inherited: ' + '; '.join(notes)]


def geo_of(r):
    if r['residency'] == 'Resident':
        g = 'IN'
    elif r['residency'] == 'NonResident':
        g = 'OUT'
    elif r['country'] == 'QA':
        g = 'IN'
    elif r['country']:
        g = 'OUT'
    else:
        g = 'UNKNOWN'
    cur = 'LC' if r['currency'] == 'QAR' else 'FC' if r['currency'] else 'UNKNOWN'
    return g, cur


def legacy_semantic(spec, rows, report_date, settings):
    """Independent per-layout measure calculation from account rows. Returns semantic values and contributions."""
    layout = spec.get('layout') or ('tb' if spec['source'] == 'TB' else 'geo')
    factor = Decimal(repr(float(spec['factor'])))
    values = defaultdict(int)
    counts = Counter()
    contrib = []
    issues = []
    exceptions = Counter()
    exc_amount = Counter()

    def add(r, sem, amt_micro, included=True, reason=None):
        contrib.append((r['fid'], r['source'], r['account'], sem, amt_micro, 1 if included else 0, reason))
        if included:
            values[sem] += amt_micro
            counts[sem] += 1

    by_customer = defaultdict(list)
    for r in rows:
        if r['unavailable']:
            contrib.append((r['fid'], r['source'], r['account'], 'EXCLUDED', micro_of_float(r['amount']), 0, r['issue'] or 'UNAVAILABLE_INPUT'))
            exceptions['unavailable'] += 1
            continue
        if r['amount'] is None:
            contrib.append((r['fid'], r['source'], r['account'], 'EXCLUDED', None, 0, 'MISSING_AMOUNT'))
            exceptions['missing_amount'] += 1
            continue
        amt = int(Decimal(micro_of_float(r['amount'])) * factor)
        g, cur = geo_of(r)
        if layout == 'geo':
            sem = GEO.get((g, cur))
            if sem is None:
                add(r, 'UNKNOWN_DIMENSION', amt, False, f'geography {g} / currency {cur} unknown')
                exc_amount['unknown_dimension'] += amt
                exceptions['unknown_dimension'] += 1
            else:
                add(r, sem, amt)
        elif layout == 'tb':
            add(r, 'ALL_GEO_' + cur, amt) if cur != 'UNKNOWN' else add(r, 'UNKNOWN_DIMENSION', amt, False, 'currency unknown')
        elif layout == 'maturity_loan':
            state = mat.bucket(r['maturity'], report_date, mat.LOAN_BANDS, settings['maturity_convention'],
                               open_ended=r['product'] in settings['open_ended_products'])
            if state in ('OVERDUE', 'MISSING'):
                add(r, state, amt, False, f'{state} maturity excluded from buckets')
                exceptions[state] += 1
                exc_amount[state] += amt
            else:
                add(r, state, amt)
        elif layout == 'maturity_deposit':
            if r['product'] in CURRENT_TYPES:
                add(r, 'DEP_CURRENT_CALL', amt)
            elif r['product'] in SAVING_TYPES and r['product'] != 'NTD':
                add(r, 'DEP_SAVING', amt)
            elif r['product'] == 'NTD':
                state = mat.bucket(r['maturity'], report_date, mat.DEPOSIT_BANDS, settings['maturity_convention'])
                if state in ('OVERDUE', 'MISSING'):
                    add(r, state, amt, False, f'{state} maturity excluded from buckets')
                    exceptions[state] += 1
                    exc_amount[state] += amt
                else:
                    add(r, state, amt)
            else:
                add(r, 'UNCLASSIFIED_PRODUCT', amt, False, f'product {r["product"]} not current/saving/time')
                exceptions['unclassified_product'] += 1
                exc_amount['unclassified_product'] += amt
        elif layout == 'risk':
            sem = next((s for s, grades in RISK if (r['risk'] or '') in grades), None)
            if sem:
                add(r, sem, amt)
            else:
                add(r, 'UNKNOWN_RISK', amt, False, f'risk grade {r["risk"]!r} not mapped')
                exceptions['unknown_risk'] += 1
                exc_amount['unknown_risk'] += amt
        elif layout == 'sector_columns':
            sec = next((s for s, pred in SECTORS if pred(r)), None)
            if sec and cur != 'UNKNOWN':
                add(r, f'SECTOR_{sec}_{cur}', amt)
            else:
                add(r, 'UNKNOWN_SECTOR', amt, False, 'sector/currency unknown; not allocated to a convenient sector')
                exceptions['unknown_sector'] += 1
                exc_amount['unknown_sector'] += amt
        elif layout == 'size' and spec.get('size_grain') == 'customer' and r.get('rim'):
            by_customer[r['rim']].append((r, amt))
            continue
        elif layout == 'size':
            thousands = Decimal(amt) / Decimal(10 ** 9)
            if thousands <= 0:
                add(r, 'NON_POSITIVE_BALANCE', amt, False, 'zero/negative balance outside positive bands')
                exceptions['non_positive'] += 1
                exc_amount['non_positive'] += amt
                continue
            for band, lo, hi in zip(SIZE_BANDS, SIZE_BOUNDS_THOUSANDS, SIZE_BOUNDS_THOUSANDS[1:]):
                if thousands > lo and (hi is None or thousands <= hi):
                    add(r, band + '_AMOUNT', amt)
                    break
        else:
            add(r, 'UNSUPPORTED_LAYOUT', amt, False, f'layout {layout} not supported')
    no_rim = 0
    for rim, items in by_customer.items():
        total = sum(a for _, a in items)
        thousands = Decimal(total) / Decimal(10 ** 9)
        band = None if thousands <= 0 else next(b for b, lo, hi in zip(SIZE_BANDS, SIZE_BOUNDS_THOUSANDS, SIZE_BOUNDS_THOUSANDS[1:])
                                                 if thousands > lo and (hi is None or thousands <= hi))
        for r, a in items:
            contrib.append((r['fid'], r['source'], r['account'], (band + '_AMOUNT') if band else 'NON_POSITIVE_BALANCE', a, 1 if band else 0,
                            f'customer {rim} total banded' if band else 'customer total zero/negative'))
        if band:
            values[band + '_AMOUNT'] += total
            counts[band + '_AMOUNT'] += 1
        else:
            exceptions['non_positive_customers'] += 1
            exc_amount['non_positive_customers'] += total
    if layout == 'size' and spec.get('size_grain') == 'customer':
        no_rim = sum(1 for r in rows if not r.get('rim') and not r['unavailable'])
        issues.append(f'Bands applied to the total per customer (RIM): {len(by_customer)} customers' + (f'; {no_rim} accounts without RIM banded individually' if no_rim else ''))
    result = dict(values)
    if layout == 'geo' and spec['source'] != 'TB':
        for s in GEO.values():
            result.setdefault(s, 0)
    if layout == 'maturity_loan':
        for s in ('MAT_NONE',) + mat.LOAN_BANDS:
            result.setdefault(s, 0)
        result['TOTAL'] = sum(result[s] for s in ('MAT_NONE',) + mat.LOAN_BANDS)
    if layout == 'maturity_deposit':
        for s in ('DEP_CURRENT_CALL', 'DEP_SAVING') + mat.DEPOSIT_BANDS:
            result.setdefault(s, 0)
        result['TOTAL'] = sum(result[s] for s in ('DEP_CURRENT_CALL', 'DEP_SAVING') + mat.DEPOSIT_BANDS)
    if layout == 'size':
        for b in SIZE_BANDS:
            result.setdefault(b + '_AMOUNT', 0)
            result[b + '_COUNT'] = counts[b + '_AMOUNT']
    if layout == 'sector_columns':
        for s, _ in SECTORS:
            for cur in ('LC', 'FC'):
                result.setdefault(f'SECTOR_{s}_{cur}', 0)
        result['TOTAL_LC'] = sum(result[f'SECTOR_{s}_LC'] for s, _ in SECTORS)
        result['TOTAL_FC'] = sum(result[f'SECTOR_{s}_FC'] for s, _ in SECTORS)
        result['TOTAL'] = result['TOTAL_LC'] + result['TOTAL_FC']
    if layout == 'risk':
        for s, _ in RISK:
            result.setdefault(s, 0)
        issues.append('Indirect risk grades require an external feed; indirect columns unavailable')
    for k, n in exceptions.items():
        issues.append(f'{k}: {n} records' + (f', {Decimal(exc_amount[k]) / 10**9:,.3f} thousand excluded' if exc_amount.get(k) else ''))
    if layout in ('maturity_loan', 'maturity_deposit'):
        issues.append(f'Maturity convention {settings["maturity_convention"]} is provisional; overdue/missing kept separate')
    return {'layout': layout, 'semantic': result, 'counts': dict(counts), 'contributions': contrib, 'issues': issues,
            'exceptions': dict(exceptions)}


def categ_rows(store, source_sha256, filt, weights):
    params = [source_sha256]
    where = 'source_sha256=? AND ' + categ_compile(filt, params)
    out = []
    for row_no, sid, amount, cur, et in store.execute(
            f'SELECT row_no, source_id, amount_micro, currency, event_type FROM categ_events WHERE {where}', params):
        w, state = weights[row_no]
        out.append({'row_no': row_no, 'source_id': sid, 'amount': amount, 'currency': cur, 'event_type': et, 'weight': w, 'state': state})
    return out


def categ_semantic(mapping, rows):
    sign = mapping['categ']['sign']
    geo = mapping['categ'].get('geography', 'UNKNOWN')
    values = defaultdict(int)
    contrib = []
    unresolved = 0
    for r in rows:
        cur = 'LC' if r['currency'] == 'QAR' else 'FC'
        sem = GEO.get((geo, cur), f'UNKNOWN_GEO_{cur}')
        amt = r['amount'] * sign
        if not r['weight']:
            contrib.append((r['row_no'], 'CATEG_ENTRY', r['source_id'], 'EXCLUDED', amt, 0, r['state']))
            continue
        if r['state'] == 'UNRESOLVED_REPEAT':
            unresolved += amt
        contrib.append((r['row_no'], 'CATEG_ENTRY', r['source_id'], sem, amt, 1, r['state']))
        values[sem] += amt
    issues = ['Category events: P&L period/YTD completeness not established; result is partial']
    if geo == 'UNKNOWN':
        issues.append('Category events carry no residency; geography unknown, so primary In/Out columns are unavailable')
    if unresolved:
        issues.append(f'Includes unresolved repeated observations {Decimal(unresolved) / 10**6:,.2f} QAR')
    return {'layout': 'categ', 'semantic': dict(values), 'contributions': contrib, 'issues': issues,
            'unresolved_micro': unresolved}


def cell_values(target, sem, catalogue, mapping_status):
    """Map semantic results onto the target table's validated measures."""
    measures = catalogue['tables'].get(target['table'], {}).get('measures', {})
    out = {}
    for header, m in measures.items():
        ov = (target.get('overrides') or {}).get(header)
        if ov is not None:
            v = ov['value']
            out[header] = {'value': None if v is None else (to_micro(v) * (1 if m['kind'] == 'count' else 1000)),
                           'status': 'MANUAL_OVERRIDE_EMPTY' if v is None else 'MANUAL_OVERRIDE', 'source_kind': 'MANUALLY_ADJUSTED',
                           'issues': ['Owner override: ' + ov['reason']]}
            continue
        s = m.get('semantic')
        if sem is None or s not in sem['semantic']:
            out[header] = {'value': None, 'status': 'UNAVAILABLE', 'source_kind': None,
                           'issues': ['No mapping' if sem is None else f'Measure {s} not produced by the {sem["layout"]} calculation']}
            continue
        v = int(sem['semantic'][s])  # money: QAR micro-units; count: plain integer (never divided)
        status = {'APPROVED': 'CALCULATED_SUPPORTED', 'PROVISIONAL': 'PROVISIONAL', 'DRAFT_CANDIDATE': 'DRAFT_CANDIDATE_PREVIEW'}[mapping_status]
        if sem['issues'] and status == 'CALCULATED_SUPPORTED':
            status = 'PARTIAL'
        if sem.get('unresolved_micro'):
            status = 'UNRESOLVED_DUPLICATE_BASIS'
        elif sem.get('missing_components'):
            status = 'PARTIAL'
        out[header] = {'value': v, 'status': status, 'source_kind': sem.get('source_kind'), 'issues': list(sem['issues'])}
    return out


def generate_targets(mappings, catalogue, facts, rules, store, categ_sha, weights, report_date, settings, only=None, qcb_rules=None):
    """Calculate every calculating target (or only the given ids). Returns results and contributions.

    QCB_COMPOSITION targets are assembled last, from already calculated targets, and never from references."""
    results = {}
    contributions = {}
    cache = {}

    hier = settings.get('hierarchy_predicates')

    corrections = settings.get('component_corrections')

    def stock_semantic(specs, layout=None, table=None):
        inherited = []
        specs2 = []
        for s in specs:
            s, fixes = correct_components(s, corrections)
            inherited += fixes
            s2, notes = inherit_hierarchy(s, hier)
            specs2.append(s2)
            inherited += notes
        specs = specs2
        grain = (hier or {}).get('size_band_grain', {}).get(table) if table else None
        key = json.dumps([[{k: s.get(k) for k in ('source', 'measure', 'components', 'filter', 'negative_filter', 'factor', 'layout')} for s in specs], layout, grain], sort_keys=True)
        if key in cache:
            return cache[key]
        if len({(s['source'], s['measure'], json.dumps(s.get('components')), s['factor']) for s in specs}) > 1:
            raise ValueError('Population union needs the same source, measure and sign for every rule')
        rows, errs, missing, seen, overlap = [], [], [], set(), 0
        for s in specs:
            r, e, m = facts.rows(s)
            errs += e
            missing += m
            for x in r:
                if (x['source'], x['fid']) in seen:
                    overlap += 1
                    continue
                seen.add((x['source'], x['fid']))
                rows.append(x)
        spec = dict(specs[0], layout=layout if layout is not None else specs[0].get('layout'), size_grain=grain)
        sem = legacy_semantic(spec, rows, report_date, settings)
        sem['issues'] = errs + inherited + sem['issues'] + [n for s in specs for n in s.get('notes', [])]
        if overlap:
            sem['issues'].append(f'{overlap} accounts selected by more than one source rule were counted once')
        if missing:
            sem['issues'].append('Absent balance columns: ' + ', '.join(sorted(set(missing))))
            sem['missing_components'] = sorted(set(missing))
            if spec['measure'] == 'components' and not any(t in facts.columns for t in spec['components']):
                sem['semantic'] = {}
        if spec['source'] == 'ECB_LOAN' and spec['measure'] in ('carrying', 'ethix_carrying'):
            sem['issues'].append('HYBRID: includes separately supplied Ethix Loan_Fees_QAR; not a fully T24-derived carrying amount')
            sem['source_kind'] = 'T24_PLUS_ETHIX_SUPPLEMENTARY_FEES'
        else:
            sem['source_kind'] = 'ETHIX_TRIAL_BALANCE' if spec['source'] == 'TB' else 'T24_ECB'
        sem['_rows'] = rows
        sem['_spec'] = spec
        cache[key] = sem
        return sem

    def usable(rid):
        spec = rules['rules'].get(rid)
        if spec is None:
            return None, f'Legacy rule {rid} not found'
        if not spec.get('enabled') or not spec.get('source'):
            return None, f'Legacy rule {rid} has no enabled source: ' + '; '.join(spec.get('notes', []))
        if facts is None:
            return None, 'Stock facts not loaded'
        return spec, None

    for tid, t in mappings['targets'].items():
        if only is not None and tid not in only:
            continue
        sem = None
        issues = []
        if t['status'] in CALCULATING and t['method'] == 'LEGACY_RULE':
            spec, err = usable(t['legacy_rule_id'])
            if err:
                issues.append(err)
            else:
                sem = stock_semantic([spec], table=t['table'])
        elif t['status'] in CALCULATING and t['method'] == 'QCB_POPULATION':
            specs = []
            for rid in t['legacy_rule_ids']:
                spec, err = usable(rid)
                if err:
                    issues.append(err)
                specs.append(spec)
            if not issues:
                try:
                    sem = dict(stock_semantic(specs, t.get('layout') or 'geo', table=t['table']))
                    sem['issues'] = sem['issues'] + [f'Population from QCB rule {t.get("qcb_code")} ({t["qcb_rule_id"]})']
                except ValueError as exc:
                    issues.append(str(exc))
        elif t['status'] in CALCULATING and t['method'] == 'SOURCE_RULE':
            try:
                sem = _source_rule(t, stock_semantic, store, categ_sha, weights, facts)
            except ValueError as exc:
                issues.append(f'Logic builder rule not computable: {exc}')
        elif t['status'] in CALCULATING and t['method'] == 'CATEG_EVENTS':
            if categ_sha is None:
                issues.append('No category source in this run')
            else:
                rows = categ_rows(store, categ_sha, t['categ']['filter'], weights)
                sem = categ_semantic(t, rows)
                sem['source_kind'] = 'T24_CATEG_ENTRY'
        elif t['status'] in CALCULATING and t['method'] in ('SUBTOTAL_OF_CHILDREN', 'QCB_COMPOSITION'):
            issues.append('Assembled after the component targets are calculated')
        cells = cell_values(t, sem, catalogue, t['status']) if t['status'] in CALCULATING or t.get('overrides') else \
            {h: {'value': None, 'status': 'NOT_APPLICABLE' if t['status'] == 'NOT_APPLICABLE' else 'UNAVAILABLE', 'source_kind': None,
                 'issues': [f'Mapping {t["status"]}: {t.get("evidence") or ""}']}
             for h in catalogue['tables'].get(t['table'], {}).get('measures', {})}
        if t['status'] in CALCULATING and sem is None:
            for c in cells.values():
                if c['status'] not in ('MANUAL_OVERRIDE', 'MANUAL_OVERRIDE_EMPTY'):
                    c['status'] = 'UNAVAILABLE'
                    c['issues'] = issues + c['issues']
        results[tid] = {'target': t, 'cells': cells, 'semantic': sem['semantic'] if sem else None,
                        'layout': sem['layout'] if sem else None, 'issues': issues + (sem['issues'] if sem else []), '_sem': sem}
        if sem:
            contributions[tid] = sem['contributions']
    _residual_others(mappings, results, contributions, catalogue, report_date, settings, only)
    _subtotals(mappings, results, catalogue)
    if qcb_rules:
        _compositions(mappings, results, contributions, catalogue, qcb_rules)
    for r in results.values():
        r.pop('_sem', None)
    return results, contributions


OTHERS = re.compile(r'^\W*(\d+(\.\d+)*\W*)?others?\b', re.I)


def _residual_others(mappings, results, contributions, catalogue, report_date, settings, only):
    """An 'Others' item means 'not elsewhere classified': records already reported by its named sibling items
    (or their sub-items) are removed from it and from its own sub-items."""
    targets = mappings['targets']
    by_parent = defaultdict(list)
    for tid, t in targets.items():
        if t.get('parent_code'):
            by_parent[(t['table'], t['parent_code'])].append(tid)

    def subtree(tid):
        t = targets[tid]
        return [k for k, x in targets.items() if x['table'] == t['table'] and x['item_code'].startswith(t['item_code'])]

    for (table, parent), kids in by_parent.items():
        for others in kids:
            if not OTHERS.match(targets[others].get('description') or ''):
                continue
            named = set()
            for k in kids:
                if k == others:
                    continue
                for d in subtree(k):
                    named |= {(x[1], x[0]) for x in contributions.get(d, []) if x[5] and x[0] is not None}
            if not named:
                continue
            for tid in subtree(others):
                if tid not in results:
                    continue
                sem = results[tid].get('_sem')
                if not sem or '_rows' not in sem:
                    continue
                rows = [r for r in sem['_rows'] if (r['source'], r['fid']) not in named]
                removed = len(sem['_rows']) - len(rows)
                if not removed:
                    continue
                t = targets[tid]
                new = legacy_semantic(sem['_spec'], rows, report_date, settings)
                new['issues'] = [f'Residual "Others": {removed} records already reported in named items under {parent} excluded'] + sem['issues']
                new['source_kind'] = sem.get('source_kind')
                new['missing_components'] = sem.get('missing_components', [])
                results[tid]['cells'] = cell_values(t, new, catalogue, t['status'])
                results[tid]['semantic'] = new['semantic']
                results[tid]['issues'] = new['issues']
                contributions[tid] = new['contributions']

STATUS_RANK = ['CALCULATED_SUPPORTED', 'PROVISIONAL', 'PARTIAL', 'DRAFT_CANDIDATE_PREVIEW', 'UNRESOLVED_DUPLICATE_BASIS']
STOCK_SOURCES = ('ECB', 'ECB_LOAN', 'ECB_DEPOSIT', 'TB')


def _source_rule(t, stock_semantic, store, categ_sha, weights, facts):
    """Logic-builder mapping: the sum of its parts. Each part is a stock selection (ECB / ECB+loan / ECB+deposit /
    trial balance, possibly expanded from a GL Report line) or a category-entry selection."""
    from .target_mappings import TABLE_LAYOUT
    from .report_mapping import validate_spec
    parts = t.get('parts') or []
    if not parts:
        raise ValueError('no parts')
    layout = TABLE_LAYOUT.get(t['table'], 'geo')
    sems = []
    for i, p in enumerate(parts, start=1):
        if p.get('kind') == 'CATEG':
            if categ_sha is None:
                raise ValueError('no category-entry source loaded')
            s = categ_semantic({'categ': {'sign': p.get('sign', 1), 'geography': p.get('geography', 'UNKNOWN')}},
                               categ_rows(store, categ_sha, p['filter'], weights))
            s['source_kind'] = 'T24_CATEG_ENTRY'
        else:
            spec = {'source': p['source'], 'measure': p.get('measure', 'components'), 'components': list(p.get('components') or []),
                    'filter': p.get('filter'), 'negative_filter': None, 'factor': p.get('factor', 1), 'enabled': True,
                    'notes': [], 'path': '', 'layout': None, 'preserve_original':p.get('preserve_original',False)}
            validate_spec(spec)
            if spec['source'] not in STOCK_SOURCES:
                raise ValueError(f'part {i}: unsupported source')
            if facts is None:
                raise ValueError('account database not loaded')
            s = stock_semantic([spec], None if spec['source'] == 'TB' else layout, table=t['table'])
        s = dict(s, issues=[f'Part {i}: {p.get("label") or p.get("source") or p.get("kind")}'] + list(s['issues']))
        sems.append(s)
    values = defaultdict(int)
    seen = defaultdict(set)
    contrib, issues, kinds = [], [], set()
    overlap = 0
    for i, s in enumerate(sems, start=1):
        for k, v in s['semantic'].items():
            values[k] += v
        comps = tuple(sorted(parts[i - 1].get('components') or [])) or ('categ',)
        for x in s['contributions']:
            if x[5] and x[0] is not None:
                key = (x[1], x[0])
                if comps in seen[key]:
                    overlap += 1
                seen[key].add(comps)
            contrib.append(tuple(x[:6]) + (f'part {i}' + (f': {x[6]}' if x[6] else ''),))
        issues += s['issues']
        kinds.add(s.get('source_kind'))
    if overlap:
        issues.append(f'WARNING: {overlap} records selected by two parts with the same balance types (counted twice)')
    return {'layout': sems[0]['layout'] if len({x['layout'] for x in sems}) == 1 else 'mixed', 'semantic': dict(values),
            'contributions': contrib, 'issues': issues, 'source_kind': ' + '.join(sorted(k for k in kinds if k)),
            'missing_components': sorted({t for s in sems for t in s.get('missing_components', [])})}


def _compositions(mappings, results, contributions, catalogue, qcb_rules):
    """QCB_COMPOSITION: each measure = the other side of its QCB '=' rule, evaluated on generated cells only.
    Repeated passes let compositions use other compositions; anything missing stays unavailable."""
    from . import qcb_validations as q
    from decimal import Decimal
    index = {r['rule_id']: r for r in qcb_rules}
    todo = [tid for tid, r in results.items() if r['target']['method'] == 'QCB_COMPOSITION' and r['target']['status'] in CALCULATING]

    def lookup(table, item, code):
        tid = f'{table}|{item}'
        h = q.header_for(table, code, catalogue)
        if tid not in results or h is None:
            raise KeyError(f'{table} {item} {code} not generated')
        cell = results[tid]['cells'].get(h)
        if cell is None or cell['value'] is None:
            raise KeyError(f'{table} {item} {h} unavailable')
        used.append((tid, h, cell))
        return Decimal(cell['value'])

    for _ in range(8):
        progressed = False
        for tid in todo:
            r = results[tid]
            t = r['target']
            for code, ref in t['qcb_composition'].items():
                h = q.header_for(t['table'], code, catalogue)
                if h is None or (r['cells'][h]['value'] is not None) or r['cells'][h]['status'].startswith('MANUAL'):
                    continue
                rule = index.get(ref['rule_id'])
                if rule is None:
                    r['cells'][h]['issues'] = [f'QCB rule {ref["rule_id"]} not loaded']
                    continue
                expr = rule['right_ast'] if ref['side'] == 'left' else rule['left_ast']
                used = []
                try:
                    value = q.evaluate(expr, lookup)
                except KeyError as exc:
                    r['cells'][h]['issues'] = [f'QCB composition {rule["qcb_code"]} waiting: {exc.args[0]}']
                    continue
                worst = max((STATUS_RANK.index(c['status']) if c['status'] in STATUS_RANK else 3 for _, _, c in used), default=3)
                status = STATUS_RANK[max(worst, 3 if t['status'] == 'DRAFT_CANDIDATE' else worst)]
                if any(c['status']=='PARTIAL' for _, _, c in used):
                    status = 'PARTIAL'
                r['cells'][h] = {'value': int(value), 'status': status,
                                 'source_kind': 'QCB_COMPOSITION',
                                 'issues': [f'QCB rule {rule["qcb_code"]} ({rule["rule_id"]}): {rule["left"] if ref["side"] == "right" else rule["right"]}'] +
                                           sorted({i for _, _, c in used for i in c['issues'] if 'HYBRID' in i or 'Absent' in i})}
                contributions.setdefault(tid, []).extend((None, 'TARGET', f'{ctid}#{ch}', r['target']['table'] + ':' + code, c['value'], 1, 'QCB composition component')
                                                         for ctid, ch, c in used)
                progressed = True
        if not progressed:
            break
    for tid in todo:
        r = results[tid]
        r['layout'] = 'qcb_composition'
        r['semantic'] = {catalogue['tables'][r['target']['table']]['measures'][h]['semantic']: c['value']
                         for h, c in r['cells'].items() if c['value'] is not None}
        for c in r['cells'].values():
            if c['value'] is None and not c['status'].startswith('MANUAL'):
                c['status'] = 'UNAVAILABLE'

def partition_diagnostics(mappings, contributions, parents=None):
    """For a parent and its immediate children: records counted in two children (overlap) and parent
    records in no child (uncovered). Hierarchy-derived partitions are diagnostics for review, since
    some BO children are 'of which' views rather than exclusive splits."""
    by_parent = defaultdict(list)
    for tid, t in mappings['targets'].items():
        if t.get('parent_code'):
            by_parent[f'{t["table"]}|{t["parent_code"]}'].append(tid)
    out = []
    for parent, kids in by_parent.items():
        if parents is not None and parent not in parents:
            continue
        kids = [k for k in kids if k in contributions]
        if parent not in contributions or len(kids) < 1:
            continue
        seen = defaultdict(list)
        for k in kids:
            for fid, src, rec, sem, amt, inc, _ in contributions[k]:
                if inc:
                    seen[(src, fid, sem)].append((k, amt))
        overlap = {key: v for key, v in seen.items() if len(v) > 1}
        parent_rows = {(src, fid, sem): amt for fid, src, rec, sem, amt, inc, _ in contributions[parent] if inc}
        uncovered = {key: amt for key, amt in parent_rows.items() if key not in seen}
        outside = {key: v for key, v in seen.items() if key not in parent_rows}
        if overlap or uncovered or outside:
            out.append({'parent': parent, 'children': kids, 'overlap_records': len(overlap),
                        'overlap_amount_micro': sum(a for v in overlap.values() for _, a in v[1:]),
                        'uncovered_parent_records': len(uncovered), 'uncovered_amount_micro': sum(uncovered.values()),
                        'child_records_outside_parent': len(outside),
                        'examples': [str(k) for k in list(overlap)[:3] + list(uncovered)[:3]]})
    return out


def _subtotals(mappings, results, catalogue):
    """Explicit SUBTOTAL_OF_CHILDREN: immediate children only, additive primary money measures only."""
    from .target_mappings import check_disjoint_codes
    for tid, t in sorted(mappings['targets'].items(), key=lambda x: -len(x[1]['item_code'])):  # deepest first
        if t['method'] != 'SUBTOTAL_OF_CHILDREN' or t['status'] not in CALCULATING or tid not in results:
            continue
        kids = [k for k, x in mappings['targets'].items() if x['table'] == t['table'] and x.get('parent_code') == t['item_code']]
        check_disjoint_codes([mappings['targets'][k]['item_code'] for k in kids])
        for header, m in catalogue['tables'][t['table']]['measures'].items():
            cell = results[tid]['cells'][header]
            if cell['status'].startswith('MANUAL'):
                continue
            if not m.get('additive') or m['kind'] == 'rate':
                cell.update(value=None, status='NOT_APPLICABLE', issues=['Non-additive measure is not summed'])
                continue
            vals = [results[k]['cells'][header] for k in kids if k in results]
            if not vals or any(v['value'] is None for v in vals):
                cell.update(value=None, status='UNAVAILABLE', issues=['One or more children unavailable; subtotal withheld'])
                continue
            worst = max((STATUS_RANK.index(v['status']) if v['status'] in STATUS_RANK else 3 for v in vals), default=3)
            if t['status'] == 'DRAFT_CANDIDATE':
                worst = max(worst, 3)
            cell.update(value=sum(v['value'] for v in vals), status='PARTIAL' if any(v['status']=='PARTIAL' for v in vals) else STATUS_RANK[worst], source_kind='HIERARCHY_SUBTOTAL',
                        issues=['Subtotal of ' + str(len(vals)) + ' immediate items'] + sorted({i for v in vals for i in v['issues'] if 'HYBRID' in i}))
