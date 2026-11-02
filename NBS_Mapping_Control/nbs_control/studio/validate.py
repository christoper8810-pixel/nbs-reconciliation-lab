"""Mapping validation across the workbook's own sheets (and the source records when supplied).

Classification of each finding: MAPPING_DEFECT, REFERENCE_DATA, SOURCE_DATA, STRUCTURE or INFORMATION.
Workbook-only proposals are created only where the correction is determined by the workbook itself.
"""
from __future__ import annotations

import re
from collections import defaultdict
from decimal import Decimal

from openpyxl.utils import column_index_from_string

from . import conditions as C

ZERO = Decimal(0)
ADDR = re.compile(r"^'(?P<sheet>.+)'!(?P<col>[A-Z]+)(?P<row>\d+)$")


def parse_addr(a):
    m = ADDR.match(a or '')
    if not m:
        return None
    return m.group('sheet'), int(m.group('row')), column_index_from_string(m.group('col'))


class Findings:
    def __init__(self):
        self.items, self.proposals = [], []

    def add(self, check, severity, classification, message, cell='', **kw):
        self.items.append({'id': f'V{len(self.items) + 1:05d}', 'check': check, 'severity': severity, 'classification': classification,
                           'cell': cell, 'message': message, **kw})

    def propose(self, kind, edits, reason, evidence, confidence, **kw):
        p = {'kind': kind, 'edits': edits, 'reason': reason, 'evidence': evidence, 'confidence': confidence, 'origin': 'VALIDATION',
             'affected_records': kw.pop('affected_records', 0), 'financial_impact': kw.pop('financial_impact', None), **kw}
        self.proposals.append(p)
        return p


def edit(addr_text, old, new):
    sheet, row, col = parse_addr(addr_text)
    return {'cell': addr_text, 'sheet': sheet, 'row': row, 'col': col, 'existing': old, 'proposed': new}


def run(model, alloc=None, sigs=None):
    F = Findings()
    _compile_issues(model, F)
    _references(model, F, sigs)
    _rules(model, F, alloc)
    _lines(model, F, alloc)
    _gl_mapping(model, F)
    if alloc is not None:
        _source(model, F, alloc)
    return F


def _compile_issues(m, F):
    for i in m.issues:
        cls = 'MAPPING_DEFECT' if i['severity'] == 'ERROR' else 'STRUCTURE'
        F.add(i['type'], i['severity'], cls, i['message'], i['cell'])
        if i['type'] == 'MALFORMED_RANGE' and i.get('value'):
            fixed, changed = _swap_ranges(i['value'])
            if changed:
                F.propose('SWAP_RANGE_BOUNDS', [edit(i['cell'], i['value'], fixed)], f'Range bounds reversed in {i["cell"]}',
                          f'{i["value"]!r} has its low bound above its high bound; no value can satisfy it, so the rule is unusable. '
                          f'Swapping gives {fixed!r}.', 'HIGH', dimension=i.get('dimension'))
    for role, info in m.column_maps.items():
        for e in info['evidence']:
            F.add('COLUMN_MAP', 'INFO' if 'not recognised; column not used' in e else 'WARNING', 'STRUCTURE', e)


def _swap_ranges(text):
    changed = False

    def rep(mm):
        nonlocal changed
        lo, hi = int(mm.group(1)), int(mm.group(2))
        if lo > hi:
            changed = True
            return f'{hi}-{lo}'
        return mm.group(0)
    return re.sub(r'(?<![\d.])(\d+)\s*-\s*(\d+)(?![\d.])', rep, text), changed


def _values(cond):
    return list(cond.exact) + [v for r in cond.ranges for v in r]


def _references(m, F, sigs):
    ref = {'category': (lambda v: m.category_ok(v), 'CATEGORY sheet'),
           'sector': ((lambda v: v in m.sectors) if m.sectors else (lambda v: None), 'SEGMENT sheet')}
    for d in ('branch', 'dao', 'product', 'company', 'currency', 'balance_type'):
        if d in m.refsets:
            codes, where = m.refsets[d]
            ref[d] = ((lambda codes: lambda v: v in codes)(codes), where)
    for r in m.rules:
        for d, cond in r.conds.items():
            if d not in ref:
                continue
            check, where = ref[d]
            bad = [str(v) for v in cond.exact if check(str(v)) is False]
            if d == 'category':
                bad += [str(v) for lo_hi in cond.ranges for v in lo_hi if check(str(v)) is False]
            else:
                codes = {'sector': m.sectors}.get(d) or (m.refsets.get(d) or (set(),))[0]
                for lo, hi in cond.ranges:
                    if codes and not any(c.isdigit() and lo <= int(c) <= hi for c in codes):
                        bad.append(f'{lo}-{hi} (covers no known code)')
            if bad:
                F.add(f'UNKNOWN_{d.upper()}', 'ERROR', 'REFERENCE_DATA', f'{d} value(s) {", ".join(sorted(set(bad)))} not in the {where}',
                      r.cells.get(d, ''), line=r.line, rule=r.id)
        cur = r.conds.get('currency')
        if cur and 'currency' not in m.refsets:
            bad = [v for v in cur.exact if not re.fullmatch(r'[A-Z]{3}', v)]
            if bad:
                F.add('INVALID_CURRENCY', 'ERROR', 'MAPPING_DEFECT', f'Currency value(s) {", ".join(bad)} are not ISO codes',
                      r.cells.get('currency', ''), line=r.line, rule=r.id)
        cats = r.conds.get('category')
        if cats and m.categories:
            mods = {(m.category_info(v) or {}).get('module') for v in cats.exact if str(v).isdigit()}
            mods.discard(None)
            mods.discard('')
            if len(mods) > 1:
                F.add('MIXED_CATEGORY_MODULES', 'WARNING', 'MAPPING_DEFECT',
                      f'One condition mixes categories of modules {", ".join(sorted(mods))}', r.cells.get('category', ''), line=r.line, rule=r.id)


def _rules(m, F, alloc):
    seen = defaultdict(list)
    for r in m.rules:
        if not r.usable:
            F.add('RULE_NOT_EXECUTABLE', 'ERROR', 'MAPPING_DEFECT', '; '.join(r.errors), f"'{m.wb.roles.get('GL_REPORT')}'!{r.row}",
                  line=r.line, rule=r.id)
            continue
        if not r.conds:
            F.add('UNRESTRICTED_RULE', 'ERROR', 'MAPPING_DEFECT', f'Criteria row of {r.line} restricts nothing (would take every record)',
                  f"'{m.wb.roles.get('GL_REPORT')}'!{r.row}", line=r.line, rule=r.id)
        sig = tuple(sorted((d, c.signature()) for d, c in r.conds.items()))
        seen[sig].append(r)
    for sig, rs in seen.items():
        lines = sorted({r.line for r in rs})
        if len(rs) > 1:
            F.add('DUPLICATE_CONDITIONS' if len(lines) == 1 else 'CONTRADICTORY_DUPLICATE', 'ERROR' if len(lines) > 1 else 'WARNING',
                  'MAPPING_DEFECT', f'Identical conditions in rules {", ".join(r.id for r in rs)} (lines {", ".join(lines)})',
                  ', '.join(r.cells.get(next(iter(r.conds), ''), '') for r in rs[:4]), rules=[r.id for r in rs])
    # potential overlaps between different detail lines (conservative; observed overlaps are reported from the source)
    dl = [r for r in m.rules if r.usable and r.conds and m.lines[r.line]['type'] == 'D']
    bybt = defaultdict(list)
    free = []
    for r in dl:
        bt = r.conds.get('balance_type')
        if bt and bt.exact and not (bt.ranges or bt.patterns):
            for v in bt.exact:
                bybt[v].append(r)
        else:
            free.append(r)
    pairs = set()
    groups = list(bybt.values()) + [free + [r for v in bybt.values() for r in v]] if free else list(bybt.values())
    for g in groups:
        for i, a in enumerate(g):
            for b in g[i + 1:]:
                if a.line == b.line or (a.id, b.id) in pairs or (b.id, a.id) in pairs or len(pairs) > 200000:
                    continue
                if all(C.intersects(a.conds[d], b.conds[d]) for d in set(a.conds) & set(b.conds)):
                    pairs.add((a.id, b.id))
    observed = defaultdict(lambda: [0, ZERO])
    if alloc is not None:
        for s in alloc.sigs:
            ls = alloc.lines_of[s.id]
            if len(ls) > 1 and s.path == 'CRITERIA':
                rs = sorted(alloc.sig_rules[s.id])
                for i, x in enumerate(rs):
                    for y in rs[i + 1:]:
                        observed[(x, y)][0] += s.count
                        observed[(x, y)][1] += s.amount
    for a, b in sorted(pairs):
        ra, rb = next(r for r in dl if r.id == a), next(r for r in dl if r.id == b)
        obs = observed.get((a, b)) or observed.get((b, a))
        if alloc is not None and not obs:
            continue  # with source data only report overlaps that actually capture records
        F.add('OVERLAPPING_CONDITIONS', 'ERROR' if obs else 'WARNING', 'MAPPING_DEFECT',
              f'{a} ({ra.describe()}) and {b} ({rb.describe()}) can both take the same record: double allocation to lines '
              f'{ra.line} and {rb.line}' + (f'; observed on {obs[0]} records, amount {obs[1]}' if obs else ''),
              ra.cells.get(next(iter(ra.conds)), ''), rules=[a, b], records=obs[0] if obs else 0, amount=obs[1] if obs else None)


def _lines(m, F, alloc):
    glmap_lines = {g['line'] for g in m.glmap if g['line']}
    for lid, ln in m.lines.items():
        if ln['type'] == 'D' and not ln['rules'] and lid not in glmap_lines:
            F.add('UNALLOCATED_LINE', 'WARNING', 'MAPPING_DEFECT', f'Detail line {lid} has no condition and no GL Mapping row refers to it',
                  ln['cell'], line=lid)
        if not ln['type_given']:
            F.add('LINE_TYPE_INFERRED', 'INFO', 'STRUCTURE', f'Line {lid} has no H / D / T type; treated as {ln["type"]}', ln['cell'], line=lid)
        if ln['type'] == 'T':
            if not ln.get('total_members'):
                F.add('TOTAL_WITHOUT_MEMBERS', 'ERROR', 'STRUCTURE', f'Total line {lid} sums nothing', ln['cell'], line=lid)
            elif ln.get('total_basis') == 'INFERRED_SECTION':
                F.add('TOTAL_MEMBERS_INFERRED', 'WARNING', 'STRUCTURE', f'Total line {lid} has no explicit member list; taken as the '
                      f'detail lines above it in its section: {", ".join(ln["total_members"])}', ln['cell'], line=lid)
        if alloc is not None and ln['type'] == 'D' and ln['rules']:
            used = sum(len(alloc.match.get(rid, ())) for rid in ln['rules'])
            if not used and lid not in glmap_lines:
                F.add('LINE_RECEIVES_NO_SOURCE', 'INFO', 'INFORMATION', f'No source record satisfies the conditions of {lid} '
                      '(possibly outdated rule, or the source extract does not cover it)', ln['cell'], line=lid)


def _gl_mapping(m, F):
    by_key = defaultdict(list)
    for g in m.glmap:
        by_key[(g['legacy_gl'], g['currency'])].append(g)
        cells = g['cells']
        if g['line'] and g['line'] not in m.lines:
            close = [l for l in m.lines if l.replace(' ', '').upper() == g['line'].replace(' ', '').upper()]
            F.add('GLMAP_UNKNOWN_LINE', 'ERROR', 'MAPPING_DEFECT', f'GL Mapping row {g["row"]} refers to report line {g["line"]!r}, '
                  'which the GL Report does not define', cells.get('line', ''), legacy_gl=g['legacy_gl'])
            if len(close) == 1:
                F.propose('NORMALISE_LINE_REFERENCE', [edit(cells['line'], g['line'], close[0])], 'Line reference differs only by spacing / case',
                          f'{g["line"]!r} matches GL Report line {close[0]!r} after removing spaces and case', 'HIGH')
        if g['category'] and m.categories and m.category_ok(g['category']) is False:
            F.add('GLMAP_UNKNOWN_CATEGORY', 'ERROR', 'REFERENCE_DATA', f'Category {g["category"]} not in the CATEGORY sheet',
                  cells.get('category', ''), legacy_gl=g['legacy_gl'])
        if g['target_gl'] and m.coa and g['target_gl'] not in m.coa:
            F.add('GLMAP_GL_NOT_IN_COA', 'ERROR', 'REFERENCE_DATA', f'Transact GL {g["target_gl"]} not in the COA sheet',
                  cells.get('target_gl', ''), legacy_gl=g['legacy_gl'])
        info = m.category_info(g['category']) if g['category'] else None
        if info and info['target_gl'] and g['target_gl'] and info['target_gl'].upper() != g['target_gl']:
            F.add('GLMAP_GL_VS_CATEGORY', 'WARNING', 'MAPPING_DEFECT', f'Transact GL {g["target_gl"]} differs from the CATEGORY sheet GL '
                  f'{info["target_gl"]} for category {g["category"]} (CATEGORY row {info["row"]})', cells.get('target_gl', ''),
                  legacy_gl=g['legacy_gl'])
        if g['category'] and g['line'] and m.rules:
            dims = {'category': g['category'], 'currency': g['currency'] or None}
            sure = sorted({r.line for r in m.rules if r.usable and m.lines[r.line]['type'] == 'D' and r.match(dims) is True})
            maybe = sorted({r.line for r in m.rules if r.usable and m.lines[r.line]['type'] == 'D' and r.match(dims) is None})
            if g['line'] not in sure and g['line'] not in maybe and (sure or maybe):
                msg = (f'GL Mapping row {g["row"]} sends category {g["category"]} to {g["line"]}, but the GL Report conditions allocate that '
                       f'category to {", ".join(sure) or "-"}' + (f' (possibly {", ".join(maybe)})' if maybe else ''))
                F.add('GLMAP_LINE_VS_CRITERIA', 'ERROR', 'MAPPING_DEFECT', msg, cells.get('line', ''), legacy_gl=g['legacy_gl'])
                if len(sure) == 1 and not maybe:
                    F.propose('GLMAP_LINE_FROM_CRITERIA', [edit(cells['line'], g['line'], sure[0])], 'GL Mapping line contradicts the GL Report',
                              msg, 'MEDIUM', legacy_gl=g['legacy_gl'])
    for k, rows in by_key.items():
        variants = {(g['line'], g['target_gl']) for g in rows}
        if len(rows) > 1:
            F.add('GLMAP_DUPLICATE' if len(variants) == 1 else 'GLMAP_CONFLICT', 'WARNING' if len(variants) == 1 else 'ERROR',
                  'MAPPING_DEFECT', f'Legacy GL {k[0]} {k[1]} appears in rows {", ".join(str(g["row"]) for g in rows)}'
                  + ('' if len(variants) == 1 else f' with different targets {sorted(variants)}'), rows[0]['cells'].get('legacy_gl', ''))


def _source(m, F, alloc):
    un = defaultdict(lambda: [0, ZERO, set()])
    for s in alloc.sigs:
        st = alloc.status(s)
        if st in ('UNALLOCATED', 'NO_GL_MAPPING', 'GL_MAPPING_WITHOUT_LINE', 'UNDECIDED', 'NO_ATTRIBUTES'):
            k = (st, s.dims.get('category') or s.dims.get('pl_category') or s.dims.get('legacy_gl') or '-', s.dims.get('balance_type') or '-')
            un[k][0] += s.count
            un[k][1] += s.amount
            un[k][2].update(s.accounts[:5])
    for (st, key, bt), (n, amt, acc) in sorted(un.items(), key=lambda kv: -abs(kv[1][1])):
        F.add('SOURCE_' + st, 'ERROR' if st != 'UNDECIDED' else 'WARNING', 'MAPPING_DEFECT' if st != 'NO_ATTRIBUTES' else 'SOURCE_DATA',
              f'{n} source records ({key} / {bt}) are {st.lower().replace("_", " ")}: amount {amt}', records=n, amount=amt,
              sample_accounts=sorted(acc)[:5])
    # misalignment: a rule column whose values never occur in that source dimension but all occur in another one
    domains = {d: {v for v in vals if v} for d, vals in alloc.by.items()}
    gcols = m.column_maps.get('GL_REPORT', {}).get('columns', {})
    for r in m.rules:
        for d, cond in r.conds.items():
            vals = {str(v) for v in cond.exact}
            if not vals or cond.ranges or cond.patterns or not domains.get(d) or vals & domains[d]:
                continue
            others = [d2 for d2, dom in domains.items() if d2 != d and dom and vals <= dom]
            if not others:
                continue
            d2 = others[0]
            msg = (f'{r.id}: {d.upper()} value(s) {", ".join(sorted(vals))} never occur as {d} in the source but all occur as {d2}')
            F.add('POSSIBLE_MAPPING_COLUMN_MISALIGNMENT', 'ERROR', 'MAPPING_DEFECT', msg, r.cells.get(d, ''), line=r.line, rule=r.id,
                  expected_dimension=d, observed_dimension=d2)
            if d2 in gcols and d2 not in r.conds:
                sheet, row, _c = parse_addr(r.cells[d])
                from .workbook import addr as mk
                F.propose('MOVE_TO_COLUMN', [edit(r.cells[d], r.raw[d], ''), edit(mk(sheet, row, gcols[d2]), '', r.raw[d])],
                          f'Values written in the {d.upper()} column belong to {d2.upper()}', msg, 'MEDIUM', rule=r.id, line=r.line,
                          move=(d, d2))
