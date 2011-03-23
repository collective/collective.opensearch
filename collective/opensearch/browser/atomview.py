from zope.interface import implements, Interface

from Products.Five import BrowserView
from Products.CMFCore.utils import getToolByName

from collective.opensearch import opensearchMessageFactory as _


class IAtomView(Interface):
    """
    Atom view interface
    """



class AtomView(BrowserView):
    """
    Atom browser view
    """
    implements(IAtomView)

    def __init__(self, context, request):
        self.context = context
        self.request = request

    @property
    def portal_catalog(self):
        return getToolByName(self.context, 'portal_catalog')

    @property
    def portal(self):
        return getToolByName(self.context, 'portal_url').getPortalObject()


