import fs from 'node:fs/promises';
import path from 'node:path';
import {Workbook, SpreadsheetFile} from '@oai/artifact-tool';
const dir=path.dirname(new URL(import.meta.url).pathname.replace(/^\/([A-Za-z]:)/,'$1'));
const data=JSON.parse(await fs.readFile(path.join(dir,'NBS_Temenos_Mapping_Review.json'),'utf8'));
const wb=Workbook.create();
const cols=n=>{let s='';for(let i=n;i;i=Math.floor((i-1)/26))s=String.fromCharCode(65+(i-1)%26)+s;return s};
const literal=v=> typeof v==='string'&&/^[=]/.test(v)?"'"+v:v??'';
function sheet(name,title,heads,rows,widths){
 const s=wb.worksheets.add(name); const end=cols(heads.length);
 s.getRange(`A2:${end}2`).merge();s.getRange('A2').values=[[title]];
 s.getRange(`A2:${end}2`).format.font={name:'Arial',size:14,bold:true,color:'#17324D'};
 s.getRange(`A4:${end}4`).values=[heads];
 s.getRange(`A4:${end}4`).format={fill:'#17324D',font:{name:'Arial',size:10,bold:true,color:'#FFFFFF'},wrapText:true,rowHeight:32};
 for(let start=0;start<rows.length;start+=300){const chunk=rows.slice(start,start+300).map(r=>r.map(literal));s.getRange(`A${start+5}:${end}${start+4+chunk.length}`).values=chunk;}
 if(rows.length){s.getRange(`A5:${end}${rows.length+4}`).format={font:{name:'Arial',size:10},verticalAlignment:'top',rowHeight:56,wrapText:true};
 const t=s.tables.add(`A4:${end}${rows.length+4}`,true,name.replace(/\W/g,'')+'Table');t.showFilterButton=true;}
 (widths??heads.map(()=>24)).forEach((w,i)=>s.getRange(`${cols(i+1)}4:${cols(i+1)}${rows.length+4}`).format.columnWidth=w);
 s.freezePanes.freezeRows(4);return s;
}
const summary=sheet('Meeting','NBS mapping • original Temenos logic • 21 October 2026',['What to present','Evidence / position'],[
 ['Reporting date','30 September 2026; category file retains 1 October raw dates under the confirmed September policy.'],
 ['NBS scope',`${data.manifest.items} items across ${data.manifest.tables} tables; ${data.manifest.original_linked_items} linked to original Temenos rows; ${data.manifest.items-data.manifest.original_linked_items} need an original-row decision.`],
 ['Mapping style','Original category, sector, industry, residence, currency and ASSET TYPE wording; original parents and column conditions remain visible.'],
 ['Current engine','Current selection and balance formula appear beside the original. Empirical product rules, Ethix fees and inferred conditions are identified.'],
 ['GL logic used',`Read-only snapshot of GL mapping v${data.manifest.gl_snapshot.mapping_version.id}, completed run ${data.manifest.gl_snapshot.run.id}; ${data.manifest.gl_snapshot.run.created_at}.`],
 ['Three immediate corrections','Correct provenance labels; stop forced-zero overdraft/loan rules; show absent balance types as partial or unavailable.'],
 ['Acceptances','DEFPAY/DEFPAYBL are the GL acceptance family; ACPTBANK is excluded as the same exposure. Original NBS uses ACPTCONTRABL; reconcile the definition before changing it.'],
 ['Balance examples','Raw signed ECB QAR totals, with QAR-thousands next to them. They illustrate components; they are not additive balance-sheet totals.'],
 ['Meeting decisions','Review the 14 topics in Decisions. Record decisions in the blue input cells on NBS mapping; they do not automatically change the engine.'],
 ['Original source',`${data.manifest.catalog_sources.T24.file_name}; SHA256 ${data.manifest.catalog_sources.T24.sha256}`],
 ['Coverage and balances','A linked rule does not prove a reconciled balance. No 100% reconciliation claim is made.'],
 ['Files to share','This workbook and NBS_Temenos_Presentation.html. No customer account numbers are included.']
],[32,112]);
summary.getRange('A5:B16').format.rowHeight=44;
const mh=['Table','QCB item code','Description','Original Temenos reference','Category wording','Sector wording','Industry wording','Original balance types','Residence wording','Currency wording','Original line text','Parent conditions','Column/header conditions','Current engine source','Current account selection','Current signed balance formula','Current method','Current status','Differences / decisions','Proposed synchronization','Stakeholder decision','Owner','Original Temenos source table'];
const mr=data.mapping.map(r=>[r.table,r.item_code,r.description,r.temenos_reference,r.category,r.sector,r.industry,r.original_types,r.residence,r.currency,r.original_line,r.original_parents,r.original_headers,r.current_source,r.current_selection,r.current_types,r.current_method,r.current_status,r.review,r.proposed_logic,r.stakeholder_decision,r.owner,r.original_source_table]);
const map=sheet('NBS mapping','NBS mapping • exact original wording beside current engine rule',mh,mr,[10,24,38,34,48,42,42,56,34,34,80,68,64,28,72,86,25,24,88,72,40,24,55]);
map.getRange(`U5:V${mr.length+4}`).format.fill='#FFF2CC';map.getRange(`U5:V${mr.length+4}`).format.font={name:'Arial',size:10,color:'#0000FF'};
const tableRows=[...new Set(data.mapping.map(r=>r.table))].sort().map(t=>{const rr=data.mapping.filter(r=>r.table===t);return[t,rr.length,rr.filter(r=>r.temenos_reference).length,rr.filter(r=>!r.temenos_reference).length,rr.filter(r=>r.current_method==='LEGACY_RULE').length,rr.filter(r=>r.current_method!=='LEGACY_RULE').length]});
const index=sheet('Table index','All 50 NBS tables • mapping coverage, not balance reconciliation',['Table','NBS items','Original Temenos row linked','Original row unresolved','Legacy-rule method','Other / derived method'],tableRows,[12,18,28,28,24,26]);
index.getRange('B5:F54').format.numberFormat='#,##0';
const decisions=sheet('Decisions','Meeting decisions • evidence and recommended handling',['No','Topic','Original reference','Original logic','Latest GL finding','Proposed synchronization','Owner / status','Evidence'],data.decisions.map(r=>[r.id,r.topic,r.original_reference,r.original_logic,r.gl_finding,r.proposal,r.owner,r.evidence]),[8,28,35,68,86,86,34,68]);
decisions.getRange('A5:H18').format.rowHeight=100;
const ex=sheet('Balance examples','Worked ECB totals • source signs retained • no double counting',['Example','Original population','Exact balance types','Account rows','Nonzero rows','Raw signed QAR','Raw signed QAR thousand','Status','Missing types','Explanation'],data.examples.map(r=>[r.example,r.criteria,r.balance_types,r.account_rows,r.nonzero_rows,Number(r.raw_qar),Number(r.raw_qar_thousands),r.status,r.missing_types,r.explanation]),[38,32,38,16,16,26,28,18,24,90]);
ex.getRange('F5:G12').format.numberFormat='#,##0.00;(#,##0.00);0.00';
const raw=[...new Map(data.original_cells.map(r=>[r.sheet+'|'+r.cell+'|'+r.text,r])).values()].sort((a,b)=>a.sheet.localeCompare(b.sheet)||a.source_row-b.source_row||a.cell.localeCompare(b.cell));
sheet('Original cells','Original Temenos cells • unique source cells • no rewritten wording',['Worksheet','Cell','Source row','Cell type','Original text'],raw.map(r=>[r.sheet,r.cell,r.source_row,r.type,r.text]),[26,16,16,16,145]);
const gl=sheet('GL balance evidence',`GL tool snapshot • run ${data.manifest.gl_snapshot.run.id} / mapping v${data.manifest.gl_snapshot.mapping_version.id} • raw signed QAR`,['Source','Balance type','DKBGL destination','Outcome','Signed QAR','Source records','Allocation groups'],data.gl_balances.map(r=>[r.source,r.balance_type,r.gl_line,r.outcome,Number(r.signed_qar),r.source_records,r.groups]),[16,28,26,22,30,20,22]);
gl.getRange(`E5:E${data.gl_balances.length+4}`).format.numberFormat='#,##0.00;(#,##0.00);0.00';
wb.recalculate();
console.log((await wb.inspect({kind:'region',sheetId:'Balance examples',range:'A4:J8',maxChars:1800,tableMaxRows:5,tableMaxCols:10})).ndjson);
const preview=await wb.render({sheetName:'Meeting',range:'A2:B12',scale:1.3,format:'png'});
await fs.writeFile(path.join(dir,'Meeting_preview.png'),new Uint8Array(await preview.arrayBuffer()));
await (await SpreadsheetFile.exportXlsx(wb)).save(path.join(dir,'NBS_Temenos_Mapping_for_21Oct2026.xlsx'));
console.log(JSON.stringify({mappingRows:mr.length,rawUniqueCells:raw.length,glEvidenceRows:data.gl_balances.length,sheets:7}));
