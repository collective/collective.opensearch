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

from zope.interface import Interface, implements
from zope.component import adapts, getUtility
from zope.formlib.form import FormFields

from zope.schema import TextLine, Text, Bool , Choice
from Products.CMFDefault.formlib.schema import SchemaAdapterBase
from Products.CMFPlone.interfaces import IPloneSiteRoot
from Products.CMFPlone import PloneMessageFactory as _
from Products.CMFCore.interfaces import IPropertiesTool
from plone.app.controlpanel.form import ControlPanelForm


class IOpenSearchSettingsForm(Interface):
    """ The view interface for the open search prefs form """

    title = TextLine(title=_(u'Title'),
                     description=_(u'Title of your site to appear in OpenSearch.'),)

    description = Text(title=_(u'Description'),
                           description=_(u'A human-readable description of the'
                                         'search engine.'))

    tags = Text(title=_(u'Tags'),
                description=_(u'Tags, one per line.'),
                required=False)

    contact = TextLine(title=_(u'Contact'),
                       description=_(u'An email address of someone to contact.'),
                       required=False)

    longName = TextLine(title=_(u'Longname'),
                        description=_(u'Contains an extended human-readable title that identifies this search engine.'),
                        required=False)

    attribution = TextLine(title=_(u'Attribution'),
                        description=_(u'Contains a list of all sources or entities that should be credited for the content contained in the search feed. '),
                        required=False)
    
    developer = TextLine(title=_(u'Developer'),
                        description=_(u'Contains the human-readable name or identifier of the creator or maintainer of the description document.  '),
                        required=False)   
                        
    adult = Bool(title=_(u'AdultContent'),
                    description=_(u'Contains a boolean value that should be set to true if the search results may contain material intended only for adults. '),
                    required=False)

    syndi = Choice(title=_(u'Syndication Rights'),
                           description=_(u'The syndication rights of the content.'),
                           vocabulary='Available Syndication',
                           required=True)

    searchMethod = Choice(title=_(u'Suggestion Method'),
                           description=_(u'Select the method to search , you can search in the title of the document or in the content ( title by defualt ) .'),
                           vocabulary='Suggestion Method',
                           required=True)

    allowRSS = Bool(title=_(u'Allow OpenSearch via RSS'),
                    description=_(u'Allow OpenSearch via RSS'),
                    required=False)

    allowAtom = Bool(title=_(u'Allow OpenSearch via Atom'),
                     description=_(u'Allow OpenSearch via Atom'),
                     required=False)

    allowXHTML = Bool(title=_(u'Allow OpenSearch via XHTML + xml'),
                      description=_(u'Allow OpenSearch via XHTML + xml'),
                      required=False)
                      
    allowDiscovery = Bool(title=_(u'Allow Autodiscovery in all the pages'),
                          description=_(u'Instead of allow autodiscovery only in the main page.'),
                                                required=False)
                                                
class OpenSearchControlPanelAdapter(SchemaAdapterBase):
    """ 
    Adapter that adapts the control panel form values to portal_properties. 
    """

    adapts(IPloneSiteRoot)
    implements(IOpenSearchSettingsForm)

    def __init__(self, context):
        super(OpenSearchControlPanelAdapter, self).__init__(context)
        pt = getUtility(IPropertiesTool)
        self.osprops = pt.opensearch_properties

    def get_title(self):
        return self.osprops.title

    def set_title(self, title):
        self.osprops.title = title

    def get_description(self):
        return self.osprops.description

    def set_description(self, desc):
        self.osprops.description = desc

    def get_tags(self):
        return self.osprops.tags

    def set_tags(self, tags):
        self.osprops.tags = tags

    def get_contact(self):
        return self.osprops.contact

    def set_contact(self, contact):
        self.osprops.contact = contact

    def get_allowRSS(self):
        return self.osprops.allowRSS

    def set_allowRSS(self, allow):
        self.osprops.allowRSS = allow

    def get_allowAtom(self):
        return self.osprops.allowAtom 

    def set_allowAtom(self, allow):
        self.osprops.allowAtom = allow

    def get_allowXHTML(self):
        return self.osprops.allowXHTML

    def set_allowXHTML(self, allow):
        self.osprops.allowXHTML = allow

    def get_allowDiscovery(self):
        return self.osprops.allowDiscovery
    
    def set_allowDiscovery(self,allow):
        self.osprops.allowDiscovery = allow

    def get_syndi(self):
        return self.osprops.syndi
        
    def set_syndi(self,syndi):
        self.osprops.syndi = syndi

    def get_longName(self):
        return self.osprops.longName
        
    def set_longName(self,lname):
        self.osprops.longName = lname
    
    def get_attr(self):
        return self.osprops.attribution
        
    def set_attr(self,attribution):
        self.osprops.attribution = attribution

    def get_adult(self):
        return self.osprops.adult 
        
    def set_adult(self,adult):
        self.osprops.adult = adult

    def get_devel(self):
        return self.osprops.developer
        
    def set_devel(self,devel):
        self.osprops.developer = devel

    def get_sMethod(self):
        return self.osprops.searchMethod
        
    def set_sMethod(self,method):
        self.osprops.searchMethod = method

    title = property(get_title, set_title)
    description = property(get_description, set_description)
    tags = property(get_tags, set_tags)
    contact = property(get_contact, set_contact)
    longName = property(get_longName, set_longName)
    attribution = property (get_attr,set_attr)
    developer = property (get_devel,set_devel)
    syndi = property(get_syndi,set_syndi)
    adult = property(get_adult,set_adult)
    allowRSS = property(get_allowRSS, set_allowRSS)
    allowAtom = property(get_allowAtom, set_allowAtom)
    allowXHTML = property(get_allowXHTML, set_allowXHTML)
    allowDiscovery = property(get_allowDiscovery,set_allowDiscovery)
    searchMethod = property(get_sMethod,set_sMethod)


class OpenSearchPrefsForm(ControlPanelForm):
    """ The preferences form. """
    implements(IOpenSearchSettingsForm)
    form_fields = FormFields(FormFields(IOpenSearchSettingsForm))

    label = _(u'Open Search Settings Form')
    description = _(u'An OpenSearch description document can be used to describe the web interface of a search engine. In this form you can edit the information about your site.')
    form_name = _(u'OpenSearch Settings')


                           

