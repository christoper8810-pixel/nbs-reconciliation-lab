"""Optional legacy reference model of the supplied Ethix balance-sheet SQL (bs.docx).

The SQL is never executed. Its CASE conditions are parsed by a narrow grammar into typed predicates
(Left(field,n) In/Not In, field In/Not In/=/!=, And/Or/parentheses). Unsupported syntax fails
loudly. Rules are evaluated in their original order, first match wins, with fallback group 38.
Literal-zero output lines stay LEGACY_LITERAL_ZERO, never certified totals. Group 17 and the
fallback are not consumed by any output line and are reported as omitted balances.
"""
from __future__ import annotations
import csv
import re
from decimal import Decimal
from pathlib import Path

FIELDS = {'A.ledger_no': 'ledger', 'A.acct_no': 'account'}
SIGN_PREFIX5 = ('19045', '23000', '23010', '23020', '28000', '28010', '28020', '23050', '23070', '23055', '23085')
SIGN_EXACT = ('1900000010', '1900000011', '1900010055', '2309000001', '2309010001', '2309020001', '2309030001',
              '2309040001', '2309060001')
FALLBACK_GROUP = 38
OMITTED_GROUPS = (17, FALLBACK_GROUP)
_TOKEN = re.compile(r"\s*(?:(?P<str>'[^']*')|(?P<num>\d+)|(?P<op>!=|<>|=|,|\(|\))|(?P<word>[A-Za-z_.]+))", re.S)


class LegacyRuleError(ValueError):
    pass


def tokens(text):
    out, pos = [], 0
    text = text.strip()
    while pos < len(text):
        m = _TOKEN.match(text, pos)
        if not m or m.end() == pos:
            raise LegacyRuleError(f'Unsupported legacy SQL syntax near {text[pos:pos+30]!r}')
        pos = m.end()
        kind = m.lastgroup
        val = m.group(kind)
        out.append((kind, val[1:-1] if kind == 'str' else val))
    return out


class _Parser:
    def __init__(self, text):
        self.t = tokens(text)
        self.i = 0

    def peek(self, k=0):
        return self.t[self.i + k] if self.i + k < len(self.t) else (None, None)

    def take(self, kind=None, value=None):
        tok = self.peek()
        if (kind and tok[0] != kind) or (value and str(tok[1]).lower() != value.lower()):
            raise LegacyRuleError(f'Expected {value or kind}, found {tok[1]!r}')
        self.i += 1
        return tok

    def parse(self):
        node = self.expr()
        if self.i != len(self.t):
            raise LegacyRuleError(f'Trailing legacy SQL tokens: {self.t[self.i:]}')
        return node

    def expr(self):
        left = self.conj()
        while str(self.peek()[1]).lower() == 'or':
            self.take()
            left = {'any': [left, self.conj()]}
        return left

    def conj(self):
        left = self.atom()
        while str(self.peek()[1]).lower() == 'and':
            self.take()
            left = {'all': [left, self.atom()]}
        return left

    def atom(self):
        if self.peek()[1] == '(':
            self.take('op', '(')
            node = self.expr()
            self.take('op', ')')
            return node
        prefix = None
        if str(self.peek()[1]).lower() == 'left':
            self.take()
            self.take('op', '(')
            field = self.field()
            self.take('op', ',')
            prefix = int(self.take('num')[1])
            self.take('op', ')')
        else:
            field = self.field()
        negate = False
        word = str(self.peek()[1]).lower()
        if word == 'not':
            self.take()
            negate = True
            word = str(self.peek()[1]).lower()
        if word == 'in':
            self.take()
            self.take('op', '(')
            values = [self.take('str')[1]]
            while self.peek()[1] == ',':
                self.take()
                values.append(self.take('str')[1])
            self.take('op', ')')
        elif self.peek()[1] in ('=', '!=', '<>'):
            op = self.take('op')[1]
            values = [self.take('str')[1]]
            negate = negate or op in ('!=', '<>')
        else:
            raise LegacyRuleError(f'Unsupported comparison {self.peek()[1]!r}')
        node = {'field': field, 'prefix': prefix, 'values': values}
        return {'not': node} if negate else node

    def field(self):
        name = self.take('word')[1]
        if name not in FIELDS:
            raise LegacyRuleError(f'Unknown legacy field {name!r}')
        return FIELDS[name]


def parse(text):
    return _Parser(text).parse()


def match(node, row):
    if 'all' in node:
        return all(match(x, row) for x in node['all'])
    if 'any' in node:
        return any(match(x, row) for x in node['any'])
    if 'not' in node:
        return not match(node['not'], row)
    v = row.get(node['field']) or ''
    if node['prefix']:
        v = v[:node['prefix']]
    return v in node['values']


def load_rules(case_csv):
    rules = []
    with open(case_csv, encoding='utf-8-sig', newline='') as f:
        for r in csv.DictReader(f):
            group = int(re.match(r'\s*(\d+)', r['label']).group(1))
            rules.append({'order': int(r['case_order']), 'group': group, 'label': r['label'].strip(),
                          'condition': r['condition_as_supplied'], 'predicate': parse(r['condition_as_supplied'])})
    rules.sort(key=lambda x: x['order'])
    return rules


def load_outputs(lines_csv):
    out = []
    with open(lines_csv, encoding='utf-8-sig', newline='') as f:
        for r in csv.DictReader(f):
            out.append({'line': int(r['output_number']), 'description': r['description'].strip(),
                        'groups': [int(g) for g in r['group_numbers'].split(',') if g.strip()], 'mode': r['value_mode']})
    return out


def legacy_sign(ledger):
    return -1 if ledger[:5] in SIGN_PREFIX5 or ledger in SIGN_EXACT else 1


def classify(rules, row):
    for rule in rules:
        if match(rule['predicate'], row):
            return rule['group']
    return FALLBACK_GROUP


def run(rules, outputs, rows):
    """rows: dicts with ledger, account, amount (Decimal, raw sign). Returns legacy reference lines."""
    groups = {}
    for row in rows:
        g = classify(rules, row)
        amt = row['amount'] * legacy_sign(row['ledger']) / Decimal(1000)
        acc = groups.setdefault(g, {'rows': 0, 'amount_thousands': Decimal(0), 'raw_amount': Decimal(0)})
        acc['rows'] += 1
        acc['amount_thousands'] += amt
        acc['raw_amount'] += row['amount']
    consumed = {g for o in outputs for g in o['groups']}
    lines = []
    for o in outputs:
        if o['mode'] == 'LITERAL_ZERO':
            lines.append({**o, 'value': None, 'status': 'LEGACY_LITERAL_ZERO_NOT_CERTIFIED',
                          'note': 'The supplied SQL returns literal 0; Crystal total formulas were not supplied'})
        else:
            v = sum((groups.get(g, {}).get('amount_thousands', Decimal(0)) for g in o['groups']), Decimal(0))
            lines.append({**o, 'value': v, 'status': 'LEGACY_REFERENCE_MODEL'})
    omitted = {g: groups[g] for g in groups if g not in consumed}
    return {'lines': lines, 'groups': groups, 'omitted_groups': omitted,
            'omitted_nonzero': {g: v for g, v in omitted.items() if v['raw_amount'] != 0},
            'note': 'Optional legacy reference only; Ethix display signs are not T24 source signs'}
