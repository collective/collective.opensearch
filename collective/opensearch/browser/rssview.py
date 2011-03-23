from zope.interface import implements, Interface

from Products.Five import BrowserView
from Products.CMFCore.utils import getToolByName

from collective.opensearch import opensearchMessageFactory as _


class IRSSView(Interface):
    """
    RSS view interface
    """




class RSSView(BrowserView):
    """
    RSS browser view
    """
    implements(IRSSView)

    def __init__(self, context, request):
        self.context = context
        self.request = request

    @property
    def portal_catalog(self):
        return getToolByName(self.context, 'portal_catalog')

    @property
    def portal(self):
        return getToolByName(self.context, 'portal_url').getPortalObject()

