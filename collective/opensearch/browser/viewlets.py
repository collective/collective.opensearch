##################################################################################
#    Copyright (c) 2009 Massachusetts Institute of Technology, All rights reserved.
#
#    This program is free software; you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, version 2.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program; if not, write to the Free Software
#    Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
##################################################################################

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
        if 'collective.jaop' in qi.objectIds():
          if props:
              # Get the specific opensearch_properties
              self.osprops = props.opensearch_properties
          else:
              self.osprops = None
        else:
          self.osprops = None
        # We get the Portal object to show the autodiscovery only in the root page
        portal_url = getToolByName(context, "portal_url")
        self.portal = portal_url.getPortalObject()

    def getTitle(self):
        returnValue = ""
        if ( self.osprops != None ):
            returnValue = self.osprops.shortName
        return returnValue

    def render(self):
        returnValue = ""
        if ( self.osprops != None ):
            # Render the autodiscovery snippet if the page is the Default page of Site Root
            if ( self.context.getId() == self.portal.getDefaultPage() ):
                return self._template()
        return ""

