#       This program is free software; you can redistribute it and/or modify
#       it under the terms of the GNU General Public License as published by
#       the Free Software Foundation; either version 2 of the License, or
#       (at your option) any later version.
#
#       This program is distributed in the hope that it will be useful,
#       but WITHOUT ANY WARRANTY; without even the implied warranty of
#       MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#       GNU General Public License for more details.
#
#       You should have received a copy of the GNU General Public License
#       along with this program; if not, write to the Free Software
#       Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#       MA 02110-1301, USA.
import json
from zope.interface import implements, Interface
from zope.component import getUtility
from plone.registry.interfaces import IRegistry

from Products.Five import BrowserView
from Products.CMFCore.utils import getToolByName

from collective.opensearch import opensearchMessageFactory as _
from collective.opensearch.interfaces.settings import IOpenSearchSettings

class ISuggestionView(Interface):
    """
    Suggestion view interface
    """



class SuggestionView(BrowserView):
    """
    Suggestion browser view
    """
    implements(ISuggestionView)
    limit = 10

    def __init__(self, context, request):
        self.context = context
        self.request = request
        registry = getUtility(IRegistry)
        try:
            settings = registry.forInterface(IOpenSearchSettings)
            self.limit = setting.suggestion_limit
        except (KeyError, AttributeError):
            pass

    @property
    def portal_catalog(self):
        return getToolByName(self.context, 'portal_catalog')

    @property
    def portal(self):
        return getToolByName(self.context, 'portal_url').getPortalObject()

    def __call__(self):
        self.request.RESPONSE.setHeader('Content-Type','application/json; charset=utf-8')
        if self.limit==0:
            return json.dumps([])
        form = self.request.form
        searchterm = form.get('command', '')
        if ( searchterm == '*' ):
            searchterm = ''
        json_results = [searchterm, ]
        if searchterm:
            searchterm += '*'
        search_results = self.portal_catalog(Title = searchterm, sort_limit=self.limit)[:self.limit]
        json_results += [result.Title for result in search_results]
        return json.dumps(json_results)
