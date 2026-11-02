"""Whole-TB reconstruction and controlled final aggregation.

Legacy cut-off TB + authorised mappings -> independently expected Temenos TB -> actual TB -> difference.

Legacy TB lines covered by an account-level population (engines A/B/C, linked by LEGACY_GL) are
reconstructed from that population; the TB-versus-population gap is a completeness exception and is
never allocated to a target GL. Lines without a population form the explicitly labelled DIRECT stream,
mapped through the legacy GL mapping only when it has exactly one target. Several targets without
account-level allocation evidence stay MULTI_TARGET_UNRESOLVED - never first GL, equal split or forced zero.
"""
from __future__ import annotations

from collections import defaultdict
from decimal import Decimal

from .criteria import split_items
from .tables import amount, text

ZERO = Decimal(0)
STREAMS = ('A', 'B', 'C', 'D')


def tolerance(cfg):
    t = cfg.get('tolerance') or {}
    return Decimal(str(t.get('absolute', '0.01'))), Decimal(str(t.get('relative', '0')))


def within(diff, a, b, tol):
    absolute, relative = tol
    return abs(diff) <= max(absolute, relative * max(abs(a), abs(b)))


def _date(v):
    if v is None:
        return ''
    if hasattr(v, 'date') and callable(getattr(v, 'date')):
        return v.date().isoformat()
    if hasattr(v, 'isoformat'):
        return v.isoformat()
    s = text(v)
    if len(s) == 8 and s.isdigit():
        return f'{s[:4]}-{s[4:6]}-{s[6:]}'
    return s[:10]


def gl_mapping_index(rows):
    idx, diags = defaultdict(set), []
    seen = defaultdict(set)
    for r in rows or []:
        gl = text(r.get('LEGACY_GL')).upper()
        if not gl:
            continue
        ccy = text(r.get('CURRENCY')).upper()
        tg = text(r.get('TARGET_GL')).upper()
        targets = split_items(tg) if tg else []
        if not targets:
            diags.append({'type': 'GL_MAPPING_WITHOUT_TARGET', 'legacy_gl': gl, 'currency': ccy, 'row': r['_row']})
        seen[(gl, ccy)].add(tuple(targets))
        idx[(gl, ccy)].update(targets)
    for k, v in seen.items():
        if len(v) > 1:
            diags.append({'type': 'GL_MAPPING_REPEATED_ROWS', 'legacy_gl': k[0], 'currency': k[1],
                          'variants': sorted('|'.join(x) for x in v)})
    return idx, diags


def lookup(idx, gl, ccy):
    return sorted(idx.get((gl, ccy)) or idx.get((gl, '')) or ())


def classify(cfg, gl):
    for p, cls in ((cfg.get('gl_class_from_target') or {}).get('prefixes') or {}).items():
        if gl.startswith(p):
            return cls
    return ''


def reconstruct(inputs, engines, cfg):
    tol = tolerance(cfg)
    sc = cfg.get('sign_convention') or {}
    s_legacy, s_actual = Decimal(str(sc.get('legacy_tb', 1))), Decimal(str(sc.get('actual_tb', 1)))
    exceptions = []
    # 1. legacy TB
    legacy, legacy_class, legacy_rows = defaultdict(lambda: ZERO), {}, defaultdict(int)
    legacy_total = ZERO
    for r in inputs.get('legacy_tb') or []:
        gl, ccy = text(r.get('LEGACY_GL')).upper(), text(r.get('CURRENCY')).upper()
        a = amount(r.get('BALANCE'))
        if not gl or a is None:
            exceptions.append({'category': 'MISSING_SOURCE_RECORD', 'level': 'LEGACY_TB', 'legacy_gl': gl, 'currency': ccy,
                               'amount': ZERO, 'reason': f'Legacy TB row {r["_row"]} has no GL or amount'})
            continue
        a *= s_legacy
        legacy[(gl, ccy)] += a
        legacy_rows[(gl, ccy)] += 1
        legacy_total += a
        if text(r.get('CLASS')):
            legacy_class[gl] = text(r.get('CLASS')).upper()
    for k, n in legacy_rows.items():
        if n > 1:
            exceptions.append({'category': 'DUPLICATE_RULE_OR_SOURCE', 'level': 'LEGACY_TB', 'legacy_gl': k[0], 'currency': k[1],
                               'amount': legacy[k], 'reason': f'{n} legacy TB rows for the same GL and currency (summed, flagged)'})
    gmap, gmap_diags = gl_mapping_index(inputs.get('gl_mapping'))
    # 2. engine populations by legacy GL
    pop, pop_engines = defaultdict(lambda: ZERO), defaultdict(set)
    for e in engines.values():
        for k, v in (e.get('population') or {}).items():
            pop[k] += v
            pop_engines[k].add(e['engine'])
    expected = defaultdict(lambda: defaultdict(lambda: ZERO))
    legacy_of_gl = defaultdict(set)
    for e in engines.values():
        for k, v in (e.get('expected') or {}).items():
            expected[k][e['engine']] += v
        for c in e.get('components') or []:
            if c['status'] == 'MAPPED' and c['legacy_gl']:
                legacy_of_gl[(c['target_gl'], c['currency'])].add(c['legacy_gl'])
    pl_pending = (engines.get('C') or {}).get('status') == 'SOURCE_PENDING'
    legacy_lines, unallocated = [], []
    multi_candidates = defaultdict(lambda: ZERO)
    totals = defaultdict(lambda: ZERO)
    for (gl, ccy), a in sorted(legacy.items()):
        line = {'legacy_gl': gl, 'currency': ccy, 'class': legacy_class.get(gl, ''), 'tb_amount': a}
        if (gl, ccy) in pop:
            p = pop[(gl, ccy)]
            gap = a - p
            line.update(stream='/'.join(sorted(pop_engines[(gl, ccy)])), population=p, gap=gap, targets=lookup(gmap, gl, ccy),
                        status='POPULATION_COMPLETE' if within(gap, a, p, tol) else 'POPULATION_GAP')
            totals['covered_tb'] += a
            totals['population_linked'] += p
            if not within(gap, a, p, tol):
                totals['population_gap'] += gap
                exceptions.append({'category': 'MISSING_SOURCE_RECORD', 'level': 'LEGACY_GL', 'legacy_gl': gl, 'currency': ccy,
                                   'amount': gap, 'reason': f'Legacy TB {a} vs account-level population {p} '
                                                           f'(engines {line["stream"]}); gap not allocated to any target GL'})
        else:
            targets = lookup(gmap, gl, ccy)
            line.update(stream='D', population=None, gap=None, targets=targets)
            if a == 0:
                line['status'] = 'ZERO_BALANCE'
            elif pl_pending and line['class'] == 'PL':
                # Never fall back to the GL mapping for PL while the PL source is missing: that would be a false success.
                line['status'] = 'SOURCE_PENDING'
                line['stream'] = 'C'
                totals['pending'] += a
            elif not targets:
                line['status'] = 'UNMAPPED_LEGACY_GL'
                totals['direct_unallocated'] += a
                unallocated.append({'legacy_gl': gl, 'currency': ccy, 'amount': a, 'status': 'MISSING_MAPPING', 'candidates': []})
                exceptions.append({'category': 'MISSING_MAPPING', 'level': 'LEGACY_GL', 'legacy_gl': gl, 'currency': ccy,
                                   'amount': a, 'reason': 'Legacy GL has no target in the GL mapping and no account-level population'})
            elif len(targets) > 1:
                line['status'] = 'MULTI_TARGET_UNRESOLVED'
                totals['direct_unallocated'] += a
                for t in targets:
                    multi_candidates[(t, ccy)] += a
                unallocated.append({'legacy_gl': gl, 'currency': ccy, 'amount': a, 'status': 'MULTI_TARGET_UNRESOLVED', 'candidates': targets})
                exceptions.append({'category': 'MULTI_TARGET_ALLOCATION_UNRESOLVED', 'level': 'LEGACY_GL', 'legacy_gl': gl,
                                   'currency': ccy, 'amount': a, 'candidates': targets,
                                   'reason': f'Legacy GL maps to {len(targets)} target GLs ({", ".join(targets)}) and no '
                                             'account-level balance-type / status / category evidence allocates it'})
            else:
                line['status'] = 'DIRECT_MAPPED'
                expected[(targets[0], ccy)]['D'] += a
                legacy_of_gl[(targets[0], ccy)].add(gl)
                totals['direct_mapped'] += a
        legacy_lines.append(line)
    for k, p in pop.items():
        if k not in legacy:
            totals['population_unlinked'] += p
            exceptions.append({'category': 'MISSING_SOURCE_RECORD', 'level': 'LEGACY_GL', 'legacy_gl': k[0], 'currency': k[1],
                               'amount': p, 'reason': 'Account-level population carries a legacy GL / currency that is not in the legacy TB'})
    # engine components without legacy GL link, and engine targets outside the authorised GL mapping
    conflict = defaultdict(lambda: [ZERO, 0, set()])
    for e in engines.values():
        for c in e.get('components') or []:
            if not c['legacy_gl']:
                totals['population_unlinked'] += c['amount']
            if c['status'] != 'MAPPED':
                totals['engine_unresolved'] += c['amount']
                unallocated.append({'legacy_gl': c['legacy_gl'], 'currency': c['currency'], 'amount': c['amount'],
                                    'status': c['status'], 'candidates': c['candidates'], 'engine': c['engine'],
                                    'account': c['account'], 'balance_type': c['balance_type']})
                continue
            totals['engine_mapped'] += c['amount']
            allowed = lookup(gmap, c['legacy_gl'], c['currency']) if c['legacy_gl'] else []
            if allowed and c['target_gl'] not in allowed:
                k = (c['engine'], c['legacy_gl'], c['currency'], c['target_gl'], c['rule_id'])
                conflict[k][0] += c['amount']
                conflict[k][1] += 1
                conflict[k][2].add(c['account'])
                c['gl_mapping_conflict'] = allowed
    for (eng, lgl, ccy, tgl, rule), (amt, n, accts) in sorted(conflict.items()):
        exceptions.append({'category': 'WRONG_TARGET_GL', 'level': 'RULE', 'engine': eng, 'legacy_gl': lgl, 'currency': ccy,
                           'target_gl': tgl, 'rule_id': rule, 'amount': amt, 'records': n, 'accounts': len(accts),
                           'candidates': lookup(gmap, lgl, ccy),
                           'reason': f'Rule {rule} allocates to {tgl}, which is not among the authorised GL-mapping targets '
                                     f'{", ".join(lookup(gmap, lgl, ccy))} for legacy GL {lgl}'})
    # 3. actual TB, movements, roll-forward
    actual, actual_class, actual_dates = defaultdict(lambda: ZERO), {}, defaultdict(lambda: ZERO)
    actual_rows = defaultdict(int)
    for r in inputs.get('actual_tb') or []:
        gl, ccy = text(r.get('TARGET_GL')).upper(), text(r.get('CURRENCY')).upper()
        a = amount(r.get('BALANCE'))
        if not gl or a is None:
            continue
        actual[(gl, ccy)] += a * s_actual
        actual_rows[(gl, ccy)] += 1
        actual_dates[_date(r.get('BUSINESS_DATE'))] += 1
        if text(r.get('CLASS')):
            actual_class[gl] = text(r.get('CLASS')).upper()
    for k, n in actual_rows.items():
        if n > 1:
            exceptions.append({'category': 'ACTUAL_TB_DISCREPANCY', 'level': 'ACTUAL_TB', 'target_gl': k[0], 'currency': k[1],
                               'amount': actual[k], 'reason': f'{n} actual TB rows for one GL / currency (summed, flagged)'})
    cutover = cfg.get('cutover_date')
    tb_dates = sorted(d for d in actual_dates if d)
    tb_date = tb_dates[-1] if tb_dates else ''
    movements, mov_types, mov_excluded = defaultdict(lambda: ZERO), defaultdict(lambda: defaultdict(lambda: ZERO)), []
    for r in inputs.get('post_cob_movements') or []:
        gl, ccy = text(r.get('TARGET_GL')).upper(), text(r.get('CURRENCY')).upper()
        a, d = amount(r.get('BALANCE')), _date(r.get('BUSINESS_DATE'))
        validated = text(r.get('VALIDATED')).upper() not in ('N', 'NO', 'FALSE', '0')
        reason = None
        if a is None or not gl:
            reason = 'missing GL or amount'
        elif not cutover:
            reason = 'no cutover_date configured: movements cannot be placed before/after migration'
        elif not d:
            reason = 'movement has no business date'
        elif d <= cutover:
            reason = f'dated {d}, on or before cutover {cutover}: belongs to the migrated balance, not post-COB'
        elif tb_date and d > tb_date:
            reason = f'dated {d}, after the actual TB date {tb_date}'
        elif not validated:
            reason = 'movement not validated'
        if reason:
            mov_excluded.append({'row': r['_row'], 'target_gl': gl, 'currency': ccy, 'amount': a, 'date': d, 'reason': reason})
            continue
        movements[(gl, ccy)] += a
        mov_types[(gl, ccy)][text(r.get('MOVEMENT_TYPE')).upper() or 'UNSPECIFIED'] += a
    # 4. GL-level reconciliation
    incomplete = defaultdict(set)
    for e in engines.values():
        for g, reasons in (e.get('incomplete_gls') or {}).items():
            incomplete[g].update(reasons)
    for (g, _ccy) in multi_candidates:
        incomplete[g].add('candidate target of a multi-target legacy GL left unallocated')
    pending = {k for k, e in engines.items() if e.get('status') == 'SOURCE_PENDING'}
    gl_rows = []
    for key in sorted(set(expected) | set(actual) | set(multi_candidates)):
        gl, ccy = key
        streams = expected.get(key, {})
        exp = sum(streams.values(), ZERO)
        act = actual.get(key, ZERO)
        mov = movements.get(key, ZERO)
        opening_actual = act - mov
        diff = opening_actual - exp
        lg = sorted(legacy_of_gl.get(key, ()))
        cls = actual_class.get(gl) or next((legacy_class[x] for x in lg if x in legacy_class), '') or classify(cfg, gl) or 'UNKNOWN'
        reasons = sorted(incomplete.get(gl, ()))
        if cls == 'PL' and 'C' in pending and not streams:
            status, why = 'SOURCE_PENDING', engines['C'].get('reason', 'PL source pending')
        elif reasons and not within(diff, exp, opening_actual, tol):
            status, why = 'INCOMPLETE', '; '.join(reasons)
        elif reasons:
            status, why = 'INCOMPLETE', 'Agrees within tolerance but open items may belong here: ' + '; '.join(reasons)
        elif within(diff, exp, opening_actual, tol):
            status, why = 'RECONCILED', ''
        elif key not in actual:
            status, why = 'EXPECTED_ONLY', 'Expected balance has no actual TB line'
        elif not streams:
            status, why = 'ACTUAL_ONLY', 'Actual TB line with no expected source balance'
        else:
            status, why = 'DIFFERENCE', 'Expected and actual differ beyond tolerance'
        mapping = 'MAPPED' if streams and not reasons else 'PARTIAL' if streams else 'UNMAPPED' if key in actual else 'UNRESOLVED_CANDIDATE'
        gl_rows.append({'target_gl': gl, 'currency': ccy, 'class': cls, 'legacy_gls': lg, 'expected': exp,
                        'expected_by_stream': {s: streams.get(s, ZERO) for s in STREAMS if s in streams},
                        'actual_closing': act if key in actual else None, 'post_cob_movements': mov,
                        'actual_opening': opening_actual, 'difference': diff, 'abs_difference': abs(diff),
                        'unresolved_candidate_amount': multi_candidates.get(key, ZERO) + sum(
                            (e.get('unresolved_by_gl') or {}).get(key, ZERO) for e in engines.values()),
                        'mapping_status': mapping, 'recon_status': status, 'exception_reason': why})
    rollforward = []
    if cutover:
        for key in sorted(set(movements) | {(r['target_gl'], r['currency']) for r in gl_rows if r['actual_closing'] is not None}):
            row = next((r for r in gl_rows if (r['target_gl'], r['currency']) == key), None)
            if row is None:
                continue
            exp, mov = row['expected'], movements.get(key, ZERO)
            act = row['actual_closing'] or ZERO
            rollforward.append({'target_gl': key[0], 'currency': key[1], 'opening_migrated_expected': exp,
                                'validated_post_cob_movements': mov, 'by_type': dict(mov_types.get(key, {})),
                                'computed_closing': exp + mov, 'actual_closing': act, 'rollforward_difference': act - exp - mov})
    # 5. GL Report H/D/T (engine A rule lines)
    gl_report = build_gl_report(engines.get('A'))
    # 6. benchmark (never a source of expected balances)
    bench_rows = None
    if inputs.get('benchmark') is not None:
        bench = defaultdict(lambda: ZERO)
        for r in inputs['benchmark']:
            gl, ccy = text(r.get('TARGET_GL')).upper(), text(r.get('CURRENCY')).upper()
            a = amount(r.get('BALANCE'))
            if gl and a is not None:
                bench[(gl, ccy)] += a
        bench_rows = []
        for key in sorted(set(bench) | set(expected)):
            e = sum(expected.get(key, {}).values(), ZERO)
            b = bench.get(key)
            d = (b or ZERO) - e
            bench_rows.append({'target_gl': key[0], 'currency': key[1], 'expected': e, 'benchmark': b, 'difference': d,
                               'status': 'ONLY_EXPECTED' if b is None else 'ONLY_IN_BENCHMARK' if key not in expected else
                               'AGREES' if within(d, e, b, tol) else 'DIFFERS'})
    totals['legacy_tb'] = legacy_total
    totals['expected'] = sum((sum(v.values(), ZERO) for v in expected.values()), ZERO)
    totals['actual'] = sum(actual.values(), ZERO)
    totals['movements'] = sum(movements.values(), ZERO)
    return {'gl_rows': gl_rows, 'legacy_lines': legacy_lines, 'unallocated': unallocated, 'exceptions': exceptions,
            'gl_mapping_diagnostics': gmap_diags, 'gmap': {k: sorted(v) for k, v in gmap.items()}, 'rollforward': rollforward, 'movements_excluded': mov_excluded,
            'gl_report': gl_report, 'benchmark': bench_rows, 'totals': dict(totals), 'tb_dates': dict(actual_dates),
            'tb_date': tb_date, 'cutover_date': cutover, 'tolerance': {'absolute': str(tol[0]), 'relative': str(tol[1])},
            'actual_supplied': inputs.get('actual_tb') is not None, 'legacy_supplied': inputs.get('legacy_tb') is not None}


def _expand_total(spec, order):
    """'L1, L3..L7' or 'L1, L3-L7' -> line ids; ranges follow the rule-file line order."""
    out, errors = [], []
    for item in split_items(spec or ''):
        sep = '..' if '..' in item else ('-' if item.count('-') == 1 and item.split('-')[1].strip() in order else None)
        if sep:
            a, b = [x.strip() for x in item.split(sep)]
            if a in order and b in order and order.index(a) <= order.index(b):
                out += order[order.index(a):order.index(b) + 1]
            else:
                errors.append(f'range {item} not resolvable in line order')
        elif item in order:
            out.append(item)
        else:
            errors.append(f'line {item} not defined')
    return out, errors


def build_gl_report(engine_a):
    if not engine_a or engine_a.get('status') != 'COMPLETE':
        return []
    rs, by_line = engine_a['ruleset'], engine_a['by_line']
    order = list(rs.lines)
    values, rows = {}, []
    comp_counts = defaultdict(int)
    for c in engine_a['components']:
        if c['status'] == 'MAPPED':
            comp_counts[c['line']] += 1
    for lid in order:
        ln = rs.lines[lid]
        if ln['type'] == 'D':
            values[lid] = by_line.get(lid, ZERO)
    def total(lid, stack=()):
        if lid in stack:
            return None, ['circular total']
        ln = rs.lines[lid]
        if ln['type'] == 'D':
            return values.get(lid, ZERO), []
        if ln['type'] == 'H':
            return ZERO, []
        ids, errs = _expand_total(ln['total_of'], order)
        s = ZERO
        for x in ids:
            if rs.lines[x]['type'] == 'H':
                continue
            v, e = total(x, stack + (lid,))
            errs += e
            if v is not None:
                s += v
        return s, errs
    for lid in order:
        ln = rs.lines[lid]
        if ln['type'] == 'H':
            rows.append({'line': lid, 'type': 'H', 'description': ln['description'], 'target_gl': ln['target'], 'amount': None,
                         'components': 0, 'status': 'HEADER'})
        elif ln['type'] == 'D':
            rows.append({'line': lid, 'type': 'D', 'description': ln['description'], 'target_gl': ln['target'],
                         'amount': values[lid], 'components': comp_counts.get(lid, 0), 'rules': ln['rules'],
                         'status': 'DETAIL' if ln['rules'] else 'DETAIL_WITHOUT_CRITERIA'})
        else:
            v, errs = total(lid)
            rows.append({'line': lid, 'type': 'T', 'description': ln['description'], 'target_gl': ln['target'],
                         'amount': v, 'components': 0, 'total_of': ln['total_of'],
                         'status': 'TOTAL' if not errs else 'TOTAL_ERROR: ' + '; '.join(errs)})
    return rows
