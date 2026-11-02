"""Structural crosswalk from legacy report rows to QCB item codes.

QCB item codes encode the report hierarchy: <statement>-<table>-<line prefix><two-digit ordinals>.
For example legacy path "01 Inside Qatar > 02 INDUSTRY > 04 MANUFACTURING > 01 Food" in Table 44 is
QCB code 1-044-01020401. The line prefix differs per table (e.g. '' for Table 44, '1' for Table 2,
'104' for Table 7), so it is learned per table as the prefix whose generated codes exist in the BO and
whose item descriptions agree with the legacy row text. A link is accepted only when the code exists;
its text agreement is recorded so disagreements go to review rather than being trusted.
"""
from __future__ import annotations
import re
from collections import defaultdict

BASE = {'Assets': ('100', '1'), 'Liabilities': ('200', '2'), 'Contra Items': ('300', '3'), 'Income': ('400', '4'), 'Expenses': ('500', '5')}
STOP = {'and', 'of', 'the', 'in', 'other', 'others', 'by', 'from', 'to', 'for', 'on', 'a'}


def _strip(text):
    """Drop leading dots and numbering such as '....01 ', '1. ', '1.2 ', 'II - ', 'A. '."""
    return re.sub(r'^[\s.]*(?:\d+(?:\.\d+)*|[ivxlc]+|[a-z])(?:[\s.\-)]+)', '', str(text).strip().lower(), count=1).strip()


def words(text):
    return {w for w in re.findall(r'[a-z]+', _strip(text)) if w not in STOP}


def _same(a, b):
    """Spelling variants (aluminium/aluminum, istisnaa/istisna, reverse/reversed, non-qatari/non-qataris)."""
    n = min(len(a), len(b), 6)
    return a == b or (n >= 5 and a[:n] == b[:n])


def text_score(a, b):
    """Share of content words that agree. BO descriptions are cut at 30 characters, so legacy words that the
    truncated BO text could not contain are ignored."""
    a, b = _strip(a), _strip(b)
    if len(b) >= 27:  # BO text was cut at 30 characters including its own numbering
        a = a[:len(b)]
    wa, wb = words(a), words(b)
    if not wa and not wb:
        return 1.0
    matched_a = {w for w in wa if any(_same(w, x) for x in wb)}
    matched_b = {x for x in wb if any(_same(w, x) for w in wa)}
    return (len(matched_a) + len(matched_b)) / max(1, len(wa) + len(wb))


def ordinals(path):
    """Two-digit ordinals of each path level; leading non-numbered levels (e.g. bank name) are skipped."""
    out = []
    for part in path.split(' > '):
        m = re.match(r'^\.*\s*(\d+)\b', part.strip())
        if m:
            out.append(m.group(1))
        elif out:
            return None  # an unnumbered level inside the hierarchy: no structural code
    return out or None


def table_of(spec):
    if spec.get('base'):
        return BASE[spec['base']][0]
    return str(spec['table']).zfill(3) if spec.get('table') else None


def candidate_codes(spec, prefix):
    o = ordinals(spec['path'])
    if not o:
        return []
    table = table_of(spec)
    statements = '12345'
    codes = []
    variants = [o]
    if len(o[0]) == 1:  # a root written as '4 Income'
        variants = [o[1:]] if len(o) > 1 else [[]]
    for v in variants:
        suffix = prefix + ''.join(x.zfill(2) for x in v)
        if not suffix:
            suffix = prefix
        for s in statements:
            codes.append(f'{s}-{table}-{suffix}')
    return codes


def learn_prefixes(rules, bo_items):
    """bo_items: {table: {code: description}}. Returns {table: (prefix, confirmed_count, tried)}."""
    by_table = defaultdict(list)
    for spec in rules.values():
        t = table_of(spec)
        if t and t in bo_items:
            by_table[t].append(spec)
    chosen = {}
    for t, specs in by_table.items():
        suffixes = [c.split('-', 2)[2] for c in bo_items[t]]
        prefixes = {''} | {s[:k] for s in suffixes for k in range(1, min(len(s), 5) + 1)}
        best = ('', 0)
        for p in sorted(prefixes, key=lambda x: (len(x), x)):
            score = 0
            for spec in specs:
                hits = [c for c in candidate_codes(spec, p) if c in bo_items[t]]
                if len(hits) == 1 and text_score(spec['path'].split(' > ')[-1], bo_items[t][hits[0]]) >= 0.5:
                    score += 1
            if score > best[1]:
                best = (p, score)
        chosen[t] = (best[0], best[1], len(specs))
    return chosen


def structural_crosswalk(rules, bo_items):
    """Returns ({code: [match]}, prefixes). Each match: rule id, text score, path, basis."""
    prefixes = learn_prefixes(rules, bo_items)
    links = defaultdict(list)
    for rid, spec in rules.items():
        t = table_of(spec)
        if t not in prefixes or prefixes[t][1] == 0:
            continue
        hits = [c for c in candidate_codes(spec, prefixes[t][0]) if c in bo_items[t]]
        if len(hits) != 1:
            continue
        score = text_score(spec['path'].split(' > ')[-1], bo_items[t][hits[0]])
        links[hits[0]].append({'rule_id': rid, 'text_score': round(score, 3), 'path': spec['path'], 'row': spec.get('row'),
                               'basis': 'STRUCTURAL_CODE_TEXT_CONFIRMED' if score >= 0.5 else 'STRUCTURAL_CODE_TEXT_DIFFERS'})
    return dict(links), prefixes
