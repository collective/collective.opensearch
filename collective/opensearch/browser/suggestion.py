#############################################################################
#                                                                           #
#    This file is part of Jaop                                              #
#                                                                           #
#    Jaop is free software: you can redistribute it and/or modify           #
#    it under the terms of the GNU General Public License as published by   #
#    the Free Software Foundation, either version 3 of the License, or      #
#    (at your option) any later version.                                    #
#                                                                           #
#    Jaop is distributed in the hope that it will be useful,                #
#    but WITHOUT ANY WARRANTY; without even the implied warranty of         #
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the          #
#    GNU General Public License for more details.                           #
#                                                                           #
#    You should have received a copy of the GNU General Public License      #
#    along with Jaop.  If not, see <http://www.gnu.org/licenses/>.          #
#                                                                           #
#############################################################################

from zope.publisher.browser import BrowserView
from Products.CMFCore.utils import getToolByName
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.CMFCore.utils import getToolByName
from Products.CMFCore import utils as cmfutils


class OpenSearchSuggestion(BrowserView):
    """ 
    A Browser view that returns XML instead of HTML.
    It also accesses preferences from the portal_preferences
    Tool. 
    """

    render = ViewPageTemplateFile('suggestion.pt')
    
    def __init__(self, context, request):
        self.context = context
        self.request = request

    def __call__(self):
        self.request.response.setHeader('Content-Type', 'application/json')
        return self.render()

    def SearchSuggestions(self,busqueda):
        props = getToolByName(self.context, 'portal_properties', None)
        catalog = cmfutils.getToolByName(self.context, 'portal_catalog')

        if ( busqueda == '*' ):
            busqueda = ''
        kwargs = {}            
        if props:
              if hasattr(props,'opensearch_properties'):
                if ( props.opensearch_properties.searchMethod == "title"):
                    kwargs['Title'] = "*" + busqueda + "*"
                elif ( props.opensearch_properties.searchMethod == "content"):
                    kwargs['SearchableText'] = "*" + busqueda + "*"

        search_results = catalog(**kwargs)
        # self.context.plone_log("DEBUG -> term = " +str(busqueda) + " :: result = " + str(search_results))      
        return search_results[0:5]
              
