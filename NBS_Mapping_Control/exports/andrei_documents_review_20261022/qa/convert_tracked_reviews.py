from __future__ import print_function
import os,sys,time,glob,json
import uno
from com.sun.star.beans import PropertyValue
base=os.path.dirname(os.path.abspath(__file__))
ctx=uno.getComponentContext();resolver=ctx.ServiceManager.createInstanceWithContext('com.sun.star.bridge.UnoUrlResolver',ctx)
remote=None
for attempt in range(60):
    try:remote=resolver.resolve('uno:socket,host=127.0.0.1,port=2097;urp;StarOffice.ComponentContext');break
    except Exception:time.sleep(0.5)
if remote is None:raise RuntimeError('Private converter did not start')
desktop=remote.ServiceManager.createInstanceWithContext('com.sun.star.frame.Desktop',remote)
def prop(name,value):p=PropertyValue();p.Name=name;p.Value=value;return p
pdfdir=os.path.join(base,'tracked_christopher_joseph','pdf')
if not os.path.isdir(pdfdir):os.makedirs(pdfdir)
checks=[]
try:
    for name in glob.glob(os.path.join(base,'tracked_christopher_joseph','render_inputs','*.docx')):
        doc=desktop.loadComponentFromURL(uno.systemPathToFileUrl(name),'_blank',0,
          (prop('Hidden',True),prop('ReadOnly',True),prop('UpdateDocMode',0),
           prop('MacroExecutionMode',uno.getConstantByName('com.sun.star.document.MacroExecMode.NEVER_EXECUTE'))))
        if doc is None:raise RuntimeError('Could not load '+name)
        redlines=doc.getRedlines()
        assert redlines.Count>0
        authors=set();unknown=[]
        for i in range(redlines.Count):
            redline=redlines.getByIndex(i)
            author=redline.getPropertyValue('RedlineAuthor');authors.add(author)
            if author!='Christopher Joseph' and len(unknown)<4:
                unknown.append({'index':i,'type':redline.getPropertyValue('RedlineType'),
                                'author':author,'text':redline.getString()[:180]})
        assert authors==set(['Christopher Joseph']),authors
        doc.ShowChanges=True
        target=os.path.join(pdfdir,os.path.splitext(os.path.basename(name))[0]+'.pdf')
        doc.storeToURL(uno.systemPathToFileUrl(target),(prop('FilterName','writer_pdf_Export'),
          prop('Overwrite',True),prop('FilterData',(prop('ExportNotes',False),prop('ExportNotesPages',False)))))
        checks.append({'document':os.path.basename(name),'recognized_redlines':redlines.Count,'authors':sorted(authors),'unknown_examples':unknown})
        doc.close(True)
        print('Converted:',os.path.basename(target),'recognized revisions',checks[-1]['recognized_redlines']);sys.stdout.flush()
finally:desktop.terminate()
with open(os.path.join(base,'tracked_christopher_joseph','native_checks.json'),'w') as f:json.dump(checks,f,indent=2)
