import unittest2 as unittest
from zope.component import getUtility
from plone.registry.interfaces import IRegistry
from Products.CMFCore.utils import getToolByName

from ..testing import ABSTRACT_MARKASREAD_INTEGRATION_TESTING
from ..interfaces import IPreferences


class TestSetup(unittest.TestCase):

    layer = ABSTRACT_MARKASREAD_INTEGRATION_TESTING

    def setUp(self):
        self.app = self.layer['app']
        self.portal = self.layer['portal']
        self.qi_tool = getToolByName(self.portal, 'portal_quickinstaller')

    def test_product_is_installed(self):
        """Validate that our products GS profile has been run and the product
            installed
        """
        pid = 'abstract.markasread'
        installed = [p['id'] for p in self.qi_tool.listInstalledProducts()]
        self.assertTrue(pid in installed,
                        'package appears not to have been installed')

    def test_preferences(self):
        prefs = getUtility(IRegistry).forInterface(IPreferences)
        self.assertEqual(prefs.text, None)
        self.assertEqual(prefs.allowed_types, None)
