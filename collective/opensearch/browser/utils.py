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
import feedparser
import urllib2, urllib, urlparse
import chardet
from time import time
import logging
from elementtree.ElementTree import XML, tostring
from htmllaundry import sanitize
from plone.memoize import ram

from zope.component import getUtility
from plone.registry.interfaces import IRegistry
from collective.opensearch.interfaces.settings import IOpenSearchSettings

logger = logging.getLogger('collective.opensearch')

def substitute_parameters(url, form):
    """ The search client must replace every instance of a template
        parameter with a value before the search request is performed.

        If a search engine wishes to indicate that a template parameter
        is optional and can be replaced with the empty string, then
        the "?" notation should be used.

    http://www.opensearch.org/Specifications/OpenSearch/1.1#Substitution_rules
    """

    #urlparse.parse_qs(urlparse.urlparse(urllib.unquote('http://api.search.yahoo.com/WebSearchService/rss/webSearch.xml?appid=yahoosearchwebrss&query=%7BSearchTerms%7D&adult_ok=1&adult_ok=2')).query)
    #urllib.urlencode((('query', 'Search Terms'), ('adult_ok', '1'), ('adult_ok', '2'), ('appid', 'yahoosearchwebrss')))

    url_obj = urlparse.urlparse(urllib.unquote(url))
    query = urlparse.parse_qs(url_obj.query)
    params = []
    for k,v_list in query.iteritems():
        for v in v_list:
            if v.startswith('{') and v.endswith('?}'):
                parameter = form.get(v[1:-2], None)
                if parameter:
                    params.append((k,parameter))
            elif v.startswith('{') and v.endswith('}'):
                parameter = form.get(v[1:-1], None)
                if parameter:
                    params.append((k,parameter))
                else:
                     logger.info('missing parameter: %s' % v)
            else:
                params.append((k,v))
    parsed_url = urlparse.urlunparse((url_obj.scheme, url_obj.netloc,
        url_obj.path, url_obj.params, urllib.urlencode(params),
        url_obj.fragment))
    if (not('{searchTerms}' in query) and
        form.get('searchTerms', None) and
        (parsed_url.find('%7BsearchTerms%7D') > 0)):
        # this is a hack to get urls not conforming to opensearch definitions
        # (i.e {searchTerms} is not a parameter value on its own) working anyway
        # for e.g http://www.eprints.org/
        parsed_url = parsed_url.replace('%7BsearchTerms%7D', form.get('searchTerms',''))
    return parsed_url

def sanitize_kml_description(description):
    if description:
        desc = description[0].text
        #sanitize html snippet to avoid XSS
        return sanitize(desc)

def sanitize_kml(kmlstring):
    kmldom = XML(kmlstring)
    ns = kmldom.tag.strip('kml')
    placemarks = kmldom.findall('.//%sPlacemark' % ns)
    for placemark in placemarks:
        summary = placemark.findall('%sdescription' % ns)
        summary[0].text = sanitize_kml_description(summary)
    return tostring(kmldom, 'utf-8')

def parse_kml(kmlstring):
    entries=[]
    kmldom = XML(kmlstring)
    ns = kmldom.tag.strip('kml')
    placemarks = kmldom.findall('.//%sPlacemark' % ns)
    for placemark in placemarks:
        entry = {'title':'', 'summary':'', 'summary_detail':
                                {'type':'text/html'},
                'link':'', 'tags': None}
        title = placemark.findall(ns + 'name')
        if title:
            entry['title'] = title[0].text
        else:
            entry['title'] =''
        summary = placemark.findall(ns+'description')
        entry['summary'] = sanitize_kml_description(summary)
        links = placemark.findall('{http://www.w3.org/2005/Atom}link')
        for link in links:
            entry['link'] = link.attrib.get('href')
        entries.append(entry)
    return entries

def _fetch_url_cachekey(fun, url):
    RAM_CACHE_SECONDS = 360
    try:
        registry = getUtility(IRegistry)
        settings = registry.forInterface(IOpenSearchSettings)
        RAM_CACHE_SECONDS = settings.cache_timeout
    except:
        pass
    ckey = [url]
    ckey.append(time() // RAM_CACHE_SECONDS)
    return ckey

@ram.cache(_fetch_url_cachekey)
def fetch_url(url):
    ''' fetches a remote url and in case of success returns
    type: type of fetched url (feed, kml)
    result: parsed feed, kml
    '''
    result = None
    rtype =  None
    errors = None
    try:
        feed = urllib2.urlopen(url)
    except urllib2.URLError, e:
        print e
        errors = e
        return {'errors': errors, 'result': None, 'type': None}

    if feed.info().type in ["application/atom+xml", "application/rss+xml"]:
        result = feedparser.parse(feed)
        rtype = 'feed'
    elif feed.info().type == 'application/vnd.google-earth.kml+xml':
        result = feed.read()
        rtype = 'kml'
    elif feed.info().type == 'text/xml':
        body = feed.read()
        # before passing it to etree we need to determine the encoding
        try:
            charset = feed.headers.getparam('charset')
            pbody = body.decode(charset).encode('ascii', 'xmlcharrefreplace')
        except (UnicodeDecodeError, LookupError):
            charset = chardet.detect(body)['encoding']
            pbody = body.decode(charset, 'ignore').encode('ascii', 'xmlcharrefreplace')
        try:
            tree = XML(pbody)
            if u'http://www.opengis.net/kml/' in tree.tag:
                rtype = 'kml'
                result = pbody.encode('utf-8')
            elif tree.tag.endswith('kml'):
                rtype = 'kml'
                result = pbody.encode('utf-8')
            else:
                result = feedparser.parse(body, response_headers = feed.headers.dict)
                rtype='feed'

        except Exception, e:
            logger.info('exeption raised in fetch_url: %s' % e)
            #ElementTree cannot parse this, -> probably a messed up feed
            errors = e
            result = feedparser.parse(body, response_headers = feed.headers.dict)
            rtype='feed'
    if rtype == 'kml':
        result = sanitize_kml(result)
    return {'errors': errors, 'result': result, 'type': rtype}
