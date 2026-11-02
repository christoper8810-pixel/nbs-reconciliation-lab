import sqlite3,json
c=sqlite3.connect('data/bank_20260930.sqlite')
queries={
'industry':"SELECT m.source,count(*),sum(m.amount) FROM unique_records e JOIN unique_records m ON e.account=m.account WHERE e.source='ECB' AND m.source IN ('LOAN','DEPOSIT') AND e.industry IS NOT NULL AND e.industry!=m.industry GROUP BY m.source",
'unmatched_loan':"SELECT m.account,m.product,m.amount,m.industry FROM unique_records m WHERE m.source='LOAN' AND NOT EXISTS(SELECT 1 FROM unique_records e WHERE e.source='ECB' AND e.account=m.account) ORDER BY abs(m.amount) DESC LIMIT 8",
'RCM_issues':"SELECT e.account,e.components,l.outstanding,l.earned FROM unique_records e JOIN unique_records l ON e.account=l.account WHERE e.source='ECB' AND l.source='LOAN' AND e.account IN ('400001330890','400001908413','400001910029','400001913411')"
}
for key,q in queries.items():print(key,c.execute(q).fetchall())
c.close()
