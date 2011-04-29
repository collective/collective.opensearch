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
import urllib2
from time import time
import elementtree.ElementTree as ET
import xml.dom.minidom
from plone.memoize import ram

from zope.component import getUtility
from plone.registry.interfaces import IRegistry
from collective.opensearch.interfaces.settings import IOpenSearchSettings


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
        body = feed.read().encode('utf-8')
        pxml = xml.dom.minidom.parseString(body)
        if pxml.documentElement.namespaceURI.startswith('http://www.opengis.net/kml/'):
            rtype = 'kml'
            result = body
        else:
            result = feedparser.parse(body, response_headers = feed.headers.dict)
            rtype='feed'

    return {'errors': errors, 'result': result, 'type': rtype}
