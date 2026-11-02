"""Compiled mapping rules with explicit specificity, precedence and ambiguity.

A rule file is read in its original order (GL Report style):

* RULE_ID / LINE populated   -> starts a line (TYPE H header, D detail, T total; default D).
* RULE_ID blank              -> continuation row of the current line: an additional OR criteria set.
* a criteria cell of '^'     -> inherits that cell from the previous criteria row of the same line.
* criteria.inherit_blank_columns (config) -> blank cells on continuation rows inherit as well.
* RANGE_NAME + RANGE_VALUES  -> named list/range used as '*NAME' in any criteria cell.
* TARGET_GL may list several GLs; such a rule is MULTI_TARGET and never allocates by itself.
* PRIORITY (integer, higher wins) is an explicit precedence override; otherwise specificity decides:
  (priority, restricted dimensions, exact-only restricted dimensions). Equally specific matches with
  different targets are AMBIGUOUS - never "first rule wins".
"""
from __future__ import annotations

from collections import defaultdict

from . import criteria as C
from .tables import text

LINE_TYPES = ('H', 'D', 'T')


class Rule:
    __slots__ = ('id', 'line', 'seq', 'row', 'crit', 'bt_names', 'bt_error', 'targets', 'priority', 'errors',
                 'raw', 'spec', 'unavailable')

    def __init__(self, **kw):
        for k in self.__slots__:
            setattr(self, k, kw.get(k))

    @property
    def usable(self):
        return not self.errors and not self.bt_error and not self.unavailable and bool(self.targets)

    @property
    def multi_target(self):
        return len(self.targets or []) > 1

    def as_dict(self):
        return {'rule_id': self.id, 'line': self.line, 'source_row': self.row, 'priority': self.priority,
                'targets': self.targets, 'balance_types': self.bt_names, 'criteria': {k: v.values() if v.restricted else 'ANY'
                                                                                     for k, v in self.crit.items()},
                'errors': self.errors, 'bt_error': self.bt_error, 'unavailable_dimensions': self.unavailable,
                'specificity': list(self.spec), 'raw': self.raw}


class RuleSet:
    def __init__(self, rules, lines, named, diagnostics, dim_columns, with_bt):
        self.rules = rules
        self.lines = lines
        self.named = named
        self.diagnostics = diagnostics
        self.dim_columns = dim_columns
        self.with_bt = with_bt
        self.by_bt = defaultdict(list)
        self.any_bt = []
        self._memo = {}
        self.legacy = False

    def index(self, bt_resolver=None):
        """bt_resolver(name) -> schema balance type or None. Builds the BT index used for matching."""
        self.by_bt.clear()
        self.any_bt = []
        for r in self.rules:
            if not r.usable:
                continue
            if self.with_bt:
                for name in r.bt_names:
                    atomic = bt_resolver(name) if bt_resolver else name
                    if atomic:
                        self.by_bt[atomic].append(r)
            else:
                self.any_bt.append(r)
        self._memo.clear()

    def match(self, dims, bt=None, memo_key=None):
        """Return (status, rules). status: MAPPED | NO_RULE | AMBIGUOUS | MULTI_TARGET_UNRESOLVED."""
        if memo_key is not None:
            hit = self._memo.get((memo_key, bt))
            if hit is not None:
                return hit
        pool = self.by_bt.get(bt, ()) if self.with_bt else self.any_bt
        cands = [r for r in pool if all(c.matches(dims.get(d)) for d, c in r.crit.items())]
        res = resolve_legacy(cands) if self.legacy else resolve(cands)
        if memo_key is not None and len(self._memo) < 2_000_000:
            self._memo[(memo_key, bt)] = res
        return res

    def candidates_ignoring(self, dims, bt, ignore):
        """Rules that would match if the 'ignore' dimension(s) were not tested (diagnostics only)."""
        pool = self.by_bt.get(bt, ()) if self.with_bt else self.any_bt
        return [r for r in pool if all(c.matches(dims.get(d)) for d, c in r.crit.items() if d not in ignore)]


def resolve(cands):
    if not cands:
        return 'NO_RULE', []
    best = max(r.spec for r in cands)
    top = sorted((r for r in cands if r.spec == best), key=lambda r: r.id)
    targets = {tuple(r.targets) for r in top}
    if len(targets) > 1:
        return 'AMBIGUOUS', top
    if top[0].multi_target:
        return 'MULTI_TARGET_UNRESOLVED', top
    return 'MAPPED', top


def resolve_legacy(cands):
    """BEFORE baseline only: the original behaviour - first matching rule in file order, first listed target GL."""
    if not cands:
        return 'NO_RULE', []
    first = min(cands, key=lambda r: (r.row, r.seq))
    return 'MAPPED', [first]


def _int(v, default=0):
    s = text(v)
    try:
        return int(float(s)) if s else default
    except ValueError:
        return None


def load(rows, dim_columns, cfg=None, with_bt=True, legacy=False, available_dims=None):
    """Compile rule rows. available_dims: dimensions the source can supply (others -> DIMENSION_NOT_AVAILABLE)."""
    ccfg = {**C.DEFAULTS, **((cfg or {}).get('criteria') or {})}
    inherit_tok = ccfg.get('inherit_token', '^')
    inherit_blank = set(ccfg.get('inherit_blank_columns') or [])
    named, diags = {}, []
    for r in rows:
        name, vals = text(r.get('RANGE_NAME')), r.get('RANGE_VALUES')
        if name:
            key = name.lstrip('*').upper()
            if key in named and named[key] != text(vals):
                diags.append({'type': 'NAMED_RANGE_REDEFINED', 'name': key, 'row': r['_row']})
            named[key] = text(vals)
    crit_cols = list(dim_columns) + (['BALANCE_TYPE'] if with_bt else [])
    rules, lines, line_order = [], {}, []
    current, prev_raw = None, None
    for r in rows:
        lid = text(r.get('RULE_ID'))
        has_crit = any(text(r.get(c)) for c in crit_cols)
        if lid:
            ltype = (text(r.get('TYPE')) or 'D').upper()[:1]
            if ltype not in LINE_TYPES:
                diags.append({'type': 'UNKNOWN_LINE_TYPE', 'line': lid, 'row': r['_row'], 'value': ltype})
                ltype = 'D'
            if lid in lines:
                diags.append({'type': 'DUPLICATE_LINE_ID', 'line': lid, 'row': r['_row'],
                              'first_row': lines[lid]['row']})
                current = lines[lid]
            else:
                current = {'line': lid, 'type': ltype, 'description': text(r.get('DESCRIPTION')), 'row': r['_row'],
                           'target': text(r.get('TARGET_GL')), 'total_of': text(r.get('TOTAL_OF')),
                           'priority': _int(r.get('PRIORITY')), 'seq': len(line_order), 'rules': []}
                lines[lid] = current
                line_order.append(lid)
            prev_raw = None
        elif not has_crit:
            continue
        if current is None:
            diags.append({'type': 'CONTINUATION_WITHOUT_LINE', 'row': r['_row']})
            continue
        if not has_crit:
            continue
        if current['type'] != 'D':
            diags.append({'type': 'CRITERIA_ON_NON_DETAIL_LINE', 'line': current['line'], 'row': r['_row']})
            continue
        raw, errors = {}, []
        for col in crit_cols:
            v = text(r.get(col))
            if v == inherit_tok or (not lid and not v and col in inherit_blank):
                if prev_raw is None:
                    if v == inherit_tok:
                        errors.append(f'{col}: inherit marker with no previous criteria row')
                    v = ''
                else:
                    v = prev_raw.get(col, '')
            raw[col] = v
        prev_raw = raw
        crit = {}
        for col in dim_columns:
            try:
                crit[col.lower()] = C.parse(raw[col], named, ccfg, legacy=legacy)
            except C.CriteriaError as exc:
                errors.append(f'{col}: {exc}')
        crit = {k: v for k, v in crit.items() if v.restricted}
        bt_names, bt_error = [], None
        if with_bt:
            try:
                bt_raw = raw['BALANCE_TYPE'].strip()
                if legacy and bt_raw and not bt_raw.startswith('*'):
                    btc = C.Criterion('SET', exact=frozenset([bt_raw.upper()]), source=bt_raw)  # old adapter: whole cell literal
                else:
                    btc = C.parse(bt_raw, named, {**ccfg, 'blank_means': 'UNRESTRICTED'})
                if not btc.restricted:
                    bt_error = 'NO_ATOMIC_BALANCE_TYPE'
                elif btc.ranges or btc.prefixes or btc.kind != 'SET':
                    bt_error = 'BALANCE_TYPE_NOT_ATOMIC'
                else:
                    bt_names = sorted(btc.exact)
            except C.CriteriaError as exc:
                bt_error = f'BALANCE_TYPE: {exc}'
        tgt_text = text(r.get('TARGET_GL')) or current['target']
        targets = sorted(set(C.split_items(tgt_text))) if tgt_text else []
        if not targets:
            errors.append('NO_TARGET_GL')
        pr = _int(r.get('PRIORITY'), None) if text(r.get('PRIORITY')) else current['priority']
        if pr is None:
            errors.append('PRIORITY_NOT_INTEGER')
            pr = 0
        unavailable = sorted(d for d in crit if available_dims is not None and d not in available_dims)
        seq = len(current['rules']) + 1
        rule = Rule(id=f"{current['line']}#{seq}", line=current['line'], seq=seq, row=r['_row'], crit=crit,
                    bt_names=bt_names, bt_error=bt_error, targets=targets, priority=pr, errors=errors, raw=raw,
                    spec=(pr, len(crit) + (1 if with_bt else 0), sum(1 for c in crit.values() if c.exact_only)),
                    unavailable=unavailable)
        current['rules'].append(rule.id)
        rules.append(rule)
    # Static duplicate / conflict detection on identical criteria signatures.
    groups = defaultdict(list)
    for rule in rules:
        sig = (tuple(sorted((k, C.signature(v)) for k, v in rule.crit.items())), tuple(rule.bt_names), rule.priority)
        groups[sig].append(rule)
    for sig, rs in groups.items():
        if len(rs) > 1:
            tg = {tuple(x.targets) for x in rs}
            diags.append({'type': 'DUPLICATE_RULE' if len(tg) == 1 else 'CONFLICTING_DUPLICATE_RULES',
                          'rules': [x.id for x in rs], 'targets': sorted('|'.join(t) for t in tg)})
    for rule in rules:
        if rule.errors:
            diags.append({'type': 'RULE_INVALID', 'rule': rule.id, 'row': rule.row, 'errors': rule.errors})
        if rule.bt_error:
            diags.append({'type': rule.bt_error.split(':')[0], 'rule': rule.id, 'row': rule.row, 'detail': rule.bt_error})
        if rule.unavailable:
            diags.append({'type': 'DIMENSION_NOT_AVAILABLE', 'rule': rule.id, 'row': rule.row, 'dimensions': rule.unavailable})
        if rule.multi_target:
            diags.append({'type': 'MULTI_TARGET_RULE', 'rule': rule.id, 'row': rule.row, 'targets': rule.targets})
    ordered = {lid: lines[lid] for lid in line_order}
    rs = RuleSet(rules, ordered, named, diags, [c.lower() for c in dim_columns], with_bt)
    rs.legacy = legacy
    return rs
