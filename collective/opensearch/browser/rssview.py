from DateTime import DateTime
from zope.interface import implements, Interface
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from baseview import BaseView, BaseEntry

class RSSEntry(BaseEntry):

    def pub_date(self):
        return DateTime(self.brain.Date).rfc822()


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
    _type="application/rss+xml"
    LinkEntry = RSSEntry

    def __call__(self):
        self.request.RESPONSE.setHeader('Content-Type','application/rss+xml; charset=utf-8')
        return super(RSSView, self).__call__()


