from zope.interface import implements, Interface
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from baseview import BaseView

class IRSSView(Interface):
    """
    RSS view interface
    """


class RSSView(BaseView):
    """
    RSS browser view
    """
    implements(IRSSView)
    render = ViewPageTemplateFile('rssview.pt')


    def __call__(self):
        self.request.RESPONSE.setHeader('Content-Type','text/xml; charset=utf-8')
        return super(RSSView, self).__call__()


