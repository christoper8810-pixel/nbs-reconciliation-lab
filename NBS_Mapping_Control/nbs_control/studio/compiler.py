"""Compile the workbook's own conditions into executable rules, keeping the original text and cell of every condition.

GL Report: a populated LINE cell starts a line (type H / D / T). Each row with any condition cell is one
criteria set of the current line (AND across columns, OR inside a cell). Rows without a LINE cell continue the
line above (OR between criteria rows). A '^' (or '"', 'DITTO') cell inherits the previous criteria row of the line.
Named ranges come from the GL Report range table (name / field / start / end), workbook defined names and
CATEGORY range groups, in that order. Every condition that cannot be interpreted is reported with its cell.
"""
from __future__ import annotations

from collections import OrderedDict, defaultdict

from . import conditions as C
from .workbook import addr, text

DIMS = ('app', 'market', 'currency', 'category', 'pl_category', 'pl_product', 'sector', 'pl_sector', 'pl_department',
        'balance_type', 'product', 'department', 'dao', 'branch', 'company', 'residence', 'segment')
INHERIT = {'^', '"', 'DITTO', '〃'}
LINE_TYPES = {'H': 'H', 'HEADER': 'H', 'HEADING': 'H', 'D': 'D', 'DETAIL': 'D', 'T': 'T', 'TOTAL': 'T', 'SUBTOTAL': 'T', 'S': 'T'}


class Rule:
    __slots__ = ('id', 'line', 'row', 'conds', 'cells', 'raw', 'formulas', 'errors', 'priority', 'seq')

    def __init__(self, **kw):
        for k in self.__slots__:
            setattr(self, k, kw.get(k))

    @property
    def usable(self):
        return not self.errors

    def match(self, dims):
        """True, False, or None when a restricted dimension is absent from the record."""
        unknown = False
        for d, c in self.conds.items():
            m = c.matches(dims.get(d))
            if m is False:
                return False
            if m is None:
                unknown = True
        return None if unknown else True

    def specificity(self):
        return (self.priority or 0, len(self.conds), sum(c.specificity() for c in self.conds.values()))

    def describe(self):
        return ' AND '.join(f'{d.upper()} {c.describe()}' for d, c in self.conds.items()) or 'no condition'


class Model:
    def __init__(self, wb, cfg):
        self.wb, self.cfg = wb, cfg or {}
        self.lines, self.rules, self.named, self.issues = OrderedDict(), [], {}, []
        self.glmap, self.categories, self.column_maps = [], [], {}
        self.sectors, self.coa, self.refsets = set(), set(), {}
        self.space = bool(self.cfg.get('space_separates_values', True))

    def issue(self, kind, sheet, row, col, message, severity='ERROR', **kw):
        self.issues.append({'type': kind, 'severity': severity, 'cell': addr(sheet, row, col) if col else f"'{sheet}'!{row}",
                            'sheet': sheet, 'row': row, 'message': message, **kw})

    def category_ok(self, code):
        if not self.categories:
            return None
        n = int(code) if str(code).isdigit() else None
        return any((n is not None and lo <= n <= hi) or str(code) == str(lo) for lo, hi, *_ in self.categories)

    def category_info(self, code):
        n = int(code) if str(code).isdigit() else None
        for lo, hi, group, module, tgl, row in self.categories:
            if n is not None and lo <= n <= hi:
                return {'group': group, 'module': module, 'target_gl': tgl, 'row': row}
        return None


def compile_workbook(wb, cfg=None):
    m = Model(wb, cfg)
    _reference_sheets(m)
    _named_ranges(m)
    _gl_report(m)
    _gl_mapping(m)
    return m


def _reference_sheets(m):
    wb = m.wb
    hr, cols, ev = wb.column_map('CATEGORY')
    m.column_maps['CATEGORY'] = {'header_row': hr, 'columns': cols, 'evidence': ev}
    if hr:
        sheet = wb.roles['CATEGORY']
        group = None
        for r, cells in wb.rows(sheet, hr + 1):
            g = text(cells.get(cols.get('group')))
            group = g or group
            code = text(cells.get(cols.get('code'))) or text(cells.get(5))
            if not code.isdigit():
                continue
            to = text(cells.get(cols.get('code_to')))
            hi = int(to) if to.isdigit() and int(to) >= int(code) else int(code)
            m.categories.append((int(code), hi, text(cells.get(cols.get('range_group'))) or group,
                                 text(cells.get(cols.get('module'))), text(cells.get(cols.get('target_gl'))), r))
    hr, cols, ev = wb.column_map('SEGMENT')
    m.column_maps['SEGMENT'] = {'header_row': hr, 'columns': cols, 'evidence': ev}
    if hr:
        for r, cells in wb.rows(wb.roles['SEGMENT'], hr + 1):
            s = text(cells.get(cols.get('sector')))
            code = s.split('-')[0].strip().split(' ')[0] if s else ''
            if code.isdigit():
                m.sectors.add(code)
    hr, cols, ev = wb.column_map('COA')
    m.column_maps['COA'] = {'header_row': hr, 'columns': cols, 'evidence': ev}
    if hr:
        for r, cells in wb.rows(wb.roles['COA'], hr + 1):
            v = text(cells.get(cols.get('code')))
            if v:
                m.coa.add(v.upper())
    for role in ('BRANCH', 'DAO', 'PRODUCT', 'COMPANY', 'CURRENCY', 'BALANCE_TYPE'):
        codes, ref = wb.reference_codes(role)
        if codes:
            m.refsets[role.lower()] = (codes, ref)


def _named_ranges(m):
    wb = m.wb
    hr, cols, ev = wb.column_map('GL_REPORT')
    m.column_maps['GL_REPORT'] = {'header_row': hr, 'columns': cols, 'evidence': ev}
    if hr and 'range_name' in cols:
        sheet = wb.roles['GL_REPORT']
        for r, cells in wb.rows(sheet, hr + 1):
            name = text(cells.get(cols['range_name'])).lstrip('*').upper()
            if not name:
                continue
            start, end = text(cells.get(cols.get('range_start'))), text(cells.get(cols.get('range_end')))
            body = f'{start}-{end}' if start.isdigit() and end.isdigit() else start
            if end and not (start.isdigit() and end.isdigit()):
                m.issue('NAMED_RANGE_BOUNDS', sheet, r, cols.get('range_end'), f'Range {name} end {end!r} with non-numeric start {start!r}')
            if not body:
                m.issue('NAMED_RANGE_EMPTY', sheet, r, cols['range_name'], f'Named range {name} has no values')
                continue
            if name in m.named and m.named[name]['text'] != body:
                m.issue('NAMED_RANGE_REDEFINED', sheet, r, cols['range_name'],
                        f'{name} redefined ({m.named[name]["text"]!r} at {m.named[name]["ref"]} vs {body!r})')
            m.named[name] = {'text': body, 'ref': addr(sheet, r, cols['range_name']), 'source': 'GL Report range table',
                             'field': text(cells.get(cols.get('range_field'))).upper().replace('CATEEGORY', 'CATEGORY')}
    for name, d in wb.defined_names.items():
        m.named.setdefault(name, {'text': ', '.join(d['values']), 'ref': d['ref'], 'source': 'workbook defined name', 'field': ''})
    groups = defaultdict(list)
    for lo, hi, group, *_rest, row in m.categories:
        if group:
            groups[group.upper().replace(' ', '_')].append(f'{lo}-{hi}' if hi != lo else str(lo))
    for g, items in groups.items():
        m.named.setdefault(g, {'text': ', '.join(items), 'ref': f"'{wb.roles.get('CATEGORY')}' range group {g}",
                               'source': 'CATEGORY range group', 'field': 'CATEGORY'})


def _named_texts(m):
    return {k: v['text'] for k, v in m.named.items()}


def _gl_report(m):
    wb = m.wb
    info = m.column_maps['GL_REPORT']
    hr, cols = info['header_row'], info['columns']
    if not hr:
        m.issues.append({'type': 'SHEET_MISSING', 'severity': 'ERROR', 'cell': '', 'sheet': 'GL Report', 'row': 0,
                         'message': 'No GL Report sheet: report-line conditions cannot be compiled'})
        return
    sheet = wb.roles['GL_REPORT']
    named = _named_texts(m)
    dim_cols = {d: cols[d] for d in DIMS if d in cols}
    current, prev = None, None
    for r, cells in wb.rows(sheet, hr + 1):
        lid = text(cells.get(cols.get('line')))
        populated = {d: c for d, c in dim_cols.items() if text(cells.get(c)) or (sheet, r, c) in wb.unresolved_formulas}
        if lid:
            t = LINE_TYPES.get(text(cells.get(cols.get('type'))).upper())
            if lid in m.lines:
                m.issue('DUPLICATE_LINE_ID', sheet, r, cols['line'], f'Line {lid} already defined at {m.lines[lid]["cell"]}')
                current = m.lines[lid]
            else:
                current = {'line': lid, 'type': t or ('D' if populated else 'H'), 'type_given': bool(t),
                           'description': text(cells.get(cols.get('description'))), 'row': r, 'cell': addr(sheet, r, cols['line']),
                           'total_of': text(cells.get(cols.get('total_of'))), 'target_gl': text(cells.get(cols.get('target_gl'))),
                           'rules': [], 'seq': len(m.lines)}
                m.lines[lid] = current
            prev = None
        if not populated:
            continue
        if current is None:
            m.issue('CRITERIA_WITHOUT_LINE', sheet, r, None, 'Condition row before any LINE')
            continue
        if current['type'] == 'H':
            m.issue('CRITERIA_ON_HEADER_LINE', sheet, r, None, f'Header line {current["line"]} carries conditions', 'WARNING')
        conds, cells_ref, raw, forms, errors = {}, {}, {}, {}, []
        for d, c in dim_cols.items():
            v = text(cells.get(c))
            f = wb.formula(sheet, r, c)
            if v.upper() in INHERIT:
                if prev is None or d not in prev['raw']:
                    errors.append(f'{addr(sheet, r, c)} inherits {d} but no previous criteria row of the line has it')
                    continue
                v, inherited = prev['raw'][d], prev['cells'][d]
            else:
                inherited = None
            if not v and (sheet, r, c) in wb.unresolved_formulas:
                errors.append(f'{addr(sheet, r, c)} {d}: formula {f} has no calculated value and cannot be evaluated here')
                m.issue('UNRESOLVED_FORMULA', sheet, r, c, f'{d}: formula {f} has no cached value; open and save the workbook in Excel '
                        'so the value is calculated', value=f, dimension=d)
                continue
            if not v:
                continue
            cells_ref[d] = inherited or addr(sheet, r, c)
            raw[d] = v
            if f:
                forms[d] = f
            try:
                cond = C.parse(v, named, m.space)
            except C.ConditionError as exc:
                errors.append(f'{addr(sheet, r, c)} {d}: {exc}')
                m.issue('MALFORMED_RANGE' if 'MALFORMED_RANGE' in str(exc) else 'UNRESOLVED_REFERENCE' if 'not defined' in str(exc)
                        else 'UNINTERPRETABLE_CONDITION', sheet, r, c, f'{d}: {exc}', value=v, dimension=d)
                continue
            if cond.restricted:
                conds[d] = cond
        rule = Rule(id=f'{current["line"]}#{len(current["rules"]) + 1}', line=current['line'], row=r, conds=conds, cells=cells_ref,
                    raw=raw, formulas=forms, errors=errors, priority=0, seq=len(m.rules))
        current['rules'].append(rule.id)
        m.rules.append(rule)
        prev = {'raw': raw, 'cells': cells_ref}
    for lid, ln in m.lines.items():
        if ln['type'] == 'T':
            ln['total_members'], ln['total_basis'] = _total_members(m, lid)


def _total_members(m, lid):
    order = list(m.lines)
    ln = m.lines[lid]
    if ln['total_of']:
        out = []
        for item in C.split(ln['total_of'], True):
            if '..' in item or (item.count('-') == 1 and item.split('-')[1] in m.lines):
                a, b = item.replace('..', '-').split('-', 1)
                if a in m.lines and b in m.lines and order.index(a) <= order.index(b):
                    out += order[order.index(a):order.index(b) + 1]
                    continue
            if item in m.lines:
                out.append(item)
            else:
                m.issue('TOTAL_REFERENCE_UNKNOWN', m.wb.roles['GL_REPORT'], ln['row'], None, f'Total {lid} refers to undefined line {item}')
        return out, 'EXPLICIT'
    i = order.index(lid)
    out = []
    for prev in reversed(order[:i]):
        if m.lines[prev]['type'] in ('H', 'T'):
            break
        out.append(prev)
    return list(reversed(out)), 'INFERRED_SECTION'


def _gl_mapping(m):
    wb = m.wb
    hr, cols, ev = wb.column_map('GL_MAPPING')
    m.column_maps['GL_MAPPING'] = {'header_row': hr, 'columns': cols, 'evidence': ev}
    if not hr:
        return
    sheet = wb.roles['GL_MAPPING']
    for r, cells in wb.rows(sheet, hr + 1):
        old = text(cells.get(cols.get('legacy_gl')))
        if not old:
            continue
        gl10 = old.split('-')[-1] if '-' in old else old
        m.glmap.append({'row': r, 'legacy_gl': old.upper(), 'gl10': gl10.upper(), 'currency': text(cells.get(cols.get('currency'))).upper(),
                        'target_gl': text(cells.get(cols.get('target_gl'))).upper(), 'category': text(cells.get(cols.get('category'))),
                        'line': text(cells.get(cols.get('line'))), 'classification': text(cells.get(cols.get('classification'))).upper(),
                        'description': text(cells.get(cols.get('description'))),
                        'cells': {f: addr(sheet, r, c) for f, c in cols.items()}})
