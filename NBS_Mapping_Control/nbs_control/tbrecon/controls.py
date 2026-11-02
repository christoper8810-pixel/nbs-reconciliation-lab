"""Independent reconciliation controls. Status: PASS | WARN | FAIL | INCOMPLETE | NOT_APPLICABLE."""
from __future__ import annotations

from collections import defaultdict
from decimal import Decimal

from .tb import within

ZERO = Decimal(0)


def _c(cid, name, status, detail, values=None):
    return {'id': cid, 'control': name, 'status': status, 'detail': detail, 'values': values or {}}


def build(engines, recon, exceptions, cfg, tol):
    out = []
    A, B, Cc = engines.get('A', {}), engines.get('B', {}), engines.get('C', {})
    # 1 completeness and duplicates
    vals, warn = {}, []
    for k, e in engines.items():
        ci = e.get('controls_input')
        if not ci:
            vals[k] = e.get('status')
            continue
        vals[k] = {kk: ci.get(kk) for kk in ('rows', 'duplicate_source_keys', 'duplicate_source_accounts', 'missing_amount_rows', 'key_errors')
                   if ci.get(kk) is not None}
        if ci.get('duplicate_source_keys') or ci.get('duplicate_source_accounts'):
            warn.append(f'{k}: duplicate source records retained and flagged')
        if ci.get('missing_amount_rows'):
            warn.append(f'{k}: {ci["missing_amount_rows"]} rows without an amount excluded and reported')
        if ci.get('key_errors'):
            warn.append(f'{k}: CONSOL_KEY errors {ci["key_errors"]}')
    dup_legacy = [e for e in exceptions if e['category'] == 'DUPLICATE_RULE_OR_SOURCE' and e['level'] in ('LEGACY_TB',)]
    if dup_legacy:
        warn.append(f'{len(dup_legacy)} repeated legacy TB GL/currency lines')
    out.append(_c('C01', 'Source row completeness and duplicate detection', 'WARN' if warn else 'PASS', '; '.join(warn) or
                  'All rows used; no duplicate source records', vals))
    # 2 totals before / after normalisation
    st, det, vals = 'PASS', [], {}
    for k, e in engines.items():
        ci = e.get('controls_input')
        if not ci:
            continue
        before = ci['raw_total'] * ci['sign']
        after = ci.get('component_total') if k == 'A' else sum((c['amount'] for c in e['components']), ZERO)
        vals[k] = {'before': before, 'after': after, 'difference': after - before}
        if after != before:
            st = 'FAIL'
            det.append(f'{k}: normalised total differs by {after - before}')
    if not vals:
        st = 'INCOMPLETE'
    out.append(_c('C02', 'Source totals before and after normalisation', st, '; '.join(det) or
                  'Every non-zero source amount is present after unpivot / normalisation (exact Decimal equality)', vals))
    # 3 atomic balance-type totals
    if A.get('status') == 'COMPLETE':
        bad, vals = [], {}
        for bt, total in sorted(A['column_totals'].items()):
            parts = A['bt_totals'].get(bt, {})
            s = sum(parts.values(), ZERO)
            vals[bt] = {'source_column_total': total, **{k: v for k, v in parts.items()}}
            if s != total:
                bad.append(bt)
        unresolved = sorted(bt for bt, p in A['bt_totals'].items() if any(k != 'MAPPED' for k in p))
        out.append(_c('C03', 'Atomic balance-type totals (source column = mapped + each unresolved status)',
                      'FAIL' if bad else 'WARN' if unresolved or A['unsupported_balance_types'] else 'PASS',
                      (f'Mismatch for {bad}. ' if bad else '') +
                      (f'Unresolved amounts remain for {len(unresolved)} balance types. ' if unresolved else '') +
                      (f'{len(A["unsupported_balance_types"])} rule balance types are not in the source schema.' if A['unsupported_balance_types'] else '')
                      or 'Every balance-type column total equals its classified components and all are mapped',
                      vals))
    else:
        out.append(_c('C03', 'Atomic balance-type totals', 'INCOMPLETE', A.get('reason', 'Engine A not run')))
    # 4 mapping coverage
    vals, st, det = {}, 'PASS', []
    for k, e in engines.items():
        if e.get('status') != 'COMPLETE':
            vals[k] = e.get('status')
            st = 'INCOMPLETE' if st == 'PASS' else st
            det.append(f'{k}: {e.get("reason")}')
            continue
        vals[k] = {'counts': e['stats'], 'amounts': e['status_amounts']}
        others = {s: n for s, n in e['stats'].items() if s != 'MAPPED'}
        if others:
            st = 'WARN' if st in ('PASS', 'INCOMPLETE') else st
            det.append(f'{k}: ' + ', '.join(f'{s} {n}' for s, n in sorted(others.items())))
    out.append(_c('C04', 'Mapping coverage (missing, ambiguous, multi-target, contra, invalid)', st, '; '.join(det) or 'Every component mapped', vals))
    # 5 expected vs actual
    t = recon['totals']
    if not recon['actual_supplied']:
        out.append(_c('C05', 'Expected versus actual TB totals', 'INCOMPLETE', 'Actual TB not supplied'))
    else:
        by_class = defaultdict(lambda: {'expected': ZERO, 'actual_opening': ZERO, 'difference': ZERO, 'gl_lines': 0, 'open': 0})
        for r in recon['gl_rows']:
            b = by_class[r['class']]
            b['expected'] += r['expected']
            b['actual_opening'] += r['actual_opening']
            b['difference'] += r['difference']
            b['gl_lines'] += 1
            b['open'] += r['recon_status'] != 'RECONCILED'
        statuses = defaultdict(int)
        for r in recon['gl_rows']:
            statuses[r['recon_status']] += 1
        st = 'PASS' if set(statuses) <= {'RECONCILED'} else 'INCOMPLETE' if set(statuses) <= {'RECONCILED', 'SOURCE_PENDING', 'INCOMPLETE'} else 'FAIL'
        out.append(_c('C05', 'Expected versus actual TB totals', st, ', '.join(f'{k} {v}' for k, v in sorted(statuses.items())),
                      {'by_class': dict(by_class), 'status_counts': dict(statuses)}))
    # 5b whole-TB walk: no amount disappears
    engine_total = sum((c['amount'] for e in engines.values() for c in e.get('components') or []), ZERO)
    walk = {
        'legacy_tb_total': t.get('legacy_tb', ZERO), 'direct_mapped': t.get('direct_mapped', ZERO),
        'direct_unallocated': t.get('direct_unallocated', ZERO), 'source_pending': t.get('pending', ZERO),
        'covered_by_account_populations': t.get('covered_tb', ZERO),
        'engine_population_total': engine_total, 'engine_mapped': t.get('engine_mapped', ZERO),
        'engine_unresolved': t.get('engine_unresolved', ZERO), 'expected_total': t.get('expected', ZERO)}
    checks = {
        'legacy = direct mapped + direct unallocated + pending + covered': walk['legacy_tb_total'] - walk['direct_mapped'] - walk['direct_unallocated']
        - walk['source_pending'] - walk['covered_by_account_populations'],
        'engine population = engine mapped + engine unresolved': engine_total - walk['engine_mapped'] - walk['engine_unresolved'],
        'expected = direct mapped + engine mapped': walk['expected_total'] - walk['direct_mapped'] - walk['engine_mapped'],
    }
    walk['checks'] = checks
    out.append(_c('C05B', 'Source -> classification -> mapping -> expected TB walk (no amount disappears)',
                  'PASS' if all(v == 0 for v in checks.values()) else 'FAIL',
                  'All buckets tie exactly' if all(v == 0 for v in checks.values()) else 'Bucket walk does not tie: ' + str(checks), walk))
    # 6 multi-target cardinality
    multi = [l for l in recon['legacy_lines'] if len(l.get('targets') or []) > 1]
    unresolved = [l for l in multi if l['status'] == 'MULTI_TARGET_UNRESOLVED']
    out.append(_c('C06', 'Multi-target mapping cardinality', 'WARN' if unresolved else 'PASS',
                  f'{len(multi)} legacy GL/currency lines map to several targets; {len(unresolved)} remain unallocated '
                  f'(no account-level evidence); {len(multi) - len(unresolved)} allocated from account-level populations',
                  {'multi_target_lines': len(multi), 'unresolved': [(l['legacy_gl'], l['currency'], l['targets']) for l in unresolved]}))
    # 7 currency-level differences
    if recon['actual_supplied']:
        ccy = defaultdict(lambda: {'expected': ZERO, 'actual_opening': ZERO, 'difference': ZERO})
        for r in recon['gl_rows']:
            ccy[r['currency']]['expected'] += r['expected']
            ccy[r['currency']]['actual_opening'] += r['actual_opening']
            ccy[r['currency']]['difference'] += r['difference']
        bad = [k for k, v in ccy.items() if not within(v['difference'], v['expected'], v['actual_opening'], tol)]
        out.append(_c('C07', 'Currency-level differences', 'FAIL' if bad else 'PASS', f'Currencies with net difference: {sorted(bad)}' if bad
                      else 'Every currency nets within tolerance (individual GLs may still differ)', dict(ccy)))
    else:
        out.append(_c('C07', 'Currency-level differences', 'INCOMPLETE', 'Actual TB not supplied'))
    # 8 sign normalisation and contra
    contra = {'mapped': ZERO, 'unresolved': ZERO}
    for c in A.get('components') or []:
        if c['contra']:
            contra['mapped' if c['status'] == 'MAPPED' else 'unresolved'] += c['amount']
    signs = {k: str(v) for k, v in (cfg.get('sign_convention') or {}).items() if not k.startswith('_')}
    sign_exc = [e for e in exceptions if e['category'] == 'SIGN_CONVENTION_MISMATCH']
    out.append(_c('C08', 'Sign normalisation and contra balances', 'WARN' if sign_exc or contra['unresolved'] else 'PASS',
                  f'Sign multipliers {signs}; contra mapped {contra["mapped"]}, contra unresolved {contra["unresolved"]} (kept separate); '
                  f'{len(sign_exc)} GL lines show an exact sign reversal', {'signs': signs, 'contra': contra}))
    # 9 business-date integrity
    dates = {d: n for d, n in recon['tb_dates'].items()}
    issues = []
    if len([d for d in dates if d]) > 1:
        issues.append(f'Actual TB has several business dates {sorted(dates)}')
    if '' in dates:
        issues.append(f'{dates[""]} actual TB rows without business date')
    if recon['movements_excluded']:
        issues.append(f'{len(recon["movements_excluded"])} post-COB movements excluded (see roll-forward)')
    st = 'FAIL' if len([d for d in dates if d]) > 1 else 'WARN' if issues else 'PASS'
    if not recon['cutover_date']:
        st, issues = ('INCOMPLETE' if recon['movements_excluded'] else st), issues + ['No cutover_date configured: actual TB treated as the migrated opening position']
    elif recon['tb_date'] and recon['tb_date'] < recon['cutover_date']:
        st = 'FAIL'
        issues.append(f'Actual TB date {recon["tb_date"]} precedes cutover {recon["cutover_date"]}')
    out.append(_c('C09', 'Pre / post-COB business-date integrity', st, '; '.join(issues) or 'Single TB date; movements dated after cutover',
                  {'tb_dates': dates, 'cutover': recon['cutover_date'], 'tb_date': recon['tb_date']}))
    # 11 benchmark
    if recon['benchmark'] is None:
        out.append(_c('C11', 'Independent benchmark (e.g. TrialBalance_withConsolKey.csv)', 'NOT_APPLICABLE', 'Benchmark not supplied; not required'))
    else:
        diff = [b for b in recon['benchmark'] if b['status'] != 'AGREES']
        out.append(_c('C11', 'Independent benchmark comparison (benchmark only, never a source)', 'WARN' if diff else 'PASS',
                      f'{len(diff)} GL/currency lines differ from the benchmark', {'lines': len(recon['benchmark']), 'differences': len(diff)}))
    # 12 layout verification
    unv = sorted(set(f'{k}.{d}' for k, e in engines.items() for d, v in (e.get('layout') or {}).items() if not v['verified']))
    out.append(_c('C12', 'CONSOL_KEY layout verification', 'WARN' if unv else 'PASS',
                  f'Unverified segments in use: {", ".join(unv)}' if unv else 'All used segments verified', {'unverified': unv}))
    return out
