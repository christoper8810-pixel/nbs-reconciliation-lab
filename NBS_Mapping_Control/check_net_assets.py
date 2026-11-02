import json,sqlite3
c=sqlite3.connect('data/bank_20260930.sqlite')
doc=json.load(open('config/generation_rules.json',encoding='utf-8'))
from nbs_control.report_mapping import compile_filter
for r in [46,49]:
 s=next(x for x in doc['rules'].values() if x['row']==r);params=[];f=compile_filter(s['filter'],params,alias='m')
 print(r,s['filter']);print(c.execute('SELECT gl,sum(amount) FROM unique_records m WHERE source=\'TB\' AND '+f+' GROUP BY gl',params).fetchall())
c.close()
