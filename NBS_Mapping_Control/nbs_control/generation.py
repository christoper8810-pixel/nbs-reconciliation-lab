"""Generate provisional NBS amounts with visible source, variance and missing-data states."""
from __future__ import annotations
import csv,json,re,sqlite3,uuid,math,hashlib
import copy
from contextvars import ContextVar
from collections import Counter
from contextlib import closing
from datetime import date,datetime,timezone
from pathlib import Path

from .bank_data import xlsx_rows,load_manifest,sha,number
from .report_mapping import compile_filter,draft_rules,validate_spec,term,allof,sector_filter,CURRENT_TYPES,SAVING_TYPES

SOURCES=('ECB','ECB_LOAN','ECB_DEPOSIT','TB')
MEASURES=('outstanding','earned','unearned','carrying','ethix_carrying','deposit','amount')
_query_cache=ContextVar('nbs_generation_queries',default=None)

def read_template(path):return {r:v for r,v in xlsx_rows(path)}

SETTINGS_PATH=Path(__file__).resolve().parent.parent/'config'/'rebuild_settings.json'
DEFAULT_SETTINGS={'schema_version':1,'report_date':'2026-09-30','maturity_convention':'DAY_COUNT','open_ended_products':[],
    'notes':['maturity_convention is provisional: the Ethix boundary logic (calendar vs fixed days) has not been supplied',
             'open_ended_products lists products evidenced as having no contractual maturity; none is evidenced yet']}

def rebuild_settings():
    if SETTINGS_PATH.exists():return {**DEFAULT_SETTINGS,**json.loads(SETTINGS_PATH.read_text(encoding='utf-8'))}
    return dict(DEFAULT_SETTINGS)

def initialize_rules(service,template,output):
    output=Path(output)
    if output.exists():return json.loads(output.read_text(encoding='utf-8'))
    rules=draft_rules(service.catalog,read_template(template))
    rules['template_sha256']=sha(template)
    rules['authorization']='User: proceed without waiting for approval; retain notes; 2026-10-14'
    output.parent.mkdir(parents=True,exist_ok=True)
    output.write_text(json.dumps(rules,indent=2)+'\n',encoding='utf-8')
    return rules

def save_rule(path,key,spec,actor,reason):
    if not actor.strip() or not reason.strip():raise ValueError('Enter your name and a change note')
    path=Path(path);rules=json.loads(path.read_text(encoding='utf-8'))
    if key not in rules['rules']:raise ValueError('Unknown mapping ID')
    validate_spec(spec)
    old=rules['rules'][key]
    for field in ('id','row','description','path','section','table','base','fingerprint'):
        if spec.get(field)!=old.get(field):raise ValueError(f'{field} identifies the report row and cannot be changed')
    history=path.parent/'generation_history';history.mkdir(exist_ok=True)
    event={'at':datetime.now(timezone.utc).isoformat(),'actor':actor,'reason':reason,'id':key,'before':old,'after':spec}
    (history/(datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S')+'-'+uuid.uuid4().hex[:8]+'.json')).write_text(json.dumps(event,indent=2),encoding='utf-8')
    rules['rules'][key]=spec
    tmp=path.with_suffix('.tmp');tmp.write_text(json.dumps(rules,indent=2)+'\n',encoding='utf-8');tmp.replace(path)

def validate_product_policies(doc):
    if not isinstance(doc,dict) or not isinstance(doc.get('products'),dict):raise ValueError('Policies need a products object')
    for product,policy in doc['products'].items():
        if not re.fullmatch(r'[A-Z][A-Z0-9_]*',product):raise ValueError('Product name must be an exact uppercase code')
        if not isinstance(policy,dict) or not isinstance(policy.get('enabled'),bool):raise ValueError('Policy enabled must be true or false')
        if not isinstance(policy.get('add_ethix_fees'),bool):raise ValueError('add_ethix_fees must be true or false')
        for field in ('parent_coefficients','linked_coefficients'):
            if not isinstance(policy.get(field),dict):raise ValueError(f'{field} must be an object')
            for name,v in policy[field].items():
                if not re.fullmatch(r'[A-Z][A-Z0-9_]*',name) or not isinstance(v,(int,float)) or not math.isfinite(v) or abs(v)>10:raise ValueError('Invalid component name or coefficient')
        if policy['linked_coefficients'] and product!='CLM':raise ValueError('Linked policies currently support only verified CLM / CLS pairs')

def prepare_facts(c,balance_rules,manifest,as_of,product_policies=None):
    """One row per account; duplicate keys and currency conflicts never fan out joins."""
    if product_policies:validate_product_policies(product_policies)
    columns=set(manifest['ECB']['component_columns'])
    missing={g:[t for t in ts if t not in columns] for g,ts in balance_rules['groups'].items()}
    def component_sum(types,alias='e'):
        return '+'.join(f"COALESCE(json_extract({alias}.components,'$.{t}'),0)" for t in types if t in columns) or '0'
    outstanding=component_sum(balance_rules['groups']['OUTSTANDING'])
    earned=component_sum(balance_rules['groups']['AMORTIZED_EARNED'])
    unearned=component_sum(balance_rules['groups']['UNEARNED_PROFIT'])
    # Materialized per-account facts permit many report filters without repeatedly decoding JSON.
    c.execute('DROP TABLE IF EXISTS temp.facts')
    c.execute('CREATE TEMP TABLE facts AS SELECT * FROM unique_records WHERE 0')
    c.execute('ALTER TABLE facts ADD COLUMN carrying REAL')
    c.execute('ALTER TABLE facts ADD COLUMN ethix_carrying REAL')
    c.execute('ALTER TABLE facts ADD COLUMN deposit REAL')
    c.execute('ALTER TABLE facts ADD COLUMN unavailable INTEGER DEFAULT 0')
    c.execute('ALTER TABLE facts ADD COLUMN days INTEGER')
    c.execute('ALTER TABLE facts ADD COLUMN reference REAL')
    c.execute('ALTER TABLE facts ADD COLUMN issue TEXT')
    c.execute("INSERT INTO facts (source,account,currency,gl,amount,source_row) SELECT 'TB',account,currency,gl,amount,source_row FROM unique_records WHERE source='TB'")
    c.execute("INSERT INTO facts (source,account,arrangement,currency,country,company,category,sector,industry,components,source_row) SELECT source,account,arrangement,currency,country,company,category,sector,industry,components,source_row FROM unique_records WHERE source='ECB'")
    c.execute("UPDATE facts SET country=substr(company,1,2) WHERE source='ECB' AND CAST(category AS INTEGER) BETWEEN 10000 AND 10025 AND (country IS NULL OR country='') AND company LIKE 'QA%'")
    bad_links=c.execute("SELECT linked_account FROM unique_records WHERE source='LOAN' AND product='CLM' AND linked_account!='' GROUP BY linked_account HAVING count(*)>1").fetchall()
    bad={r[0] for r in bad_links}
    c.execute('CREATE TEMP TABLE bad_links(account TEXT PRIMARY KEY)')
    c.executemany('INSERT INTO bad_links VALUES (?)',[(x,) for x in bad])
    for src,kind in [('LOAN','ECB_LOAN'),('DEPOSIT','ECB_DEPOSIT')]:
        # For sparse empty CONSOL_KEY, use the exact account's supplied currency; contradicting currencies are not joined.
        c.execute(f"""INSERT INTO facts (source,account,arrangement,currency,country,company,category,sector,industry,
            residency,personal,rim,product,risk,maturity,effective,gl,fees,components,source_row,linked_account,reference)
            SELECT ?,e.account,e.arrangement,COALESCE(e.currency,m.currency),e.country,e.company,e.category,e.sector,
            COALESCE(NULLIF(e.industry,''),m.industry),m.residency,m.personal,m.rim,m.product,m.risk,m.maturity,m.effective,
            m.gl,m.fees,e.components,e.source_row,m.linked_account,m.amount FROM unique_records e JOIN unique_records m
            ON e.account=m.account AND (e.currency=m.currency OR e.currency IS NULL)
            WHERE e.source='ECB' AND m.source=?""",(kind,src))
    c.execute(f"UPDATE facts AS e SET outstanding=-({outstanding}),earned=-({earned}),unearned=-({unearned}) WHERE source='ECB_LOAN'")
    c.execute("""UPDATE facts AS f SET outstanding=outstanding-COALESCE((SELECT json_extract(ch.components,'$.CREDIT')
        FROM unique_records ch WHERE ch.source='ECB' AND ch.account=f.linked_account AND ch.currency=f.currency AND ch.category='6050'),0),
        earned=earned-COALESCE((SELECT json_extract(ch.components,'$.ACCDEPOSITPFT') FROM unique_records ch
        WHERE ch.source='ECB' AND ch.account=f.linked_account AND ch.currency=f.currency AND ch.category='6050'),0),
        unavailable=CASE WHEN f.category='3713' AND f.linked_account NOT IN (SELECT account FROM bad_links)
        AND EXISTS (SELECT 1 FROM unique_records ch WHERE ch.source='ECB' AND ch.account=f.linked_account AND ch.currency=f.currency AND ch.category='6050')
        THEN 0 ELSE 1 END, issue='CLM signed parent plus linked CLS; unverified links excluded'
        WHERE f.source='ECB_LOAN' AND f.product='CLM'""")
    c.execute("UPDATE facts SET carrying=outstanding+earned+fees WHERE source='ECB_LOAN'")
    c.execute("""UPDATE facts SET unavailable=1,issue='COMMITMENT_ONLY_NO_DRAWN_BALANCE'
        WHERE source='ECB_LOAN' AND product!='CLM' AND abs(COALESCE(carrying,0))<0.00001 AND abs(COALESCE(reference,0))>1
        AND (abs(COALESCE(json_extract(components,'$.CURCOMMITMENT'),0))>0 OR abs(COALESCE(json_extract(components,'$.TOTCOMMITMENT'),0))>0)""")
    c.execute("UPDATE facts SET ethix_carrying=carrying WHERE source='ECB_LOAN'")
    for product,policy in (product_policies or {}).get('products',{}).items():
        if not policy.get('enabled'):continue
        expression=[]
        for typ,coefficient in policy['parent_coefficients'].items():
            if not re.fullmatch(r'[A-Z][A-Z0-9_]*',typ) or not isinstance(coefficient,(float,int)) or abs(coefficient)>10:raise ValueError('Invalid product component policy')
            expression.append(f"({coefficient})*COALESCE(json_extract(f.components,'$.{typ}'),0)")
        for typ,coefficient in policy.get('linked_coefficients',{}).items():
            if not re.fullmatch(r'[A-Z][A-Z0-9_]*',typ) or not isinstance(coefficient,(float,int)) or abs(coefficient)>10:raise ValueError('Invalid linked component policy')
            expression.append(f"({coefficient})*COALESCE((SELECT json_extract(ch.components,'$.{typ}') FROM unique_records ch WHERE ch.source='ECB' AND ch.account=f.linked_account AND ch.currency=f.currency AND ch.category='6050'),0)")
        if policy.get('add_ethix_fees'):expression.append('f.fees')
        if not expression:raise ValueError('Empty product measure')
        c.execute('UPDATE facts AS f SET ethix_carrying='+ '+'.join(expression)+" WHERE f.source='ECB_LOAN' AND f.product=?",(product,))
    c.execute("UPDATE facts SET deposit=COALESCE(json_extract(components,'$.CREDIT'),0)+COALESCE(json_extract(components,'$.CURACCOUNT'),0) WHERE source='ECB_DEPOSIT'")
    c.execute("UPDATE facts SET days=CAST(julianday(substr(maturity,1,10))-julianday(?) AS INTEGER) WHERE source IN ('ECB_LOAN','ECB_DEPOSIT') AND maturity!=''",(as_of,))
    for field in ('category','sector','industry','source'):
        c.execute(f'CREATE INDEX facts_{field} ON facts({field})')
    checks={
        'as_of':as_of,
        'joined_loans':c.execute("SELECT count(*) FROM facts WHERE source='ECB_LOAN'").fetchone()[0],
        'joined_deposits':c.execute("SELECT count(*) FROM facts WHERE source='ECB_DEPOSIT'").fetchone()[0],
        'unresolved_clm_links':c.execute("SELECT count(*) FROM facts WHERE source='ECB_LOAN' AND product='CLM' AND unavailable=1").fetchone()[0],
        'shared_clm_children':len(bad),
        'clm_linked':c.execute("SELECT count(*) FROM facts WHERE source='ECB_LOAN' AND product='CLM' AND unavailable=0").fetchone()[0],
        'missing_balance_columns':missing,
        'unknown_consol_key':c.execute("SELECT count(*) FROM facts WHERE source='ECB' AND category IS NULL").fetchone()[0],
        'maturity_missing_loans':c.execute("SELECT count(*) FROM facts WHERE source='ECB_LOAN' AND days IS NULL").fetchone()[0],
        'maturity_overdue_loans':c.execute("SELECT count(*) FROM facts WHERE source='ECB_LOAN' AND days<0").fetchone()[0],
        'commitment_only_loan_accounts':c.execute("SELECT count(*) FROM facts WHERE source='ECB_LOAN' AND issue='COMMITMENT_ONLY_NO_DRAWN_BALANCE'").fetchone()[0],
        'industry_differences':dict(c.execute("SELECT m.source,count(*) FROM unique_records e JOIN unique_records m ON e.account=m.account WHERE e.source='ECB' AND m.source IN ('LOAN','DEPOSIT') AND e.industry IS NOT NULL AND e.industry!=m.industry GROUP BY m.source")),
        'loan_currency_conflicts':c.execute("SELECT count(*) FROM unique_records e JOIN unique_records m ON e.account=m.account WHERE e.source='ECB' AND m.source='LOAN' AND e.currency IS NOT NULL AND e.currency!=m.currency").fetchone()[0],
        'deposit_currency_conflicts':c.execute("SELECT count(*) FROM unique_records e JOIN unique_records m ON e.account=m.account WHERE e.source='ECB' AND m.source='DEPOSIT' AND e.currency IS NOT NULL AND e.currency!=m.currency").fetchone()[0],
    }
    return checks

def numeric_cells(values):return {k:number(v) for k,v in values.items() if k!='A' and number(v) is not None}

def query(c,spec,extra=None,dimension='geo',component_columns=(),divisor=1000):
    cache=_query_cache.get()
    key=json.dumps([{k:spec.get(k) for k in ('source','measure','components','filter','negative_filter','factor','enabled','notes')},extra,dimension,list(component_columns),divisor],sort_keys=True)
    if cache is not None and key in cache:return copy.deepcopy(cache[key])
    result=_query(c,spec,extra,dimension,component_columns,divisor)
    if cache is not None:cache[key]=copy.deepcopy(result)
    return result

def _query(c,spec,extra=None,dimension='geo',component_columns=(),divisor=1000):
    validate_spec(spec)
    if not spec['enabled'] or not spec['source']:return {'values':{},'status':'UNAVAILABLE','count':0,'issues':spec.get('notes',[])}
    params=[spec['source']];where='f.source=? AND '+compile_filter(allof(spec.get('filter'),extra),params)
    measure=spec['measure'];issues=list(spec.get('notes',[]));missing=[]
    if measure=='components':
        ts=spec['components'];missing=[x for x in ts if x not in component_columns]
        if not ts:return {'values':{},'status':'UNAVAILABLE','count':0,'issues':issues+['Balance components undefined']}
        expression='+'.join(f"COALESCE(json_extract(f.components,'$.{t}'),0)" for t in ts if t in component_columns)
        if not expression:return {'values':{},'status':'UNAVAILABLE','count':0,'issues':issues+['All required balance columns absent: '+', '.join(missing)]}
        if missing:issues.append('Absent balance columns: '+', '.join(missing))
    elif measure in MEASURES:expression='f.'+measure
    else:return {'values':{},'status':'UNAVAILABLE','count':0,'issues':issues+['Measure undefined']}
    if spec.get('negative_filter'):
        nparams=[];negative=compile_filter(spec['negative_filter'],nparams)
        expression=f'(CASE WHEN {negative} THEN -({expression}) ELSE ({expression}) END)'
        params=nparams+nparams+params
    factor=spec['factor']
    country="CASE WHEN f.residency='Resident' THEN 'IN' WHEN f.residency='NonResident' THEN 'OUT' WHEN f.country='QA' THEN 'IN' WHEN f.country IS NOT NULL AND f.country!='' THEN 'OUT' ELSE 'UNKNOWN' END"
    cur="CASE WHEN f.currency='QAR' THEN 'LC' WHEN f.currency IS NOT NULL AND f.currency!='' THEN 'FC' ELSE 'UNKNOWN' END"
    groups=c.execute(f"SELECT {country} geo,{cur} cur,count(*),sum(CASE WHEN unavailable=0 THEN ({expression}) END),sum(CASE WHEN unavailable!=0 OR ({expression}) IS NULL THEN 1 ELSE 0 END) FROM facts f WHERE {where} GROUP BY geo,cur",params).fetchall()
    values={};count=sum(r[2] for r in groups);unavailable=sum(r[4] or 0 for r in groups)
    if dimension=='geo':
        bucket={('IN','LC'):'B',('IN','FC'):'C',('OUT','LC'):'E',('OUT','FC'):'F'}
        for geo,cur,n,amount,bad in groups:
            if (geo,cur) not in bucket:
                if amount and abs(amount)>0.00001:issues.append(f'{n} records lack geographic/currency dimensions')
                continue
            if amount is not None:values[bucket[geo,cur]]=factor*amount/divisor
        # An explicit available population with no rows for a known dimension has a genuine zero.
        if spec['source']!='TB':
            for col in ('B','C','E','F'):values.setdefault(col,0.0)
        for out,left,right in [('D','B','C'),('G','E','F'),('H','B','E'),('I','C','F'),('J','H','I')]:
            if left in values and right in values:values[out]=values[left]+values[right]
    else:
        amount=sum((r[3] or 0) for r in groups)
        values={'amount':factor*amount/divisor,'count':count-unavailable}
    if spec['source']=='TB':issues.append('TB geographic allocation unavailable; aggregate retained separately')
    if unavailable:issues.append(f'{unavailable} records excluded due to missing CLM links, commitment-only data or monetary inputs')
    status='PARTIAL' if missing or unavailable or any('lack geographic' in x for x in issues) else 'PROVISIONAL'
    return {'values':values,'status':status,'count':count,'issues':issues,'missing_components':missing,
            'total_available':sum((r[3] or 0)*factor/divisor for r in groups)}

def calc_row(c,spec,manifest,divisor,checks):
    validate_spec(spec)
    if not spec['enabled'] or not spec['source']:
        return {'values':{},'status':'UNAVAILABLE','count':0,'issues':list(spec.get('notes',[]))}
    layout=spec.get('layout','geo');cols=manifest['ECB']['component_columns']
    if layout=='risk':
        values={};issues=[];count=0
        for col,grades in [('B',['1','2','3','4','5','6']),('D',['7']),('H',['8']),('J',['9']),('L',['10'])]:
            r=query(c,spec,term('risk','in',grades),dimension='total',component_columns=cols,divisor=divisor)
            if r['values']:values[col]=r['values']['amount'];count+=r['count'];issues.extend(r['issues'])
        for col,a,b in [('F','B','D'),('N','H','J'),('P','F','N')]:
            if a in values and b in values:values[col]=values[a]+values[b]+(values.get('L',0) if col=='N' else 0)
        issues.append('Direct grades mapped 1â€“6 / 7 / 8 / 9 / 10; indirect risk and provisions require external feeds')
        return {'values':values,'status':'PARTIAL','count':count,'issues':list(dict.fromkeys(issues))}
    if layout in ('maturity_loan','maturity_deposit'):
        # Semantic buckets mapped to the validated template header (Table 10 row 769 / Table 24 row 1240).
        from .maturity import bucket,LOAN_BANDS,DEPOSIT_BANDS,TEMPLATE_T10,TEMPLATE_T24
        settings=rebuild_settings()
        values={};issues=[];count=0;semantic={}
        colmap=TEMPLATE_T10 if layout=='maturity_loan' else TEMPLATE_T24
        if layout=='maturity_deposit':
            for key,types in [('DEP_CURRENT_CALL',CURRENT_TYPES),('DEP_SAVING',[t for t in SAVING_TYPES if t!='NTD'])]:
                r=query(c,spec,term('product','in',types),dimension='total',component_columns=cols,divisor=divisor)
                if r['values']:semantic[key]=r['values']['amount'];issues.extend(r['issues']);count+=r['count']
        measure=spec['measure'] if spec['measure'] in MEASURES else None
        if measure:
            flt=allof(spec.get('filter'),term('product','eq',['NTD'])) if layout=='maturity_deposit' else spec.get('filter')
            params=[spec['source']];pred=compile_filter(flt,params)
            bands=LOAN_BANDS if layout=='maturity_loan' else DEPOSIT_BANDS
            if layout=='maturity_loan':semantic['MAT_NONE']=0.0
            for b in bands:semantic.setdefault(b,0.0)
            exceptions=Counter();exc_amount=Counter()
            for maturity,product,amount in c.execute(f'SELECT maturity,product,{measure} FROM facts f WHERE source=? AND {pred} AND unavailable=0',params):
                state=bucket(maturity,checks.get('as_of') or settings['report_date'],bands,settings['maturity_convention'],
                             open_ended=product in settings['open_ended_products'])
                count+=1
                if state in ('OVERDUE','MISSING'):
                    exceptions[state]+=1;exc_amount[state]+=(amount or 0)*spec['factor']/divisor;continue
                semantic[state]=semantic.get(state,0.0)+(amount or 0)*spec['factor']/divisor
            for state in exceptions:issues.append(f'{state}: {exceptions[state]} accounts, {exc_amount[state]:,.3f} excluded from buckets and total')
        if semantic:semantic['TOTAL']=sum(v for k,v in semantic.items())
        values={colmap[k]:v for k,v in semantic.items() if k in colmap}
        issues.append('Overdue, missing maturity and no-maturity are separate states; convention '+settings['maturity_convention']+' (provisional; actual report boundary logic not supplied)')
        return {'values':values,'semantic':semantic,'status':'PARTIAL','count':count,'issues':list(dict.fromkeys(issues))}
    if layout=='size':
        values={};issues=[];count=0;measure=spec['measure']
        if measure not in MEASURES:return {'values':{},'status':'UNAVAILABLE','count':0,'issues':['Measure unavailable']}
        bounds=[0,100,1000,2500,10000,50000,100000,500000,1000000,float('inf')]
        for i,(lo,hi) in enumerate(zip(bounds,bounds[1:])):
            params=[spec['source']];pred=compile_filter(spec.get('filter'),params)
            n,a=c.execute(f'SELECT count(*),sum({measure}) FROM facts f WHERE source=? AND {pred} AND unavailable=0 AND {measure}>? AND {measure}<=?',params+[lo*divisor,hi*divisor]).fetchone()
            values[chr(66+2*i)]=n;values[chr(67+2*i)]=(a or 0)*spec['factor']/divisor;count+=n
        values['T']=sum(values[chr(66+2*i)] for i in range(9));values['U']=sum(values[chr(67+2*i)] for i in range(9))
        issues.append('Size distribution uses account balances; customer aggregation requires a separate agreed convention')
        issues.append('Zero and negative balances are excluded from positive amount bands and require separate review')
        return {'values':values,'status':'PARTIAL','count':count,'issues':issues}
    if layout=='sector_columns':
        values={};issues=[];count=0
        sectors=[allof(term('personal','eq',['NonPersonal']),term('industry','prefix',['441'])),
                 allof(term('personal','eq',['NonPersonal']),term('industry','prefix',['2'])),
                 allof(term('personal','eq',['NonPersonal']),term('industry','prefix',['3'])),
                 allof(term('personal','eq',['NonPersonal']),term('industry','prefix',['4']),{'not':term('industry','prefix',['441'])}),term('personal','eq',['Personal'])]
        for i,s in enumerate(sectors):
            for j,cur in enumerate([term('currency','eq',['QAR']),{'not':term('currency','eq',['QAR'])}]):
                r=query(c,spec,allof(s,cur),dimension='total',component_columns=cols,divisor=divisor)
                if r['values']:values[chr(66+2*i+j)]=r['values']['amount'];count+=r['count'];issues.extend(r['issues'])
        if values:
            values['L']=sum(values.get(chr(66+2*i),0) for i in range(5));values['M']=sum(values.get(chr(67+2*i),0) for i in range(5));values['N']=values['L']+values['M']
        return {'values':values,'status':'PROVISIONAL','count':count,'issues':list(dict.fromkeys(issues))}
    r=query(c,spec,component_columns=cols,divisor=divisor)
    if spec['source']=='TB':
        # Supply only combined local/foreign totals; don't invent inside/outside geography.
        vals={}
        for col,cur in [('H',term('currency','eq',['QAR'])),('I',{'not':term('currency','eq',['QAR'])})]:
            a=query(c,spec,cur,dimension='total',component_columns=cols,divisor=divisor)
            if a['values']:vals[col]=a['values']['amount']
        if vals:vals['J']=sum(vals.values())
        r.update(values=vals,status='PARTIAL')
    if spec['source']=='ECB_LOAN' and spec['measure'] in ('outstanding','carrying','ethix_carrying','earned','unearned'):
        groups=['OUTSTANDING','AMORTIZED_EARNED'] if spec['measure'] in ('carrying','ethix_carrying') else [{'outstanding':'OUTSTANDING','earned':'AMORTIZED_EARNED','unearned':'UNEARNED_PROFIT'}[spec['measure']]]
        absent=[t for g in groups for t in checks['missing_balance_columns'][g]]
        if absent:r['status']='PARTIAL';r['issues'].append('Owner group columns absent: '+', '.join(absent))
    return r

def generate(database,template,rules_path,balance_rules,output_dir):
    _query_cache.set({})
    mapping_bytes=Path(rules_path).read_bytes();rules=json.loads(mapping_bytes);mapping_hash=hashlib.sha256(mapping_bytes).hexdigest()
    manifest=load_manifest(database);rows=read_template(template)
    if rules.get('template_sha256')!=sha(template):raise ValueError('Report template changed; rebuild and review the row mapping before generation')
    if not isinstance(rules['display_divisor'],(int,float)) or rules['display_divisor']<=0:raise ValueError('Invalid reporting unit')
    for src in ('LOAN','DEPOSIT'):
        if src in manifest and set(manifest[src]['dates'])!={rules['reporting_date']}:raise ValueError(f'{src} date does not match reporting date')
    output_dir=Path(output_dir);output_dir.mkdir(parents=True,exist_ok=True)
    from .rebuild_store import open_bank_readonly
    with closing(open_bank_readonly(database)) as c:
        print('Preparing account facts and verified links',flush=True)
        policy_path=Path(rules_path).parent/'report_product_policies.json'
        product_policies=json.loads(policy_path.read_text(encoding='utf-8')) if policy_path.exists() else None
        checks=prepare_facts(c,balance_rules,manifest,rules['reporting_date'],product_policies)
        sections={};results={}
        for key,spec in rules['rules'].items():
            result=calc_row(c,spec,manifest,rules['display_divisor'],checks)
            results[key]={**result,'id':key,'row':spec['row'],'description':spec['description'],'section':spec['section'],
                          'path':spec['path'],'source':spec['source'],'reference':numeric_cells(rows.get(spec['row'],{})),
                          'evidence':spec.get('evidence'),'table':spec.get('table'),'base':spec.get('base')}
            sections.setdefault(spec['section'],[]).append(key)
            if len(results)%300==0:print(f"Calculated {len(results)} report rows",flush=True)
        # Derive unconfigured headings from immediate children only, never both children and grandchildren.
        for ids in sections.values():
            for key in reversed(ids):
                r=results[key];spec=rules['rules'][key]
                if r['values'] or spec['source'] or not spec['enabled']:continue
                prefix=r['path']+' > '
                children=[results[k] for k in ids if results[k]['path'].startswith(prefix) and ' > ' not in results[k]['path'][len(prefix):]]
                if children:
                    populated=[x for x in children if x['values']]
                    if populated:
                        cols=set().union(*(set(x['values']) for x in populated))
                        r['values']={col:sum(x['values'].get(col,0) for x in populated if x['values'].get(col) is not None) for col in cols}
                        r['status']='PARTIAL';r['issues']+=['Immediate-child subtotal; missing child values or overlap require review'];r['source']='SUBTOTAL'
            for key in ids:
                r=results[key]
                if r['values'] or not re.fullmatch(r'(?:grand\s+)?total',r['description'].strip(),re.I):continue
                preceding=[results[k] for k in ids if results[k]['row']<r['row'] and re.match(r'^\.*\s*\d',results[k]['description'].strip())]
                roots=[x for x in preceding if not any(x['path'].startswith(other['path']+' > ') for other in preceding if other['id']!=x['id'])]
                available=[x for x in roots if x['values']]
                if available:
                    cols=set().union(*(set(x['values']) for x in available))
                    r['values']={col:sum(x['values'].get(col,0) for x in available if x['values'].get(col) is not None) for col in cols}
                    r['status']='PARTIAL';r['source']='SUBTOTAL'
                    r['issues']+=['Available top-level rows only; unavailable rows excluded. Total remains partial until all components reconcile.']
        flat=[]
        for r in results.values():
            r['variance']={col:r['values'].get(col)-value for col,value in r['reference'].items() if r['values'].get(col) is not None}
            for col in sorted(set(r['reference'])|set(r['values']),key=lambda x:(len(x),x)):
                flat.append({'mapping_id':r['id'],'section':r['section'],'row':r['row'],'cell':col+str(r['row']),'description':r['description'],
                             'generated':r['values'].get(col),'ethix_reference':r['reference'].get(col),'difference':r['variance'].get(col),
                             'status':r['status'],'source':r['source'],'matched_accounts':r['count'],'notes':' | '.join(dict.fromkeys(r['issues']))})
        summary={'as_of':rules['reporting_date'],'units':'QAR thousands (counts remain counts)','report_sections':len(sections),
                 'rows':len(results),'rows_with_amounts':sum(bool(x['values']) for x in results.values()),
                 'states':dict(Counter(x['status'] for x in results.values())),
                 'numeric_reference_cells':sum(len(x['reference']) for x in results.values()),
                 'numeric_generated_cells':sum(v is not None for x in results.values() for v in x['values'].values()),
                 'comparable_cells':sum(len(x['variance']) for x in results.values()),
                 'within_one_thousand':sum(abs(v)<=1 for x in results.values() for v in x['variance'].values()),
                 'fully_reconciled':False}
        result={'summary':summary,'checks':checks,'manifest':manifest,'template':str(Path(template).resolve()),
                'template_sha256':sha(template),'mapping_sha256':mapping_hash,'database':str(Path(database).resolve()),
                'generated_at':datetime.now(timezone.utc).isoformat(),'rows':list(results.values()),'sections':sections}
        result['product_policies']=product_policies
        result['mapping_snapshot']=rules['rules']
        path=output_dir/'NBS_generated_review.json';path.write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
        with (output_dir/'NBS_generated_vs_Ethix.csv').open('w',encoding='utf-8-sig',newline='') as f:
            fields=['mapping_id','section','row','cell','description','generated','ethix_reference','difference','status','source','matched_accounts','notes']
            writer=csv.DictWriter(f,fieldnames=fields);writer.writeheader()
            for record in flat:
                record={k:("'"+v if isinstance(v,str) and v.startswith(('=','+','-','@')) else v) for k,v in record.items()}
                writer.writerow(record)
        (output_dir/'generation_notes.json').write_text(json.dumps({'summary':summary,'checks':checks,'manifest':manifest,'authorization':rules.get('authorization'),'product_policies':product_policies},indent=2),encoding='utf-8')
        return result
