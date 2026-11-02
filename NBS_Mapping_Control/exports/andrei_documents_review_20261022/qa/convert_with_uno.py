from __future__ import print_function
import os,sys,time,glob
import uno
from com.sun.star.beans import PropertyValue

base=os.path.dirname(os.path.abspath(__file__))
ctx=uno.getComponentContext()
resolver=ctx.ServiceManager.createInstanceWithContext('com.sun.star.bridge.UnoUrlResolver',ctx)
remote=None
for attempt in range(60):
    try:
        remote=resolver.resolve('uno:socket,host=127.0.0.1,port=2097;urp;StarOffice.ComponentContext')
        break
    except Exception: time.sleep(0.5)
if remote is None: raise RuntimeError('Private converter did not start')
desktop=remote.ServiceManager.createInstanceWithContext('com.sun.star.frame.Desktop',remote)
def prop(name,value):
    p=PropertyValue();p.Name=name;p.Value=value;return p
pdfdir=os.path.join(base,'pdf')
if not os.path.isdir(pdfdir): os.makedirs(pdfdir)
try:
    for name in glob.glob(os.path.join(os.path.dirname(base),'revised','*.docx')):
        doc=desktop.loadComponentFromURL(uno.systemPathToFileUrl(name),'_blank',0,
             (prop('Hidden',True),prop('ReadOnly',True),prop('UpdateDocMode',0),
              prop('MacroExecutionMode',uno.getConstantByName('com.sun.star.document.MacroExecMode.NEVER_EXECUTE'))))
        if doc is None: raise RuntimeError('Could not load '+name)
        target=os.path.join(pdfdir,os.path.splitext(os.path.basename(name))[0]+'.pdf')
        doc.storeToURL(uno.systemPathToFileUrl(target),(prop('FilterName','writer_pdf_Export'),
            prop('Overwrite',True),prop('FilterData',(prop('ExportNotes',False),prop('ExportNotesPages',False)))))
        doc.close(True)
        print('Converted:',os.path.basename(target))
        sys.stdout.flush()
finally:
    desktop.terminate()
