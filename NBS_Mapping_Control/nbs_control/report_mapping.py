"""Editable report specifications drafted from source evidence, never executed text."""
from __future__ import annotations
import json,re,math
from pathlib import Path

CURRENT_TYPES=['CAL','CUR','SAL','WMI']
SAVING_TYPES=['DHW','MSP','MSS','NTD','PIA','PSV','SAV','SSV','YSV']

def leaf(text):return re.sub(r'^\.*\s*\d+\s*','',str(text)).strip().lower()
def term(field,op,values):return {'field':field,'op':op,'values':values}
def allof(*args):
    parts=[x for x in args if x]
    return {'all':parts} if len(parts)>1 else parts[0] if parts else None

def sector_filter(path):
    p=path.lower()
    personal=term('personal','eq',['Personal'])
    corporate=term('personal','eq',['NonPersonal'])
    nbf=term('industry','prefix',['441'])
    public=term('industry','prefix',['1','2','3'])
    private={'any':[personal,allof(corporate,term('industry','prefix',['4']),{'not':nbf})]}
    if 'non-bank financial' in p:return allof(corporate,nbf)
    if 'government inst' in p and 'semi' not in p:return allof(corporate,term('industry','prefix',['2']))
    if 'semi-government' in p or 'semi government' in p:return allof(corporate,term('industry','prefix',['3']))
    if 'public sector' in p:return allof(corporate,public)
    if 'private sector' in p:return private
    if 'personal' in p:return personal
    return None

def numeric_selector(text,field,token):
    match=re.search(r'\b'+token+r'\s*(NOT\s+EQUAL\s+TO|<>|=|IS\s+NOT\s+EQUAL\s+TO)\s*([\d\s,\-&]+)',text,re.I)
    if not match:return None
    chars=match.group(2)
    atoms=[]
    for lo,hi,single in re.findall(r'(\d+)\s*-\s*(\d+)|(\d+)',chars):
        if lo:atoms.append({'field':field,'op':'range','values':[int(lo),int(hi)]})
        else:atoms.append(term(field,'eq',[single]))
    if not atoms:return None
    s=atoms[0] if len(atoms)==1 else {'any':atoms}
    if 'NOT' in match.group(1).upper() or '<>' in match.group(1):s={'not':s}
    excluded=re.search(r'BUT\s+NOT\s+EQUAL\s+TO\s+(?:'+token+r'\s*)?([\d\s,]+)',text,re.I)
    if excluded:s=allof(s,{'not':term(field,'in',re.findall(r'\d+',excluded.group(1)))})
    return s

def t24_spec(item,by_id):
    candidates=item.get('nbs_row_candidates',[])
    if len(candidates)!=1:return None
    target=by_id[candidates[0]['business_id']]
    peers=[m for m in by_id.values() if m['source_system']=='T24' and m['block_key']==target['block_key'] and m['source_row']<=target['source_row']]
    parts=[];components=[];notes=[]
    for m in peers:
        if m['business_id']!=target['business_id'] and not (m['path_key'] and target['path_key'].startswith(m['path_key']+' > ')):continue
        vals=[c.get('alias',{}).get('value',c.get('value')) for c in m['cells'] if c['column']!=m.get('description_column') and c.get('type')!='f']
        text='\n'.join(str(v) for v in vals if isinstance(v,str))
        # Prefer the domestic selector; conflicting overseas legacy text stays visible in provenance.
        if vals:text=str(vals[0])
        for field,token in [('category','CATEGORY'),('sector','SECTOR'),('industry','INDUSTRY')]:
            s=numeric_selector(text,field,token)
            if s:parts.append(s)
        types=re.search(r'ASSET\s*TYPE\s*=\s*([A-Z0-9_\s,&]+)',text,re.I)
        if types:
            components=[t for t in re.findall(r'\b[A-Z][A-Z0-9_]+\b',types.group(1).upper()) if t not in ('CATEGORY','SECTOR','AND','ASSET','TYPE')]
        if re.search(r'CUSTOMER[.]STATUS|CRM|CR[.]ASSET[.]CLASS|REMAINING|MATURITY|TREASURY',text,re.I):notes.append('Additional source dimension or external feed must be verified')
    if not parts:return None
    return {'source':'ECB','filter':allof(*parts),'measure':'components','components':components,
            'notes':notes,'evidence':f"T24 {target['sheet']}!row {target['source_row']}", 'target_id':target['business_id']}

def gl_filter(text):
    """Narrow GL selector grammar. Unparsed complex arithmetic is withheld."""
    if re.search(r'minus|\+|under',text,re.I):return None
    text=re.sub(r'^[KLNM]:\s*','',text)
    nums=re.findall(r'\b\d{2,10}\b',text)
    if not nums:return None
    if re.search(r'from|loan|deposit|sic|rim|account type',text,re.I):return None
    split=re.split(r'Except|Exclude',text,flags=re.I)
    include=re.findall(r'\b\d{2,10}\b',split[0]);exclude=re.findall(r'\b\d{2,10}\b',' '.join(split[1:]))
    if not include:return None
    pred=term('gl','prefix',include)
    return allof(pred,{'not':term('gl','prefix',exclude)}) if exclude else pred

def draft_rules(catalog,template_rows):
    by_id={m['business_id']:m for m in catalog['mappings']}
    rules={};sections=[]
    for section in catalog['sections']:
        sections.append({'id':section['section_id'],'title':section.get('title',section.get('ethix_title',''))})
    for m in catalog['mappings']:
        if m['source_system']!='ETHIX' or m['kind'] not in ('RULE','LABEL'):continue
        row=m['source_row']; label=m['description']
        if not label or row not in template_rows:continue
        if label.lower().startswith('dukhan bank'):continue
        if leaf(label)!=leaf(template_rows[row].get('A','')):continue
        key=m['business_id'];path=m['hierarchy_path'];p=path.lower();name=leaf(label);table=m['table_number'];base=m['base_report']
        text='\n'.join(str(c.get('alias',{}).get('value',c['value'])) for c in m['cells'] if c['column']!=m.get('description_column') and (c['type']!='f' or c.get('alias',{}).get('status')=='RESOLVED'))
        spec={'id':key,'row':row,'description':label,'path':path,'section':m['block_key'],
              'table':table,'base':base,'source':None,'filter':None,'measure':None,'components':[],
              'factor':1,'enabled':True,'notes':[],'evidence':f"Ethix mapping row {row}",'kind':'UNRESOLVED',
              'fingerprint':m['fingerprint']}
        sf=sector_filter(path)
        if table in (8,9,10,11,12,13,36,44) or (base=='Assets' and ('credit facilities' in p or 'all loan' in text.lower())):
            if 'non-bank financial' in p:sf=allof(sf,{'not':term('industry','eq',['44108'])})
            spec.update(source='ECB_LOAN',filter=sf,measure='carrying',kind='ACCOUNT_JOIN')
            spec['notes'].append('ECB owner components plus separately supplied Ethix Loan_Fees_QAR; not a T24 fee crosswalk')
            if table==11:spec['measure']='outstanding';spec['layout']='risk'
            elif table==10:spec['layout']='maturity_loan'
            elif table==12:spec['layout']='size'
            elif table==13:spec['source']=None;spec['notes'].append('Collateral/security feed absent')
            elif table==36:spec['source']=None;spec['notes'].append('Country exposure classification needs counterparty and instrument data')
            elif table==44:spec['layout']='sector_columns'
            if name=='overdraft':spec.update(source=None,measure=None);spec['notes'].append('Overdraft account and credit-card populations require verified source scope')
            if name=='loans and advances' or name=='loans':spec['filter']=allof(sf,term('product','eq',['SYN']))
            if "murabaha" in name:spec['filter']=allof(sf,{'not':term('product','in',['SYN','IST','IJR'])})
            if 'istisna' in name:spec['filter']=allof(sf,term('product','eq',['IST']))
            if 'ijara' in name:spec['filter']=allof(sf,term('product','eq',['IJR']))
            if name in ('mudaraba','diminishing musharaka') or 'micro small' in name or 'housing' in name or 'consumer' in name:
                spec['source']=None;spec['notes'].append('Product/subdivision mapping not supplied')
            if base=='Assets' and row==13:spec['filter']=term('industry','eq',['44108'])
            if base=='Assets' and row==33:spec['filter']=allof(sf,{'not':term('industry','eq',['44108'])})
            if base=='Assets' and row==35:spec.update(source='ECB_LOAN',filter=term('rim','eq',['2398']),measure='carrying')
            if base=='Assets' and row==37:spec['filter']=allof(sf,{'not':term('rim','eq',['2398'])})
            if base=='Assets' and row==40:spec['filter']=term('product','eq',['SYN'])
            if base=='Assets' and row==41:spec['filter']=allof(sf,{'not':term('product','eq',['SYN'])});spec['notes'].append('SYN excluded to prevent overlap with Loans and advances; credit-card GL remains unavailable')
        elif table in (23,24,25,45) or (base=='Liabilities' and 'all deposits' in text.lower()):
            spec.update(source='ECB_DEPOSIT',filter=sf,measure='deposit',kind='ACCOUNT_JOIN')
            if table==24:spec['layout']='maturity_deposit'
            elif table==25:spec['layout']='size'
            elif table==45:spec['layout']='sector_columns'
            if 'current and call' in p:spec['filter']=allof(sf,term('product','in',CURRENT_TYPES))
            elif 'saving and time' in p:spec['filter']=allof(sf,term('product','in',SAVING_TYPES))
            if 'corporates' in name:spec['filter']=allof(spec['filter'],term('personal','eq',['NonPersonal']))
            if name=='personal':spec['filter']=allof(spec['filter'],term('personal','eq',['Personal']))
            if 'resident' in p:
                spec['filter']=allof(spec['filter'],term('residency','eq',['NonResident' if 'non-resident' in p or 'nonresident' in p else 'Resident']))
        direct=t24_spec(m,by_id)
        if direct and (spec['source'] is None or table not in (8,9,10,11,12,13,23,24,25,36,44,45)):
            spec.update(direct);spec['kind']='T24_SELECTOR'
            if not spec['components']:
                if spec['source']=='ECB':spec.update(source=None);spec['notes'].append('Exact balance components are not defined for this selector')
        # Economic industry detail comes from matching full-path T24 rule, with joined Ethix metadata as fallback.
        if direct and table in (9,23,44,45):
            industry=numeric_selector(' '.join(str(c['value']) for c in by_id[direct['target_id']]['cells']),'industry','INDUSTRY')
            if industry:
                spec['filter']=allof(sf,industry)
                if table in (9,44):spec.update(source='ECB_LOAN',measure='carrying')
                if table in (23,45):spec.update(source='ECB_DEPOSIT',measure='deposit')
                if table in (44,45):spec['layout']='sector_columns'
        if not spec['source']:
            gf=gl_filter(text)
            if gf and (not table or table not in (10,11,12,13,16,17,18,24,25,26,28,38)):
                spec.update(source='TB',filter=gf,measure='amount',kind='SUPPLEMENTARY_TB')
                spec['notes'].append('Ethix trial balance supplementary source; geographic split absent')
                if re.search(r'\b180\d{7}\b',text) and re.search(r'\b280\d{7}\b',text):
                    split=re.split(r'Except|Exclude',text,flags=re.I)
                    if len(split)>1:
                        gross=re.findall(r'\b180\d{7}\b',split[0]);contra=re.findall(r'\b280\d{7}\b',' '.join(split[1:]))
                        spec['filter']=term('gl','in',gross+contra)
                        spec['negative_filter']=term('gl','in',contra)
                        spec['notes'].append('Net assets deduct specified positive 280 contra balances from gross 180 balances')
        if table==11 and ('suspense' in name or 'deferred' in name or 'provisions' in name):
            spec['source']=None;spec['notes'].append('Risk grade split and exact measure for this adjustment unavailable')
        if spec['source'] in ('ECB_LOAN','ECB_DEPOSIT'):
            # A sector inherited from a parent cannot distinguish an unmapped child (e.g. QFC or housing).
            allowed=('non-bank financial inst.','non-bank financial institutions','public sector','private sector',
                     'government inst.','semi-government inst.','islamic finance','loans and advances','loans',
                     "murabaha - musawma","istisna'a",'finance ijara','current and call','saving and time',
                     'corporates','personal','inside qatar','outside qatar','total')
            inherited_only=spec.get('filter')==sf
            if inherited_only and name not in allowed and row not in (13,33,35,37,40,41):
                spec['source']=None;spec['notes'].append('Parent sector does not define this child; specific subdivision filter required')
        if spec['source'] in ('ECB_LOAN','ECB_DEPOSIT') and not spec['filter'] and name!='total':
            spec['source']=None;spec['notes'].append('Required row population filter not yet defined')
        if spec['source']=='ECB' and spec['measure']=='components':
            if spec['components'] and all(t=='DEBIT' or 'ACCOUNT' in t or 'DEFERREDPFT' in t or 'PRINCIPALPFT' in t for t in spec['components']) and not any(t=='CREDIT' for t in spec['components']):
                spec['factor']=-1
                spec['notes'].append('Presentation multiplier -1 for signed asset balances; original ECB signs retained in source')
            if table==1 and 'cash on hand' in name:
                spec['geography_proxy']='company_country_for_cash'
                spec['notes'].append('Cash location uses booking company jurisdiction where customer residence is absent; provisional assumption')
        if spec['measure']=='carrying':
            spec['measure']='ethix_carrying'
            spec['notes'].append('Empirical RCM / CLM report policies applied; original owner group sum remains separately available as carrying')
        rules[key]=spec
    return {'schema_version':1,'reporting_date':'2026-09-30','display_divisor':1000,
            'blank_pivot_values':'zero_for_present_columns','missing_component_columns':'partial',
            'basis':'User authorized best available mapping, 2026-10-14. Generated amounts are provisional; live Ethix values are reference only.',
            'rules':rules}

FILTER_FIELDS={'category','sector','industry','personal','rim','product','risk','gl','currency','country','residency','maturity','effective','account'}
def compile_filter(f,params,alias='f',depth=0):
    if depth>10:raise ValueError('Filter nesting exceeds ten levels')
    if f is None:return '1=1'
    if not isinstance(f,dict):raise ValueError('Filter must be a structured object')
    for group,sep in [('all',' AND '),('any',' OR ')]:
        if group in f:
            if set(f)!={group} or not isinstance(f[group],list) or not f[group]:raise ValueError('Invalid filter group')
            return '('+sep.join(compile_filter(x,params,alias,depth+1) for x in f[group])+')'
    if 'not' in f:
        if set(f)!={'not'}:raise ValueError('Invalid not filter')
        return '(NOT '+compile_filter(f['not'],params,alias,depth+1)+')'
    if set(f)!={'field','op','values'} or f['field'] not in FILTER_FIELDS:raise ValueError('Unknown filter field or keys')
    field=alias+'.'+f['field'];vals=f['values'];op=f['op']
    if not isinstance(vals,list) or not vals or len(vals)>1000:raise ValueError('Filter requires 1–1000 values')
    if op=='range':
        if len(vals)!=2 or not all(isinstance(v,(int,float)) for v in vals) or vals[0]>vals[1]:raise ValueError('Invalid numeric range')
        params.extend(vals);return f'CAST({field} AS INTEGER) BETWEEN ? AND ?'
    if op=='prefix':
        if any('%' in str(v) or '_' in str(v) for v in vals):raise ValueError('Wildcards are not accepted in prefix values')
        params.extend(str(v)+'%' for v in vals);return '('+' OR '.join(field+' LIKE ?' for v in vals)+')'
    if op not in ('eq','in'):raise ValueError('Unknown filter operator')
    if op=='eq' and len(vals)!=1:raise ValueError('eq requires one value')
    params.extend(str(v) for v in vals);return field+' IN ('+','.join('?' for v in vals)+')'

def validate_spec(spec):
    if spec.get('source') not in (None,'ECB','ECB_LOAN','ECB_DEPOSIT','TB'):raise ValueError('Unsupported source')
    if spec.get('measure') not in (None,'components','carrying','ethix_carrying','outstanding','earned','unearned','deposit','amount'):raise ValueError('Unsupported measure')
    compile_filter(spec.get('filter'),[])
    if spec.get('negative_filter'):compile_filter(spec['negative_filter'],[])
    if not isinstance(spec.get('factor'),(int,float)) or not math.isfinite(spec['factor']) or abs(spec['factor'])>100:raise ValueError('Factor must be a finite number between -100 and 100')
    if not isinstance(spec.get('enabled'),bool):raise ValueError('Enabled must be true or false')
    if not isinstance(spec.get('components'),list) or any(not re.fullmatch(r'[A-Z][A-Z0-9_]*',x) for x in spec['components']):raise ValueError('Components must be exact uppercase balance type identifiers')
