from zope import schema
from zope.interface import Interface
from plone.theme.interfaces import IDefaultPloneLayer
from zope.annotation.interfaces import IAttributeAnnotatable

from abstract.markasread import MessageFactory as _


class IAbstractMarkAsReadLayer(IDefaultPloneLayer):
    """Marker interface that defines a Zope 3 browser layer.
    """


class IMarkAsReadForm(Interface):
    """ The view for Mark as read  prefs form. """

    text = schema.TextLine(
            title=_('text_label', u"Mark as read text"),
            description=_('text_description',
                 u"Insert text for users."),
            required=False,
        )

    allowed_types = schema.Tuple(title=_(u'Portal types'),
          description=_(u'Portal types mark as read viewlet may be attached to.'),
          missing_value=tuple(),
          value_type=schema.Choice(
                   vocabulary="plone.app.vocabularies.UserFriendlyTypes"),
          required=False)


class IMarkAsReadAttributeAnnotatable(IAttributeAnnotatable):
    """ IAttributeAnnotatable Marker interface """


class IMarkAsReadAnnotatableAdapter(Interface):
    """ Utility Interface """
    
    def checkMarkAsReadAttributeAnnotatableObject():
        """ check if annotatable """

    def makeAnnotation():
        """annotating method"""

    def removeAnnotation():
        """remove userid from read users annotation on obj"""
        
    def resetAnnotation():
        """deleting annotations method"""

    def getAnnotation():
        """get annotations by name"""

    def IsReadedByUser():
        """check if userid is in annotation for obj"""
    