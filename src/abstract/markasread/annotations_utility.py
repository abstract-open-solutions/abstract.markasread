#-*- coding:utf-8 -*-
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
        """ docstring """
        return IMarkAsReadAttributeAnnotatable.providedBy(self.context)

    def makeAnnotation(self, userid):
        """annotating method"""
        ## make annotation
        if self.checkMarkAsReadAttributeAnnotatableObject():
            obj_annotated = IAnnotations(self.context)
            if obj_annotated.get('read_users', None):
                if userid not in obj_annotated['read_users']:
                    obj_annotated['read_users'].append(userid)
            else:
                obj_annotated['read_users'] = [userid,]
            self.context.reindexObject()
        else:
            obj_annotated = self.context
        return obj_annotated

    def removeAnnotation(self, userid):
        """remove userid from read users annotation on obj"""
        if self.checkMarkAsReadAttributeAnnotatableObject():
            obj_annotated = IAnnotations(self.context)
            if obj_annotated.get('read_users', None) and \
                                (userid in obj_annotated['read_users']):
                obj_annotated['read_users'].remove(userid)
                self.context.reindexObject()
        else:
            obj_annotated = self.context
        return obj_annotated
        
    def resetAnnotation(self):
        """deleting annotations method"""
        if self.checkMarkAsReadAttributeAnnotatableObject():
            obj_annotated = IAnnotations(self.context)
            obj_annotated['read_users'] = []
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
