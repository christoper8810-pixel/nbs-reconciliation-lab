import sqlite3,json
c=sqlite3.connect('data/bank_20260930.sqlite')
for sql in ["select source,count(*) from records group by source", "select category,count(*),sum(json_extract(components,'$.CURACCOUNT')),sum(json_extract(components,'$.CREDIT')) from records where source='ECB' group by category order by count(*) desc limit 16", "select name from sqlite_master where type='table'"]:
 print(sql,c.execute(sql).fetchall(),flush=True)
c.close()
