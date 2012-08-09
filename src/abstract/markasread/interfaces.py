from zope import schema
from zope.interface import Interface
from zope.location.interfaces import ILocation
from plone.theme.interfaces import IDefaultPloneLayer

from . import MessageFactory as _


class IPreferences(Interface):
    """The preferences
    """

    text = schema.Text(
        title=_(u"Text"),
        description=_(u'A descriptive text that appears'
                      u' on top of the "mark as read" checkbox'),
        required=False
    )

    allowed_types = schema.Tuple(
        title=_(u"Types"),
        description=_(u"The types that can be marked as read"),
        missing_value=tuple(),
        value_type=schema.Choice(
            vocabulary="plone.app.vocabularies.UserFriendlyTypes"
        ),
        required=False
    )


class IMarkForm(Interface):
    read = schema.Bool(
        title=_(u'Have you read this content?'),
        description=_(u'Check this field if you have read this document.'),
        required=True,
        default=False,
    )


class IBrowserLayer(IDefaultPloneLayer):
    """The browser layer of the package
    """


class IMarkable(Interface):
    """Whether the context can be "marked as read"
    """


class IStorage(ILocation):
    """Where the information on "who has read this" is kept.
    """

    def add(userid):
        """Adds the passed ``userid`` to the list of those
        who have read the context
        """

    def remove(userid):
        """Removes ``userid`` from the list of those
        who have read the context.

        Raises ``KeyError`` if ``userid`` is not present in the list.
        """

    def __contains__(userid):
        """Whether ``userid`` is in the list of those who have read.
        """

    def __iter__():
        """Returns an iterator that yields the user IDs
        that have read the context
        """

    def clear():
        """Wipes out all the information contained in the storage.

        Handle with care. Keep away from children below age 30.
        """
