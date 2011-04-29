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
from z3c.form import interfaces

from zope import schema
from zope.interface import Interface

from collective.opensearch import opensearchMessageFactory as _

class IOpenSearchSettings(Interface):
    """Global settings. This describes records stored in the
    configuration registry and obtainable via plone.registry.
    """

    short_name = schema.TextLine(title=_(u'Title'),
        description=_(u'A short name for your Open Search widget. Limited to 16 characters'),
        max_length=16,
        min_length=2,
        required=True,
        default=u'Search Site',)

    description = schema.Text(title=_(u'Description'),
        description=_(u'A human-readable description of the'
                     'search engine. Limited to 1024 characters'),
        max_length=1024,
        min_length=2,
        required=True,
        default=u'Search this site using open search ...',)

    tags = schema.TextLine(title=_(u'Tags'),
        description=_(u'A set of words that are used as keywords to identify and categorize this search content delimited by the space character. '),
        required=False,
        max_length=256,
        default=u'',)

    contact = schema.TextLine(title=_(u'Contact'),
        description=_(u'An email address of someone to contact.'),
        required=False,
        default=u'',)

    suggestion_limit = schema.Int(title=_(u'Suggestions'),
        description=_(u'Number of suggestions to be returned to the browser (0 turns suggestions off).'),
        required=True,
        min = 0,
        max = 100,
        default=5,)

    example = schema.TextLine(title=_(u'Example'),
        description=_(u'''OpenSearch description documents
        should include at least one Query element of type="example"
        that is expected to return search results.
        Search clients may use this example query to
        validate that the search engine is working properly.'''),
        required=True,
        default=u'None',)

    category_indexes = schema.List(
        title=_(u"Category Indexes"),
        description=_(u"Select the indexes to use as categories"),
        default=['Subject'],
        value_type=schema.Choice(vocabulary='collective.opensearch.indexes'),
        required=True)


    cache_timeout = schema.Int(title=_(u'Cache time'),
        description=_(u'Time in seconds a search feed is cached before refetching it'),
        required=True,
        min = 1,
        max = 24*60*60,
        default=360,)
