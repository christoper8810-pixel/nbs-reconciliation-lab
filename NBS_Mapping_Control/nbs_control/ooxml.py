"""Raw, cached-value-only OOXML reader. No formulas, macros, connections or document text run.

Unlike bank_data.xlsx_rows this preserves the original <v> text so long decimal strings and
identifiers are not converted to binary floats, and it reports the cell type and address.
"""
from __future__ import annotations
import posixpath
import re
import zipfile
from datetime import date, timedelta
from lxml import etree

NS = '{http://schemas.openxmlformats.org/spreadsheetml/2006/main}'
REL = '{http://schemas.openxmlformats.org/officeDocument/2006/relationships}'
PKG_REL = '{http://schemas.openxmlformats.org/package/2006/relationships}'
_PARSER = etree.XMLParser(resolve_entities=False, no_network=True, huge_tree=True)


def col_index(col: str) -> int:
    n = 0
    for ch in col:
        n = n * 26 + ord(ch) - 64
    return n


def sheets(path):
    """Return [(sheet name, part path)] in workbook order."""
    with zipfile.ZipFile(path) as z:
        wb = etree.fromstring(z.read('xl/workbook.xml'), _PARSER)
        rels = etree.fromstring(z.read('xl/_rels/workbook.xml.rels'), _PARSER)
        targets = {r.get('Id'): r.get('Target') for r in rels.iter(PKG_REL + 'Relationship')}
        out = []
        for s in wb.iter(NS + 'sheet'):
            target = targets[s.get(REL + 'id')]
            part = target.lstrip('/') if target.startswith('/') else posixpath.normpath('xl/' + target)
            out.append((s.get('name'), part))
        return out


def inspect_package(path):
    """Report active content without executing it."""
    with zipfile.ZipFile(path) as z:
        names = z.namelist()
        formulas = 0
        for n in names:
            if n.startswith('xl/worksheets/') and n.endswith('.xml'):
                with z.open(n) as f:
                    for _, el in etree.iterparse(f, events=('end',), tag=NS + 'f'):
                        formulas += 1
                        el.clear()
        return {'formula_cells': formulas,
                'vba': any(n.lower().endswith('vbaproject.bin') for n in names),
                'external_links': [n for n in names if n.startswith('xl/externalLinks/')],
                'connections': 'xl/connections.xml' in names,
                'query_tables': [n for n in names if 'queryTable' in n]}


def _shared_strings(z):
    out = []
    if 'xl/sharedStrings.xml' in z.namelist():
        with z.open('xl/sharedStrings.xml') as f:
            for _, el in etree.iterparse(f, events=('end',), tag=NS + 'si'):
                out.append(''.join(el.itertext()))
                el.clear()
    return out


def raw_rows(path, part):
    """Yield (row number, {column: (text, kind)}) where kind is s/n/b/e/str. Blank cells omitted."""
    with zipfile.ZipFile(path) as z:
        strings = _shared_strings(z)
        with z.open(part) as f:
            for _, row in etree.iterparse(f, events=('end',), tag=NS + 'row'):
                values = {}
                for c in row:
                    if c.tag != NS + 'c':
                        continue
                    col = re.sub(r'\d', '', c.get('r'))
                    t = c.get('t') or 'n'
                    if t == 'inlineStr':
                        is_ = c.find(NS + 'is')
                        values[col] = (''.join(is_.itertext()) if is_ is not None else '', 's')
                        continue
                    v = c.find(NS + 'v')
                    if v is None or v.text is None:
                        continue
                    if t == 's':
                        values[col] = (strings[int(v.text)], 's')
                    else:
                        values[col] = (v.text, t)
                yield int(row.get('r')), values
                row.clear()
                while row.getprevious() is not None:
                    del row.getparent()[0]


def excel_serial_date(text) -> str | None:
    try:
        n = float(text)
    except (TypeError, ValueError):
        return None
    if not n.is_integer() or not 20000 < n < 80000:
        return None
    return (date(1899, 12, 30) + timedelta(days=int(n))).isoformat()


def yyyymmdd(text) -> str | None:
    """T24 dates exported as numbers such as 20261001."""
    if text in (None, ''):
        return None
    s = str(text).strip()
    if s.endswith('.0'):
        s = s[:-2]
    if not re.fullmatch(r'\d{8}', s):
        raise ValueError(f'Date is not YYYYMMDD: {text!r}')
    d = date(int(s[:4]), int(s[4:6]), int(s[6:]))
    return d.isoformat()


def identifier(text) -> str:
    """Exact identifier text; integral numeric cells lose only a trailing '.0' or exponent form."""
    if text is None:
        return ''
    s = str(text).strip()
    if re.fullmatch(r'-?\d+\.0+', s):
        return s.split('.')[0]
    if re.fullmatch(r'-?\d+(\.\d+)?[eE]\+?\d+', s):
        from decimal import Decimal
        d = Decimal(s)
        if d == d.to_integral_value():
            return format(d.to_integral_value(), 'f')
    return s
