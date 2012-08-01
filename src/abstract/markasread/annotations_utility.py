#-*- coding:utf-8 -*-
from zope.component import getUtility
from zope.interface import implements
from zope.annotation.interfaces import IAnnotations
from plone.registry.interfaces import IRegistry

from .interfaces import IMarkAsReadAnnotatableUtility
from .interfaces import IMarkAsReadAttributeAnnotatable
from .interfaces import IMarkAsReadForm


class MarkAsReadAnnotatableUtility(object):
    """ class utility """
    implements(IMarkAsReadAnnotatableUtility)

    @property
    def settings(self):
        settings = getUtility(IRegistry).forInterface(IMarkAsReadForm, False)
        return settings
        
    def checkMarkAsReadAttributeAnnotatableObject(self, obj=None):
        """ docstring """
        is_annotatable = IMarkAsReadAttributeAnnotatable.providedBy(obj)
        if is_annotatable and (self.settings.allowed_types is not None):
            portal_type = getattr(obj, 'portal_type', None)
            if portal_type in self.settings.allowed_types:
                return True
        return False

    def makeAnnotation(self, userid='', obj=None):
        """annotating method"""
        ## make annotation
        if self.checkMarkAsReadAttributeAnnotatableObject(obj):
            obj_annotated = IAnnotations(obj)
            if userid:
                if obj_annotated.get('read_users', None):
                    if userid not in obj_annotated['read_users']:
                        obj_annotated['read_users'].append(userid)
                else:
                    obj_annotated['read_users'] = [userid,]
            obj.reindexObject()
        else:
            obj_annotated = obj
        return obj_annotated

    def removeAnnotation(self, userid='', obj=None):
        """remove userid from read users annotation on obj"""
        if self.checkMarkAsReadAttributeAnnotatableObject(obj):
            obj_annotated = IAnnotations(obj)
            if hasattr(obj_annotated, 'read_users') and \
                                (userid in obj_annotated['read_users']):
                obj_annotated['read_users'].remove(userid)
                obj.reindexObject()
        else:
            obj_annotated = obj
        return obj_annotated
        
    def resetAnnotation(self, obj=None):
        """deleting annotations method"""
        if self.checkMarkAsReadAttributeAnnotatableObject(obj):
            obj_annotated = IAnnotations(obj)
            obj_annotated['read_users'] = []
            obj.reindexObject()
        else:
            obj_annotated = obj
        return obj_annotated

    def getAnnotation(self, obj=None):
        """get annotations by name"""
        if self.checkMarkAsReadAttributeAnnotatableObject(obj):
            obj_annotated = IAnnotations(obj)
            value = obj_annotated.get('read_users', [])
        else:
            value = []
        return value

    def IsReadedByUser(self, userid='', obj=None):
        """check if userid is in annotation for obj"""
        read_users = self.getAnnotation(obj)
        return userid in read_users
