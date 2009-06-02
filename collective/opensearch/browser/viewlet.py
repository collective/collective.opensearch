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

from Products.Five.viewlet.viewlet import ViewletBase
from Products.CMFCore.utils import getToolByName
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.CMFCore.utils import getToolByName
from Products.CMFCore import utils as cmfutils
from Products.CMFPlone.interfaces import IPloneSiteRoot

class AutoDiscovery(ViewletBase):
    """ Viewlet for AutoDiscovery """
    _template = ViewPageTemplateFile('autodiscovery.pt')
    _blank_template = ViewPageTemplateFile('blank.pt')

    def __init__(self, context, request, view, manager):
        # Implement the ViewletBase
        super(ViewletBase, self).__init__(context, request, view, manager)
        # Get the Portal Properties tool
        props = getToolByName(context, 'portal_properties', None)
        qi = getToolByName(context, 'portal_quickinstaller', None)  

        portal_url = getToolByName(context, "portal_url")
        self.portal = portal_url.getPortalObject()                

        #if 'Jaop' in qi.objectIds():
        if props:
              # Get the specific opensearch_properties
              if hasattr(props,'opensearch_properties'):
                self.osprops = props.opensearch_properties
              else:
                self.osprops = None
        else:
              self.osprops = None
        # else:
        #   self.portal.plone_log("none3");
        #  self.osprops = None
        # We get the Portal object to show the autodiscovery only in the root page
        portal_url = getToolByName(context, "portal_url")
        self.portal = portal_url.getPortalObject()

    def getTitle(self):
        returnValue = ""
        if ( self.osprops != None ):
            returnValue = self.osprops.title
        return returnValue

    def render(self):
        returnValue = ""
        if ( self.osprops != None ):
            if ( self.osprops.allowDiscovery != True ):
                # Render the autodiscovery snippet if the page is the Default page of Site Root
                if ( self.context.getId() == self.portal.getDefaultPage() ):
                    returnValue= self._template()
            else:
                returnValue = self._template()
        return returnValue
