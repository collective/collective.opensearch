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

from plone.app.layout.viewlets import common as base
from zope.component import getUtility
from plone.registry.interfaces import IRegistry
from collective.opensearch.interfaces.settings import IOpenSearchSettings

class AutoDiscovery(base.ViewletBase):
    """ Viewlet for AutoDiscovery """
    settings = None

    def __init__(self, context, request, view, manager):
        # Implement the ViewletBase
        super(AutoDiscovery, self).__init__(context, request, view, manager)
        # Get the registry
        registry = getUtility(IRegistry)
        try:
            self.settings = registry.forInterface(IOpenSearchSettings)
        except KeyError:
            pass


    def getTitle(self):
        try:
            return self.settings.short_name
        except (KeyError, AttributeError):
            return 'N/A'



