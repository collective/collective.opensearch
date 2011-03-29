

Project Description
===================

collective.opensearch adds the possibility to read and write OpenSearch
compatible search results in your Plone site.

OpenSearch is a collection of simple formats for the sharing of search results.

OpenSearch helps search engines and search clients communicate by
introducing a common set of formats to perform search requests
and syndicate search results.
The OpenSearch description document format can be used to describe a
search engine so that it can be used by search client applications.
The OpenSearch response elements can be used to extend existing
syndication formats, such as RSS and Atom, with the extra metadata
needed to return search results.

collective.opensearch enables you to syndicate the search results of
your plone site by formatting them in the RSS or Atom formats,
augmented with OpenSearch response elements.

collective.opensearch adds a view to the link type that lets you search
OpenSearch (or other searches that return RSS or Atom so any plone site)
compatible search providers within your site. When you add a link with an
open search url this view will be automatically set.

To search e.g. plone.org from your site add a search feed with the url: ::

    http://plone.org/search_rss?SearchableText={searchTerms}

You can combine several open search links as a metasearch. All OpenSearch links
inside a folder will be queried and their results displayed when you change
the view of a folder to 'Open Search View'

- Code repository: http://svn.plone.org/svn/collective/collective.opensearch/
- Questions and comments to product-developers@lists.plone.org
- Report bugs at http://plone.org/products/collective.opensearch/issues

