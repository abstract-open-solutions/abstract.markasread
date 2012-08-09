from Products.CMFCore.utils import getToolByName


def get_current_user(context):
    pm = getToolByName(context, 'portal_membership')
    return pm.getAuthenticatedMember()
