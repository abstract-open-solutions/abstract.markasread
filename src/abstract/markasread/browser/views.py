from Products.CMFCore.utils import getToolByName
from Products.Five.browser import BrowserView

from ..interfaces import IStorage


class UsersList(BrowserView):

    def get_users(self):
        """Return a list of users who have already read the content
        """
        pm = getToolByName(self.context, 'portal_membership')
        storage = IStorage(self.context)
        results = []
        for usr in storage:
            member = pm.getMemberById(usr)
            if member:
                results.append(
                    {
                        'userid': member.getProperty('id'),
                        'fullname': member.getProperty('fullname'),
                    }
                )
        return results
