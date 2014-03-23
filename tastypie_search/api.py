from tastypie.resources import ModelResource
from tastypie import fields

from tastypie_search.searchable import SearchableResourceMixin

from tastypie_search.models import USState, Capitol

import logging

class USStateResource(ModelResource):
    class Meta:
        queryset = USState.objects.all()
        resource_name = 'us_state'
        allowed_methods = ['get']

class CapitolResource(SearchableResourceMixin, ModelResource):
    state = fields.ToOneField(USStateResource, 'state', full=True)

    class Meta:
        queryset = Capitol.objects.all()
        limit = 10
        resource_name = 'capitol'
        allowed_methods = ['get']

