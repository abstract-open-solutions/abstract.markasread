from plone.indexer.decorator import indexer
from zope.component import getUtility

from .interfaces import IMarkAsReadAnnotatableUtility
from .interfaces import IMarkAsReadAttributeAnnotatable

from logging import getLogger
logger = getLogger('abstract.markasread - indexer')


@indexer(IMarkAsReadAttributeAnnotatable)
def read_users(obj, **kw):
    """id into old db"""
    utility = getUtility(
        IMarkAsReadAnnotatableUtility, name="abstract.markasread_annotations")
    ret = utility.getAnnotation(obj)
    return ret
