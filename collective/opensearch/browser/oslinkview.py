from zope.interface import implements, Interface

from Products.Five import BrowserView
from Products.CMFCore.utils import getToolByName

from collective.opensearch import opensearchMessageFactory as _
import feedparser


class IOsLinkView(Interface):
    """
    OsLink view interface
    """

class OsLinkView(BrowserView):
    """
    OsLink browser view
    """
    implements(IOsLinkView)
    searchterm = ''

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def get_search_results(self):
        url = self.context.getRemoteUrl()
        search_term = self.request.form.get('SearchableText', None)
        if not search_term:
                return []
        self.searchterm = search_term
        qurl = url.replace('%7BsearchTerms%7D',search_term)
        results= feedparser.parse(qurl)
        return results['entries']


