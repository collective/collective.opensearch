from zope.interface import implements, Interface
from zope.component import getUtility

from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.Five import BrowserView

from plone.registry.interfaces import IRegistry
from Products.CMFCore.utils import getToolByName

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


    def get_title(self):
        return self.settings.short_name

    def get_description(self):
        return self.settings.description

    def get_tags(self):
        return self.settings.tags

    def get_contact(self):
        return self.settings.contact

    def allow_suggestions(self):
        return self.settings.suggestion_limit > 0

    def __call__(self):
        self.request.RESPONSE.setHeader('Content-Type','text/xml; charset=utf-8')
        return ViewPageTemplateFile('descriptionview.pt')(self)
