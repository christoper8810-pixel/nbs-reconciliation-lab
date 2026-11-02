"""Verify exported snapshot amounts and every comparison against immutable run results."""
import math
from pathlib import Path
import openpyxl

def verify_report_workbook(path,result):
    path=Path(path)
    wb=openpyxl.load_workbook(path,read_only=True,data_only=True)
    try:
        if wb.sheetnames!=['Overview','Generated NBS','Ethix reference','Comparison','Mapping notes']:raise ValueError('Unexpected report workbook tabs')
        expected={r['row']:r for r in result['rows']};by_id={r['id']:r for r in result['rows']}
        checked=0
        def same(actual,value,where):
            if not isinstance(actual,(int,float)) or not math.isfinite(actual) or abs(actual-value)>max(.000001,abs(value)*1e-12):raise ValueError('Workbook amount mismatch at '+where)
        for name,field in [('Generated NBS','values'),('Ethix reference','reference')]:
            for row in wb[name].iter_rows():
                spec=expected.get(row[0].row)
                if not spec:continue
                for cell in row:
                    if cell.column_letter in spec[field]:
                        value=spec[field][cell.column_letter]
                        if value is not None:same(cell.value,value,name+'!'+cell.coordinate);checked+=1
                    if cell.data_type=='e':raise ValueError('Formula error at '+name+'!'+cell.coordinate)
        compared=0
        for row in wb['Comparison'].iter_rows(min_row=2,values_only=True):
            if not row[0]:continue
            compared+=1
            spec=by_id[row[0]];col=row[2];g=spec['values'].get(col);e=spec['reference'].get(col)
            if g is not None:same(row[4],g,'Comparison generated '+str(row[1])+col)
            if e is not None:same(row[5],e,'Comparison reference '+str(row[1])+col)
            if g is not None and e is not None:same(row[6],g-e,'Comparison difference '+str(row[1])+col)
            elif row[6] not in ('n.a.',None):raise ValueError('Unavailable difference was changed into a number')
        return {'numeric_cells_verified':checked,'compared_rows_verified':compared}
    finally:wb.close()
