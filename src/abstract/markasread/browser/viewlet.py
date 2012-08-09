# -*- coding: utf-8 -*-
from zope.component import getUtility, getMultiAdapter
from plone.registry.interfaces import IRegistry
from plone.app.layout.viewlets import ViewletBase
from plone.memoize.instance import memoizedproperty
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from ..interfaces import IStorage
from ..interfaces import IPreferences
from ..utils import get_current_user


class Viewlet(ViewletBase):

    index = ViewPageTemplateFile("templates/viewlet.pt")

    @memoizedproperty
    def settings(self):
        settings = getUtility(IRegistry).forInterface(IPreferences)
        return settings

    def is_visible(self):
        """Whether to show the viewlet or not.

        Returns ``True`` if the current user is authenticated
        and the context is within the list of content types
        that are set to support this behavior
        (``allowed_types`` in the preferences),
        ``False`` otherwise.
        """
        ps = getMultiAdapter(
            (self.context, self.request),
            name="plone_portal_state"
        )
        if ps.anonymous:
            return False
        if self.context.portal_type not in self.settings.allowed_types:
            return False
        return True

    def is_read(self):
        """Whether the current user has already read this content.

        Returns ``True`` if this is the case,
        ``False`` otherwise
        """
        current_user = get_current_user(self.context)
        storage = IStorage(self.context)
        return current_user.getProperty('id') in storage
