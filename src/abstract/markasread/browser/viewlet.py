# -*- coding: utf-8 -*-
from Acquisition import aq_inner

from zope.interface import implements
from zope.component import getUtility, getMultiAdapter

from z3c.form import form, button, field
from z3c.form.interfaces import IFormLayer
from plone.z3cform import z2

from plone.registry.interfaces import IRegistry
from plone.app.layout.viewlets import ViewletBase
from plone.memoize.instance import memoizedproperty

from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from ..interfaces import IStorage
from ..interfaces import IPreferences
from ..interfaces import IMarkForm
from ..interfaces import IMarkable
from ..utils import get_current_user
from .. import MessageFactory as _


class MarkFormAdapter(object):
    implements(IMarkForm)

    def __init__(self, context):
        self.context = context

    @property
    def member_id(self):
        return get_current_user(self.context).getProperty('id')

    @property
    def storage(self):
        return IStorage(self.context)

    def get_read(self):
        return self.member_id in self.storage

    def set_read(self, value):
        if value:
            self.storage.add(self.member_id)
        else:
            self.storage.remove(self.member_id)

    read = property(get_read, set_read)


class MarkForm(form.Form):
    template = ViewPageTemplateFile("templates/form.pt")
    fields = field.Fields(IMarkForm)
    # ignoreContext = True

    @button.buttonAndHandler(_(u'Save'))
    def handleSave(self, action):
        # pylint: disable=W0613, W0612
        data, errors = self.extractData()
        if errors:
            return

        # TODO: write some message to user
        IMarkForm(self.context).read = data['read']


class Viewlet(ViewletBase):

    index = ViewPageTemplateFile("templates/viewlet.pt")

    @memoizedproperty
    def settings(self):
        settings = getUtility(IRegistry).forInterface(IPreferences)
        return settings

    def update(self):
        super(Viewlet, self).update()
        if self.available():
            z2.switch_on(self, request_layer=IFormLayer)
            self.form = MarkForm(aq_inner(self.context), self.request)
            self.form.update()

    def available(self):
        return IMarkable.providedBy(self.context)

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

        if ps.anonymous():
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
