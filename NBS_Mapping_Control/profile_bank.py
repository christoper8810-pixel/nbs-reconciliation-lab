import collections,json,openpyxl
from pathlib import Path

out={}
for p in Path('data/bank_sources').glob('*.xlsx'):
    if p.name.startswith('NBS'): continue
    w=openpyxl.load_workbook(p,read_only=True,data_only=True)
    s=w.active
    it=s.iter_rows(values_only=True)
    head=next(it)
    if p.name.startswith('Historical'):
        next(it);head=next(it)
    wanted=[i for i,h in enumerate(head) if h in ['Business_Date','Account_Type','Acct_Type','Rim_Class','Rim_Class_Description','Residency','residency','Account_Class','Class_Code','Risk_Rating','Segment','Sic_Code','Sector_Code','Cur']]
    counts={head[i]:collections.Counter() for i in wanted}
    ids=collections.Counter(); n=0
    for row in it:
        if not any(x is not None for x in row): continue
        n+=1
        for i in wanted:counts[head[i]][str(row[i]).strip()]+=1
        if 'Account_No' in head:ids[str(row[head.index('Account_No')])]+=1
    out[p.name]={'rows':n,'counts':{k:v.most_common(70) for k,v in counts.items()},'duplicate_accounts':sum(v>1 for v in ids.values())}
    w.close()
inv=json.loads(Path('source_inventory.json').read_text(encoding='utf-8'))
rules=[{'row':x['source_row'],'sheet':x['sheet'],'description':x['description'],'rule':x['rule_text']} for x in inv if x['source_system']=='ETHIX' and x['rule_text']]
Path('data/ethix_rules.json').write_text(json.dumps(rules,indent=2),encoding='utf-8')
Path('data/bank_profile.json').write_text(json.dumps(out,indent=2),encoding='utf-8')
print(json.dumps(out,indent=2))
