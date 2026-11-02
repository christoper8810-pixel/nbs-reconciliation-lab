"""Read-only source snapshot. Workbook formulas and attached SQL are never executed."""
import sys, json, gzip, hashlib, sqlite3, zipfile, re
from pathlib import Path
from collections import Counter
from lxml import etree as E

ROOT=Path(__file__).resolve().parents[2]
OUT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT))
from nbs_control.ooxml import sheets, NS, _shared_strings

def sha(p):
 h=hashlib.sha256()
 with p.open('rb') as f:
  for b in iter(lambda:f.read(1048576),b''): h.update(b)
 return h.hexdigest()

def scan(label,p):
 rows={}; stats=[]
 with zipfile.ZipFile(p) as z:
  strings=_shared_strings(z)
  for name,part in sheets(p):
   dest={}; forms=0; serialized=0; blanks=0
   with z.open(part) as f:
    for _,r in E.iterparse(f,events=('end',),tag=NS+'row',resolve_entities=False,no_network=True,huge_tree=True):
     serialized+=1
     for c in r:
      if c.tag!=NS+'c':continue
      addr=c.get('r');t=c.get('t','n');v=c.find(NS+'v');form=c.find(NS+'f')
      if t=='inlineStr': val=''.join(c.find(NS+'is').itertext())
      elif v is not None and v.text is not None:val=strings[int(v.text)] if t=='s' else v.text
      else:val=None
      formula=form.text if form is not None else None
      if form is not None:forms+=1
      if val is None and form is None:blanks+=1;continue
      dest[addr]={'v':val,'t':t,**({'f':formula or '', 'fa':dict(form.attrib)} if form is not None else {})}
     r.clear()
     while r.getprevious() is not None:del r.getparent()[0]
   rows[name]=dest
   stats.append({'source':label,'sheet':name,'populated_cells':len(dest),'formula_cells':forms,'serialized_rows':serialized,'empty_styled_cells':blanks})
   print(label,name,len(dest),'cells',flush=True)
 meta={'label':label,'path':str(p),'filename':p.name,'sha256':sha(p),'sheets':len(rows),'cells':sum(len(x) for x in rows.values()),'sheet_counts':stats}
 with gzip.open(OUT/(label+'_cells.json.gz'),'wt',encoding='utf-8') as f:json.dump(rows,f,ensure_ascii=False)
 return meta

def main():
 db=Path(r'C:\Users\Test\Downloads\GL mapping\data\recon.db');wal=Path(str(db)+'-wal')
 # Immutable read only if the committed database has no outstanding WAL pages.
 if wal.exists() and wal.stat().st_size:raise RuntimeError('Live WAL: obtain a read-only transaction snapshot first')
 before=(db.stat().st_size,db.stat().st_mtime_ns)
 c=sqlite3.connect(db.as_uri()+'?mode=ro&immutable=1',uri=True);c.row_factory=sqlite3.Row;c.execute('PRAGMA query_only=ON');c.execute('BEGIN')
 run=dict(c.execute("SELECT id,version_id,engine_version,created_at FROM run WHERE status='complete' AND is_preview=0 ORDER BY id DESC LIMIT 1").fetchone())
 chain=[];vid=run['version_id'];changes=[]
 while vid:
  ver=dict(c.execute('SELECT id,file_id,parent_id,name,created_at FROM mapping_version WHERE id=?',(vid,)).fetchone());chain.insert(0,ver);vid=ver['parent_id']
 for v in chain:changes.extend(dict(x) for x in c.execute('SELECT * FROM mapping_change WHERE version_id=? ORDER BY seq,id',(v['id'],)))
 inp=dict(c.execute('SELECT id,filename,stored_path,sha256 FROM input_file WHERE id=?',(chain[-1]['file_id'],)).fetchone())
 c.rollback();c.close()
 assert before==(db.stat().st_size,db.stat().st_mtime_ns) and (not wal.exists() or not wal.stat().st_size),'Database changed during snapshot'
 glmeta={'run':run,'versions':chain,'input':inp,'changes':changes,'mode':'immutable read with empty WAL and unchanged file metadata'}
 (OUT/'gl_version.json').write_text(json.dumps(glmeta,indent=2),encoding='utf-8')
 paths=[('EHAB',Path(r'C:\Users\Test\Downloads\NBS01 Mapping (Ehab).xlsx')),('SYSTEMS',Path(r'C:\Users\Test\Downloads\NBS MAPPING - 6 Oct 2026.xlsx')),('GL_CURRENT_BASE',Path(inp['stored_path'])),('GL_09SEP',Path(r'C:\Users\Test\Downloads\GL Mapping 9 Sept 2026 v1.xlsx'))]
 metas=[]
 for label,p in paths:
  meta=scan(label,p);metas.append(meta)
  (OUT/'source_manifest.json').write_text(json.dumps(metas,indent=2),encoding='utf-8')
 assert metas[2]['sha256'].lower()==inp['sha256'].lower()
 print('DONE',[(m['label'],m['cells']) for m in metas],flush=True)

if __name__=='__main__':main()
