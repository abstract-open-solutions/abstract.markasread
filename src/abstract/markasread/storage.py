from zope.component import adapts
from BTrees.OIBTree import OISet
from zope.interface import implements
from zope.annotation import factory

from .interfaces import IStorage
from .interfaces import IMarkable


class Storage(OISet):
    """Where the information on "who has read this" is kept.
    """

    implements(IStorage)
    adapts(IMarkable)

    def add(self, userid):
        super(Storage, self).add(userid)
        self.__parent__.reindexObject()

    def remove(self, userid):
        super(Storage, self).remove(userid)
        self.__parent__.reindexObject()


AnnotatedStorage = factory(Storage)
