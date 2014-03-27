""" Additional Haystack Signal Processors

This module provides additional HAYSTACK_SIGNAL_PROCESSOR classes to reindex more effeciently.
They may be tied to various other haystack-related libraries.

They are not tied to `tastypie_search` in any way! Use them anywhere Haystack is installed.
"""
import sys
from django.conf import settings

# TODO: Using "importlib" requires py2.7; find another way.
import inspect
import importlib

from haystack.indexes import SearchIndex
from queued_search.signals import QueuedSignalProcessor

import logging
logger = logging.getLogger(__name__)

def indexed_models():
    """ Use introspection to find haystack's indexed models.
    These models need to trigger `update_index` when the ORM changes them.

    Each application in settings.INSTALLED_APPS must have the module:

        import app.search_indexes

    ... and there must be classes derived from:

        import haystack.indexes.SearchIndex
    """
    models_list = []
    for app in settings.INSTALLED_APPS:
        try:
            # find app.search_indexes modules in each app...
            search_indexes = importlib.import_module('%s.search_indexes' % app)
            search_indexes = [ m for n, m in inspect.getmembers(search_indexes, inspect.isclass) if issubclass(m, SearchIndex) ]
            logger.debug("%s.search_indexes: %r" % (app, search_indexes))
            models_list = [ m().get_model() for m in search_indexes ]
            logger.debug("Indexed Models: %r" %  models_list)
        except ImportError as e:
            pass

    return models_list


class ModelCheckingQueuedSignalProcessor(QueuedSignalProcessor):
    """ This signal processor tells Haystack to queue up only
    the models that have full text indexes.

    Declare this signal processor class in the django.settings as a full path.
    
    HAYSTACK_SIGNAL_PROCESSOR='tastypie_search.signals.ModelCheckingQueuedSignalProcessor'
    """

    def __init__(self, *args, **kwargs):
        super(ModelCheckingQueuedSignalProcessor, self).__init__(*args, **kwargs)
        self._indexed_models = tuple(indexed_models())

    def enqueue_save(self, sender, instance, **kwargs):
        if isinstance(instance, self._indexed_models):
            return self.enqueue('update', instance)

    def enqueue_delete(self, sender, instance, **kwargs):
        if isinstance(instance, self._indexed_models):
            return self.enqueue('delete', instance)

