from zope.interface import implements, Interface
from atomview import AtomEntry, IAtomView, AtomView
import json


class IJsonView(IAtomView):
    pass


class JsonView(AtomView):

    def render(self):
        self.request.RESPONSE.setHeader('Content-Type','application/json; charset=utf-8')
        metadata = {
            "title": self.feed_title() +': ' + self.searchterm,
            "updated": self.updated(),
            "id": self.uid,
            "generator": {"uri": "http://plone.org/products/plos",
                        "version": "1.0",
                        "name": "collective.opensearch"},
            "totalResults": self.total_results,
            "startIndex": self.start,
            "itemsPerPage": self.max_items,
            }
        result_list = []
        for result in self.search_results:
            result_list.append({
                "title": result.title(),
                "url": result.link(),
                "content": result.summary(),
                "relevance": result.relevance_score(),
                "type": result.get_type(),
                "id": result.get_uid(),
                "category": result.tags(),
                "published": result.published(),
                "updated": result.updated(),
                "author": result.author(),
                })
        return json.dumps({"metadata": metadata, "results" : result_list})
