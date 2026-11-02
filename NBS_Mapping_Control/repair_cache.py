import json,sqlite3
from nbs_control.bank_data import date_value
c=sqlite3.connect('data/bank_20260930.sqlite')
for field in ('maturity','effective'):
    rows=c.execute(f"SELECT rowid,{field} FROM records WHERE source IN ('LOAN','DEPOSIT') AND {field} IS NOT NULL AND {field}!=''").fetchall()
    c.executemany(f'UPDATE records SET {field}=? WHERE rowid=?',[(date_value(float(v)) if v.replace('.','',1).isdigit() else v,i) for i,v in rows])
c.execute('DROP TABLE unique_records');c.execute('DROP TABLE duplicate_accounts')
c.execute('CREATE TABLE duplicate_accounts AS SELECT source,account,currency,count(*) n FROM records GROUP BY source,account,currency HAVING count(*)>1')
c.execute('CREATE TABLE unique_records AS SELECT r.* FROM records r WHERE NOT EXISTS (SELECT 1 FROM duplicate_accounts d WHERE d.source=r.source AND d.account=r.account AND d.currency IS r.currency)')
c.execute('CREATE UNIQUE INDEX unique_account_idx ON unique_records(source,account,currency)')
m=json.loads(c.execute("SELECT value FROM metadata WHERE key='manifest'").fetchone()[0])
for src in ('LOAN','DEPOSIT'):
    m[src]['dates']={date_value(float(k)) if k.isdigit() else k:v for k,v in m[src]['dates'].items()}
    m['exact_account_joins'][src]=c.execute("SELECT count(*) FROM unique_records e JOIN unique_records m ON e.account=m.account AND e.currency=m.currency WHERE e.source='ECB' AND m.source=?",(src,)).fetchone()[0]
m['duplicates']=[dict(zip(('source','accounts'),r)) for r in c.execute('SELECT source,count(*) FROM duplicate_accounts GROUP BY source')]
c.execute("UPDATE metadata SET value=? WHERE key='manifest'",(json.dumps(m),));c.commit();c.close()
open('data/bank_manifest.json','w',encoding='utf-8').write(json.dumps(m,indent=2))
print(m['exact_account_joins'],m['duplicates'])
