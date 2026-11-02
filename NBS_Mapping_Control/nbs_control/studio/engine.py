"""Expected BO allocation: source records -> compiled workbook conditions -> report lines.

Records are aggregated into signatures (identical dimension values), and each rule is evaluated once per
distinct dimension value through inverted indexes, so large extracts are not scanned rule by rule.
Two allocation paths, both from the workbook:
* CRITERIA   - the record carries T24 attributes (category / PL category ...): GL Report conditions.
* GL_MAPPING - the record carries only a legacy GL: the GL Mapping sheet row gives the report line.
"""
from __future__ import annotations

from collections import defaultdict
from decimal import Decimal

from . import conditions as C
from .compiler import DIMS

ZERO = Decimal(0)


class Sig:
    __slots__ = ('id', 'dims', 'amount', 'count', 'accounts', 'refs', 'path', 'glrows')

    def __init__(self, i, dims):
        self.id, self.dims = i, dims
        self.amount, self.count, self.accounts, self.refs, self.glrows = ZERO, 0, [], [], []
        self.path = None


class Allocation:
    def __init__(self, model, sigs, cfg):
        self.m, self.sigs, self.cfg = model, sigs, cfg or {}
        self.policy = self.cfg.get('overlap_policy', 'ALL')
        self.by = defaultdict(lambda: defaultdict(set))          # dim -> value -> sig ids
        self.crit_ids = set()
        for s in sigs:
            if s.dims.get('category') or s.dims.get('pl_category'):
                s.path = 'CRITERIA'
                self.crit_ids.add(s.id)
            elif s.dims.get('legacy_gl'):
                s.path = 'GL_MAPPING'
            else:
                s.path = 'NO_ATTRIBUTES'
            for d in DIMS:
                self.by[d][s.dims.get(d)].add(s.id)
        self.rules = {r.id: r for r in model.rules}
        self.match, self.undecided = {}, {}
        self.sig_rules = defaultdict(set)
        self.sig_undecided = defaultdict(set)
        for r in model.rules:
            if r.usable and model.lines[r.line]['type'] == 'D':
                self._eval_rule(r)
        self.glindex = defaultdict(list)
        for g in model.glmap:
            for k in ((g['legacy_gl'], g['currency']), (g['legacy_gl'], ''), (g['gl10'], g['currency']), (g['gl10'], '')):
                self.glindex[k].append(g)
        self.lines_of = {s.id: self._lines(s) for s in sigs}

    # --- rule evaluation through value indexes
    def _cond_ids(self, d, cond):
        ok, unknown = set(), set()
        for v, ids in self.by[d].items():
            if v is None:
                unknown |= ids
            elif cond.matches(v):
                ok |= ids
        return ok, unknown

    def rule_sets(self, r, conds=None, ignore=()):
        conds = r.conds if conds is None else conds
        match, maybe = set(self.crit_ids), set(self.crit_ids)
        for d, cond in conds.items():
            if d in ignore:
                continue
            ok, unknown = self._cond_ids(d, cond)
            match &= ok
            maybe &= ok | unknown
        return match, maybe - match

    def _eval_rule(self, r, conds=None):
        match, und = self.rule_sets(r, conds)
        for i in self.match.get(r.id, ()):
            self.sig_rules[i].discard(r.id)
        for i in self.undecided.get(r.id, ()):
            self.sig_undecided[i].discard(r.id)
        self.match[r.id], self.undecided[r.id] = match, und
        for i in match:
            self.sig_rules[i].add(r.id)
        for i in und:
            self.sig_undecided[i].add(r.id)
        return match

    def _lines(self, s):
        if s.path == 'CRITERIA':
            rs = [self.rules[x] for x in self.sig_rules.get(s.id, ())]
            lines = sorted({r.line for r in rs})
            if len(lines) > 1 and self.policy == 'MOST_SPECIFIC':
                best = max(r.specificity() for r in rs)
                top = sorted({r.line for r in rs if r.specificity() == best})
                return tuple(top) if len(top) == 1 else ()
            return tuple(lines)
        if s.path == 'GL_MAPPING':
            rows = self.glindex.get((s.dims['legacy_gl'], s.dims.get('currency') or '')) or self.glindex.get((s.dims['legacy_gl'], ''))
            s.glrows = [g['row'] for g in rows or []]
            return tuple(sorted({g['line'] for g in rows or [] if g['line']}))
        return ()

    def status(self, s):
        lines = self.lines_of[s.id]
        if s.path == 'NO_ATTRIBUTES':
            return 'NO_ATTRIBUTES'
        if not lines:
            if s.path == 'CRITERIA' and self.sig_undecided.get(s.id):
                return 'UNDECIDED'
            return 'UNALLOCATED' if s.path == 'CRITERIA' else ('NO_GL_MAPPING' if not s.glrows else 'GL_MAPPING_WITHOUT_LINE')
        if len(lines) > 1:
            return 'OVERLAP' if s.path == 'CRITERIA' else 'GL_MAPPING_CONFLICT'
        return 'ALLOCATED'

    def recompute(self, ids):
        for i in ids:
            self.lines_of[i] = self._lines(self.sigs[i])

    # --- what-if helpers
    def try_rule(self, r, new_conds):
        """Return {sig_id: (old_lines, new_lines)} if the rule's conditions were replaced (state restored afterwards)."""
        old_match = set(self.match.get(r.id, set()))
        old_conds, old_errors = r.conds, r.errors
        was_active = r.id in self.match
        r.conds, r.errors = new_conds, []
        new_match = self._eval_rule(r)
        affected = old_match ^ new_match
        before = {i: self.lines_of[i] for i in affected}
        self.recompute(affected)
        after = {i: self.lines_of[i] for i in affected}
        r.conds, r.errors = old_conds, old_errors
        if was_active:
            self._eval_rule(r)
        else:
            for i in self.match.pop(r.id, ()):
                self.sig_rules[i].discard(r.id)
            for i in self.undecided.pop(r.id, ()):
                self.sig_undecided[i].discard(r.id)
        self.recompute(affected)
        return {i: (before[i], after[i]) for i in affected if before[i] != after[i]}

    def apply_rule(self, r, new_conds, raw_dim=None, raw_text=None):
        r.conds, r.errors = new_conds, []
        if raw_dim:
            r.raw[raw_dim] = raw_text
        if self.m.lines[r.line]['type'] == 'D':
            ids = self.match.get(r.id, set()) | self._eval_rule(r)
            before = {i: self.lines_of[i] for i in ids}
            self.recompute(ids)
            return {i: (before[i], self.lines_of[i]) for i in ids if before[i] != self.lines_of[i]}
        return {}

    def glmap_sigs(self, row):
        return [s.id for s in self.sigs if s.path == 'GL_MAPPING' and row in s.glrows]


def expected(alloc, key_dims):
    """Expected amount per key (line + key_dims). Overlapping records count in each matched line (literal execution)."""
    E = defaultdict(lambda: ZERO)
    contrib = defaultdict(list)
    for s in alloc.sigs:
        for line in alloc.lines_of[s.id]:
            k = (line,) + tuple(s.dims.get(d) or '' for d in key_dims)
            E[k] += s.amount
            contrib[k].append(s.id)
    return E, contrib


def key_of(line, s, key_dims):
    return (line,) + tuple(s.dims.get(d) or '' for d in key_dims)


def totals(model, E, key_dims):
    """Add T-line totals from their members (D lines first, nested totals resolved recursively)."""
    out = dict(E)
    rest = {k[1:] for k in E}
    memo = {}

    def tot(lid, rk, stack=()):
        if (lid, rk) in memo:
            return memo[(lid, rk)]
        ln = model.lines.get(lid)
        if ln is None or lid in stack:
            return ZERO
        if ln['type'] == 'D':
            v = E.get((lid,) + rk, ZERO)
        elif ln['type'] == 'T':
            v = sum((tot(x, rk, stack + (lid,)) for x in ln.get('total_members', [])), ZERO)
        else:
            v = ZERO
        memo[(lid, rk)] = v
        return v
    for lid, ln in model.lines.items():
        if ln['type'] == 'T':
            for rk in rest:
                v = tot(lid, rk)
                if v:
                    out[(lid,) + rk] = v
    return out


__all__ = ['Allocation', 'Sig', 'expected', 'totals', 'key_of', 'C']
