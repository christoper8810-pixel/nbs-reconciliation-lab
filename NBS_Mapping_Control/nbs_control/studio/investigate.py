"""Automated discrepancy investigation by verified what-if re-execution.

For every BO difference the engine builds candidate single-cell corrections from the evidence (records that
nearly satisfy a line's conditions, records that cause an excess, GL Mapping rows, validation proposals),
re-executes the workbook conditions with the edit applied, and keeps only edits that measurably reduce the
differences. Confidence:
  HIGH       every touched line closes within tolerance, nothing worsens, and no other cell achieves the same;
  MEDIUM     closes the touched lines but alternatives exist, or removes at least half the touched difference;
  LOW        some improvement only;
  UNRESOLVED differences no candidate explains (with the responsible party and the evidence still needed).
Edits are applied greedily (best first) so later proposals are evaluated on the corrected state; each proposal
records the proposals it depends on.
"""
from __future__ import annotations

from collections import defaultdict
from decimal import Decimal

from . import conditions as C
from .engine import key_of
from .validate import parse_addr

ZERO = Decimal(0)
RANK = {'HIGH': 3, 'MEDIUM': 2, 'LOW': 1}


def _tokens(raw, space):
    return C.split(raw, space)


def text_add(raw, v, space):
    if not raw:
        return v
    toks = _tokens(raw, space)
    if v.isdigit():
        n = int(v)
        for t in toks:
            mm = C._RANGE.match(t.upper())
            if mm:
                lo, hi = int(mm.group(1)), int(mm.group(2))
                if n == hi + 1:
                    return raw.replace(t, f'{lo}-{n}', 1)
                if n == lo - 1:
                    return raw.replace(t, f'{n}-{hi}', 1)
    sep = '\n' if '\n' in raw else ', '
    return raw.rstrip() + sep + v


def text_remove(raw, v, space):
    toks = _tokens(raw, space)
    up = [t.upper() for t in toks]
    if v in up:
        rest = [t for t, u in zip(toks, up) if u != v]
        return ', '.join(rest) if rest else None
    if v.isdigit():
        n = int(v)
        for t in toks:
            mm = C._RANGE.match(t.upper())
            if mm:
                lo, hi = int(mm.group(1)), int(mm.group(2))
                if lo <= n <= hi:
                    if n == lo:
                        new = f'{lo + 1}-{hi}' if hi > lo + 1 else str(hi)
                    elif n == hi:
                        new = f'{lo}-{hi - 1}' if hi - 1 > lo else str(lo)
                    else:
                        return raw.rstrip() + ', !' + v
                    return raw.replace(t, new, 1) if lo != hi else None
    return raw.rstrip() + ', !' + v


class Investigation:
    def __init__(self, model, alloc, E, A, key_dims, tol, cfg=None):
        self.m, self.al, self.key_dims, self.tol = model, alloc, key_dims, tol
        self.cfg = cfg or {}
        self.space = bool(self.cfg.get('space_separates_values', True))
        self.E, self.A = defaultdict(lambda: ZERO, E), A
        self.named = {k: v['text'] for k, v in model.named.items()}
        self.proposals, self.applied = [], []

    def D(self, k):
        return self.A.get(k, ZERO) - self.E.get(k, ZERO)

    def open_keys(self):
        keys = set(self.E) | set(self.A)
        return [k for k in keys if k[0] in self.m.lines and self.m.lines[k[0]]['type'] == 'D' and abs(self.D(k)) > self.tol]

    # ---------------------------------------------------------------- evaluation
    def _delta(self, changes):
        dE = defaultdict(lambda: ZERO)
        recs, accts, moved = 0, set(), ZERO
        for i, (old, new) in changes.items():
            s = self.al.sigs[i]
            for l in old:
                dE[key_of(l, s, self.key_dims)] -= s.amount
            for l in new:
                dE[key_of(l, s, self.key_dims)] += s.amount
            recs += s.count
            accts.update(s.accounts)
            moved += s.amount
        return dE, recs, accts, moved

    def score(self, changes):
        dE, recs, accts, moved = self._delta(changes)
        touched = [k for k, v in dE.items() if v]
        if not touched:
            return None
        before = {k: self.D(k) for k in touched}
        after = {k: self.D(k) - dE[k] for k in touched}
        old_abs = sum((abs(v) for v in before.values()), ZERO)
        new_abs = sum((abs(v) for v in after.values()), ZERO)
        worse = [k for k in touched if abs(after[k]) > abs(before[k]) + self.tol]
        resolved = all(abs(after[k]) <= self.tol for k in touched)
        return {'improvement': old_abs - new_abs, 'old_abs': old_abs, 'resolved': resolved, 'worse': worse,
                'touched': {self._kstr(k): {'before': before[k], 'after': after[k]} for k in touched}, 'records': recs,
                'accounts': len(accts), 'sample_accounts': sorted(accts)[:10], 'moved': moved, 'dE': dE}

    def _kstr(self, k):
        return ' / '.join(str(x) for x in k if x != '') or str(k[0])

    def grade(self, sc):
        if sc is None or sc['improvement'] <= self.tol:
            return None
        if sc['worse']:
            return None                      # never trade one line's error for another's
        if sc['resolved']:
            return 'HIGH'
        if sc['improvement'] >= sc['old_abs'] / 2:
            return 'MEDIUM'
        return 'LOW' if sc['improvement'] >= sc['old_abs'] / 10 else None

    # ---------------------------------------------------------------- candidates
    def candidates(self):
        out = []
        open_lines = defaultdict(list)
        for k in self.open_keys():
            open_lines[k[0]].append(k)
        rules = {r.id: r for r in self.m.rules}
        own = {}
        for lid in open_lines:
            for rid in self.m.lines[lid]['rules']:
                r = rules[rid]
                if not r.usable:
                    continue
                for d, cond in r.conds.items():
                    cell = r.cells.get(d, '')
                    pa = parse_addr(cell)
                    if not pa or pa[1] != r.row:
                        continue            # inherited cell: editing it would change another row too
                    near, _u = self.al.rule_sets(r, ignore=(d,))
                    near -= self.al.match.get(r.id, set())
                    vals = defaultdict(lambda: ZERO)
                    for i in near:
                        v = self.al.sigs[i].dims.get(d)
                        if v:
                            vals[v] += self.al.sigs[i].amount
                    for v, _a in sorted(vals.items(), key=lambda kv: -abs(kv[1]))[:15]:
                        out.append(('ADD', r, d, v))
                    vals = defaultdict(lambda: ZERO)
                    for i in self.al.match.get(r.id, ()):
                        v = self.al.sigs[i].dims.get(d)
                        if v:
                            vals[v] += self.al.sigs[i].amount
                    for v, _a in sorted(vals.items(), key=lambda kv: -abs(kv[1]))[:15]:
                        out.append(('REMOVE', r, d, v))
        neg = sorted({k[0] for ks in open_lines.values() for k in ks}, key=lambda l: -abs(sum(self.D(k) for k in open_lines[l])))
        for g in self.m.glmap:
            if 'line' not in g['cells']:
                continue
            ids = self.al.glmap_sigs(g['row'])
            if not ids:
                continue
            if g['line'] in open_lines or not g['line']:
                for y in neg[:40]:
                    if y != g['line']:
                        out.append(('GLMAP', g, y, ids))
        return out

    def evaluate(self, cand):
        kind = cand[0]
        if kind in ('ADD', 'REMOVE'):
            _k, r, d, v = cand
            raw = r.raw.get(d, '')
            new = text_add(raw, v, self.space) if kind == 'ADD' else text_remove(raw, v, self.space)
            if new is None or new == raw:
                return None
            try:
                cond = C.parse(new, self.named, self.space)
            except C.ConditionError:
                return None
            conds = dict(r.conds)
            conds[d] = cond
            changes = self.al.try_rule(r, conds)
            if any(len(new) > 1 and len(new) > len(old) for old, new in changes.values()):
                return None                  # would create a double allocation: never a correction
            if kind == 'REMOVE':
                # Removing a value may only move money to another line or end a double allocation; leaving records
                # outside every line would merely hide BO differences.
                if any(not new and len(old) <= 1 for old, new in changes.values()):
                    return None
            sc = self.score(changes)
            if sc is None:
                return None
            contiguous = kind == 'ADD' and not new.startswith(raw.rstrip() + ',') and not new.startswith(raw.rstrip() + '\n')
            return {'kind': 'EXTEND_CONDITION' if kind == 'ADD' else 'RESTRICT_CONDITION', 'rule': r, 'dim': d, 'value': v,
                    'contiguous': contiguous,
                    'edits': [{'cell': r.cells[d], 'existing': raw, 'proposed': new}], 'apply': ('RULE', r, conds, d, new),
                    'changes': changes, 'score': sc}
        if kind == 'GLMAP':
            _k, g, y, ids = cand
            changes = {}
            for i in ids:
                old = self.al.lines_of[i]
                new = tuple(sorted({y} | (set(old) - {g['line']}))) if g['line'] else (y,)
                if new != old:
                    changes[i] = (old, new)
            sc = self.score(changes)
            if sc is None:
                return None
            return {'kind': 'GLMAP_LINE_CHANGE', 'glrow': g, 'value': y, 'edits': [{'cell': g['cells']['line'], 'existing': g['line'],
                                                                                    'proposed': y}],
                    'apply': ('GLMAP', g, y), 'changes': changes, 'score': sc}
        return None

    def evaluate_validation(self, p):
        """BO evidence for a workbook-only proposal: one condition cell, a column move on one row, or a GL Mapping line cell."""
        edits = p['edits']
        if p.get('move') and p.get('rule'):
            r = next((x for x in self.m.rules if x.id == p['rule']), None)
            d, d2 = p['move']
            if r is None:
                return None
            try:
                cond = C.parse(edits[1]['proposed'], self.named, self.space)
            except C.ConditionError:
                return None
            conds = {k: v for k, v in r.conds.items() if k != d}
            conds[d2] = cond
            changes = self.al.try_rule(r, conds)
            return {'changes': changes, 'score': self.score(changes), 'apply': ('RULE', r, conds, d2, edits[1]['proposed'])}
        if len(edits) != 1:
            return None
        e = edits[0]
        for g in self.m.glmap:
            if g['cells'].get('line') == e['cell']:
                ids = self.al.glmap_sigs(g['row'])
                changes = {}
                for i in ids:
                    old = self.al.lines_of[i]
                    new = tuple(sorted({e['proposed']} | (set(old) - {g['line']})))
                    if new != old:
                        changes[i] = (old, new)
                return {'changes': changes, 'score': self.score(changes), 'apply': ('GLMAP', g, e['proposed'])}
        for r in self.m.rules:
            for d, cell in r.cells.items():
                if cell == e['cell']:
                    try:
                        cond = C.parse(e['proposed'], self.named, self.space)
                    except C.ConditionError:
                        return None
                    conds = dict(r.conds)
                    conds[d] = cond
                    changes = self.al.try_rule(r, conds)
                    return {'changes': changes, 'score': self.score(changes), 'apply': ('RULE', r, conds, d, e['proposed'])}
        return None

    def apply(self, ev):
        a = ev['apply']
        if a[0] == 'RULE':
            _t, r, conds, d, new = a
            changes = self.al.apply_rule(r, conds, d, new)
        else:
            _t, g, y = a
            old_line = g['line']
            g['line'] = y
            ids = self.al.glmap_sigs(g['row'])
            before = {i: self.al.lines_of[i] for i in ids}
            self.al.recompute(ids)
            changes = {i: (before[i], self.al.lines_of[i]) for i in ids if before[i] != self.al.lines_of[i]}
            g['_original_line'] = g.get('_original_line', old_line)
        dE, *_ = self._delta(changes)
        for k, v in dE.items():
            self.E[k] += v

    # ---------------------------------------------------------------- main loop
    def run(self, validation_proposals=(), max_iter=60):
        for p in validation_proposals:
            ev = self.evaluate_validation(p) if self.A else None
            if ev and ev['score']:
                g = self.grade(ev['score'])
                p['bo_evidence'] = {k: {'before': str(v['before']), 'after': str(v['after'])} for k, v in ev['score']['touched'].items()}
                p['affected_records'] = ev['score']['records']
                p['financial_impact'] = ev['score']['moved']
                if g is None:
                    p['confidence'] = 'LOW'
                    p['note'] = 'BO evidence does not support this workbook-only correction; review before approving'
                else:
                    p['confidence'] = g if RANK[g] >= RANK.get(p['confidence'], 0) else p['confidence']
                    self.apply(ev)
                    self.applied.append(p)
        for it in range(max_iter):
            evs = [ev for ev in (self.evaluate(c) for c in self.candidates()) if ev]
            graded = [(self.grade(ev['score']), ev) for ev in evs]
            graded = [(g, ev) for g, ev in graded if g]
            if not graded:
                break
            graded.sort(key=lambda x: (-RANK[x[0]], -x[1]['score']['improvement'], not x[1].get('contiguous'), x[1]['edits'][0]['cell']))
            g, best = graded[0]
            alts = [ev for gg, ev in graded[1:] if gg == g and ev['edits'][0]['cell'] != best['edits'][0]['cell']
                    and set(ev['score']['touched']) == set(best['score']['touched'])
                    and abs(ev['score']['improvement'] - best['score']['improvement']) <= self.tol]
            same_line = best.get('rule') is not None and all(a.get('rule') is not None and a['rule'].line == best['rule'].line for a in alts)
            if g == 'HIGH' and alts and not (same_line and best.get('contiguous')):
                g = 'MEDIUM'
            self.proposals.append(self._proposal(best, g, alts, it))
            self.apply(best)
        return self.proposals

    def _proposal(self, ev, grade, alts, it):
        sc = ev['score']
        if ev['kind'] == 'GLMAP_LINE_CHANGE':
            g = ev['glrow']
            reason = (f'GL Mapping row {g["row"]} (legacy GL {g["legacy_gl"]}) sends its balances to {ev["edits"][0]["existing"] or "no line"}; '
                      f'the BO report carries them on {ev["value"]}')
            ref = f'GL Mapping row {g["row"]}'
        else:
            r, d, v = ev['rule'], ev['dim'], ev['value']
            verb = 'does not include' if ev['kind'] == 'EXTEND_CONDITION' else 'wrongly includes'
            reason = f'Condition {d.upper()} of {r.id} ({r.describe()}) {verb} {v}'
            ref = f'{r.id} (line {r.line}, row {r.row})'
        evidence = (f'Re-executing the workbook with this edit moves {sc["records"]} records ({sc["accounts"]} accounts, amount {sc["moved"]}) '
                    f'and changes the BO differences: ' + '; '.join(f'{k}: {v["before"]} -> {v["after"]}' for k, v in sc['touched'].items()))
        if alts:
            evidence += '. Alternative cells with the same effect: ' + ', '.join(a['edits'][0]['cell'] for a in alts[:5])
        return {'kind': ev['kind'], 'edits': ev['edits'], 'reason': reason, 'rule_ref': ref, 'evidence': evidence,
                'affected_records': sc['records'], 'affected_accounts': sc['accounts'], 'sample_accounts': sc['sample_accounts'],
                'financial_impact': sc['moved'], 'improvement': sc['improvement'], 'lines': {k: {'before': str(v['before']), 'after': str(v['after'])}
                                                                                            for k, v in sc['touched'].items()},
                'confidence': grade, 'origin': 'BO_RECONCILIATION', 'responsibility': 'MAPPING', 'iteration': it,
                'depends_on_previous': it > 0, 'alternatives': [a['edits'][0]['cell'] for a in alts[:5]]}

    # ---------------------------------------------------------------- residual classification
    def residuals(self, bo_meta, src_report, dups, presentation):
        out = []
        dates_src = set(src_report.get('dates') or {})
        dates_bo = set(bo_meta.get('dates') or [])
        timing = bool(dates_src and dates_bo and not (dates_src & dates_bo))
        summarized = not self.key_dims
        for k in sorted(set(self.E) | set(self.A), key=lambda x: tuple(str(y) for y in x)):
            line = self.m.lines.get(k[0])
            if line and line['type'] != 'D':
                continue
            e, a = self.E.get(k, ZERO), self.A.get(k)
            d = (a or ZERO) - e
            if abs(d) <= self.tol:
                continue
            ks = self._kstr(k)
            if line is None:
                cat, resp, conf, need = ('LINE_NOT_IN_MAPPING', 'MAPPING_OR_BO', 'MEDIUM',
                                         f'Confirm whether BO line {k[0]} should exist; the workbook has no such line')
            elif a is None:
                cat, resp, conf, need = ('MISSING_IN_BO', 'BO_REPORT', 'MEDIUM',
                                         f'BO output for line {k[0]} (expected {e} from the workbook conditions)')
            elif e and abs(a + e) <= self.tol:
                cat, resp, conf, need = 'SIGN_PRESENTATION', 'BO_REPORT', 'HIGH', 'BO sign convention for this line'
            elif e and abs(a * 1000 - e) <= max(self.tol * 1000, abs(e) * Decimal('0.0005')):
                cat, resp, conf, need = 'SCALE_PRESENTATION', 'BO_REPORT', 'HIGH', 'BO amount unit (thousands?)'
            elif k in dups and abs(d - dups[k]) <= self.tol:
                cat, resp, conf, need = 'DUPLICATE_BO_ROWS', 'BO_REPORT', 'HIGH', 'BO extract duplicates rows for this line'
            elif timing:
                cat, resp, conf, need = ('TIMING_POSSIBLE', 'TIMING', 'LOW',
                                         f'Source dates {sorted(dates_src)[:3]} differ from BO dates {sorted(dates_bo)[:3]}: align the dates')
            elif not line['rules'] and not any(g['line'] == k[0] for g in self.m.glmap):
                cat, resp, conf, need = 'LINE_WITHOUT_CONDITIONS', 'MAPPING', 'HIGH', f'Conditions for line {k[0]}'
            elif k not in self.E:
                cat, resp, conf, need = ('NO_SOURCE_RECORDS_FOR_LINE', 'SOURCE_DATA', 'UNRESOLVED',
                                         f'Account-level source records for line {k[0]} (no supplied record satisfies or nearly satisfies its conditions)')
            elif summarized:
                cat, resp, conf, need = ('INSUFFICIENT_DETAIL', 'UNDETERMINED', 'UNRESOLVED',
                                         f'Account-level BO detail for line {k[0]}: the BO report has line totals only')
            else:
                cat, resp, conf, need = ('UNEXPLAINED', 'UNDETERMINED', 'UNRESOLVED',
                                         f'Account-level BO detail for {ks} to compare record by record')
            out.append({'key': ks, 'line': k[0], 'expected': e, 'actual': a, 'difference': d, 'category': cat, 'responsibility': resp,
                        'confidence': conf, 'evidence_needed': need})
        if presentation:
            for kind, v in presentation.items():
                out.append({'key': '(all lines)', 'line': '', 'expected': None, 'actual': None, 'difference': None,
                            'category': 'GLOBAL_' + kind.upper(), 'responsibility': 'BO_REPORT', 'confidence': 'MEDIUM',
                            'evidence_needed': v['finding'] + f' ({v["lines"]} of {v["of"]} lines)'})
        return out
