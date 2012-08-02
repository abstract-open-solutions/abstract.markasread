#-*- coding:utf-8 -*-
from BTrees.OIBTree import OISet
from zope.component import getUtility
from zope.interface import implements
from zope.annotation.interfaces import IAnnotations
from plone.registry.interfaces import IRegistry

from .interfaces import IMarkAsReadAnnotatableAdapter
from .interfaces import IMarkAsReadAttributeAnnotatable
from .interfaces import IMarkAsReadForm


class MarkAsReadAnnotatableAdapter(object):
    """ class utility """
    implements(IMarkAsReadAnnotatableAdapter)

    def __init__(self, context):
        """Initialize our adapter"""
        self.context = context

    @property
    def settings(self):
        settings = getUtility(IRegistry).forInterface(IMarkAsReadForm, False)
        return settings

    def checkMarkAsReadAttributeAnnotatableObject(self):
        """ check if current object is annotatable for mark as read feature """
        return IMarkAsReadAttributeAnnotatable.providedBy(self.context)

    def makeAnnotation(self, userid):
        """annotating method"""
        ## make annotation
        if self.checkMarkAsReadAttributeAnnotatableObject():
            obj_annotated = IAnnotations(self.context)
            if not obj_annotated.get('read_users', None):
                obj_annotated['read_users'] = OISet()
            obj_annotated['read_users'].add(userid)
            self.context.reindexObject()

    def removeAnnotation(self, userid):
        """remove userid from read users annotation on obj"""
        if self.checkMarkAsReadAttributeAnnotatableObject():
            obj_annotated = IAnnotations(self.context)
            if obj_annotated.get('read_users', None) and \
                                (userid in obj_annotated['read_users']):
                obj_annotated['read_users'].remove(userid)
                self.context.reindexObject()

    def resetAnnotation(self):
        """deleting annotations method"""
        if self.checkMarkAsReadAttributeAnnotatableObject():
            obj_annotated = IAnnotations(self.context)
            obj_annotated['read_users'] = OISet()
            self.context.reindexObject()
        else:
            obj_annotated = self.context
        return obj_annotated

    def getAnnotation(self):
        """get annotations by name"""
        if self.checkMarkAsReadAttributeAnnotatableObject():
            obj_annotated = IAnnotations(self.context)
            value = obj_annotated.get('read_users', [])
        else:
            value = []
        return value

    def IsReadedByUser(self, userid):
        """check if userid is in annotation for obj"""
        read_users = self.getAnnotation()
        return userid in read_users
