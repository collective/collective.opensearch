from zope.interface import implements, Interface
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from baseview import BaseView

class IAtomView(Interface):
    """
    Atom view interface
    """



class AtomView(BaseView):
    """
    Atom browser view
    """
    implements(IAtomView)
    render = ViewPageTemplateFile('atomview.pt')


    def __call__(self):
        self.request.RESPONSE.setHeader('Content-Type','text/xml; charset=utf-8')
        return super(AtomView, self).__call__()



