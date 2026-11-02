from __future__ import print_function
import uno,os,time
from com.sun.star.beans import PropertyValue
ctx=uno.getComponentContext();res=ctx.ServiceManager.createInstanceWithContext('com.sun.star.bridge.UnoUrlResolver',ctx)
for i in range(60):
    try:remote=res.resolve('uno:socket,host=127.0.0.1,port=2097;urp;StarOffice.ComponentContext');break
    except:time.sleep(0.5)
desktop=remote.ServiceManager.createInstanceWithContext('com.sun.star.frame.Desktop',remote)
base=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
p=PropertyValue();p.Name='Hidden';p.Value=True
for n in ['originals/LCR & NSFR (Solo) - Mapping Review.docx','revised/LCR and NSFR Solo Review Revised 22Oct2026.docx']:
    doc=desktop.loadComponentFromURL(uno.systemPathToFileUrl(os.path.join(base,n)),'_blank',0,(p,))
    print(n)
    for t in [doc.TextTables.getByIndex(0),doc.TextTables.getByIndex(1)]:
        print('width',t.Width,'separators',[(x.Position,x.IsVisible) for x in t.TableColumnSeparators])
    doc.close(True)
desktop.terminate()
