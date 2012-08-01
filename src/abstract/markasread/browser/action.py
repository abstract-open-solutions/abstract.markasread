from Products.CMFCore.utils import getToolByName
from Products.Five.browser import BrowserView

from ..interfaces import IMarkAsReadAnnotatableAdapter
from .. import MessageFactory as _


class MarkAsReadAction(BrowserView):
    """Annotate object as read by current user"""

    @property
    def catalog(self):
        return getToolByName(self.context, 'portal_catalog')

    def __call__(self):
        """make annotation action"""
        read = self.request.get('read', '')
        userid = self.request.get('userid', '')
        uid = self.request.get('uid', '')

        return_url = self.context.absolute_url()
        if not read:
            message = _(u"You have to selct checkbox")
        else:
            brain = self.catalog.searchResults(UID=uid)
            if brain:
                brain = brain[0]
                obj = brain.getObject()
                if userid:
                    adapted = IMarkAsReadAnnotatableAdapter(obj)
                    adapted.makeAnnotation(userid)
                    message = _(u"You have read this object")
                    return_url = obj.absolute_url()
                else:
                    message = _(u"Error! No user specified")
            else:
                message = _(u"Error! No object to read")

        self.context.plone_utils.addPortalMessage(message)
        return self.request.response.redirect(return_url)
