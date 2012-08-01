from zope.interface import implements
from zope.component import adapts
from zope.component import getUtility
from zope.component import getMultiAdapter
from zope.event import notify
from zope.formlib import form

from plone.registry.interfaces import IRegistry
from plone.protect import CheckAuthenticator
from plone.app.form.validators import null_validator
from plone.app.controlpanel.form import ControlPanelForm
from plone.app.controlpanel.events import ConfigurationChangedEvent

from Products.CMFDefault.formlib.schema import SchemaAdapterBase
from Products.CMFPlone.interfaces import IPloneSiteRoot
from Products.statusmessages.interfaces import IStatusMessage
from Products.CMFPlone import PloneMessageFactory as _p

from abstract.markasread import MessageFactory as _
from abstract.markasread.interfaces import IMarkAsReadForm


class MarkAsReadControlPanelAdapter(SchemaAdapterBase):
    """ Control Panel adapter """

    adapts(IPloneSiteRoot)
    implements(IMarkAsReadForm)

    def __init__(self, context):
        super(MarkAsReadControlPanelAdapter, self).__init__(context)
        self.settings = getUtility(IRegistry).forInterface(IMarkAsReadForm, False)
        self.context = context

    def get_text(self):
        return self.settings.text

    def set_text(self, text):
        self.settings.text = text

    text = property(get_text, set_text)
    
    def get_allowed_types(self):
        if self.settings.allowed_types:
            return self.settings.allowed_types
        return []

    def set_allowed_types(self, allowed_types):
        self.settings.allowed_types = allowed_types

    allowed_types = property(get_allowed_types, set_allowed_types)


class MarkAsReadForm(ControlPanelForm):
    """ The view class for the mark as read preferences form. """

    implements(IMarkAsReadForm)
    form_fields = form.FormFields(IMarkAsReadForm)

    label = _(u'Mark As Read Settings Form')
    description = _(u'Select properties for Mark As Read')
    form_name = _(u'Mark As Read Settings')

    @form.action(_p(u'label_save', default=u'Save'), name=u'save')
    def handle_edit_action(self, action, data):
        CheckAuthenticator(self.request)
        if form.applyChanges(self.context, self.form_fields, data,
                             self.adapters):
            self.status = _p("Changes saved.")
            notify(ConfigurationChangedEvent(self, data))
            self._on_save(data)
        else:
            self.status = _p("No changes made.")

    @form.action(_p(u'label_cancel', default=u'Cancel'),
                 validator=null_validator,
                 name=u'cancel')
    def handle_cancel_action(self, action, data):
        IStatusMessage(self.request).addStatusMessage(_p("Changes canceled."),
                                                      type="info")
        url = getMultiAdapter((self.context, self.request),
                              name='absolute_url')()
        self.request.response.redirect(url + '/plone_control_panel')
        return ''
