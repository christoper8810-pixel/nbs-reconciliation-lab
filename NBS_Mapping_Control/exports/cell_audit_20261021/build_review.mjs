import fs from 'node:fs/promises';
import path from 'node:path';
import {Workbook,SpreadsheetFile} from '@oai/artifact-tool';
const dir=path.dirname(new URL(import.meta.url).pathname.replace(/^\/([A-Za-z]:)/,'$1'));
const d=JSON.parse(await fs.readFile(path.join(dir,'audit.json'),'utf8'));
const test=JSON.parse(await fs.readFile(path.join(dir,'acceptance_results.json'),'utf8'));
const wb=Workbook.create();
const opening=wb.worksheets.add('Read first');
const col=n=>{let s='';for(;n;n=Math.floor((n-1)/26))s=String.fromCharCode(65+(n-1)%26)+s;return s};
const lit=v=>typeof v==='string'&&v.startsWith('=')?"'"+v:v??'';
function sheet(name,title,headers,rows,widths,heights=45){
 console.log('Building '+name+' ('+rows.length+' rows)');
 const s=name==='Read first'?opening:wb.worksheets.add(name);s.showGridLines=false;
 s.getRange('A2').values=[[title]];s.getRange('A2').format.font={name:'Arial',size:14,bold:true,color:'#15324C'};
 const end=col(headers.length);
 s.getRange(`A4:${end}4`).values=[headers];
 s.getRange(`A4:${end}4`).format={fill:'#15324C',font:{name:'Arial',size:10,bold:true,color:'#FFFFFF'},wrapText:true,rowHeight:34,horizontalAlignment:'center',verticalAlignment:'center'};
 for(let i=0;i<rows.length;i+=400){const chunk=rows.slice(i,i+400).map(r=>r.map(lit));s.getRange(`A${i+5}:${end}${i+4+chunk.length}`).values=chunk;}
 if(rows.length){
  s.getRange(`A5:${end}${rows.length+4}`).format={font:{name:'Arial',size:10,color:'#24384C'},wrapText:true,rowHeight:heights,verticalAlignment:'top'};
  const t=s.tables.add(`A4:${end}${rows.length+4}`,true,name.replace(/[^A-Za-z]/g,'')+'Data');t.showFilterButton=true;
 }
 widths.forEach((w,i)=>s.getRange(`${col(i+1)}4:${col(i+1)}${rows.length+4}`).format.columnWidth=w);
 s.freezePanes.freezeRows(4);console.log('Built '+name);return s;
}
const counts=d.counts;
const issueHeads=['Finding','Status','Table','Issue','Systems worksheet','Systems cells','Ehab cells','GL references','Missing categories','Additional categories','Evidence','9 September comparison','Proposed handling','Limits / uncertainty','Other source evidence','Stakeholder decision','Owner'];
const issues=sheet('Findings','Every finding occurrence • original cells preserved',issueHeads,d.findings.map(f=>[f.id,f.status,f.table,f.title,f.systems_sheet,f.systems_cells,f.ehab_cells,f.gl_cells,f.missing_categories,f.extra_categories,f.detail,f.baseline_9sep,f.action,f.limits,f.other_evidence,'','']),[15,18,15,51,25,25,20,46,43,43,96,72,86,88,86,45,26],66);
issues.getRange(`P5:Q${d.findings.length+4}`).format.fill='#FFF2CC';issues.getRange(`P5:Q${d.findings.length+4}`).format.font={name:'Arial',size:10,color:'#0000CC'};
issues.getRange(`B5:B${d.findings.length+4}`).conditionalFormats.add('containsText',{text:'CONFIRMED',format:{fill:'#FCE7E7',font:{bold:true,color:'#8B1C24'}}});
const last=d.findings.length+4;
const summaryRows=[
 ['Result','The original mapping contains confirmed specification/formula defects and unresolved source differences. Category-set agreement alone does not validate an NBS rule.'],
 ['Populated NBS cells scanned',counts.nbs_populated_cells],
 ['All source cells scanned',d.sources.reduce((s,x)=>s+x.cells,0)],
 ['Source worksheets scanned',d.sources.reduce((s,x)=>s+x.sheets,0)],
 ['Finding occurrences',d.findings.length],
 ['Confirmed occurrences',null],['Category / source differences',null],['Missing supplied inputs',null],['Ambiguous operators',null],['Other review items',null],
 ['How counts work','A repeated condition in another cell is a separate occurrence. One cell can have multiple findings. These are not counts of independent misstatements.'],
 ['GL bridge','Old GL split on hyphens; the sixth segment remains a ten-digit text identifier. Full GL row conditions remain in GL_sixth_segment_trace.csv and Referenced_GL_rows.csv.'],
 ['GL dates',`9 September original compared with the current supplied workbook plus logged mapping v${d.gl_version.run.version_id} change. Current completed GL run ${d.gl_version.run.id}. Later differences are shown separately.`],
 ['Ehab comparisons',`${counts.comparisons} linked row comparisons. A missing numeric bridge or treasury source remains unverified.`],
 ['Validation',`${test.passed} acceptance checks passed. Original hashes, cell coverage, parsing boundaries and independent examples were verified.`],
 ['Balance amounts','This is a mapping audit. No unsupported monetary impact or 100% balance reconciliation is claimed.'],
 ['Reporting basis','30 September 2026. The category extract keeps its original 1 October dates under the owner-confirmed September effective-date policy.'],
 ['Editable decisions','Yellow columns on Findings record a stakeholder decision and owner. They do not silently amend the engine or source workbooks.'],
 ['Full evidence','GL_sixth_segment_trace.csv, Referenced_GL_rows.csv and NBS_cell_scan.csv contain the complete supporting rows. The offline HTML shows full text without requiring Python or internet.'],
 ['Method limits','Rules scan every populated cell; semantic correctness still depends on the configured Temenos fields, complete source feeds and regulatory classification decisions. Blank or styled empty cells are counted in coverage, not treated as working rules.']
];
const summary=sheet('Read first','Ehab • Systems 6 October • GL category audit',['Review','Result'],summaryRows,[34,124],45);
for(const [offset,status] of [[5,'CONFIRMED'],[6,'DIFFERENCE'],[7,'INPUT GAP'],[8,'AMBIGUOUS'],[9,'REVIEW']])summary.getRange(`B${offset+5}`).formulas=[[`=COUNTIF(Findings!$B$5:$B$${last},"${status}")`]];
summary.getRange('B6:B14').format.numberFormat='#,##0';
summary.tabColor='#15324C';issues.tabColor='#355F83';
const cp=['Ehab cell','Schedule','Line','Ehab original rule','Systems row','Criterion source cells','Systems categories','Current GL categories','9 September GL categories','Missing vs current','Additional vs current','Missing vs 9 September','Additional vs 9 September','Result','Limit / scope'];
sheet('GL comparison','Ehab sixth-segment categories beside exact Systems selectors',cp,d.comparisons.map(x=>[x.ehab_cell,x.table,x.description,x.ehab_rule,x.systems_reference,x.criterion_references,x.systems_categories,x.gl_current_categories,x.gl_9sep_categories,x.missing_current,x.extra_current,x.missing_9sep,x.extra_9sep,x.status,x.note]),[17,17,48,80,32,62,76,76,76,66,66,66,66,28,100],65);
const affectedCells=d.cell_ledger.filter(x=>x.findings);
sheet('Affected cells','Original cells with findings • full source ledger in NBS_cell_scan.csv',['Source','Worksheet','Cell','Cell type','Original formula','Original cached value','Finding references','Scan result'],affectedCells.map(x=>[x.source,x.sheet,x.cell,x.type,x.formula,x.value,x.findings,x.scan_result]),[17,30,16,15,75,140,76,45],40);
const coverage=d.sources.flatMap(m=>m.sheet_counts.map(s=>[m.label,m.filename,s.sheet,s.populated_cells,s.formula_cells,s.serialized_rows,s.empty_styled_cells,m.sha256]));
const sourceSheet=sheet('Source coverage','Every supplied worksheet • immutable source hashes',['Source','Workbook','Worksheet','Populated cells','Formula cells','Serialized rows','Styled empty cells','SHA256'],coverage,[26,88,35,22,20,22,25,80],32);
sourceSheet.getRange(`D5:G${coverage.length+4}`).format.numberFormat='#,##0';
wb.recalculate();
const inspect=await wb.inspect({kind:'region',sheetId:'Read first',range:'A4:B14',maxChars:2800,tableMaxRows:11,tableMaxCols:2});
await fs.writeFile(path.join(dir,'workbook_inspection.txt'),inspect.ndjson);
for(const [name,range] of [['Read first','A2:B13'],['Findings','A2:G9'],['GL comparison','A2:E10'],['Affected cells','A2:F10'],['Source coverage','A2:E12']]){
 const b=await wb.render({sheetName:name,range,scale:1.2,format:'png'});await fs.writeFile(path.join(dir,name.replaceAll(' ','_')+'_preview.png'),new Uint8Array(await b.arrayBuffer()));
}
await (await SpreadsheetFile.exportXlsx(wb)).save(path.join(dir,'NBS_Ehab_Systems_GL_Cell_Audit_21Oct2026.xlsx'));
console.log(JSON.stringify({sheets:5,findings:d.findings.length,comparisons:d.comparisons.length,traceRowsCsv:d.trace.length,affectedCellRows:affectedCells.length,fullCellRowsCsv:d.cell_ledger.length}));
