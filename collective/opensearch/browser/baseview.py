import urllib
import ZTUtils
from DateTime import DateTime
from zope.component import getUtility

from Products.Five import BrowserView

from Products.CMFCore.utils import getToolByName
from Products.Archetypes.interfaces.referenceable import IReferenceable
from Products.CMFPlone.interfaces import IPloneSiteRoot
from Products.ATContentTypes.interfaces.topic import IATTopic

from plone.registry.interfaces import IRegistry

from collective.opensearch import opensearchMessageFactory as _
from collective.opensearch.interfaces.settings import IOpenSearchSettings
from collective.opensearch.browser import search


def not_implemented(*args, **kwargs):
    raise NotImplementedError


class BaseEntry(object):

    def __init__(self, context, request, brain):
        self.context = context
        self.request = request
        self.brain=brain
        self.portal_membership = getToolByName(self.context, 'portal_membership')
        self.portal_url = getToolByName(self.context, 'portal_url')()
        registry = getUtility(IRegistry)
        self.settings = registry.forInterface(IOpenSearchSettings)

    def get_author_info(self, creator):
        author = self.portal_membership.getMemberInfo(creator)
        ad = {'name': creator,
              'uri': self.portal_url + '/author/' + creator}
        if author:
            if author['fullname']:
                ad['name'] = author['fullname']
            if author['home_page']:
                ad['uri'] = author['home_page']
        return ad

    def has_searchterm(self):
        url = self.context.getRemoteUrl()
        return url.find('%7BsearchTerms%7D') > 0

    def title(self):
        return self.brain.Title

    def get_uid(self):
        return self.portal_url + '/resolveuid/' + self.brain.UID

    def link(self):
        return self.brain.getURL()

    def summary(self):
        return self.brain.Description

    def author(self):
        return self.get_author_info(self.brain.Creator)

    def tags(self):
        taglist=[]
        for cat in self.settings.category_indexes:
            scheme_url="%s/search?%s:list=" %( self.portal_url, cat)
            if getattr(self.brain, cat, None):
                for subject in getattr(self.brain, cat):
                    scheme_url="%s/search?%s%%3Alist=%s" % (self.portal_url,
                                                        cat, subject)
                    taglist.append( {'term': subject,
                            'label': subject,
                            'scheme': scheme_url})
        return taglist

    def relevance_score(self):
        if self.brain.data_record_normalized_score_:
            return float(self.brain.data_record_normalized_score_)/100.0

    def get_type(self):
        return self.brain.Type

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
    _type = 'text'
    _params = ''
    url = ''
    LinkEntry = BaseEntry
    query=None


    def __init__(self, context, request):
        self.context = context
        self.request = request
        registry = getUtility(IRegistry)
        self.settings = registry.forInterface(IOpenSearchSettings)
        portal_qi = getToolByName(context, 'portal_quickinstaller')
        self.version=portal_qi.getProductVersion('collective.opensearch')
        self.url = self.context.absolute_url() + '/' + self.__name__ + '?'

    def _get_params(self, start=0):
        indexes=self.portal_catalog.indexes()
        sorts = ['sort_on', 'sort_order', 'sort_limit']
        form = self.request.form
        params = {'b_start': start, 'b_size': self.max_items}
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
        params = self._get_params(self.start)
        url = self.context.absolute_url() + '/opensearch_html.html?'
        return {'href': url + params,
                'rel': 'alternate',
                'type': 'text/html'
                }

    def _self_link(self):
        params = self._get_params(self.start)
        return {'href': self.url + params,
                'rel': 'self',
                'type': self._type,
                }

    def _first_link(self):
        if self.start > 0:
            params = self._get_params(0)
            return {'href': self.url + params,
                    'rel': 'first',
                    'type': self._type,
                    }


    def _last_link(self):
        last = (self.total_results / self.max_items) * self.max_items
        if self.start + self.max_items < self.total_results:
            params = self._get_params(last)
            return {'href': self.url + params,
                    'rel': 'last',
                    'type': self._type,
                    }


    def _next_link(self):
        next = self.start + self.max_items
        if next < self.total_results:
            params = self._get_params(next)
            return {'href': self.url + params,
                'rel': 'next',
                'type': self._type,
                }


    def _previous_link(self):
        prev = self.start - self.max_items
        if self.start > 0:
            params = self._get_params(prev)
            return {'href': self.url + params,
                'rel': 'previous',
                'type': self._type,
                }


    def _search_link(self):
        return {'href': '%s/opensearch_description.xml' % self.context.absolute_url(),
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


    def _get_search_results(self, results):
        for result in results:
            yield(self.LinkEntry(self.context, self.request, result))


    def portal_url(self):
        return getToolByName(self.context, 'portal_url')()

    def feed_title(self):
        return self.settings.short_name



    def __call__(self):
        if IReferenceable.providedBy(self.context):
            self.uid = self.portal_url() + '/resolveuid/' + self.context.UID()
        else:
            self.uid = self.context.absolute_url()
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

        search_results = search.get_results(self.context, self.request)

        self.search_results = self._get_search_results(search_results[self.start:self.end])
        self.total_results = len(search_results)
        self.request.RESPONSE.setHeader('Content-Type',
            '%s; charset=utf-8' % self._type)
        return self.render()


