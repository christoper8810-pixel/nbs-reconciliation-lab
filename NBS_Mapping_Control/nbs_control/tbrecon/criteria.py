"""Mapping-rule criterion tokens.

Supported, per cell:
* blank                     -> UNRESTRICTED (configurable: criteria.blank_means = UNRESTRICTED | MUST_BE_BLANK)
* '*', 'ANY', 'ALL'         -> UNRESTRICTED, stated explicitly
* '<BLANK>'                 -> the source value must be empty
* '*NAME'                   -> named range / list defined in the rule file (GL Report style)
* 'a, b\\nc; d'             -> OR alternatives (comma, semicolon, newline)
* '1000-1999'               -> inclusive integer range (both ends integers, low <= high)
* '37*'                     -> prefix
* '1000-1999, 6001, 7001'   -> inclusive range 1000..1999 OR 6001 OR 7001

The legacy mode reproduces the token handling of the original gl_mapping adapter (whitespace /
comma split, every item an exact literal, so '1000-1999' never matched a category). It exists only to
measure BEFORE statistics; it is never the default.
"""
from __future__ import annotations

import re
from dataclasses import dataclass, field

_RANGE = re.compile(r'^(\d+)\s*-\s*(\d+)$')
DEFAULTS = {'blank_means': 'UNRESTRICTED', 'explicit_any_tokens': ['*', 'ANY', 'ALL'],
            'explicit_blank_token': '<BLANK>', 'list_separators': [',', ';', '\n']}


class CriteriaError(ValueError):
    pass


@dataclass(frozen=True)
class Criterion:
    kind: str                      # ANY | BLANK | SET
    exact: frozenset = frozenset()
    ranges: tuple = ()
    prefixes: tuple = ()
    source: str = ''
    explicit: bool = False         # ANY written explicitly rather than left blank

    @property
    def restricted(self) -> bool:
        return self.kind != 'ANY'

    @property
    def exact_only(self) -> bool:
        return self.kind == 'SET' and not self.ranges and not self.prefixes

    def matches(self, value) -> bool:
        v = '' if value is None else str(value).strip().upper()
        if self.kind == 'ANY':
            return True
        if self.kind == 'BLANK':
            return v == ''
        if not v:
            return False
        if v in self.exact:
            return True
        if self.ranges and v.isdigit():
            n = int(v)
            if any(lo <= n <= hi for lo, hi in self.ranges):
                return True
        return any(v.startswith(p) for p in self.prefixes)

    def values(self) -> list:
        out = sorted(self.exact)
        out += [f'{lo}-{hi}' for lo, hi in self.ranges]
        out += [p + '*' for p in self.prefixes]
        return out


ANY = Criterion('ANY')


def split_items(text, separators=None):
    seps = separators or DEFAULTS['list_separators']
    pattern = '|'.join(re.escape(s) for s in seps)
    return [x.strip() for x in re.split(pattern, text) if x.strip()]


def parse(text, named=None, cfg=None, legacy=False) -> Criterion:
    cfg = {**DEFAULTS, **(cfg or {})}
    raw = '' if text is None else str(text)
    if isinstance(text, float) and text.is_integer():
        raw = str(int(text))
    s = raw.strip()
    if legacy:
        # Original gl_mapping._token_filter: '*NAME' resolved from the named table, otherwise whitespace / comma split,
        # every item an exact literal (so an inline '1000-1999' range never matched).
        if s.startswith('*') and len(s) > 1:
            return parse(s, named, cfg)
        items = [x.upper() for x in re.split(r'[\s,;]+', s) if x]
        if not items:
            return ANY
        return Criterion('SET', exact=frozenset(items), source=raw)
    if s == '':
        if cfg['blank_means'] == 'MUST_BE_BLANK':
            return Criterion('BLANK', source=raw)
        return ANY
    if s.upper() in [t.upper() for t in cfg['explicit_any_tokens']]:
        return Criterion('ANY', source=raw, explicit=True)
    if s.upper() == cfg['explicit_blank_token'].upper():
        return Criterion('BLANK', source=raw)
    exact, ranges, prefixes = set(), [], []
    for item in split_items(s, cfg['list_separators']):
        if item.startswith('*') and len(item) > 1:
            ref = (named or {}).get(item[1:].upper())
            if ref is None:
                raise CriteriaError(f'Named range {item} is not defined')
            sub = parse(ref, None, cfg)
            if sub.kind != 'SET':
                raise CriteriaError(f'Named range {item} must list values')
            exact |= sub.exact
            ranges += sub.ranges
            prefixes += sub.prefixes
            continue
        m = _RANGE.match(item)
        if m:
            lo, hi = int(m.group(1)), int(m.group(2))
            if lo > hi:
                raise CriteriaError(f'Range {item} has low > high')
            ranges.append((lo, hi))
        elif '-' in item and re.match(r'^\d', item):
            raise CriteriaError(f'Malformed numeric range {item!r}')
        elif item.endswith('*') and len(item) > 1:
            prefixes.append(item[:-1].upper())
        else:
            exact.add(item.upper())
    if not (exact or ranges or prefixes):
        return ANY
    return Criterion('SET', frozenset(exact), tuple(sorted(set(ranges))), tuple(sorted(set(prefixes))), raw)


def signature(c: Criterion):
    return (c.kind, tuple(sorted(c.exact)), c.ranges, c.prefixes)
