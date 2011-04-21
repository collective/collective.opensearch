from zope.interface import implements, Interface
from DateTime import DateTime
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from baseview import BaseView, BaseEntry

class AtomEntry(BaseEntry):

    def updated(self):
        return DateTime(self.brain.modified).HTML4()

    def published(self):
        return DateTime(self.brain.Date).HTML4()


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
    _type="application/atom+xml"
    LinkEntry = AtomEntry

    def updated(self):
        return DateTime().HTML4()




