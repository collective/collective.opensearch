import urllib
from zope.component import getUtility

from Products.Five import BrowserView

from Products.CMFCore.utils import getToolByName
from Products.Archetypes.interfaces.referenceable import IReferenceable
from plone.registry.interfaces import IRegistry

from collective.opensearch import opensearchMessageFactory as _
from collective.opensearch.interfaces.settings import IOpenSearchSettings
from collective.opensearch.browser import search


def not_implemented(*args, **kwargs):
    raise NotImplementedError


class BaseView(BrowserView):
    """
    Base browser view
    """
    render = not_implemented
    settings=None
    searchterm=''
    searchterm_url =''
    start = 0
    max_items = 20
    end = 0
    search_results = []
    total_results = 0
    uid = ''
    version = '1.0'

    def __init__(self, context, request):
        self.context = context
        self.request = request
        registry = getUtility(IRegistry)
        self.settings = registry.forInterface(IOpenSearchSettings)
        QI = getToolByName(context, 'portal_quickinstaller')
        self.version=QI.getProductVersion('collective.opensearch')


    def get_author_info(self, creator):
        author = self.portal_membership().getMemberInfo(creator)
        ad = {'name': creator,
              'uri': self.portal_url() + '/author/' + creator}
        if author:
            if author['fullname']:
                ad['name'] = author['fullname']
            if author['home_page']:
                ad['uri'] = author['home_page']
        return ad

    def portal_membership(self):
        return getToolByName(self.context, 'portal_membership')

    def portal_url(self):
        return getToolByName(self.context, 'portal_url')()

    def feed_title(self):
        return self.settings.short_name


    def __call__(self):
        self.searchterm = self.request.get('SearchableText','')
        self.searchterm_url = urllib.quote_plus(self.searchterm)
        #start count and end must be positive integers
        try:
            self.start = abs(int(self.request.get('b_start', 0)))
        except ValueError:
            self.start = 0
        try:
            self.max_items = abs(int(self.request.get('count', 20)))
        except ValueError:
            self.max_items=20
        try:
            self.end = abs(int(self.request.get('b_end',
                            self.start + self.max_items)))
        except ValueError:
            self.end = self.start + self.max_items
        if self.end < self.start:
            self.end = self.start
        if IReferenceable.providedBy(self.context):
            self.uid = self.portal_url + '/resolveuid/' + self.context.UID()
        else:
            self.uid = self.context.absolute_url()

        search_results = search.query_catalog(self.context, self.request,
                                    use_types_blacklist=True)
        self.search_results = search_results[self.start:self.end]
        self.total_results = len(search_results)
        return self.render()


