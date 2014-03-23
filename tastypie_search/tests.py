from django.test import TestCase
from django.test.client import Client
from django.core.management import call_command
import json

import logging
logger = logging.getLogger('tastypie_search.searchable')
logger.addHandler(logging.StreamHandler())
logger.setLevel(logging.ERROR)

from tastypie_search.models import (
    USState,
    Capitol
)

HARRISBURG_HISTORY="""
"""

TRENTON_HISTORY="""
"""

class CapitolSearchTest(TestCase):
    @classmethod
    def setUpClass(self):
        self.client = Client()

        self.nj = USState(code='NJ', name='New Jersey')
        self.nj.save()
        self.pa = USState(code='PA', name='Pennsylvania')
        self.pa.save()

        self.harrisburg_pa = Capitol(name='Harrisburg', state=self.pa, history=HARRISBURG_HISTORY)
        self.harrisburg_pa.save()
        self.trenton_nj = Capitol(name='Trenton', state=self.nj, history=TRENTON_HISTORY)
        self.trenton_nj.save()

        # Build the search index.
        ## call_command('rebuild_index', interactive=False)

    def test_states(self):
        self.assertEquals(self.nj.code, 'NJ')
        self.assertEquals(self.nj.pk, 'NJ')
        self.assertEquals(self.pa.code, 'PA')
        self.assertEquals(self.pa.pk, 'PA')

    def rest_field_type_ok(self, json_d, fieldname, type_class):
        """ REST resource must have fieldname related resource
        and it must be type_class data-type.
        """
        if fieldname in json_d:
            return isinstance(json_d[fieldname], type_class)
        else:
            return False

    def test_search(self):
        """ Find search_terms='trenton' in the index """
        resp = self.client.get("/api/v1/capitol/search/?search_terms=trenton")
        d = json.loads(resp.content)
        self.assertIn('search_terms', d['meta'], 'search terms must be in results meta')
        self.assertEquals(d['meta']['search_terms'], 'trenton')
        d = d['objects'][0] # read the first, & hopefully only, capitol city.
        self.assertTrue(self.rest_field_type_ok(d, 'name', basestring), 'name required')
        self.assertTrue(self.rest_field_type_ok(d, 'history', basestring), 'history required')
        self.assertTrue(self.rest_field_type_ok(d, 'state', dict), 'full state required')
        self.assertEquals(d['state'], {
            u'resource_uri': u'/api/v1/us_state/NJ/',
            u'code': u'NJ',
            u'name': u'New Jersey',
        })

    def test_no_search_terms(self):
        """ Show that no search_terms='' matches nothing in the index """
        resp = self.client.get("/api/v1/capitol/search/?search_terms=")
        d = json.loads(resp.content)
        self.assertIn('search_terms', d['meta'], 'search_terms must be in results meta')
        self.assertEquals(d['meta']['search_terms'], '')
        # objects list must be empty.
        self.assertEquals(d['objects'], [])

    def test_search_terms_missing(self):
        """ When "search_terms" parameter is missing, no results match the index """
        resp = self.client.get("/api/v1/capitol/search/?hello=1")
        d = json.loads(resp.content)
        self.assertIn('search_terms', d['meta'], 'search_terms must be empty string in results meta')
        self.assertEquals(d['meta']['search_terms'], '')
        # objects list must be empty.
        self.assertEquals(d['objects'], [])

