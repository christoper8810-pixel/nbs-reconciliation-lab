"""Engine A - PRODUCT_S3 / asset-type balances.

Source asset-type row -> every non-zero atomic balance-type column (unpivot, no blanket sum)
-> CONSOL_KEY decoded with the configured AC layout -> compiled GL rule for that atomic balance type
-> target GL. Minimum allocation grain: CONSOL_KEY + ATOMIC_BALANCE_TYPE + TARGET_GL.

* Rules must name atomic balance types (named groups are expanded). Every rule balance type must
  exist in the source schema or be a validated alias; otherwise it is UNSUPPORTED (reported, never 0).
* Contra / BL balance types only allocate through a rule that names them explicitly; otherwise they
  stay CONTRA_UNRESOLVED and separate from the gross balance.
* A single CONSOL_KEY may feed several GLs through different balance types.
"""
from __future__ import annotations

from collections import Counter, defaultdict
from decimal import Decimal

from . import rules as R
from .tables import amount, text

DIMS = ['CATEGORY', 'PRODUCT', 'SECTOR', 'DEPARTMENT', 'RESIDENCE', 'INDUSTRY', 'MATURITY', 'CURRENCY', 'COMPANY', 'STATUS']
ZERO = Decimal(0)


def is_contra(bt, cfg):
    return bt in set(x.upper() for x in cfg.get('contra_balance_types') or []) or \
        any(bt.startswith(p.upper()) for p in cfg.get('contra_balance_type_prefixes') or [])


def run(rows, meta, rule_rows, rule_meta, cfg, layout, legacy=False):
    out = {'engine': 'A', 'name': 'PRODUCT_S3 asset-type balances'}
    if rows is None:
        out.update(status='SOURCE_PENDING', reason='No asset-type balance file supplied')
        return out
    if rule_rows is None:
        out.update(status='SOURCE_PENDING', reason='No GL allocation rule file supplied')
        return out
    suffix = cfg.get('balance_type_column_suffix', '_BAL_QAR').upper()
    bt_cols = {h: h[:-len(suffix)] for h in meta['headers'] if h.endswith(suffix) and len(h) > len(suffix)}
    schema = set(bt_cols.values())
    aliases, alias_report = {}, []
    for a, t in (cfg.get('balance_type_aliases') or {}).items():
        ok = t.upper() in schema
        alias_report.append({'alias': a.upper(), 'target': t.upper(), 'status': 'VALID' if ok else 'INVALID_TARGET_NOT_IN_SCHEMA'})
        if ok and not legacy:
            aliases[a.upper()] = t.upper()
    explicit_dims = [d for d in DIMS if d in meta['headers'] and d.lower() not in layout.segments]
    validated_cols = [d for d in DIMS if d in meta['headers'] and d.lower() in layout.segments]
    available = set(layout.segments) | {d.lower() for d in explicit_dims}
    dim_cols = [d for d in DIMS if d in rule_meta['headers']]
    rs = R.load(rule_rows, dim_cols, cfg, with_bt=True, legacy=legacy, available_dims=available)

    def resolve_bt(name):
        if name in schema:
            return name
        return aliases.get(name)
    rs.index(resolve_bt)
    unsupported = []
    for r in rs.rules:
        for name in r.bt_names:
            if resolve_bt(name) is None:
                unsupported.append({'rule_id': r.id, 'line': r.line, 'balance_type': name, 'targets': r.targets,
                                    'row': r.row, 'reason': 'Rule balance type is not a source column or validated alias'})
    sign = Decimal(str((cfg.get('sign_convention') or {}).get('asset_balances', 1)))

    comps, stats = [], Counter()
    status_amt = defaultdict(lambda: ZERO)
    bt_totals = defaultdict(lambda: defaultdict(lambda: ZERO))
    expected = defaultdict(lambda: ZERO)
    by_line = defaultdict(lambda: ZERO)
    contributions = defaultdict(lambda: [ZERO, 0])
    unresolved_by_gl = defaultdict(lambda: ZERO)
    population = defaultdict(lambda: ZERO)
    domains = defaultdict(Counter)
    explicit_vs_key = defaultdict(Counter)
    raw_total = component_total = ZERO
    zero_cells = missing_cells = 0
    seen = Counter()
    key_errors = Counter()
    column_totals = defaultdict(lambda: ZERO)
    for row in rows:
        consol = text(row.get('CONSOL_KEY'))
        account = text(row.get('ACCOUNT_NO')) or text(row.get('ARRANGEMENT_ID'))
        arrangement = text(row.get('ARRANGEMENT_ID'))
        dims, tokens, err = layout.parse(consol)
        if err:
            key_errors[err] += 1
        else:
            for d, v in dims.items():
                if v:
                    domains[d][v] += 1
            for col in validated_cols:
                ev = text(row.get(col)).upper()
                if ev:
                    explicit_vs_key[col.lower()]['MATCH' if ev == dims.get(col.lower()) else 'DIFFER'] += 1
                    for d, v in dims.items():
                        if v == ev:
                            explicit_vs_key[col.lower()]['=' + d] += 1
        extra = {d.lower(): text(row.get(d)).upper() for d in explicit_dims}
        if extra:
            dims = {**dims, **extra}
        memo = consol + '|' + '|'.join(extra.values()) if extra else consol
        legacy_gl = text(row.get('LEGACY_GL'))
        currency = (dims.get('currency') or text(row.get('CURRENCY'))).upper()
        seen[(account, arrangement, consol)] += 1
        for col, bt in bt_cols.items():
            a = amount(row.get(col))
            if a is None:
                missing_cells += 1
                continue
            raw_total += a
            if a == 0:
                zero_cells += 1
                continue
            a = a * sign
            component_total += a
            column_totals[bt] += a
            contra = is_contra(bt, cfg)
            if err:
                status, top = 'INVALID_KEY', []
            else:
                status, top = rs.match(dims, bt, memo_key=memo)
                if status == 'NO_RULE' and contra:
                    status = 'CONTRA_UNRESOLVED'
            c = {'engine': 'A', 'source_row': row['_row'], 'account': account, 'ref': consol, 'legacy_gl': legacy_gl,
                 'currency': currency, 'balance_type': bt, 'amount': a, 'status': status, 'contra': contra,
                 'rule_id': top[0].id if status == 'MAPPED' else '', 'line': top[0].line if status == 'MAPPED' else '',
                 'target_gl': top[0].targets[0] if status == 'MAPPED' else '',
                 'candidates': sorted({t for r in top for t in r.targets}) if status != 'MAPPED' else [],
                 'candidate_rules': [r.id for r in top] if status != 'MAPPED' else [],
                 'reason': err or '', 'dims': dims}
            if status == 'MAPPED':
                expected[(c['target_gl'], currency)] += a
                by_line[c['line']] += a
                k = (consol, bt, c['target_gl'])
                contributions[k][0] += a
                contributions[k][1] += 1
            else:
                for g in c['candidates']:
                    unresolved_by_gl[(g, currency)] += a
            stats[status] += 1
            status_amt[status] += a
            bt_totals[bt][status] += a
            if legacy_gl:
                population[(legacy_gl, currency)] += a
            comps.append(c)
    duplicates = {k: n for k, n in seen.items() if n > 1}
    dup_keys = {(k[0], k[2]) for k in duplicates}
    for c in comps:
        c['duplicate_source'] = (c['account'], c['ref']) in dup_keys
    incomplete = defaultdict(set)
    for u in unsupported:
        for g in u['targets']:
            incomplete[g].add(f"rule {u['rule_id']} balance type {u['balance_type']} unavailable in source")
    for (g, _ccy), v in unresolved_by_gl.items():
        incomplete[g].add('unresolved ambiguous / multi-target allocation candidates')
    misalign = misalignment(rs, comps, domains, explicit_vs_key, layout, legacy)
    out.update(status='COMPLETE', components=comps, expected=dict(expected), by_line=dict(by_line),
               contributions=[{'consol_key': k[0], 'balance_type': k[1], 'target_gl': k[2], 'amount': v[0], 'components': v[1]}
                              for k, v in sorted(contributions.items())],
               unresolved_by_gl=dict(unresolved_by_gl), incomplete_gls={k: sorted(v) for k, v in incomplete.items()},
               population=dict(population), ruleset=rs, rule_diagnostics=rs.diagnostics, unsupported_balance_types=unsupported,
               aliases=alias_report, schema=sorted(schema), stats=dict(stats), status_amounts=dict(status_amt),
               bt_totals={k: dict(v) for k, v in bt_totals.items()}, column_totals=dict(column_totals), misalignment=misalign,
               controls_input={'rows': len(rows), 'raw_total': raw_total, 'component_total': component_total,
                               'sign': sign, 'zero_cells': zero_cells, 'missing_cells': missing_cells,
                               'duplicate_source_keys': len(duplicates), 'key_errors': dict(key_errors),
                               'explicit_vs_key': {k: dict(v) for k, v in explicit_vs_key.items()}},
               layout=layout.describe(), explicit_dimension_columns=explicit_dims)
    return out


def misalignment(rs, comps, domains, explicit_vs_key, layout, legacy):
    """POSSIBLE_MAPPING_COLUMN_MISALIGNMENT: a rule's column X holds values that never occur at key segment X
    but all occur at another segment Y (for example SECTOR holding PRODUCT codes). Evidence is per rule."""
    findings = []
    dims = [d for d in rs.dim_columns if d in layout.segments]
    pairs = defaultdict(list)
    for x in dims:
        for r in rs.rules:
            c = r.crit.get(x)
            if c is None or not c.exact or c.ranges or c.prefixes or any(v in domains[x] for v in c.exact):
                continue
            ys = [y for y in layout.segments if y != x and domains[y] and all(v in domains[y] for v in c.exact)]
            if not ys:
                continue
            ys.sort(key=lambda y: (y in r.crit, list(layout.segments).index(y)))
            pairs[(x, ys[0])].append(r)
    for (x, y), affected in pairs.items():
        ids = {r.id for r in affected}
        vals = sorted({v for r in affected for v in r.crit[x].exact})
        col_vals = sorted({v for r in rs.rules if x in r.crit for v in r.crit[x].exact})
        own = sum(1 for v in col_vals if v in domains[x]) / len(col_vals)
        by_status = defaultdict(lambda: [0, ZERO])
        rows, net, gross, accounts, examples = 0, ZERO, ZERO, set(), []
        for comp in comps:
            if comp['status'] == 'INVALID_KEY':
                continue
            alt = dict(comp['dims'])
            alt[x] = alt.get(y, '')
            cands = [r for r in rs.candidates_ignoring(alt, comp['balance_type'], (y,)) if r.id in ids]
            if not cands:
                continue
            rows += 1
            net += comp['amount']
            gross += abs(comp['amount'])
            accounts.add(comp['account'])
            by_status[comp['status'] + (' to ' + comp['rule_id'] if comp['status'] == 'MAPPED' else '')][0] += 1
            by_status[comp['status'] + (' to ' + comp['rule_id'] if comp['status'] == 'MAPPED' else '')][1] += comp['amount']
            if comp['status'] != 'MAPPED':
                comp['misalignment'] = f'{x}->{y}'
                comp['misalignment_rules'] = sorted(r.id for r in cands)
            if len(examples) < 10:
                examples.append({'account': comp['account'], 'consol_key': comp['ref'], 'balance_type': comp['balance_type'],
                                 'amount': comp['amount'], 'current_status': comp['status'], 'would_match': sorted(r.id for r in cands)})
        findings.append({
            'type': 'POSSIBLE_MAPPING_COLUMN_MISALIGNMENT', 'rule_column': x.upper(), 'expected_dimension': x,
            'observed_dimension': y, 'own_domain_hit_rate': round(own, 4), 'observed_domain_hit_rate': 1.0,
            'segment_positions': {x: layout.segments[x], y: layout.segments[y]},
            'segments_verified': {x: layout.verified[x], y: layout.verified[y]},
            'affected_rules': sorted(ids), 'rules_with_blank_' + y: sorted(r.id for r in affected if y not in r.crit),
            'rule_values': vals[:50], 'affected_rows': rows, 'affected_accounts': len(accounts), 'net_amount': net,
            'absolute_amount': gross, 'current_status_of_affected': {k: {'rows': v[0], 'amount': v[1]} for k, v in by_status.items()},
            'examples': examples,
            'evidence': (f'Rule(s) {", ".join(sorted(ids))}: {x.upper()} values {", ".join(vals[:10])} never occur at the {x} '
                         f'key segment (position {layout.segments[x]}) but all occur at the {y} segment (position '
                         f'{layout.segments[y]}). {rows} source components ({len(accounts)} accounts, net {net}) would match these '
                         f'rules if the column were read as {y}; their current status: '
                         + '; '.join(f'{k}: {v[0]}' for k, v in sorted(by_status.items())) + '.')})
    for col, cnt in explicit_vs_key.items():
        total = cnt.get('MATCH', 0) + cnt.get('DIFFER', 0)
        if not total or cnt.get('DIFFER', 0) / total < 0.5:
            continue
        others = {k[1:]: v for k, v in cnt.items() if k.startswith('=') and k[1:] != col}
        if others:
            y, n = max(others.items(), key=lambda kv: kv[1])
            findings.append({'type': 'POSSIBLE_MAPPING_COLUMN_MISALIGNMENT', 'rule_column': None, 'source_column': col.upper(),
                             'expected_dimension': col, 'observed_dimension': y, 'affected_rows': cnt['DIFFER'],
                             'evidence': f'Explicit source column {col.upper()} differs from its key segment in '
                                         f'{cnt["DIFFER"]} of {total} rows and equals the {y} segment in {n} rows.'})
    return findings
