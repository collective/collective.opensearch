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

import logging
import urllib
from zope.interface import implements, Interface

from Products.Five import BrowserView
from Products.CMFCore.utils import getToolByName

from collective.opensearch import opensearchMessageFactory as _
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from utils import fetch_url, parse_kml, substitute_parameters

logger = logging.getLogger('collective.opensearch')

class IOsLinkView(Interface):
    """
    OsLink view interface
    """

class OsLinkView(BrowserView):
    """
    OsLink browser view
    """
    implements(IOsLinkView)
    searchterm = ''
    results_template = ViewPageTemplateFile('osresults.pt')
    total_results = 0
    feed_html_link = None
    feed_title =''

    @property
    def searchterm(self):
        return self.request.form.get('searchTerms', '')

    def has_searchterm(self):
        url = self.context.getRemoteUrl()
        return url.find('%7BsearchTerms%7D') > 0


    def display_results(self):
        return self.results_template()

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def is_html(self, entry):
        if entry['summary_detail']['type'] in ['text/html',
                                            'application/xhtml+xml']:
            return True
        elif entry['summary_detail']['type']=='text/plain':
            return False
        else:
            logger.info('Unknown format for summary detail: %s' %
                entry['summary_detail']['type'])
            return False

    def search_results(self):
        url = self.context.getRemoteUrl()
        search_term = urllib.quote_plus(self.searchterm)
        if self.has_searchterm():
            if not search_term:
                    return []
            else:
                qurl = substitute_parameters(url, self.request.form)
        else:
            qurl = url
        rd = fetch_url(qurl)
        results = rd['result']
        if rd['type'] == 'feed':
            try:
                self.total_results = int(results.feed.get('opensearch_totalresults','0'))
                if self.total_results == 0:
                    self.total_results = int(results.feed.get('totalresults','0'))
            except ValueError:
                pass
            for link in results.feed.get('links', []):
                if (link['rel']=='alternate') and (link['type']=='text/html'):
                    self.feed_html_link = link['href']
            self.feed_title = results.feed.get('title', '')
            return results['entries']
        elif rd['type'] == 'kml':
            return parse_kml(results)
        else:
            return []

class OsLinkSnippet(OsLinkView):



    def __call__(self):
        return self.display_results()


