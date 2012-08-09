from zope.component import adapts
from persistent import Persistent
from BTrees.OIBTree import OISet
from zope.interface import implements
from zope.annotation import factory

from .interfaces import IStorage
from .interfaces import IMarkable


def reindex(meth, context):
    def wrapper(*args, **kwargs):
        result = meth(*args, **kwargs)
        context.reindexObject()
        return result
    return wrapper


class Storage(Persistent):
    """Where the information on "who has read this" is kept.
    """

    implements(IStorage)
    adapts(IMarkable)

    def __init__(self):
        super(Storage, self).__init__()
        self._data = OISet()
        self.__parent__ = None
        self.__name__ = None

    def __getattr__(self, name):
        if name is ('add', 'remove', 'clear'):
            return reindex(getattr(self._data, name), self.__parent__)
        return getattr(self._data, name)

    # This needs to be present because __dict__ is checked by iter() and friends
    def __iter__(self):
        return iter(self._data)


AnnotatedStorage = factory(Storage)
