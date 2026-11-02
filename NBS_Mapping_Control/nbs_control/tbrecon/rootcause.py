"""Root-cause classification, systemic issue grouping and the proposed mapping-correction worklist.

Component-level exceptions (where an amount leaves the mapped population) and GL-level residual
differences are classified separately (level COMPONENT / GL / LEGACY_GL / RULE) so the same money is
never summed twice across levels. Proposed corrections never change the approved mapping: they are a
separate worklist with original value, proposed value, reason and evidence.
"""
from __future__ import annotations

import copy
import difflib
from collections import defaultdict
from decimal import Decimal

from .tb import within

ZERO = Decimal(0)

CATEGORIES = {
    'MISSING_MAPPING': ('Missing mapping', 'Add an authorised rule / mapping for the population, or confirm it is out of scope.',
                        'Which target GL does this population belong to under the approved design?'),
    'WRONG_TARGET_GL': ('Wrong target GL', 'Correct the rule or GL-mapping target after confirming the accounting design.',
                        'Which authority (GL Report rule or legacy GL mapping) is correct for these balances?'),
    'MULTI_TARGET_ALLOCATION_UNRESOLVED': ('Multiple-target allocation unresolved',
                                           'Define an allocation rule using balance type, status or category; never split equally.',
                                           'Which attribute distinguishes the target GLs for this legacy GL?'),
    'WRONG_OR_MISSING_BALANCE_TYPE': ('Wrong / missing balance type', 'Add the atomic balance type to the correct rule, or supply a validated alias.',
                                      'Is this balance type a distinct component, a virtual aggregate, or an alias?'),
    'PRODUCT_SECTOR_MISALIGNMENT': ('PRODUCT / SECTOR column misalignment', 'Move the values to the correct rule column after owner confirmation of the CONSOL_KEY layout.',
                                    'Confirm the CONSOLIDATE.COND segment positions for PRODUCT and SECTOR.'),
    'INCORRECT_CONSOL_KEY': ('Incorrect CONSOL_KEY construction', 'Correct the key extract or the configured layout.',
                             'Is the extract truncating or re-ordering key segments?'),
    'WRONG_DIMENSION': ('Wrong category / department / residence / currency / company', 'Correct the rule criterion or the source dimension.',
                        'Is the source dimension or the rule criterion wrong?'),
    'AMBIGUOUS_MAPPING': ('Ambiguous mapping (equally specific conflicting rules)', 'Set an explicit PRIORITY or narrow one rule.',
                          'Which rule is intended to win for the overlapping population?'),
    'DUPLICATE_RULE_OR_SOURCE': ('Duplicate rule or source record', 'Remove the duplicate or document why both rows are genuine.',
                                 'Are the repeated rows separate balances or an extract duplication?'),
    'MISSING_SOURCE_RECORD': ('Missing source record', 'Supply the missing account-level records or explain the TB line.',
                              'Is the account-level extract complete for this GL and date?'),
    'INTERNAL_ACCOUNT_MAPPING_DEFECT': ('Internal-account mapping defect', 'Correct the one-to-one internal account mapping.',
                                        'What is the authorised target account for these internal accounts?'),
    'PL_MAPPING_DEFECT': ('PL mapping defect', 'Add or correct the PL rule for the PL dimensions shown.',
                          'Which target PL GL applies to this PL category / product / department?'),
    'CONTRA_BL_TREATMENT': ('Contra / BL treatment unresolved', 'Define the contra (BL) treatment explicitly in a rule; keep it separate from gross.',
                            'Is the BL balance netted into the gross GL or reported on its own contra GL?'),
    'SIGN_CONVENTION_MISMATCH': ('Sign-convention mismatch', 'Confirm the signed convention of each source; do not flip signs to force agreement.',
                                 'Which sign convention does each extract use (debit-positive / credit-positive)?'),
    'TIMING_DIFFERENCE': ('Business-date / timing difference', 'Keep migrated opening and post-COB movements separate in the roll-forward.',
                          'Are all post-COB movements validated and dated after cutover?'),
    'ACTUAL_TB_DISCREPANCY': ('Actual TB discrepancy', 'Investigate the actual Temenos TB line (missing, extra or duplicated).',
                              'Is the actual TB extract complete and correctly dated?'),
    'GENUINE_UNEXPLAINED': ('Genuine unexplained difference', 'Investigate at account level; no automatic explanation applies.',
                            'Which postings explain the residual?'),
}


def _exc(category, level, engine, amount, reason, **kw):
    return {'category': category, 'level': level, 'engine': engine, 'amount': amount, 'reason': reason, **kw}


def classify_components(engines):
    out = []
    _orig_append = out.append

    def tag(c):
        def add(e):
            if not e.get('informational'):
                c['root_category'] = e['category']
            _orig_append(e)
        return add
    a = engines.get('A') or {}
    if a.get('status') == 'COMPLETE':
        rs = a['ruleset']
        near_cache = {}
        for c in a['components']:
            st = c['status']
            emit = tag(c)
            if c.get('duplicate_source'):
                emit(_exc('DUPLICATE_RULE_OR_SOURCE', 'COMPONENT', 'A', c['amount'], 'Repeated source row (account + CONSOL_KEY)',
                                account=c['account'], consol_key=c['ref'], balance_type=c['balance_type'], informational=True))
            if st == 'MAPPED':
                continue
            base = dict(account=c['account'], consol_key=c['ref'], balance_type=c['balance_type'], currency=c['currency'],
                        legacy_gl=c['legacy_gl'], candidates=c['candidates'], rules=c['candidate_rules'])
            if st == 'AMBIGUOUS':
                emit(_exc('AMBIGUOUS_MAPPING', 'COMPONENT', 'A', c['amount'],
                                f'Equally specific rules {", ".join(c["candidate_rules"])} map to different GLs', **base))
            elif st == 'MULTI_TARGET_UNRESOLVED':
                emit(_exc('MULTI_TARGET_ALLOCATION_UNRESOLVED', 'COMPONENT', 'A', c['amount'],
                                f'Rule lists several target GLs {", ".join(c["candidates"])} without allocation evidence', **base))
            elif st == 'CONTRA_UNRESOLVED':
                emit(_exc('CONTRA_BL_TREATMENT', 'COMPONENT', 'A', c['amount'],
                                f'Contra balance type {c["balance_type"]} has no rule naming it; kept separate from gross', **base))
            elif st == 'INVALID_KEY':
                emit(_exc('INCORRECT_CONSOL_KEY', 'COMPONENT', 'A', c['amount'], f'CONSOL_KEY not parseable: {c["reason"]}', **base))
            elif c.get('misalignment'):
                emit(_exc('PRODUCT_SECTOR_MISALIGNMENT', 'COMPONENT', 'A', c['amount'],
                                f'No rule matches; would match {", ".join(c["misalignment_rules"])} if rule column '
                                f'{c["misalignment"].split("->")[0].upper()} were read as key segment {c["misalignment"].split("->")[1]}',
                                diagnostic='POSSIBLE_MAPPING_COLUMN_MISALIGNMENT', **{**base, 'rules': c['misalignment_rules']}))
            else:
                memo = (c['ref'], c['balance_type'])
                if memo not in near_cache:
                    near_cache[memo] = near_miss(rs, c['dims'], c['balance_type'])
                kind, detail, rules_ = near_cache[memo]
                if kind == 'BT':
                    emit(_exc('WRONG_OR_MISSING_BALANCE_TYPE', 'COMPONENT', 'A', c['amount'],
                                    f'No rule allocates source balance type {c["balance_type"]}'
                                    + (f'; rule(s) {", ".join(rules_)} match every other dimension' if rules_ else ''),
                                    **{**base, 'rules': rules_}))
                elif kind == 'DIM':
                    emit(_exc('WRONG_DIMENSION', 'COMPONENT', 'A', c['amount'],
                                    f'Rule(s) {", ".join(rules_)} would match except for {detail} = {c["dims"].get(detail, "")!r}',
                                    dimension=detail, **{**base, 'rules': rules_}))
                else:
                    emit(_exc('MISSING_MAPPING', 'COMPONENT', 'A', c['amount'],
                                    f'No rule for balance type {c["balance_type"]} and category {c["dims"].get("category", "")}', **base))
        for u in a.get('unsupported_balance_types') or []:
            out.append(_exc('WRONG_OR_MISSING_BALANCE_TYPE', 'RULE', 'A', None,
                            f'Rule {u["rule_id"]} uses balance type {u["balance_type"]} that the source schema does not provide '
                            '(amount unavailable, not zero)', balance_type=u['balance_type'], rules=[u['rule_id']], candidates=u['targets']))
    b = engines.get('B') or {}
    if b.get('status') == 'COMPLETE':
        for c in b['components']:
            emit = tag(c)
            base = dict(account=c['account'], currency=c['currency'], legacy_gl=c['legacy_gl'], subtype=c['status'],
                        customer_ref=c.get('customer_ref', ''))
            if c['status'] != 'MAPPED':
                emit(_exc('INTERNAL_ACCOUNT_MAPPING_DEFECT', 'COMPONENT', 'B', c['amount'], c['reason'], **base))
            for f in c.get('flags') or []:
                emit(_exc('INTERNAL_ACCOUNT_MAPPING_DEFECT', 'COMPONENT', 'B', c['amount'],
                                f'{f}: target account {c["target_account"]} for source currency {c["currency"]}',
                                target_gl=c['target_gl'], **{**base, 'subtype': f}))
            if c.get('duplicate_source'):
                emit(_exc('DUPLICATE_RULE_OR_SOURCE', 'COMPONENT', 'B', c['amount'], 'Internal account appears more than once in the source',
                                informational=True, **base))
    cc = engines.get('C') or {}
    if cc.get('status') == 'COMPLETE':
        for c in cc['components']:
            if c['status'] == 'MAPPED':
                continue
            tag(c)(_exc('PL_MAPPING_DEFECT', 'COMPONENT', 'C', c['amount'],
                            {'NO_RULE': 'No PL rule matches', 'AMBIGUOUS': 'Equally specific PL rules conflict',
                             'MULTI_TARGET_UNRESOLVED': 'PL rule lists several targets', 'INVALID_KEY': f'PL key invalid: {c["reason"]}'}
                            .get(c['status'], c['status']), subtype=c['status'], consol_key=c['ref'], currency=c['currency'],
                            pl_category=c['dims'].get('pl_category', ''), legacy_gl=c['legacy_gl'], candidates=c['candidates'],
                            rules=c['candidate_rules']))
    return out


def near_miss(rs, dims, bt):
    """('BT', None, rules) when rules match all dimensions but not the balance type; ('DIM', dim, rules) when exactly one
    dimension blocks; (None, None, [])."""
    if bt not in rs.by_bt:
        full = [r for r in rs.rules if r.usable and all(c.matches(dims.get(d)) for d, c in r.crit.items())]
        return 'BT', None, sorted(r.id for r in full)[:5]
    pool = [r for r in rs.by_bt.get(bt, ())]
    hits = defaultdict(list)
    for r in pool:
        failing = [d for d, c in r.crit.items() if not c.matches(dims.get(d))]
        if len(failing) == 1:
            hits[failing[0]].append(r.id)
    if len(hits) == 1:
        d, ids = next(iter(hits.items()))
        return 'DIM', d, sorted(ids)[:5]
    return None, None, []


STATUS_CATEGORY = {'AMBIGUOUS': 'AMBIGUOUS_MAPPING', 'MULTI_TARGET_UNRESOLVED': 'MULTI_TARGET_ALLOCATION_UNRESOLVED',
                   'MISSING_MAPPING': 'MISSING_MAPPING', 'NO_RULE': 'MISSING_MAPPING', 'CONTRA_UNRESOLVED': 'CONTRA_BL_TREATMENT',
                   'INVALID_KEY': 'INCORRECT_CONSOL_KEY'}


def open_items(recon, engines):
    """(target_gl, ccy) -> {category: amount} of unallocated money that may belong to that GL: candidates of ambiguous /
    multi-target items, or the authorised GL-mapping targets of the item's legacy GL."""
    gmap = recon.get('gmap') or {}
    out = defaultdict(lambda: defaultdict(lambda: ZERO))
    items = [(c['legacy_gl'], c['currency'], c['amount'], c['candidates'], c.get('root_category') or STATUS_CATEGORY.get(c['status'], 'MISSING_MAPPING'))
             for e in engines.values() for c in e.get('components') or [] if c['status'] != 'MAPPED']
    items += [(u['legacy_gl'], u['currency'], u['amount'], u['candidates'], STATUS_CATEGORY.get(u['status'], 'MISSING_MAPPING'))
              for u in recon['unallocated'] if not u.get('engine')]
    for lgl, ccy, amt, cands, cat in items:
        targets = set(cands or ()) or set(gmap.get((lgl, ccy)) or gmap.get((lgl, '')) or ())
        for t in targets:
            out[(t, ccy)][cat] += amt
    return out


def classify_gl(recon, tol, engines=None):
    """Classify GL-level residual differences after the roll-forward. Each open GL line gets exactly one
    classification row for its residual; explained timing amounts are separate informational rows."""
    out = []
    excluded = defaultdict(lambda: ZERO)
    for m in recon['movements_excluded']:
        if m['amount'] is not None:
            excluded[(m['target_gl'], m['currency'])] += m['amount']
        out.append(_exc('TIMING_DIFFERENCE', 'GL', 'TB', m['amount'], 'Movement excluded from roll-forward: ' + m['reason'],
                        target_gl=m['target_gl'], currency=m['currency'], informational=True))
    for r in recon['gl_rows']:
        if r['post_cob_movements']:
            out.append(_exc('TIMING_DIFFERENCE', 'GL', 'TB', r['post_cob_movements'],
                            'Validated post-COB movements separated from the migrated opening balance (explained, not a migration error)',
                            target_gl=r['target_gl'], currency=r['currency'], informational=True))
    opens = open_items(recon, engines or {})
    gaps = defaultdict(lambda: ZERO)
    for ln in recon['legacy_lines']:
        if ln['status'] == 'POPULATION_GAP':
            gaps[(ln['legacy_gl'], ln['currency'])] += ln['gap']
    rows = []
    for r in recon['gl_rows']:
        if r['recon_status'] not in ('DIFFERENCE', 'EXPECTED_ONLY', 'ACTUAL_ONLY', 'INCOMPLETE'):
            continue
        k = (r['target_gl'], r['currency'])
        timing = excluded.get(k, ZERO)
        resid = r['difference'] - timing
        if within(r['difference'], r['expected'], r['actual_opening'], tol):
            continue
        if timing and within(resid, r['expected'], r['actual_opening'], tol):
            out.append(_exc('TIMING_DIFFERENCE', 'GL', 'TB', r['difference'],
                            f'Difference equals movements excluded from the roll-forward ({timing}): business-date / validation issue',
                            target_gl=r['target_gl'], currency=r['currency'], confidence='HIGH'))
            continue
        rows.append((r, resid, timing))
    done = set()

    def emit(cat, r, amount, why, conf, **kw):
        done.add((r['target_gl'], r['currency']))
        extra = f' (after {r["_timing"]} excluded movements, timing)' if r.get('_timing') else ''
        out.append(_exc(cat, 'GL', 'TB', amount, why + extra, target_gl=r['target_gl'], currency=r['currency'], confidence=conf, **kw))
    for r, resid, timing in rows:
        r['_timing'] = timing
        if r['expected'] and within(r['actual_opening'] - timing + r['expected'], r['expected'], r['actual_opening'], tol):
            emit('SIGN_CONVENTION_MISMATCH', r, resid, f'Actual {r["actual_opening"]} is the negative of expected {r["expected"]}', 'HIGH')
    for i, (r, resid, _t) in enumerate(rows):
        if (r['target_gl'], r['currency']) in done or not resid:
            continue
        for s, resid2, _t2 in rows[i + 1:]:
            k2 = (s['target_gl'], s['currency'])
            if k2 in done or not within(resid + resid2, resid, resid2, tol):
                continue
            if r['target_gl'] == s['target_gl']:
                cat, why = 'WRONG_DIMENSION', f'Offsetting differences across currencies {r["currency"]} / {s["currency"]} on {r["target_gl"]}'
            elif r['currency'] == s['currency']:
                cat, why = 'WRONG_TARGET_GL', (f'Offsetting differences: {r["target_gl"]} {resid} and {s["target_gl"]} {resid2} '
                                               f'({r["currency"]}) indicate balances booked to / expected on the other GL')
            else:
                continue
            emit(cat, r, resid, why, 'MEDIUM', paired_with=f'{s["target_gl"]} {s["currency"]}', dimension='currency' if cat == 'WRONG_DIMENSION' else None)
            emit(cat, s, resid2, why, 'MEDIUM', paired_with=f'{r["target_gl"]} {r["currency"]}', dimension='currency' if cat == 'WRONG_DIMENSION' else None)
            break
    for r, resid, timing in rows:
        k = (r['target_gl'], r['currency'])
        if k in done:
            continue
        gap = sum((gaps.get((lg, r['currency']), ZERO) for lg in r['legacy_gls']), ZERO)
        if gap and within(resid - gap, resid, gap, tol):
            emit('MISSING_SOURCE_RECORD', r, resid, f'Difference equals the legacy TB - account population gap {gap} of legacy '
                 f'GL(s) {", ".join(r["legacy_gls"])}', 'MEDIUM')
            continue
        cats = {c: v for c, v in opens.get(k, {}).items() if v}
        total = sum(cats.values(), ZERO)
        if cats:
            primary = max(cats, key=lambda c: abs(cats[c]))
            detail = ', '.join(f'{c} {v}' for c, v in sorted(cats.items()))
            subset = None
            names = sorted(cats)
            if len(names) <= 10:
                for mask in range(1, 1 << len(names)):
                    pick = [names[i] for i in range(len(names)) if mask >> i & 1]
                    sm = sum((cats[x] for x in pick), ZERO)
                    if within(resid - sm, resid, sm, tol) and (subset is None or len(pick) < len(subset)):
                        subset = pick
            if subset and not within(resid - total, resid, total, tol):
                emit(max(subset, key=lambda c: abs(cats[c])), r, resid,
                     f'Difference exactly explained by the unallocated {" + ".join(subset)} items that may belong to this GL '
                     f'(all candidate items: {detail})', 'HIGH' if len(subset) == 1 else 'MEDIUM',
                     explained=sum((cats[x] for x in subset), ZERO))
            elif within(resid - total, resid, total, tol):
                emit(primary, r, resid, f'Difference fully explained by unallocated items that may belong to this GL: {detail}',
                     'HIGH' if len(cats) == 1 else 'MEDIUM', explained=total)
            else:
                emit(primary, r, resid, f'Difference {resid}; unallocated items that may belong to this GL total {total} ({detail}); '
                     f'residual {resid - total} not explained by them', 'LOW', explained=total)
            continue
        if r['recon_status'] == 'INCOMPLETE':
            reason = r['exception_reason']
            emit('WRONG_OR_MISSING_BALANCE_TYPE' if 'balance type' in reason else 'MULTI_TARGET_ALLOCATION_UNRESOLVED'
                 if 'multi-target' in reason else 'PL_MAPPING_DEFECT' if 'PL' in reason else 'AMBIGUOUS_MAPPING',
                 r, resid, f'Difference {resid} with open allocation items: {reason}', 'LOW')
        elif r['recon_status'] == 'ACTUAL_ONLY' and any(
                u['status'] == 'MISSING_MAPPING' and u['currency'] == r['currency'] and within(u['amount'] - resid, resid, u['amount'], tol)
                for u in recon['unallocated'] if not u.get('engine')):
            lg = [u['legacy_gl'] for u in recon['unallocated'] if not u.get('engine') and u['status'] == 'MISSING_MAPPING'
                  and u['currency'] == r['currency'] and within(u['amount'] - resid, resid, u['amount'], tol)]
            emit('MISSING_MAPPING', r, resid, f'Actual-only line equals the amount of unmapped legacy GL(s) {", ".join(lg)}: '
                 'probable missing GL-mapping row', 'MEDIUM')
        elif r['recon_status'] in ('ACTUAL_ONLY', 'EXPECTED_ONLY'):
            emit('ACTUAL_TB_DISCREPANCY', r, resid, r['exception_reason'] + '; no unallocated source item can explain it', 'MEDIUM')
        else:
            emit('GENUINE_UNEXPLAINED', r, resid, f'Residual {resid} after timing, sign, pairing, completeness and open-item tests', 'LOW')
    for r, _x, _y in rows:
        r.pop('_timing', None)
    return out


def _group_key(e):
    c = e['category']
    if e['level'] == 'GL':
        return (c, 'GL lines')
    if c == 'PRODUCT_SECTOR_MISALIGNMENT':
        return (c, 'rules ' + ','.join(e.get('rules') or []))
    if c in ('MISSING_MAPPING',) and e['level'] == 'COMPONENT':
        return (c, f'balance type {e.get("balance_type")}')
    if c == 'WRONG_DIMENSION':
        return (c, f'{e.get("dimension")} vs rules {",".join(e.get("rules") or [])}')
    if c in ('WRONG_OR_MISSING_BALANCE_TYPE', 'CONTRA_BL_TREATMENT'):
        return (c, f'balance type {e.get("balance_type")}')
    if c == 'AMBIGUOUS_MAPPING':
        return (c, 'rules ' + ','.join(e.get('rules') or []))
    if c == 'MULTI_TARGET_ALLOCATION_UNRESOLVED':
        return (c, f'legacy GL {e.get("legacy_gl")}' if e['level'] != 'COMPONENT' else 'rules ' + ','.join(e.get('rules') or []))
    if c == 'INTERNAL_ACCOUNT_MAPPING_DEFECT':
        return (c, e.get('subtype'))
    if c == 'PL_MAPPING_DEFECT':
        return (c, f'{e.get("subtype")} PL category {e.get("pl_category")}')
    if c == 'INCORRECT_CONSOL_KEY':
        return (c, e['reason'])
    if c == 'WRONG_TARGET_GL' and e['level'] == 'RULE':
        return (c, f'rule {e.get("rule_id")}')
    return (c, e['level'])


def systemic(exceptions, diagnostics=()):
    groups = defaultdict(list)
    for e in exceptions:
        groups[(e['level'] if e['level'] != 'RULE' else 'RULE',) + _group_key(e)].append(e)
    out = []
    for (level, cat, key), es in groups.items():
        amts = [e['amount'] for e in es if e['amount'] is not None]
        accounts = {e.get('account') for e in es if e.get('account')}
        rules_ = sorted({r for e in es for r in (e.get('rules') or ([e['rule_id']] if e.get('rule_id') else []))})
        title, action, question = CATEGORIES[cat]
        confs = [e.get('confidence') for e in es if e.get('confidence')]
        conf = confs[0] if confs else ('HIGH' if cat in ('MISSING_MAPPING', 'CONTRA_BL_TREATMENT', 'INCORRECT_CONSOL_KEY',
                                                          'INTERNAL_ACCOUNT_MAPPING_DEFECT', 'AMBIGUOUS_MAPPING',
                                                          'MULTI_TARGET_ALLOCATION_UNRESOLVED', 'MISSING_SOURCE_RECORD') else 'MEDIUM')
        out.append({'category': cat, 'title': title, 'level': level, 'group': key, 'records': len(es),
                    'accounts': len(accounts), 'net_amount': sum(amts, ZERO) if amts else None,
                    'absolute_amount': sum((abs(x) for x in amts), ZERO) if amts else None,
                    'amount_measurable': bool(amts), 'related_rules': rules_[:30],
                    'informational': all(e.get('informational') for e in es),
                    'proposed_action': action, 'confidence': conf, 'open_question': question,
                    'evidence': [e['reason'] for e in es[:3]]})
    out.sort(key=lambda g: (g['informational'], -(g['absolute_amount'] or ZERO), g['category']))
    for i, g in enumerate(out, 1):
        g['issue_id'] = f'RC{i:04d}'
    return out


def worklist(engines, recon, exceptions):
    items = []
    a = engines.get('A') or {}
    if a.get('status') == 'COMPLETE':
        rs = a['ruleset']
        by_id = {r.id: r for r in rs.rules}
        for f in a.get('misalignment') or []:
            if not f.get('rule_column'):
                continue
            x, y = f['rule_column'], f['observed_dimension'].upper()
            for rid in f['affected_rules']:
                r = by_id[rid]
                ox, oy = r.raw.get(x, ''), r.raw.get(y, '')
                if oy:
                    continue
                items.append({'kind': 'RULE_COLUMN_CORRECTION', 'file': 'gl_rules', 'rule_id': rid, 'source_row': r.row,
                              'original_value': f'{x}={ox!r}; {y}={oy!r}', 'proposed_value': f'{x}=\'\'; {y}={ox!r}',
                              'change': {'row': r.row, 'set': {x: '', y: ox}}, 'auto_applicable': True,
                              'reason': 'POSSIBLE_MAPPING_COLUMN_MISALIGNMENT', 'evidence': f['evidence'],
                              'amount_affected': f['net_amount'], 'confidence': 'MEDIUM'})
        schema = a.get('schema') or []
        for u in a.get('unsupported_balance_types') or []:
            close = difflib.get_close_matches(u['balance_type'], schema, n=1, cutoff=0.85)
            items.append({'kind': 'BALANCE_TYPE_ALIAS' if close else 'BALANCE_TYPE_DEFINITION', 'file': 'config/tb_recon.json',
                          'rule_id': u['rule_id'], 'source_row': u['row'], 'original_value': u['balance_type'],
                          'proposed_value': f'alias {u["balance_type"]} -> {close[0]}' if close else 'OWNER: supply the source column or remove',
                          'change': None, 'auto_applicable': False, 'reason': 'UNSUPPORTED_BALANCE_TYPE',
                          'evidence': u['reason'], 'amount_affected': None, 'confidence': 'LOW'})
        amb = defaultdict(lambda: ZERO)
        for e in exceptions:
            if e['category'] == 'AMBIGUOUS_MAPPING' and e['engine'] == 'A' and e['level'] == 'COMPONENT':
                amb[tuple(e['rules'])] += e['amount']
        for k, v in sorted(amb.items()):
            items.append({'kind': 'SET_PRIORITY', 'file': 'gl_rules', 'rule_id': ', '.join(k), 'source_row': None,
                          'original_value': 'equal specificity, different targets', 'proposed_value': 'OWNER: set PRIORITY or narrow one rule',
                          'change': None, 'auto_applicable': False, 'reason': 'AMBIGUOUS_MAPPING',
                          'evidence': f'Conflicting targets {", ".join(sorted({t for r in k for t in by_id[r].targets}))}; net {v} unallocated',
                          'amount_affected': v, 'confidence': 'HIGH'})
        gmap = recon.get('gmap') or {}
        ruled = set(rs.by_bt)
        orphan = defaultdict(lambda: [ZERO, set(), set()])
        for c in a['components']:
            if c['balance_type'] not in ruled and c['status'] in ('NO_RULE', 'CONTRA_UNRESOLVED'):
                o = orphan[(c['balance_type'], c['status'])]
                o[0] += c['amount']
                o[1].add(c['legacy_gl'])
                o[2].update(gmap.get((c['legacy_gl'], c['currency'])) or gmap.get((c['legacy_gl'], '')) or ())
        used = {t for r in rs.rules for t in r.targets}
        for (bt, st), (v, lgls, tg) in sorted(orphan.items()):
            free = sorted(tg - used)
            items.append({'kind': 'NEW_RULE_FOR_BALANCE_TYPE' if st == 'NO_RULE' else 'CONTRA_TREATMENT_RULE', 'file': 'gl_rules',
                          'rule_id': bt, 'source_row': None, 'original_value': f'no rule allocates {bt}',
                          'proposed_value': 'OWNER: add a rule for ' + bt + (f'; authorised GL-mapping targets not used by any rule: {", ".join(free)}'
                                                                           if free else ''),
                          'change': None, 'auto_applicable': False, 'reason': 'WRONG_OR_MISSING_BALANCE_TYPE' if st == 'NO_RULE' else 'CONTRA_BL_TREATMENT',
                          'evidence': f'Source balance type {bt} on legacy GL(s) {", ".join(sorted(x for x in lgls if x))}',
                          'amount_affected': v, 'confidence': 'MEDIUM' if len(free) == 1 else 'LOW'})
    b = engines.get('B') or {}
    if b.get('status') == 'COMPLETE':
        for c in b['components']:
            if c['status'] in ('MISSING_MAPPING', 'DUPLICATE_MAPPING', 'INVALID_TARGET', 'CUSTOMER_REF_UNRESOLVED'):
                items.append({'kind': 'INTERNAL_MAPPING', 'file': 'internal_mapping' if not c['customer_ref'] else 'customer_account_mapping',
                              'rule_id': c['ref'], 'source_row': c['source_row'], 'original_value': c['reason'],
                              'proposed_value': 'OWNER: supply the single authorised target account and GL', 'change': None,
                              'auto_applicable': False, 'reason': c['status'], 'evidence': f'Source row {c["source_row"]}',
                              'amount_affected': c['amount'], 'confidence': 'HIGH'})
    for u in recon['unallocated']:
        if u['status'] == 'MULTI_TARGET_UNRESOLVED' and not u.get('engine'):
            items.append({'kind': 'ALLOCATION_RULE_DESIGN', 'file': 'gl_mapping', 'rule_id': u['legacy_gl'], 'source_row': None,
                          'original_value': ', '.join(u['candidates']), 'proposed_value': 'OWNER: define allocation by balance type / status / category',
                          'change': None, 'auto_applicable': False, 'reason': 'MULTI_TARGET_ALLOCATION_UNRESOLVED',
                          'evidence': f'Legacy GL {u["legacy_gl"]} {u["currency"]} has no account-level population',
                          'amount_affected': u['amount'], 'confidence': 'HIGH'})
    for e in exceptions:
        if e['category'] == 'SIGN_CONVENTION_MISMATCH':
            items.append({'kind': 'SIGN_CONVENTION_REVIEW', 'file': 'config/tb_recon.json', 'rule_id': e['target_gl'], 'source_row': None,
                          'original_value': 'current sign_convention', 'proposed_value': 'OWNER: confirm source sign convention with evidence',
                          'change': None, 'auto_applicable': False, 'reason': e['category'], 'evidence': e['reason'],
                          'amount_affected': e['amount'], 'confidence': 'MEDIUM'})
    for i, it in enumerate(items, 1):
        it['proposal_id'] = f'PC{i:04d}'
        it['status'] = 'PROPOSED'
    return items


def apply_worklist(rule_rows, items, only=None):
    """Return a corrected COPY of the rule rows for auto-applicable proposals; the original list is untouched."""
    rows = copy.deepcopy(rule_rows)
    by_row = {r['_row']: r for r in rows}
    applied = []
    for it in items:
        if not it.get('auto_applicable') or not it.get('change') or (only and it['proposal_id'] not in only):
            continue
        r = by_row.get(it['change']['row'])
        if r is None:
            continue
        r.update(it['change']['set'])
        applied.append(it['proposal_id'])
    return rows, applied
