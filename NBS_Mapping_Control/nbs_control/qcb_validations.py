"""QCB NBS validation rules: parse, de-duplicate, evaluate. Rule text is data; nothing is executed.

A rule compares two expressions of report cells, e.g.
    $100{1-100-101}#INSIDE_LC#  =  $001{1-001-10101}#INSIDE_LC#+$001{1-001-10102}#INSIDE_LC#
A term is $<table>{<item code>}#<QCB measure>[+<QCB measure>...]#. Expressions combine terms,
parentheses, unary minus and numeric constants with + and -. Operators: =, >=, <=, <, >.
A small number of rules omit a closing '#'; they are repaired and flagged, never guessed beyond that.
"""
from __future__ import annotations
import hashlib
import re
from decimal import Decimal
from pathlib import Path

from . import ooxml

OPERATORS = ('>=', '<=', '<>', '=', '<', '>')

# QCB column codes -> semantic measure used in the BO catalogue (table-specific where they differ).
GEO = {'INSIDE_LC': 'IN_LC', 'INSIDE_FC': 'IN_FC', 'OUTSIDE_LC': 'OUT_LC', 'OUTSIDE_FC': 'OUT_FC'}
MATURITY = {'WITHOUT_MATURITY': 'MAT_NONE', 'ONE_WEEK': 'MAT_1W', 'ONE_WEEK_TO_1_MONTH': 'MAT_1M', 'ONE_TO_3_MONTHS': 'MAT_3M',
            'THREE_TO_6_MONTHS': 'MAT_6M', 'SIX_TO_12_MONTHS': 'MAT_12M', 'ONE_TO_2_YEARS': 'MAT_2Y', 'TWO_TO_5_YEARS': 'MAT_5Y',
            'TOW_TO_5_YEARS': 'MAT_5Y', 'FIVE_TO_10_YEARS': 'MAT_10Y', 'TEN_TO_20_YEARS': 'MAT_20Y', 'OVER_20_YEARS': 'MAT_GT20Y',
            'OVER_5_YEARS': 'MAT_GT5Y', 'ONE_TO_5_YEARS': 'MAT_1Y_5Y', 'OVER_10_YEARS': 'MAT_GT10Y', 'OVER_2_YEARS': 'MAT_GT2Y',
            'TOVER_2_YEARS': 'MAT_GT2Y', 'CURRENT_AND_CALL': 'DEP_CURRENT_CALL', 'SAVING': 'DEP_SAVING'}
BANDS = {'UP_TO_100': 'BAND_UPTO_100TH', 'FROM_100_1000': 'BAND_HUN_TO_1000TH', 'FROM_1000_2500': 'BAND_THOU_TO_2500TH',
         'FROM_2500_10000': 'BAND_TFHUN_TO_10000TH', 'FROM_10M_50M': 'BAND_TEN_TO_50MI', 'FROM_50M_100M': 'BAND_FIFTY_TO_100MI',
         'FROM_100M_500M': 'BAND_HUN_TO_500MI', 'FROM_500M_1000M': 'BAND_FHUN_TO_1000MI', 'OVER_1000M': 'BAND_GREATER1000MI'}
RISK = {'GOOD': 'GOOD', 'SPECIAL': 'WATCH', 'SUBSTAND': 'SUBSTANDARD', 'DOUBTFUL': 'DOUBTFUL', 'BADDEBTS': 'BAD'}
SECTOR = {'NONBANK_FIN_INST': 'NBFI', 'GOV_INST': 'GOV', 'SEMI_GOV_INST': 'SEMI_GOV', 'PRIVATE_CORP': 'PRIVATE', 'PERSONAL': 'PERSONAL'}
# Exact BO header names where the semantic key alone is not unique or the BO header text is idiosyncratic.
HEADER = {
    '004': {f'{l}_{g}_{c}': f'{"Ls" if l == "LISTED" else "Uls"} {"In" if g == "INSIDE" else "Out"} Amount {c.title()}'
            for l in ('LISTED', 'UNLISTED') for g in ('INSIDE', 'OUTSIDE') for c in ('LC', 'FC')},
    '013': {'SECURED_AMT': 'Secured Amt', 'UNSECURED_AMT': 'Unsecured Amt'},
    '016': {f'{g}_{k}': f'{v} {"In" if g == "INSIDE" else "Out"} Qatar' for g in ('INSIDE', 'OUTSIDE') for k, v in
            {'COST': 'Cost', 'PROV_DEPRECIATE': 'Prov Depre', 'PROV_DECLINE': 'Prov Decline', 'CHANG_FAIR_POS': 'Change Pos', 'CHANG_FAIR_NEG': 'Change Neg'}.items()},
    '017': {f'{g}_{k}': f'{v} {"In" if g == "INSIDE" else "Out"} Qatar' for g in ('INSIDE', 'OUTSIDE') for k, v in
            {'COST': 'Cost', 'PROV_DEPRECIATE': 'Prov Depre', 'PROV_DECLINE': 'Prov Decline'}.items()},
    '018': {'INSIDE_COST': 'Orig Cost In Qatar', 'INSIDE_AMORTIZATION': 'Amor Impair In Qatar',
            'OUTSIDE_COST': 'Orig Cost Out Qatar', 'OUTSIDE_AMORTIZATION': 'Amor Impair Out Qatar'},
    '030': {'INSIDE_PERFORM': 'Perf In Amount', 'INSIDE_NONPERFORM': 'Nperf In Amount', 'OUTSIDE_PERFORM': 'Perf Out Amount',
            'OUTSIDE_NONPERFORM': 'Nperf Out Amount'},
    '032': {'LC': 'In Amount Lc', 'FC': 'In Amount Fc'},
    '033': {'INSIDE_POSITIVE': 'Postive In Amount', 'INSIDE_NEGATIVE': 'Neg In Amount', 'OUTSIDE_POSITIVE': 'Postive Out Amount',
            'OUTSIDE_NEGATIVE': 'Neg Out Amount'},
    '037': {'OVERDRAFT': 'Over Draft', 'LOANS_AND_ADVACNES': 'Loans Advances', 'ISTISNAA': 'Istisna', 'MUDARABA_MUSHARAKA': 'Mudar Mushar',
            'OTHER_ISLAMIC_FINANCE': 'Other Islamic Finance', 'TOTAL_LESS_1_YEAR': 'Tot Less 1 Year', 'LC_AMOUNT': 'LC Amount', 'LG_AMOUNT': 'LG Amount'},
    '038': {'NOTIONAL_AMOUNT': 'Nat Amount', 'POSITIVE_FAIR_VALUE': 'Pive Fair Value', 'NEGATIVE_FAIR_VALUE': 'Negative Fair Value',
            'NOTIONAL_3_M': 'Nat In 3 Month', 'NOTIONAL_3_TO_12_M': 'Nat 3 to 12 Month', 'NOTIONAL_1_TO_5_Y': 'Nat 1 to 5 Year',
            'NOTIONAL_OVER_5_Y': 'Nat Over 5 Year'},
    '040': {'EQUITY_PARTICIPATE': 'Equity Partcip'},
    '042': {'LISTED_INSIDE_LC': 'Listed Lc', 'LISTED_INSIDE_FC': 'Listed Fc', 'UNLISTED_INSIDE_LC': 'Unlited Lc', 'UNLISTED_INSIDE_FC': 'Unlisted Fc'},
    '043': {'INSIDE_PROFIT': 'Profit Inside Qatar', 'INSIDE_LOSS': 'Loss Inside Qatar', 'OUTSIDE_PROFIT': 'Profit Outside Qatar',
            'OUTSIDE_LOSS': 'Loss Outside Qatar'},
}


class RuleSyntaxError(ValueError):
    pass


def semantic_for(table, code):
    if code in GEO:
        return GEO[code]
    if code in MATURITY:
        return MATURITY[code]
    m = re.fullmatch(r'(.+)_(NO|AMT)', code)
    if m and m.group(1) in BANDS:
        return BANDS[m.group(1)] + ('_COUNT' if m.group(2) == 'NO' else '_AMOUNT')
    m = re.fullmatch(r'(GOOD|SPECIAL|SUBSTAND|DOUBTFUL|BADDEBTS)_(DIR|INDIR)', code)
    if m:
        return RISK[m.group(1)] + ('_DIRECT' if m.group(2) == 'DIR' else '_INDIRECT')
    m = re.fullmatch(r'(.+)_(LC|FC)', code)
    if m and m.group(1) in SECTOR:
        return f'SECTOR_{SECTOR[m.group(1)]}_{m.group(2)}'
    if code in ('TOTAL_LC', 'TOTAL_FC'):
        return code
    return None


def header_for(table, code, catalogue):
    """Resolve a QCB measure code to the BO header of that table, or None (unmapped)."""
    measures = catalogue['tables'].get(table, {}).get('measures', {})
    if table in HEADER and code in HEADER[table]:
        h = HEADER[table][code]
        return h if h in measures else None
    sem = semantic_for(table, code)
    hits = [h for h, m in measures.items() if m.get('semantic') == sem]
    return hits[0] if len(hits) == 1 else None


# ---------------------------------------------------------------- parsing
_TOK = re.compile(r"\s*(?:(?P<term>\$\d+\{[^}]*\}#[^#]*?(?:#|(?=\$|[+\-]\$|\)|$)))|(?P<num>\d+(?:\.\d+)?)|(?P<op>[+\-*/()]))")
_MISSING_DOLLAR = re.compile(r'(?<![\$\d{])(\d{3})\{')


def _term(text):
    m = re.fullmatch(r'\$(\d+)\{([^}]*)\}#([^#]*)(#?)', text.strip())
    if not m:
        raise RuleSyntaxError(f'Bad term {text!r}')
    measures = [x.strip() for x in m.group(3).split('+') if x.strip()]
    if not measures:
        raise RuleSyntaxError(f'Term without measure {text!r}')
    return {'t': 'term', 'table': m.group(1).zfill(3), 'item': m.group(2).strip(), 'measures': measures, 'repaired': m.group(4) != '#'}


def repair(text):
    """Only two mechanical repairs: a term written without its leading '$', and a missing closing '#'
    (handled in the tokenizer). Returns (text, repaired?)."""
    fixed = _MISSING_DOLLAR.sub(r'$\1{', text)
    return fixed, fixed != text


def tokens(text):
    out, pos = [], 0
    text = text.strip()
    while pos < len(text):
        m = _TOK.match(text, pos)
        if not m or m.end() == pos:
            raise RuleSyntaxError(f'Unsupported rule syntax near {text[pos:pos + 40]!r}')
        pos = m.end()
        out.append((m.lastgroup, m.group(m.lastgroup)))
    return out


def parse_expr(text):
    """Recursive descent: sum := prod (('+'|'-') prod)* ; prod := unary (('*'|'/') unary)* ;
    unary := ('-'|'+')* atom ; atom := term | number | '(' sum ')'."""
    text, fixed = repair(text)
    toks = tokens(text)
    pos = [0]

    def peek():
        return toks[pos[0]] if pos[0] < len(toks) else (None, None)

    def take():
        tok = peek()
        pos[0] += 1
        return tok

    def atom():
        kind, val = take()
        if kind == 'term':
            node = _term(val)
            node['repaired'] = node['repaired'] or fixed
            return node
        if kind == 'num':
            return {'t': 'num', 'value': val}
        if val == '(':
            node = sum_()
            if take()[1] != ')':
                raise RuleSyntaxError('Unclosed parenthesis')
            return node
        raise RuleSyntaxError(f'Unexpected {val!r}')

    def unary():
        sign = 1
        while peek()[1] in ('+', '-'):
            sign *= -1 if take()[1] == '-' else 1
        node = atom()
        return node if sign == 1 else {'t': 'sum', 'parts': [(-1, node)]}

    def prod():
        node = unary()
        while peek()[1] in ('*', '/'):
            op = take()[1]
            node = {'t': 'prod', 'op': op, 'a': node, 'b': unary()}
        return node

    def sum_():
        parts = [(1, prod())]
        while peek()[1] in ('+', '-'):
            sign = -1 if take()[1] == '-' else 1
            parts.append((sign, prod()))
        return parts[0][1] if len(parts) == 1 and parts[0][0] == 1 else {'t': 'sum', 'parts': parts}

    if not toks:
        raise RuleSyntaxError('Empty expression')
    node = sum_()
    if pos[0] != len(toks):
        raise RuleSyntaxError(f'Unexpected {peek()[1]!r}')
    return node

def terms(node):
    if node['t'] == 'term':
        yield node
    elif node['t'] == 'sum':
        for _, p in node['parts']:
            yield from terms(p)
    elif node['t'] == 'prod':
        yield from terms(node['a'])
        yield from terms(node['b'])


def canonical(node):
    if node['t'] == 'term':
        return f"${node['table']}{{{node['item']}}}#{'+'.join(node['measures'])}#"
    if node['t'] == 'num':
        return str(Decimal(node['value']).normalize())
    if node['t'] == 'prod':
        return '(' + canonical(node['a']) + node['op'] + canonical(node['b']) + ')'
    return '(' + ''.join(('+' if s > 0 else '-') + canonical(p) for s, p in node['parts']) + ')'


def evaluate(node, lookup):
    """lookup(table, item, qcb_measure) -> Decimal | raises KeyError(reason)."""
    if node['t'] == 'num':
        return Decimal(node['value'])
    if node['t'] == 'term':
        return sum((lookup(node['table'], node['item'], m) for m in node['measures']), Decimal(0))
    if node['t'] == 'prod':
        a, b = evaluate(node['a'], lookup), evaluate(node['b'], lookup)
        if node['op'] == '*':
            return a * b
        if b == 0:
            raise KeyError('division by zero in rule')
        return a / b
    return sum((s * evaluate(p, lookup) for s, p in node['parts']), Decimal(0))


def n_cells(node):
    return sum(len(t['measures']) for t in terms(node))


def has_ratio(node):
    if node['t'] == 'prod':
        return True
    if node['t'] == 'sum':
        return any(has_ratio(p) for _, p in node['parts'])
    return False


# ---------------------------------------------------------------- import
def _file_date(name):
    m = re.search(r'(\d{2})(\d{2})(\d{4})', name)
    return f'{m.group(3)}-{m.group(2)}-{m.group(1)}' if m else None


def load_rules(paths):
    """All rules from the supplied workbooks, de-duplicated by canonical expression; provenance kept."""
    from .rebuild_store import sha256
    rules = {}
    descriptions = {}
    errors = []
    for path in paths:
        path = Path(path)
        digest = sha256(path)
        fdate = _file_date(path.name)
        for sheet, part in ooxml.sheets(path):
            header = None
            for row_no, cells in ooxml.raw_rows(path, part):
                vals = {k: v[0] for k, v in cells.items()}
                if vals.get('A') in ('VALIDATE_CODE', 'Code'):
                    header = vals
                    continue
                left, right = vals.get('B', ''), vals.get('C', '')
                if '$' not in left and '$' not in right:
                    if header and vals.get('A') and vals.get('B'):
                        descriptions.setdefault(ooxml.identifier(vals['A']), vals['B'].strip())
                    continue
                op = (vals.get('D') or '=').strip() or '='
                prov = {'file': path.name, 'file_sha256': digest, 'file_date': fdate, 'sheet': sheet, 'row': row_no,
                        'code': ooxml.identifier(vals.get('A', '')), 'description': (vals.get('E') or '').strip()}
                try:
                    if op not in OPERATORS:
                        raise RuleSyntaxError(f'Unknown operator {op!r}')
                    lnode, rnode = parse_expr(left), parse_expr(right)
                except RuleSyntaxError as exc:
                    errors.append({**prov, 'left': left, 'right': right, 'operator': op, 'error': str(exc)})
                    continue
                key = hashlib.sha256(f'{canonical(lnode)}|{op}|{canonical(rnode)}'.encode()).hexdigest()[:16]
                r = rules.setdefault(key, {'rule_id': 'Q' + key, 'left': left.strip(), 'right': right.strip(), 'operator': op,
                                           'left_ast': lnode, 'right_ast': rnode, 'provenance': [],
                                           'repaired': any(t['repaired'] for t in list(terms(lnode)) + list(terms(rnode))),
                                           'tables': sorted({t['table'] for t in list(terms(lnode)) + list(terms(rnode))})})
                r['provenance'].append(prov)
    for r in rules.values():
        latest = max(r['provenance'], key=lambda p: (p['file_date'] or '', p['file']))
        r['qcb_code'] = latest['code']
        r['description'] = latest['description'] or descriptions.get(latest['code'], '')
        r['latest_file'] = latest['file']
        r['kind'] = classify_rule(r)
    return sorted(rules.values(), key=lambda r: (r['latest_file'], int(r['qcb_code']) if r['qcb_code'].isdigit() else 0, r['rule_id'])), errors


def classify_rule(rule):
    lt = {t['table'] for t in terms(rule['left_ast'])}
    rt = {t['table'] for t in terms(rule['right_ast'])}
    tables = lt | rt
    if any(t >= '600' for t in tables):
        return 'ADDITIONAL_TABLE (60x not in BO workbook)'
    if rule['operator'] != '=':
        return 'INEQUALITY'
    lm = {m for t in terms(rule['left_ast']) for m in t['measures']}
    rm = {m for t in terms(rule['right_ast']) for m in t['measures']}
    if len(tables) == 1:
        return 'WITHIN_TABLE_SUBTOTAL' if lm == rm else 'WITHIN_TABLE_CROSS_MEASURE'
    if {'100', '200', '300', '400', '500'} & tables:
        return 'BASE_SCHEDULE_TO_DETAIL'
    return 'CROSS_DIMENSION_SAME_POPULATION' if lm != rm else 'CROSS_TABLE_SAME_MEASURE'


def check(rule, lookup, tolerance_per_cell=Decimal('0.5')):
    try:
        lv = evaluate(rule['left_ast'], lookup)
        rv = evaluate(rule['right_ast'], lookup)
    except KeyError as exc:
        return {'status': 'NOT_EVALUABLE', 'reason': str(exc.args[0]), 'left': None, 'right': None, 'difference': None}
    diff = lv - rv
    tol = tolerance_per_cell * (n_cells(rule['left_ast']) + n_cells(rule['right_ast']))
    if has_ratio(rule['left_ast']) or has_ratio(rule['right_ast']):
        tol = Decimal(0)  # ratio rules (average size per band) are checked as stated
    op = rule['operator']
    ok = {'=': diff == 0, '>=': diff >= 0, '<=': diff <= 0, '<': diff < 0, '>': diff > 0, '<>': diff != 0}[op]
    near = {'=': abs(diff) <= tol, '>=': diff >= -tol, '<=': diff <= tol, '<': diff < tol, '>': diff > -tol, '<>': True}[op]
    status = 'PASS' if ok else 'PASS_WITHIN_ROUNDING' if near else 'FAIL'
    return {'status': status, 'reason': None, 'left': lv, 'right': rv, 'difference': diff}


def lookup_factory(values, catalogue, available_tables):
    """values: {(table, item, header): Decimal | None}. Raises KeyError with a reason when not evaluable."""
    def lookup(table, item, code):
        if table not in available_tables:
            raise KeyError(f'table {table} not in this report version')
        h = header_for(table, code, catalogue)
        if h is None:
            raise KeyError(f'measure {code} has no validated header in table {table}')
        key = (table, item, h)
        if key not in values:
            raise KeyError(f'item {item} not in table {table}')
        v = values[key]
        if v is None:
            raise KeyError(f'{table} {item} {h} unavailable')
        return v
    return lookup


def import_rules(c, paths):
    """Register each validation workbook by hash and store the de-duplicated rules (replacing earlier imports)."""
    import json
    from .rebuild_store import register_source
    for p in paths:
        register_source(c, p, 'QCB_NBS_VALIDATIONS', 'qcb-rules-1')
    rules, errors = load_rules(paths)
    c.execute('DELETE FROM qcb_rules')
    c.executemany('INSERT INTO qcb_rules VALUES(?,?,?,?,?,?,?)',
                  [(r['rule_id'], r['qcb_code'], r['kind'], r['operator'], r['left'], r['right'], json.dumps(r)) for r in rules])
    c.commit()
    return {'rules': len(rules), 'parse_errors': errors, 'files': [str(p) for p in paths]}


def stored_rules(c):
    import json
    return [json.loads(x) for (x,) in c.execute('SELECT rule FROM qcb_rules ORDER BY rowid')]
