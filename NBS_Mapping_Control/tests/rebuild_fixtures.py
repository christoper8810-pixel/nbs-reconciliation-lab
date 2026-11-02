"""Write minimal OOXML workbooks with exact raw <v> text, for independent adapter fixtures."""
import zipfile
from xml.sax.saxutils import escape

CATEG_HEADERS = ['ID', 'COMPANY.CODE', 'AMOUNT.LCY', 'TRANSACTION.CODE', 'PL.CATEGORY', 'CUSTOMER.ID', 'ACCOUNT.OFFICER',
                 'PRODUCT.CATEGORY', 'VALUE.DATE', 'CURRENCY', 'POSITION.TYPE', 'OUR.REFERENCE', 'EXPOSURE.DATE',
                 'CURRENCY.MARKET', 'TRANS.REFERENCE', 'SYSTEM.ID', 'BOOKING.DATE', 'CONSOL.KEY', 'PROCESSING.DATE', 'SOFT.ACCTNG.DTLS']


def col(n):
    s = ''
    while n:
        n, r = divmod(n - 1, 26)
        s = chr(65 + r) + s
    return s


def _cell(ref, v):
    if v is None:
        return ''
    if isinstance(v, tuple):  # ('n', raw numeric text)
        return f'<c r="{ref}"><v>{v[1]}</v></c>'
    if isinstance(v, (int, float)):
        return f'<c r="{ref}"><v>{v}</v></c>'
    return f'<c r="{ref}" t="inlineStr"><is><t>{escape(str(v))}</t></is></c>'


def write_xlsx(path, sheets):
    """sheets: list of (name, rows) where rows is a list of lists or (row_no, {col: value}) items."""
    with zipfile.ZipFile(path, 'w') as z:
        z.writestr('[Content_Types].xml', '<?xml version="1.0"?><Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">'
                   '<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>'
                   '<Default Extension="xml" ContentType="application/xml"/>'
                   '<Override PartName="/xl/workbook.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet.main+xml"/>'
                   + ''.join(f'<Override PartName="/xl/worksheets/sheet{i+1}.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml"/>' for i in range(len(sheets)))
                   + '</Types>')
        z.writestr('_rels/.rels', '<?xml version="1.0"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
                   '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="xl/workbook.xml"/></Relationships>')
        z.writestr('xl/workbook.xml', '<?xml version="1.0"?><workbook xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main" '
                   'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"><sheets>'
                   + ''.join(f'<sheet name="{escape(n)}" sheetId="{i+1}" r:id="rId{i+1}"/>' for i, (n, _) in enumerate(sheets)) + '</sheets></workbook>')
        z.writestr('xl/_rels/workbook.xml.rels', '<?xml version="1.0"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
                   + ''.join(f'<Relationship Id="rId{i+1}" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet" Target="worksheets/sheet{i+1}.xml"/>' for i in range(len(sheets)))
                   + '</Relationships>')
        for i, (_, rows) in enumerate(sheets):
            xml = []
            for r, row in enumerate(rows, start=1):
                if isinstance(row, dict):
                    cells = ''.join(_cell(f'{k}{r}', v) for k, v in row.items())
                else:
                    cells = ''.join(_cell(f'{col(j+1)}{r}', v) for j, v in enumerate(row))
                xml.append(f'<row r="{r}">{cells}</row>')
            z.writestr(f'xl/worksheets/sheet{i+1}.xml', '<?xml version="1.0"?><worksheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main"><sheetData>'
                       + ''.join(xml) + '</sheetData></worksheet>')


def categ_row(id_, amount, pl='52258', ref='700000000090', booking='20261001', value='20260915', system='AAAA',
              soft='CHARGE-MAKE.DUE-DUE', u='SDB-CHARGE', company='QA0011003', product='3901', officer='5261', currency='QAR'):
    key = f'PL.{pl}.{currency}.{product or ""}.{officer}.1000.14.QA.44229.....{company}'
    row = [('n', id_), company, ('n', amount), ('n', '813'), ('n', pl), ('n', '173784') if ref else None, ('n', officer),
           ('n', product) if product else None, ('n', value) if value else None, currency, 'TR', ('n', ref) if ref else None,
           ('n', value) if value else None, ('n', '1'), 'AAACT1', system, ('n', booking), key, ('n', booking), soft]
    d = {col(j + 1): v for j, v in enumerate(row) if v is not None}
    if u:
        d['U'] = u
    return d


def categ_workbook(path, rows, headers=CATEG_HEADERS):
    write_xlsx(path, [('Sheet1', [{col(j + 1): h for j, h in enumerate(headers)}] + rows)])


BO_STD = ['Table Code', 'Qcb Item Code', 'Qcb Item Description', 'In LC Amount ', 'In FC Amount', 'Out LC Amount', 'Out FC Amount', 'Report Date']


def bo_sheet(table, items, headers=BO_STD, date_serial='46295', title=None):
    rows = [[], [None, None, title or f'Table ({int(table)})'], [], [None] + headers]
    for it in items:
        rows.append([None] + it + [('n', date_serial)])
    return (f'Table-{table}', rows)
