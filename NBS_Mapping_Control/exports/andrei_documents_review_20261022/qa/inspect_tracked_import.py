from __future__ import print_function
import os,glob,time,uno
from com.sun.star.beans import PropertyValue
ctx=uno.getComponentContext();res=ctx.ServiceManager.createInstanceWithContext('com.sun.star.bridge.UnoUrlResolver',ctx)
for i in range(60):
    try:remote=res.resolve('uno:socket,host=127.0.0.1,port=2097;urp;StarOffice.ComponentContext');break
    except Exception:time.sleep(0.5)
desktop=remote.ServiceManager.createInstanceWithContext('com.sun.star.frame.Desktop',remote)
p=PropertyValue();p.Name='Hidden';p.Value=True
base=os.path.dirname(os.path.abspath(__file__))
try:
    files=glob.glob(os.path.join(base,'tracked_christopher_joseph','probes','without_*settings.docx'))+glob.glob(os.path.join(base,'tracked_christopher_joseph','probes','without_comment_anchors.docx'))+glob.glob(os.path.join(os.path.dirname(base),'originals','LCR*.docx'))
    for file in files:
        doc=desktop.loadComponentFromURL(uno.systemPathToFileUrl(file),'_blank',0,(p,))
        red=doc.getRedlines();authors={}
        for i in range(red.Count):
            who=red.getByIndex(i).getPropertyValue('RedlineAuthor');authors[who]=authors.get(who,0)+1
        print(os.path.basename(file),authors)
        doc.close(True)
finally:desktop.terminate()
