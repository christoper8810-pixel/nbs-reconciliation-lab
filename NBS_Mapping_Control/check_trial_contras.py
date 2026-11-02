import sqlite3
c=sqlite3.connect('data/bank_20260930.sqlite')
for p in ('180','280','1802','2801'):
 print(p,c.execute("SELECT sum(amount),min(amount),max(amount) FROM unique_records WHERE source='TB' AND gl LIKE ?",(p+'%',)).fetchone())
c.close()
