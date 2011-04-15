from zope.interface import implements, Interface
from DateTime import DateTime
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.Five import BrowserView
from Products.CMFCore.utils import getToolByName

from collective.opensearch import opensearchMessageFactory as _
from baseview import BaseView, BaseEntry


class IHtmlView(Interface):
    """
    Html view interface
    """

class HtmlView(BaseView):
    """
    Html browser view
    """
    implements(IHtmlView)

    render = ViewPageTemplateFile('oslinkview.pt')
    results_template = ViewPageTemplateFile('osresults.pt')


    def is_html(self, entry):
         return False

    def display_results(self):
        return self.results_template()
