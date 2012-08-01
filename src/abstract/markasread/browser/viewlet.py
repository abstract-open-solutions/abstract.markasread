# -*- coding: utf-8 -*-
from zope.component import getUtility
from plone.registry.interfaces import IRegistry
from plone.app.layout.viewlets import ViewletBase
from Products.CMFCore.utils import getToolByName
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from ..interfaces import IMarkAsReadForm
from ..interfaces import IMarkAsReadAnnotatableUtility


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

    @property
    def utility(self):
        utility = getUtility(IMarkAsReadAnnotatableUtility,
            name="abstract.markasread_annotations")
        return utility

    def is_available(self):
        """Viewlet is available if
        1. current user is Authenticated
        2. if current object type is in allowed_types registry
        """
        current_user = self.getCurrentUser()
        if 'Authenticated' not in current_user.getRoles():
            return False

        if self.allowed_types is not None:
            portal_type = getattr(self.context, 'portal_type', None)
            if portal_type in self.allowed_types:
                return True
        return False

    def IsReadedByUser(self):
        current_user = self.getCurrentUser()
        userid = current_user.getProperty('id', '')
        is_read = self.utility.IsReadedByUser(userid, self.context)
        return is_read
