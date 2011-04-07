import urllib
import ZTUtils
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
    _type = None
    _params = ''
    url = ''

    def __init__(self, context, request):
        self.context = context
        self.request = request
        registry = getUtility(IRegistry)
        self.settings = registry.forInterface(IOpenSearchSettings)
        portal_qi = getToolByName(context, 'portal_quickinstaller')
        self.version=portal_qi.getProductVersion('collective.opensearch')
        self.url = self.context.absolute_url() + '/' + self.__name__ + '?'

    def _get_params(self):
        indexes=self.portal_catalog.indexes()
        sorts = ['sort_on', 'sort_order', 'sort_limit']
        form = self.request.form
        params = {}
        for k,v in form.iteritems():
            if k in indexes + sorts:
                if v:
                    params[k]=v
            elif k.endswith('_usage'):
                if  k[:-6] in indexes:
                    if v and form.get(k[:-6], False):
                        params[k]=v
        return ZTUtils.make_query(params)




    def _alternate_link(self):
        params = self._params + '&b_start=%d&b_size=%d' % (self.start,
                                                    self.max_items)
        return {'href': '%s/search?%s' % (self.portal_url(), params ),
                'rel': 'alternate',
                'type': 'text/html'
                }

    def _self_link(self):
        params = self._params + '&b_start=%d&b_size=%d' % (self.start,
                                                    self.max_items)
        return {'href': self.url + params,
                'rel': 'self',
                'type': self._type,
                }

    def _first_link(self):
        if self.start > 0:
            params = self._params + '&b_start=0&b_size=%d' % self.max_items
            return {'href': self.url + params,
                    'rel': 'first',
                    'type': self._type,
                    }


    def _last_link(self):
        last = (self.total_results / self.max_items) * self.max_items
        if self.start + self.max_items < self.total_results:
            params = self._params + '&b_start=%d&b_size=%d' % (last,
                                                        self.max_items)
            return {'href': self.url + params,
                    'rel': 'last',
                    'type': self._type,
                    }


    def _next_link(self):
        next = self.start + self.max_items
        if next < self.total_results:
            params = self._params + '&b_start=%d&b_size=%d' % (next,
                                                    self.max_items)
            return {'href': self.url + params,
                'rel': 'next',
                'type': self._type,
                }


    def _previous_link(self):
        prev = self.start - self.max_items
        if self.start > 0:
            params = self._params + '&b_start=%d&b_size=%d' % (prev,
                                                    self.max_items)
            return {'href': self.url + params,
                'rel': 'previous',
                'type': self._type,
                }


    def _search_link(self):
        return {'href': '%s/opensearch_description.xml' % self.portal_url(),
            'rel': 'search',
            'type': 'application/opensearchdescription+xml'}

    @property
    def portal_catalog(self):
        return getToolByName(self.context, 'portal_catalog')

    def links(self):
        return [self._alternate_link(),
                self._self_link(),
                self._first_link(),
                self._last_link(),
                self._next_link(),
                self._previous_link(),
                self._search_link()]



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
        # start, count and end must be positive integers
        try:
            self.start = abs(int(self.request.get('b_start', 0)))
        except ValueError:
            self.start = 0
        try:
            self.max_items = abs(int(self.request.get('b_size', 20)))
        except ValueError:
            self.max_items=20
        self.end = self.start + self.max_items
        if IReferenceable.providedBy(self.context):
            self.uid = self.portal_url + '/resolveuid/' + self.context.UID()
        else:
            self.uid = self.context.absolute_url()

        search_results = search.query_catalog(self.context, self.request,
                                    use_types_blacklist=True)
        self.search_results = search_results[self.start:self.end]
        self.total_results = len(search_results)
        self._params = self._get_params()
        return self.render()


