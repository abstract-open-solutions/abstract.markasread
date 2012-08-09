from plone.app.registry.browser import controlpanel

from ..interfaces import IPreferences
from .. import MessageFactory as _


class ControlpanelForm(controlpanel.RegistryEditForm):
    schema = IPreferences
    label = _(u'Mark As Read Settings Form')

    def updateFields(self):
        super(ControlpanelForm, self).updateFields()

    def updateWidgets(self):
        super(ControlpanelForm, self).updateWidgets()


class Controlpanel(controlpanel.ControlPanelFormWrapper):
    form = ControlpanelForm
