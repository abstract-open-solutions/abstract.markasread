from Products.CMFCore.utils import getToolByName
from Products.Five.browser import BrowserView

from ..interfaces import IStorage


class ListReadUsers(BrowserView):
    """Read users listing on context"""

    @property
    def portal_membership(self):
        return getToolByName(self.context, 'portal_membership')

    @property
    def adapted(self):
        adapted = IStorage(self.context)
        return adapted

    def getReadUsers(self):
        """list read users"""
        read_users = self.adapted.getAnnotation()
        results = []
        for ru in read_users:
            member = self.portal_membership.getMemberById(ru)
            if member:
                results.append(
                    {
                        'userid': member.getProperty('id'),
                        'fullname': member.getProperty('fullname'),
                    }
                )
        return results
