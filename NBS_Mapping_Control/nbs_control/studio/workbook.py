"""Read the Excel mapping workbook as data: cached values, formulas, defined names, and sheet / column roles.

Columns are located by their header text. The column letters used by the existing adapter (gl_mapping.py,
built against the bank workbook) are only a fallback, and every use of a fallback is recorded in the
column map so it can be checked. Nothing in the workbook is executed.
"""
from __future__ import annotations

import hashlib
import re
from pathlib import Path

from openpyxl import load_workbook
from openpyxl.utils import get_column_letter, column_index_from_string, range_boundaries

SHEET_ROLES = {
    'GL_REPORT': ('GL REPORT', 'GLREPORT', 'GL CRITERIA', 'REPORT LINES'),
    'GL_MAPPING': ('GL MAPPING', 'GLMAPPING', 'GL MAP'),
    'CATEGORY': ('CATEGORY', 'CATEGORIES'),
    'COA': ('COA', 'CHART OF ACCOUNTS'),
    'SEGMENT': ('SEGMENT', 'SECTOR'),
    'BRANCH': ('BRANCH', 'BRANCHES'),
    'DAO': ('DAO', 'ACCOUNT OFFICER'),
    'PRODUCT': ('PRODUCT', 'PRODUCTS'),
    'COMPANY': ('COMPANY', 'COMPANIES'),
    'CURRENCY': ('CURRENCY', 'CURRENCIES', 'CCY'),
    'BALANCE_TYPE': ('BALANCE TYPE', 'BALANCE TYPES', 'ASSET TYPE'),
}

COLUMNS = {
    'GL_REPORT': {
        'line': ('LINE', 'DKBGL', 'REPORT LINE', 'LINE NO', 'LINE ID'), 'type': ('TYPE', 'LINE TYPE', 'H/D/T', 'LEVEL'),
        'description': ('DESCRIPTION', 'DESC', 'LINE DESCRIPTION'), 'app': ('APP', 'APPLICATION'),
        'market': ('MARKET', 'CURRENCY MARKET'), 'currency': ('CURRENCY', 'CCY'), 'category': ('CATEGORY', 'CATEG', 'CATEGORY CODE'),
        'pl_category': ('PL CATEGORY', 'PLCATEGORY', 'PL.CATEGORY'), 'pl_product': ('PL PRODUCT', 'PLPRODUCT', 'PL.PRODUCT'),
        'sector': ('SECTOR',), 'pl_sector': ('PL SECTOR', 'PLSECTOR'), 'pl_department': ('PL DEPARTMENT', 'PLDEPARTMENT', 'PL DEPT'),
        'balance_type': ('BALANCE', 'BALANCE TYPE', 'BAL TYPE', 'ASSET TYPE'), 'note': ('NOTE', 'NOTES', 'REMARK', 'REMARKS', 'COMMENT'),
        'product': ('PRODUCT', 'PRODUCT CODE'), 'department': ('DEPARTMENT', 'DEPT', 'DEPT CODE'), 'dao': ('DAO', 'ACCOUNT OFFICER'),
        'branch': ('BRANCH', 'BRANCH CODE'), 'company': ('COMPANY', 'CO CODE', 'COMPANY CODE'), 'residence': ('RESIDENCE', 'RESIDENCY'),
        'segment': ('SEGMENT',), 'target_gl': ('GL', 'TARGET GL', 'T24 GL', 'TRANSACT GL'), 'priority': ('PRIORITY',),
        'total_of': ('TOTAL OF', 'SUM OF', 'TOTALS', 'TOTAL LINES'),
        'range_name': ('RANGE', 'RANGE NAME', 'NAME'), 'range_field': ('FIELD', 'RANGE FIELD'),
        'range_start': ('START', 'FROM', 'VALUES', 'RANGE START'), 'range_end': ('END', 'TO', 'RANGE END'),
    },
    'GL_MAPPING': {
        'legacy_gl': ('OLD GL', 'ETHIX GL', 'LEGACY GL', 'GL ACCOUNT', 'OLD GL NUMBER', 'OLD ACCOUNT'), 'currency': ('CCY', 'CURRENCY'),
        'description': ('DESCRIPTION', 'DESC', 'GL DESCRIPTION'), 'target_gl': ('TRANSACT GL', 'T24 GL', 'NEW GL', 'TEMENOS GL', 'TARGET GL'),
        'classification': ('CLASSIFICATION', 'CLASS'), 'category': ('CATEGORY', 'T24 CATEGORY'),
        'line': ('DKBGL', 'GL REPORT LINE', 'REPORT LINE', 'LINE'),
    },
    'CATEGORY': {
        'group': ('GROUP', 'CATEGORY GROUP'), 'code': ('CATEGORY', 'CODE', 'CATEGORY CODE', 'FROM'), 'code_to': ('TO', 'CODE TO'),
        'module': ('MODULE', 'APPLICATION'), 'description': ('DESCRIPTION', 'DESC', 'NAME'), 'gl_param': ('GL PARAM', 'GL PARAMETER'),
        'target_gl': ('TRANSACT GL', 'T24 GL', 'GL'), 'range_group': ('RANGE', 'RANGE GROUP'),
    },
    'SEGMENT': {'customer_type': ('CUSTOMER TYPE', 'TYPE'), 'gl_class': ('GL', 'GL CLASS', 'GL CLASSIFICATION'),
                'sector': ('SECTOR', 'SECTOR CODE'), 'segment': ('SEGMENT',)},
    'COA': {'code': ('GL', 'GL CODE', 'ACCOUNT', 'GL ACCOUNT', 'CODE', 'TRANSACT GL'), 'description': ('DESCRIPTION', 'NAME')},
}
GENERIC_CODE = ('CODE', 'ID', 'BRANCH', 'DAO', 'PRODUCT', 'COMPANY', 'CURRENCY', 'CCY', 'BALANCE TYPE', 'TYPE')
# Letter positions of the existing adapter (nbs_control/gl_mapping.py), used only when a header is not recognised.
FALLBACK = {
    'GL_REPORT': {'line': 'A', 'type': 'B', 'description': 'C', 'app': 'D', 'market': 'E', 'currency': 'F', 'category': 'G',
                  'pl_category': 'H', 'pl_product': 'I', 'sector': 'J', 'pl_sector': 'K', 'pl_department': 'L', 'balance_type': 'M',
                  'note': 'N', 'range_name': 'O', 'range_field': 'P', 'range_start': 'Q', 'range_end': 'R'},
    'GL_MAPPING': {'legacy_gl': 'A', 'currency': 'B', 'description': 'C', 'target_gl': 'E', 'classification': 'H', 'category': 'L', 'line': 'W'},
    'CATEGORY': {'group': 'A', 'code': 'B', 'code_to': 'C', 'module': 'D', 'description': 'F', 'gl_param': 'G', 'target_gl': 'H', 'range_group': 'K'},
    'SEGMENT': {'customer_type': 'A', 'gl_class': 'B', 'sector': 'C', 'segment': 'D'},
    'COA': {'code': 'G'},
}


def norm(h):
    return re.sub(r'[\s_.\-]+', ' ', str(h or '')).strip().upper()


def sha256(path):
    h = hashlib.sha256()
    with Path(path).open('rb') as f:
        for b in iter(lambda: f.read(1 << 20), b''):
            h.update(b)
    return h.hexdigest()


class Workbook:
    def __init__(self, path):
        self.path = Path(path)
        self.sha256 = sha256(path)
        self.values, self.formulas, self.max_row = {}, {}, {}
        wv = load_workbook(path, read_only=True, data_only=True)
        wf = load_workbook(path, read_only=True, data_only=False)
        try:
            self.sheetnames = list(wv.sheetnames)
            for name in self.sheetnames:
                vals, forms, mr = {}, {}, 0
                for row in wv[name].iter_rows():
                    for cell in row:
                        if getattr(cell, 'value', None) is not None:
                            vals[(cell.row, cell.column)] = cell.value
                            mr = max(mr, cell.row)
                for row in wf[name].iter_rows():
                    for cell in row:
                        v = getattr(cell, 'value', None)
                        if isinstance(v, str) and v.startswith('='):
                            forms[(cell.row, cell.column)] = v
                self.values[name], self.formulas[name], self.max_row[name] = vals, forms, mr
            self.defined_names = self._defined(wf)
        finally:
            wv.close()
            wf.close()
        self.resolved_formulas, self.unresolved_formulas = self._resolve_formulas()
        self.roles = self._roles()

    def _resolve_formulas(self):
        """Formula cells without a cached result (files saved by tools that do not calculate): resolve direct
        references (=Sheet!B6, =B6, =NAME) from the workbook itself; anything else stays unresolved and is reported."""
        ref = re.compile(r"^=\s*(?:'?(?P<sheet>[^'!]+)'?!)?\$?(?P<col>[A-Z]{1,3})\$?(?P<row>\d+)\s*$", re.I)
        resolved, unresolved = {}, {}
        for _ in range(3):                                   # references to references
            for sheet, forms in self.formulas.items():
                for (r, c), f in forms.items():
                    if self.values[sheet].get((r, c)) is not None:
                        continue
                    m = ref.match(f)
                    v = None
                    if m:
                        sh = m.group('sheet') or sheet
                        if sh in self.values:
                            v = self.values[sh].get((int(m.group('row')), column_index_from_string(m.group('col').upper())))
                    elif re.fullmatch(r'=\s*[A-Za-z_][A-Za-z0-9_.]*\s*', f) and f[1:].strip().upper() in self.defined_names:
                        vals = self.defined_names[f[1:].strip().upper()]['values']
                        v = vals[0] if len(vals) == 1 else None
                    if v is not None:
                        self.values[sheet][(r, c)] = v
                        resolved[(sheet, r, c)] = f
        for sheet, forms in self.formulas.items():
            for (r, c), f in forms.items():
                if self.values[sheet].get((r, c)) is None:
                    unresolved[(sheet, r, c)] = f
        return resolved, unresolved

    def _defined(self, wb):
        out = {}
        try:
            items = list(wb.defined_names.items())
        except AttributeError:                                  # openpyxl < 3.1
            items = [(d.name, d) for d in wb.defined_names.definedName]
        for name, dn in items:
            try:
                dests = list(dn.destinations)
            except Exception:  # noqa: BLE001 - external / constant names
                dests = []
            vals = []
            for sheet, ref in dests:
                if sheet not in self.values:
                    continue
                c1, r1, c2, r2 = range_boundaries(ref.replace('$', ''))
                for r in range(r1, r2 + 1):
                    for c in range(c1, c2 + 1):
                        v = self.values[sheet].get((r, c))
                        if v is not None and str(v).strip():
                            vals.append(text(v))
            if vals:
                out[name.upper()] = {'values': vals, 'ref': ';'.join(f'{s}!{r}' for s, r in dests)}
        return out

    def _roles(self):
        roles = {}
        for name in self.sheetnames:
            n = norm(name)
            for role, keys in SHEET_ROLES.items():
                if role not in roles and any(n == k or n.startswith(k) for k in keys):
                    roles[role] = name
                    break
        return roles

    def get(self, sheet, row, col):
        return self.values[sheet].get((row, col))

    def formula(self, sheet, row, col):
        return self.formulas[sheet].get((row, col))

    def rows(self, sheet, start):
        last = self.max_row[sheet]
        byrow = {}
        for (r, c), v in self.values[sheet].items():
            if r >= start:
                byrow.setdefault(r, {})[c] = v
        for r in range(start, last + 1):
            if r in byrow:
                yield r, byrow[r]

    def column_map(self, role):
        """(header_row, {field: column index}, evidence list). Header row = the row with most recognised headers."""
        sheet = self.roles.get(role)
        if not sheet:
            return None, {}, [f'No sheet recognised as {role}']
        spec = COLUMNS.get(role)
        best = (0, None, {})
        vals = self.values[sheet]
        for r in range(1, min(self.max_row[sheet], 20) + 1):
            found = {}
            for (rr, c), v in vals.items():
                if rr != r or not isinstance(v, str):
                    continue
                h = norm(v)
                for field, syn in (spec or {}).items():
                    if field not in found and h in syn:
                        found[field] = c
                        break
            if len(found) > best[0]:
                best = (len(found), r, found)
        n, header_row, found = best
        evidence = []
        if spec is None:
            return None, {}, ['generic reference sheet']
        if n < 2:
            header_row, found = 1, {}
            evidence.append(f'{sheet}: header row not recognised; using row 1 and the existing adapter column letters')
        for field, letter in FALLBACK.get(role, {}).items():
            if field not in found:
                col = column_index_from_string(letter)
                hdr = vals.get((header_row, col))
                if col not in found.values() and (n < 2 or not text(hdr)):
                    found[field] = col
                    evidence.append(f'{sheet}!{letter}{header_row} ({text(hdr) or "no header"}) used as {field} by position '
                                    '(existing adapter layout) - verify')
        for (rr, c), v in vals.items():
            if rr == header_row and c not in found.values() and str(v).strip():
                evidence.append(f'{sheet}!{get_column_letter(c)}{header_row} header {text(v)!r} not recognised; column not used as a condition')
        return header_row, found, evidence

    def reference_codes(self, role):
        """Codes of a simple reference sheet (BRANCH, DAO, PRODUCT, COMPANY, CURRENCY, BALANCE_TYPE)."""
        sheet = self.roles.get(role)
        if not sheet:
            return None, None
        vals = self.values[sheet]
        header = {c: norm(v) for (r, c), v in vals.items() if r == 1}
        col = next((c for c, h in sorted(header.items()) if any(k in h for k in GENERIC_CODE)), min(header) if header else 1)
        codes = {text(v).split(' ')[0].upper() for (r, c), v in vals.items() if r > 1 and c == col and text(v).strip()}
        return codes, f'{sheet}!{get_column_letter(col)}'


def text(v):
    if v is None:
        return ''
    if isinstance(v, float) and v.is_integer():
        return str(int(v))
    return str(v).strip()


def addr(sheet, row, col):
    return f"'{sheet}'!{get_column_letter(col)}{row}"
