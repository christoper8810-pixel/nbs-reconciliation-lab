"""Mapping-workbook condition grammar (one criteria cell).

    blank                         -> unrestricted (the workbook leaves the dimension open)
    *  ANY  ALL                   -> unrestricted, stated explicitly
    <BLANK>  BLANK  EMPTY         -> the source value must be empty
    3701                          -> exact value
    3701, 3702 / newline / ;      -> alternatives (OR); whitespace separates codes when no other separator is used
    1000-1999   1000..1999        -> inclusive integer range
    >=5000  <=5999  >5000  <6000  -> numeric comparison
    37*  3?01  *ABC*              -> wildcard
    !3713  NOT 3713  <>3713  EXCL 3713   -> exclusion (AND NOT); exclusions alone mean "anything except"
    *NAME                         -> named range / list (GL Report range table, workbook defined name, CATEGORY group)
    =Sheet!B5  (formula)          -> cross-sheet reference: the cached value is used and the reference is recorded

Anything else is reported as UNINTERPRETABLE: nothing is silently ignored or invented.
"""
from __future__ import annotations

import fnmatch
import re
from dataclasses import dataclass, field

_RANGE = re.compile(r'^(-?\d+)\s*(?:-|\.\.|–|TO)\s*(-?\d+)$', re.I)
_CMP = re.compile(r'^(>=|<=|>|<)\s*(-?\d+(?:\.\d+)?)$')
_NEG = re.compile(r'^(?:!|NOT\s+|<>\s*|EXCL(?:UDE)?\s+)(.+)$', re.I)
ANY_TOKENS = {'*', 'ANY', 'ALL'}
BLANK_TOKENS = {'<BLANK>', 'BLANK', 'EMPTY'}


class ConditionError(ValueError):
    pass


@dataclass
class Condition:
    kind: str = 'ANY'                 # ANY | BLANK | SET
    exact: set = field(default_factory=set)
    ranges: list = field(default_factory=list)       # (lo, hi) inclusive, numeric
    compares: list = field(default_factory=list)     # (op, number)
    patterns: list = field(default_factory=list)     # fnmatch patterns
    excl_exact: set = field(default_factory=set)
    excl_ranges: list = field(default_factory=list)
    excl_patterns: list = field(default_factory=list)
    source: str = ''
    explicit_any: bool = False
    named: list = field(default_factory=list)        # named ranges used
    notes: list = field(default_factory=list)

    @property
    def restricted(self):
        return self.kind != 'ANY'

    @property
    def has_positive(self):
        return bool(self.exact or self.ranges or self.compares or self.patterns)

    def _pos(self, v):
        if v in self.exact:
            return True
        n = _num(v)
        if n is not None:
            if any(lo <= n <= hi for lo, hi in self.ranges):
                return True
            for op, x in self.compares:
                if (op == '>=' and n >= x) or (op == '<=' and n <= x) or (op == '>' and n > x) or (op == '<' and n < x):
                    return True
        return any(fnmatch.fnmatchcase(v, p) for p in self.patterns)

    def _neg(self, v):
        if v in self.excl_exact:
            return True
        n = _num(v)
        if n is not None and any(lo <= n <= hi for lo, hi in self.excl_ranges):
            return True
        return any(fnmatch.fnmatchcase(v, p) for p in self.excl_patterns)

    def matches(self, value):
        """True / False; None when the source does not provide the dimension (cannot decide)."""
        if self.kind == 'ANY':
            return True
        if value is None:
            return None
        v = str(value).strip().upper()
        if self.kind == 'BLANK':
            return v == ''
        if not v:
            return False
        if self.has_positive and not self._pos(v):
            return False
        return not self._neg(v)

    def describe(self):
        if self.kind == 'ANY':
            return 'ANY'
        if self.kind == 'BLANK':
            return 'must be blank'
        parts = sorted(self.exact) + [f'{lo}-{hi}' for lo, hi in self.ranges] + [f'{o}{x:g}' for o, x in self.compares] + self.patterns
        ex = sorted(self.excl_exact) + [f'{lo}-{hi}' for lo, hi in self.excl_ranges] + self.excl_patterns
        return (' OR '.join(parts) if parts else 'ANY') + (' EXCEPT ' + ', '.join(ex) if ex else '')

    def signature(self):
        return (self.kind, tuple(sorted(self.exact)), tuple(sorted(self.ranges)), tuple(sorted(self.compares)),
                tuple(sorted(self.patterns)), tuple(sorted(self.excl_exact)), tuple(sorted(self.excl_ranges)),
                tuple(sorted(self.excl_patterns)))

    def specificity(self):
        """Smaller set = more specific. Exact-only conditions rank above ranges / patterns."""
        if self.kind != 'SET':
            return 0
        return 2 if (self.exact and not (self.ranges or self.compares or self.patterns)) else 1


ANY = Condition()


def _num(v):
    try:
        return float(v) if re.fullmatch(r'-?\d+(?:\.\d+)?', v) else None
    except (TypeError, ValueError):
        return None


def text_of(value):
    if value is None:
        return ''
    if isinstance(value, float) and value.is_integer():
        return str(int(value))
    return str(value)


def split(text, space_separates=True):
    s = text.replace('\r', '\n')
    if re.search(r'[,;\n]', s):
        items = re.split(r'[,;\n]+', s)
    elif space_separates:
        s = re.sub(r'\s*(-|\.\.|–)\s*', r'\1', s)                    # keep "1000 - 1999" together
        s = re.sub(r'(?i)\b(NOT|EXCL|EXCLUDE)\s+', lambda mm: mm.group(1) + '\x00', s)      # keep "NOT 3713" together
        s = re.sub(r'(>=|<=|<>|>|<)\s+', r'\1', s)
        items = [x.replace('\x00', ' ') for x in s.split()]
    else:
        items = [s]
    return [x.strip() for x in items if x.strip()]


def parse(value, named=None, space_separates=True, blank_means='UNRESTRICTED'):
    """Parse one cell. named: {NAME: raw text}. Raises ConditionError for uninterpretable content."""
    raw = text_of(value).strip()
    c = Condition(source=raw)
    if raw == '':
        if blank_means == 'MUST_BE_BLANK':
            c.kind = 'BLANK'
        return c
    up = raw.upper()
    if up in ANY_TOKENS:
        c.explicit_any = True
        return c
    if up in BLANK_TOKENS:
        c.kind = 'BLANK'
        return c
    c.kind = 'SET'
    for item in split(raw, space_separates):
        _add(c, item, named or {}, space_separates, depth=0)
    if not c.has_positive and not (c.excl_exact or c.excl_ranges or c.excl_patterns):
        raise ConditionError(f'No usable value in {raw!r}')
    return c


def _add(c, item, named, space_separates, depth, negate=False):
    if depth > 5:
        raise ConditionError('Named range nesting deeper than 5 levels')
    it = item.strip().upper()
    m = _NEG.match(it)
    if m and not negate:
        return _add(c, m.group(1), named, space_separates, depth, negate=True)
    if it.startswith('*') and len(it) > 1 and re.fullmatch(r'\*[A-Z_][A-Z0-9_.]*', it):
        ref = named.get(it[1:])
        if ref is None:
            raise ConditionError(f'Named range {it} is not defined in the workbook')
        c.named.append(it[1:])
        for sub in split(ref, space_separates):
            _add(c, sub, named, space_separates, depth + 1, negate)
        return
    m = _RANGE.match(it)
    if m:
        lo, hi = int(m.group(1)), int(m.group(2))
        if lo > hi:
            raise ConditionError(f'MALFORMED_RANGE {item!r}: low bound above high bound')
        (c.excl_ranges if negate else c.ranges).append((lo, hi))
        return
    if re.fullmatch(r'\d+\s*-\s*', it) or re.fullmatch(r'\s*-\s*\d+', it) and not it.startswith('-') or \
            re.fullmatch(r'\d+\s*-\s*\d+[A-Z]+', it) or re.fullmatch(r'\d+\s*-\s*-\d+', it):
        raise ConditionError(f'MALFORMED_RANGE {item!r}')
    m = _CMP.match(it)
    if m:
        if negate:
            raise ConditionError(f'Negated comparison {item!r} is not supported')
        c.compares.append((m.group(1), float(m.group(2))))
        return
    if any(ch in it for ch in '*?'):
        (c.excl_patterns if negate else c.patterns).append(it)
        return
    if not re.fullmatch(r'[A-Z0-9_.&/+\- ]+', it):
        raise ConditionError(f'Uninterpretable value {item!r}')
    (c.excl_exact if negate else c.exact).add(it)


def intersects(a, b):
    """Conservative test: can one value satisfy both conditions? (exclusions ignored -> may over-report overlap)."""
    if a.kind == 'ANY' or b.kind == 'ANY':
        return True
    if a.kind == 'BLANK' or b.kind == 'BLANK':
        return a.kind == b.kind
    if a.patterns or b.patterns or a.compares or b.compares:
        return True
    if a.exact & b.exact:
        return True
    for x, y in ((a, b), (b, a)):
        for v in x.exact:
            n = _num(v)
            if n is not None and any(lo <= n <= hi for lo, hi in y.ranges):
                return True
    return any(lo1 <= hi2 and lo2 <= hi1 for lo1, hi1 in a.ranges for lo2, hi2 in b.ranges)
