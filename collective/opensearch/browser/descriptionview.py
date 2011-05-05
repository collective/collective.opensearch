from zope.interface import implements, Interface
from zope.component import getUtility

from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.Five import BrowserView

from plone.registry.interfaces import IRegistry
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.interfaces import IPloneSiteRoot
from Products.ATContentTypes.interfaces.topic import IATTopic

from collective.opensearch import opensearchMessageFactory as _
from collective.opensearch.interfaces.settings import IOpenSearchSettings

class IDescriptionView(Interface):
    """
    Description view interface
    """



class DescriptionView(BrowserView):
    """
    Description browser view
    """
    implements(IDescriptionView)
    settings = None

    def __init__(self, context, request):
        self.context = context
        self.request = request
        registry = getUtility(IRegistry)
        self.settings = registry.forInterface(IOpenSearchSettings)


    def get_urls(self):
        urls = []
        urls.append({'rel': 'self',
            'template': self.context.absolute_url() + '/' + self.__name__,
            'type': 'application/opensearchdescription+xml',
            'indexOffset' : None})
        urls.append({'rel': 'results',
            'template': self.context.absolute_url() + '/opensearch_rss.xml?SearchableText={searchTerms}&b_start:int={startIndex?}&b_size:int={count?}',
            'type': 'application/rss+xml',
            'indexOffset' : '0'})
        urls.append({'rel': 'results',
            'template': self.context.absolute_url() + '/opensearch_atom.xml?SearchableText={searchTerms}&b_start:int={startIndex?}&b_size:int={count?}',
            'type': 'application/atom+xml',
            'indexOffset' : '0'})
        if self.settings.suggestion_limit > 0 and IPloneSiteRoot.providedBy(self.context):
            urls.append({'rel': 'suggestions',
                'template': self.context.absolute_url() + '/opensearch_suggestions?command={searchTerms}',
                'type': 'application/x-suggestions+json',
                'indexOffset' : None})
        if IPloneSiteRoot.providedBy(self.context):
            urls.append({'rel': 'results',
                'template': self.context.absolute_url() + '/search?SearchableText={searchTerms}',
                'type': 'text/html',
                'indexOffset' : '0'})
        elif IATTopic.providedBy(self.context):
            urls.append({'rel': 'results',
                'template': self.context.absolute_url() + '/opensearch_html.html?SearchableText={searchTerms}',
                'type': '"text/html',
                'indexOffset' : '0'})
        return urls

    def get_example(self):
         return self.settings.example

    def get_title(self):
        return self.settings.short_name

    def get_description(self):
        return self.settings.description

    def get_tags(self):
        return self.settings.tags

    def get_contact(self):
        return self.settings.contact

    def __call__(self):
        if IPloneSiteRoot.providedBy(self.context) or IATTopic.providedBy(self.context):
            self.request.RESPONSE.setHeader('Content-Type','text/xml; charset=utf-8')
            return ViewPageTemplateFile('descriptionview.pt')(self)
        else:
            return ''

