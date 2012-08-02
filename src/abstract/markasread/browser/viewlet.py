# -*- coding: utf-8 -*-
from zope.component import getUtility
from plone.registry.interfaces import IRegistry
from plone.app.layout.viewlets import ViewletBase
from Products.CMFCore.utils import getToolByName
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from ..interfaces import IMarkAsReadForm
from ..interfaces import IMarkAsReadAnnotatableAdapter


class MarkAsReadViewlet(ViewletBase):

    index = ViewPageTemplateFile("templates/markasread.pt")

    @property
    def portal_membership(self):
        return getToolByName(self.context, 'portal_membership')

    @property
    def settings(self):
        settings = getUtility(IRegistry).forInterface(IMarkAsReadForm, False)
        return settings

    @property
    def text(self):
        return self.settings.text

    @property
    def allowed_types(self):
        return self.settings.allowed_types

    def getCurrentUser(self):
        """return current user"""
        pm = self.portal_membership
        current_user = pm.getAuthenticatedMember()
        return current_user

    def getCurrentUID(self):
        return self.context.UID()

    def is_available(self):
        """Viewlet is available if
        1. current user is Authenticated
        2. if current object type is in allowed_types registry
        """
        current_user = self.getCurrentUser()
        if 'Authenticated' not in current_user.getRoles():
            return False
        portal_type = getattr(self.context, 'portal_type', None)
        allowed_types = list(self.settings.allowed_types)
        # XXX: remove Folder type from allowed types
        # it has not sense to "mark as read" folders
        if 'Folder' in allowed_types:
            allowed_types.remove('Folder')
        if portal_type not in allowed_types:
            return False
        return True

    def IsReadedByUser(self):
        current_user = self.getCurrentUser()
        userid = current_user.getProperty('id')
        adapted = IMarkAsReadAnnotatableAdapter(self.context)
        is_read = adapted.IsReadedByUser(userid)
        return is_read
