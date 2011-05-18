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
import logging
from zope.component import getUtility
from zope.component.interfaces import ComponentLookupError
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from plone.app.layout.viewlets import common as base
from plone.registry.interfaces import IRegistry

from Products.CMFPlone.interfaces import IPloneSiteRoot
from Products.ATContentTypes.interfaces.topic import IATTopic

from collective.opensearch.interfaces.settings import IOpenSearchSettings

logger = logging.getLogger('collective.opensearch')


class AutoDiscovery(base.ViewletBase):
    """ Viewlet for AutoDiscovery """
    settings = None
    template = ViewPageTemplateFile('autodiscovery.pt')

    def __init__(self, context, request, view, manager):
        # Implement the ViewletBase
        super(AutoDiscovery, self).__init__(context, request, view, manager)
        # Get the registry
        try:
            registry = getUtility(IRegistry)
            try:
                self.settings = registry.forInterface(IOpenSearchSettings)
            except KeyError:
                pass
        except Exception, e:
            logger.info('exeption raised in AutoDiscovery viewlet: %s' % e)

    def getTitle(self):
        try:
            return self.settings.short_name
        except (KeyError, AttributeError):
            return 'N/A'

    def render(self):
        if IPloneSiteRoot.providedBy(self.context) or IATTopic.providedBy(self.context):
            return self.template()
        else:
            return ''


