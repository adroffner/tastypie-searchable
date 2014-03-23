from django.conf.urls import url
from tastypie.paginator import Paginator
from haystack.query import SearchQuerySet
## from tastypie.resources import ModelResource
from tastypie.utils import trailing_slash

import logging
logger = logging.getLogger(__name__)

class SearchableResourceMixin(object):
    """ Make a Tastypie ModelResource Haystack search-enabled.

    Search URL: /api/vX/<resource_name>/search/?search_terms=full+text&limit=10&offset=0
    Returns a Tastypie ModelResource result-set like `get_list`, using the same parameter options.

    Send a `search_terms` parameter to Haystack's `AutoQuery`.
    See the Haystack documentation for the search operators.

    class ObjectResource(SearchableResourceMixin, ModelResource):
        ...
    """

    def prepend_urls(self):
        logger.debug("Add get_search() URLs to %s" % self.__class__.__name__)
        # NOTE: "prepend" these URLs *before* the parent class'.
        _prepend_urls = [
            url(r"^(?P<resource_name>%s)/search%s$" % (self._meta.resource_name, trailing_slash()),
                self.wrap_view('get_search'), name="api_get_search"),
        ]
        _prepend_urls += super(SearchableResourceMixin, self).prepend_urls()
        return _prepend_urls

    def get_search(self, request, **kwargs):
        self.method_check(request, allowed=['get'])
        self.is_authenticated(request)
        self.throttle_check(request)

        # Run the full-text query, 'search_terms', using an AutoQuery().
        search_terms = request.GET.get('search_terms', '')
        if search_terms != '':
            sqs = SearchQuerySet().models(self._meta.queryset.model).\
                load_all().auto_query(search_terms)
            logger.error("get_search: FOUND %r" % sqs)
        else:
            # AutoQuery() returns all results for search_terms == ''.
            # fix that!
            sqs = []

        objects = [ s.object for s in sqs ]
        sorted_objects = self.apply_sorting(objects, options=request.GET)

        paginator = self._meta.paginator_class(request.GET, sorted_objects,
            resource_uri=self.get_resource_uri(url_name="api_get_search"),
            limit=self._meta.limit, max_limit=self._meta.max_limit,
            collection_name=self._meta.collection_name)
        to_be_serialized = paginator.page()
        to_be_serialized['meta']['search_terms'] = search_terms

        # Dehydrate the bundles in preparation for serialization.
        bundles = []

        for obj in to_be_serialized[self._meta.collection_name]:
            bundle = self.build_bundle(obj=obj, request=request)
            bundles.append(self.full_dehydrate(bundle, for_list=True))

        to_be_serialized[self._meta.collection_name] = bundles
        to_be_serialized = self.alter_list_data_to_serialize(request, to_be_serialized)
        self.log_throttled_access(request)
        logger.debug("to_be_serialized: FOUND %r" % to_be_serialized)
        return self.create_response(request, to_be_serialized)

