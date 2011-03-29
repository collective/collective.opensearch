import urllib
from zope.interface import implements, Interface

from Products.Five import BrowserView
from Products.CMFCore.utils import getToolByName

from collective.opensearch import opensearchMessageFactory as _


class IOSFolderView(Interface):
    """
    OSFolder view interface
    """


class OSFolderView(BrowserView):
    """
    OSFolder browser view
    """
    implements(IOSFolderView)

    js_template = '''
        $.get('%(url)s',
                function(data) {
                  $('#%(id)s').html(data);
            });
            '''


    def __init__(self, context, request):
        self.context = context
        self.request = request

    @property
    def searchterm(self):
        return self.request.form.get('SearchableText', '')

    @property
    def portal_catalog(self):
        return getToolByName(self.context, 'portal_catalog')

    @property
    def portal(self):
        return getToolByName(self.context, 'portal_url').getPortalObject()


    def get_searches(self):
        type_filter = {"portal_type" : ["Link"]}
        for r in self.context.getFolderContents(contentFilter=type_filter):
            if r.getObject().getLayout() == 'oslink_view':
                yield r

    def get_js(self, link):
        vars = {}
        url = '/opensearchresults.html?SearchableText='
        vars['url'] = link.getURL() + url + urllib.quote_plus(self.searchterm)
        vars['id'] = 'searchresults-' + link.id
        return self.js_template % vars
