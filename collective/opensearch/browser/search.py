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
########################################################################
# module version of:
# Script (Python) "queryCatalog"
# use search.query_catalog instead of the script
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=
# request=None,
# show_all=False,
# quote_logic=False,
# quote_logic_indexes=['SearchableText','Description','Title'],
# use_types_blacklist=False,
# show_inactive=False,
# use_navigation_root=False
##title=wraps the portal_catalog with a rules qualified query
##

from ZODB.POSException import ConflictError
from Products.ZCTextIndex.ParseTree import ParseError
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.browser.navtree import getNavigationRoot

from Products.CMFPlone.interfaces import IPloneSiteRoot
from Products.ATContentTypes.interfaces.topic import IATTopic

def quotestring(s):
    return '"%s"' % s

def quotequery(s):
    if not s:
        return s
    try:
        terms = s.split()
    except ConflictError:
        raise
    except:
        return s
    tokens = ('OR', 'AND', 'NOT')
    s_tokens = ('OR', 'AND')
    check = (0, -1)
    for idx in check:
        if terms[idx].upper() in tokens:
            terms[idx] = quotestring(terms[idx])
    for idx in range(1, len(terms)):
        if (terms[idx].upper() in s_tokens and
            terms[idx-1].upper() in tokens):
            terms[idx] = quotestring(terms[idx])
    return ' '.join(terms)


def quote_bad_chars(s):
    """
    We need to quote parentheses when searching text indices (we use
    quote_logic_indexes as the list of text indices)
    """
    bad_chars = ["(", ")"]
    for char in bad_chars:
        s = s.replace(char, quotestring(char))
    return s

def ensureFriendlyTypes(query, context):
    ploneUtils = getToolByName(context, 'plone_utils')
    portal_type = query.get('portal_type', [])
    if not type(portal_type)==type([]):
        portal_type = [portal_type]
    Type = query.get('Type', [])
    if not type(Type)==type([]):
        Type = [Type]
    typesList = portal_type + Type
    if not typesList:
        friendlyTypes = ploneUtils.getUserFriendlyTypes(typesList)
        query['portal_type'] = friendlyTypes

def rootAtNavigationRoot(query, context):
    if 'path' not in query:
        query['path'] = getNavigationRoot(context)


def build_query(context, request, show_all=False, quote_logic=False,
                quote_logic_indexes=['SearchableText','Description','Title'],):
    show_query = show_all
    results=[]
    catalog=getToolByName(context, 'portal_catalog')
    indexes=catalog.indexes()
    query={}
    second_pass = {}

    # See http://dev.plone.org/plone/ticket/9422 for
    # an explanation of '\u3000'
    multispace = u'\u3000'.encode('utf-8')

    # Avoid creating a session implicitly.
    for k in request.keys():
        if k in ('SESSION',):
            continue
        v = request.get(k)
        if v and k in indexes:
            if k in quote_logic_indexes:
                v = quote_bad_chars(v)
                if multispace in v:
                    v = v.replace(multispace, ' ')
                if quote_logic:
                    v = quotequery(v)
            query[k] = v
            show_query = True
        elif k.endswith('_usage'):
            key = k[:-6]
            param, value = v.split(':')
            second_pass[key] = {param:value}
        elif k in ('sort_on', 'sort_order', 'sort_limit'):
            if k == 'sort_limit' and not (type(v)==type(0)):
                query[k] = int(v)
            else:
                query[k] = v

    for k, v in second_pass.items():
        qs = query.get(k)
        if qs is None:
            continue
        query[k] = q = {'query':qs}
        q.update(v)

    return query, show_query


def get_query_results(context, query, show_query, use_types_blacklist=False,
                        show_inactive=False, use_navigation_root=False):
    # doesn't normal call catalog unless some field has been queried
    # against. if you want to call the catalog _regardless_ of whether
    # any items were found, then you can pass show_all=True.
    results=[]
    catalog=getToolByName(context, 'portal_catalog')
    if show_query:
        try:
            if use_types_blacklist:
                ensureFriendlyTypes(query, context)
            if use_navigation_root:
                rootAtNavigationRoot(query, context)
            query['show_inactive'] = show_inactive
            results = catalog(**query)
        except ParseError:
            pass

    return results


def query_catalog(context, request, show_all=False, quote_logic=False,
                    quote_logic_indexes=['SearchableText','Description','Title'],
                    use_types_blacklist=False,show_inactive=False,
                    use_navigation_root=False):

    query, show_query = build_query(context, request, show_all, quote_logic, quote_logic_indexes)

    return get_query_results(context, query, show_query, use_types_blacklist,
                            show_inactive, use_navigation_root)



def combine_queries(query_base, query_supplemental):
    query = {}
    for k, v in query_base.iteritems():
        if  k in query_supplemental:
            #XXX this is the tricky bit
            # TODO combine in an meaningfull way
            # currently only done for SearchableText as this is the only
            # parameter exposed by the open search description
            # otherwise we just use the items of query_base to override
            # query_supplemental
            # probably a yagni
            if k == 'SearchableText':
                query[k] = v + ' AND ' + query_supplemental[k]
            else:
                query[k] = v
                query_supplemental.pop(k)
        else:
            query[k] = v
    for k, v in query_supplemental.iteritems():
        query[k] = v
    return query


def get_results(context, request):
        search_results = []
        if IPloneSiteRoot.providedBy(context):
            search_results = query_catalog(context, request,
                                        use_types_blacklist=True)
        elif IATTopic.providedBy(context):
            q1 = context.buildQuery()
            q2, show_query = build_query(context,request)
            query = combine_queries(q1,q2)
            search_results = get_query_results(context, query,
                                    show_query=True, use_types_blacklist=True)
        return search_results


