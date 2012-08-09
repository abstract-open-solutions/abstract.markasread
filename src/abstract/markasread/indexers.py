from plone.indexer.decorator import indexer

from .interfaces import IStorage
from .interfaces import IMarkable


@indexer(IMarkable)
def read_users(obj, **kw): # pylint: disable=W0613
    """Returns a list of user IDs that represent
    those that have "marked ``obj`` as read"
    """
    return list(IStorage(obj))
