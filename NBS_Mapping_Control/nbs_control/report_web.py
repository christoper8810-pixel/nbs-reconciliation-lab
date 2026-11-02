"""Local report upload, generation, comparison and editable mapping UI."""
import json,secrets,threading,zipfile
import re
from pathlib import Path
from datetime import datetime,timezone
from flask import request,render_template,redirect,url_for,flash,abort,send_from_directory
from .bank_data import build_database,sha,load_manifest
from .generation import generate,initialize_rules,save_rule

def register_report_routes(app,service,export_dir):
    data=service.store.data_dir;root=service.config_dir.parent
    rules_path=service.config_dir/'generation_rules.json'
    sources=data/'bank_sources';jobs=data/'generation_jobs';jobs.mkdir(parents=True,exist_ok=True)
    latest=data/'latest_generation.json'
    generation_lock=threading.Lock()

    def readable_filter(f):
        if not f:return 'All accounts from the selected source'
        if 'all' in f:return ' AND '.join('('+readable_filter(x)+')' for x in f['all'])
        if 'any' in f:return ' OR '.join('('+readable_filter(x)+')' for x in f['any'])
        if 'not' in f:return 'Exclude ('+readable_filter(f['not'])+')'
        op={'eq':'is','in':'is one of','prefix':'starts with','range':'is in the range'}
        return f["field"].replace('_',' ').title()+' '+op.get(f['op'],f['op'])+' '+', '.join(str(v) for v in f['values'])

    def basic_population(form):
        from .report_mapping import term,allof
        parts=[]
        for field in ('category','sector','industry','product','currency'):
            values=[v.strip() for v in form.get('population_'+field,'').split(',') if v.strip()]
            if field in ('product','currency'):values=[v.upper() for v in values]
            if values:parts.append(term(field,'in',values))
        for field in ('personal','residency'):
            if form.get('population_'+field):parts.append(term(field,'eq',[form['population_'+field]]))
        return allof(*parts)

    def current():
        path=Path(json.loads(latest.read_text())['result']) if latest.exists() else Path(export_dir)/'NBS_generated_review.json'
        return json.loads(path.read_text(encoding='utf-8')) if path.exists() else None

    @app.route('/reports',methods=['GET','POST'])
    def reports():
        if request.method=='POST':
            if not generation_lock.acquire(blocking=False):
                flash('A report run is already in progress. Wait for it to finish.','error');return redirect(url_for('reports'))
            job=secrets.token_hex(8);work=data/'report_runs'/job;work.mkdir(parents=True)
            state=jobs/(job+'.json')
            def status(phase,**extra):
                payload={'job':job,'phase':phase,**extra}
                temp=state.with_suffix('.tmp');temp.write_text(json.dumps(payload),encoding='utf-8');temp.replace(state)
            try:
                upload=request.files.get('ecb')
                ecb=work/'ECB.xlsx'
                if upload and upload.filename:
                    if not upload.filename.lower().endswith('.xlsx'):raise ValueError('Choose the ECB .xlsx workbook')
                    upload.save(ecb)
                else:
                    manifest=data/'bank_manifest.json'
                    if not manifest.exists():raise ValueError('Choose an ECB workbook')
                    ecb=Path(json.loads(manifest.read_text())['ECB']['path'])
                pack=request.files.get('pack')
                src=sources
                if pack and pack.filename:
                    if not pack.filename.lower().endswith('.zip'):raise ValueError('Supporting pack must be a ZIP')
                    packed=work/'supporting.zip';pack.save(packed);src=work/'sources';src.mkdir()
                    with zipfile.ZipFile(packed) as z:
                        for info in z.infolist():
                            name=Path(info.filename).name
                            if name.endswith('.xlsx') and name.startswith(('All Loan','All Deposit','Historical_Trial_Balance','NBS01')):
                                if info.file_size>250*1024*1024:raise ValueError('Supporting workbook is too large')
                                with z.open(info) as inp,(src/name).open('wb') as out:
                                    import shutil;shutil.copyfileobj(inp,out)
                def find(prefix):
                    ps=list(src.glob(prefix+'*.xlsx'))
                    if len(ps)!=1:raise ValueError(f'Expected one {prefix} workbook; found {len(ps)}')
                    return ps[0]
                paths={'LOAN':find('All Loan'),'DEPOSIT':find('All Deposit'),'TB':find('Historical_Trial_Balance')}
                template=find('NBS01');status('Reading uploaded data')
                reuse=not (upload and upload.filename) and not (pack and pack.filename) and (data/'bank_20260930.sqlite').exists()
                if not reuse and not (pack and pack.filename) and (data/'bank_20260930.sqlite').exists():
                    cached=load_manifest(data/'bank_20260930.sqlite')
                    reuse=(sha(ecb)==cached['ECB']['sha256'] and all(sha(path)==cached[kind]['sha256'] for kind,path in paths.items()))
                def work_run():
                    try:
                        database=data/'bank_20260930.sqlite' if reuse else work/'bank.sqlite'
                        if not reuse:build_database(ecb,paths,database)
                        status('Generating report amounts and comparisons')
                        initialize_rules(service,template,rules_path)
                        output=Path(export_dir)/'runs'/job
                        result=generate(database,template,rules_path,service.config['balance_rules'],output)
                        status('Complete',summary=result['summary'])
                        tmp=latest.with_suffix('.tmp');tmp.write_text(json.dumps({'job':job,'result':str((output/'NBS_generated_review.json').resolve())}),encoding='utf-8');tmp.replace(latest)
                    except Exception as exc:status('Failed',error=str(exc))
                    finally:generation_lock.release()
                threading.Thread(target=work_run,daemon=True).start()
                return redirect(url_for('report_job',job=job))
            except (ValueError,OSError,zipfile.BadZipFile) as exc:
                generation_lock.release();flash(str(exc),'error');return redirect(url_for('reports'))
        result=current();section=request.args.get('section','');search=request.args.get('q','').lower()
        rows=[];sections=[]
        if result:
            sections=list(result['sections'])
            if not section:section=sections[0]
            rows=[r for r in result['rows'] if r['section']==section and (not search or search in (r['description']+' '+r['path']).lower())]
        labels={}
        for key in sections:
            first=next(r for r in result['rows'] if r['section']==key)
            labels[key]=('Table '+str(first['table'])) if first.get('table') else (first.get('base') or key.split('|')[-1].title())
        directory=Path(json.loads(latest.read_text())['result']).parent if latest.exists() else Path(export_dir)
        return render_template('reports.html',result=result,rows=rows,sections=sections,section_labels=labels,section=section,q=search,
                               rules_exist=rules_path.exists(),has_excel=(directory/'NBS_Generated_September_2026.xlsx').exists())

    @app.route('/reports/jobs/<job>')
    def report_job(job):
        if not job.isalnum():abort(404)
        p=jobs/(job+'.json')
        if not p.exists():abort(404)
        state=json.loads(p.read_text(encoding='utf-8'))
        return render_template('report_job.html',state=state)

    @app.route('/reports/mapping/<key>',methods=['GET','POST'])
    def report_mapping(key):
        if not rules_path.exists():abort(404)
        config=json.loads(rules_path.read_text(encoding='utf-8'));spec=config['rules'].get(key)
        if not spec:abort(404)
        if request.method=='POST':
            try:
                updated=dict(spec)
                for field in ('source','measure','layout'):
                    updated[field]=request.form.get(field) or None
                updated['components']=[s.strip().upper() for s in request.form.get('components','').split(',') if s.strip()]
                updated['filter']=json.loads(request.form.get('filter','null'))
                if request.form.get('replace_population')=='on':updated['filter']=basic_population(request.form)
                updated['negative_filter']=json.loads(request.form.get('negative_filter','null'))
                updated['factor']=float(request.form['factor']);updated['enabled']=request.form.get('enabled')=='on'
                updated['notes']=[n for n in request.form.get('notes','').splitlines() if n.strip()]
                save_rule(rules_path,key,updated,request.form.get('actor',''),request.form.get('reason',''))
                flash('Mapping saved with history. Generate again to apply it to report amounts.','ok')
                return redirect(url_for('report_mapping',key=key))
            except (ValueError,KeyError) as exc:flash('Not saved: '+str(exc),'error')
        return render_template('report_mapping.html',spec=spec,readable_population=readable_filter(spec['filter']))

    @app.route('/reports/download/<name>')
    def report_download(name):
        allowed={'NBS_generated_review.json','NBS_generated_vs_Ethix.csv','generation_notes.json','NBS_Generated_September_2026.xlsx'}
        if name not in allowed:abort(404)
        directory=Path(json.loads(latest.read_text())['result']).parent if latest.exists() else Path(export_dir)
        return send_from_directory(directory.resolve(),name,as_attachment=True)

    @app.route('/reports/export-excel',methods=['POST'])
    def export_report_excel():
        import subprocess
        from .generation import read_template
        result=current()
        if not result:flash('Generate reports first.','error');return redirect(url_for('reports'))
        if not generation_lock.acquire(blocking=False):
            flash('Another report or export run is active.','error');return redirect(url_for('reports'))
        job=secrets.token_hex(8);state=jobs/(job+'.json')
        result_path=Path(json.loads(latest.read_text())['result']) if latest.exists() else Path(export_dir)/'NBS_generated_review.json'
        def write_state(phase,**other):
            temp=state.with_suffix('.tmp');temp.write_text(json.dumps({'job':job,'phase':phase,**other}),encoding='utf-8');temp.replace(state)
        write_state('Building Excel workbook')
        def work_export():
            try:
                template_values=result_path.parent/'report_template_values.json'
                template_values.write_text(json.dumps(read_template(result['template'])),encoding='utf-8')
                node=Path.home()/'.cache/codex-runtimes/codex-primary-runtime/dependencies/node/bin/node.exe'
                proc=subprocess.run([str(node),str(root/'export_generated_workbook.mjs'),str(result_path.resolve()),str(template_values.resolve())],
                                    cwd=root,capture_output=True,text=True,encoding='utf-8',errors='replace',timeout=600)
                (result_path.parent/'excel_export.log').write_text('Process return code: '+str(proc.returncode)+'\n'+proc.stdout+'\n'+proc.stderr,encoding='utf-8')
                if proc.returncode and 'Saved report workbook' not in proc.stdout:raise ValueError('Excel export failed. Details are retained in excel_export.log.')
                from .workbook_validation import verify_report_workbook
                verification=verify_report_workbook(result_path.parent/'NBS_Generated_September_2026.xlsx',result)
                write_state('Complete',summary={'file':'NBS_Generated_September_2026.xlsx','verification':verification,'process_return_code':proc.returncode})
            except Exception as exc:write_state('Failed',error=str(exc))
            finally:generation_lock.release()
        threading.Thread(target=work_export,daemon=True).start()
        return redirect(url_for('report_job',job=job))

    @app.route('/reports/product-policies',methods=['GET','POST'])
    def product_policies():
        from .generation import validate_product_policies
        path=service.config_dir/'report_product_policies.json'
        text=path.read_text(encoding='utf-8') if path.exists() else '{"products":{}}'
        if request.method=='POST':
            text=request.form.get('text','')
            try:
                parsed=json.loads(text);validate_product_policies(parsed)
                actor=request.form.get('actor','').strip();reason=request.form.get('reason','').strip()
                if not actor or not reason:raise ValueError('Enter your name and change note')
                history=service.config_dir/'generation_history';history.mkdir(exist_ok=True)
                event={'at':datetime.now(timezone.utc).isoformat(),'actor':actor,'reason':reason,
                       'before':json.loads(path.read_text(encoding='utf-8')) if path.exists() else None,'after':parsed}
                (history/('product-policies-'+secrets.token_hex(8)+'.json')).write_text(json.dumps(event,indent=2),encoding='utf-8')
                temp=path.with_suffix('.tmp');temp.write_text(json.dumps(parsed,indent=2),encoding='utf-8');temp.replace(path)
                flash('Product policies saved with history. Generate reports again to apply.','ok')
                return redirect(url_for('product_policies'))
            except (ValueError,TypeError,KeyError) as exc:flash('Not saved: '+str(exc),'error')
        return render_template('product_policies.html',text=text)
