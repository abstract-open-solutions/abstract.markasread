from plone.indexer.decorator import indexer

from .interfaces import IMarkAsReadAnnotatableAdapter
from .interfaces import IMarkAsReadAttributeAnnotatable

from logging import getLogger
logger = getLogger('abstract.markasread - indexer')


@indexer(IMarkAsReadAttributeAnnotatable)
def read_users(obj, **kw):
    """id into old db"""
    adapted = IMarkAsReadAnnotatableAdapter(obj)
    ret = adapted.getAnnotation()
    return ret
