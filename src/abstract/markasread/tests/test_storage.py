import unittest
from plone.app.testing import TEST_USER_ID
from ..interfaces import IStorage
from ..testing import ABSTRACT_MARKASREAD_FUNCTIONAL_TESTING


class StorageTest(unittest.TestCase):

    layer = ABSTRACT_MARKASREAD_FUNCTIONAL_TESTING

    def test_storage(self):
        page = self.layer['portal']['testpage']
        storage = IStorage(page)
        self.assertTrue(IStorage.providedBy(storage))

    def test_add_remove(self):
        page = self.layer['portal']['testpage']
        storage = IStorage(page)
        self.assertTrue(TEST_USER_ID not in storage)
        storage.add(TEST_USER_ID)
        self.assertTrue(TEST_USER_ID in storage)
        storage.remove(TEST_USER_ID)
        self.assertTrue(TEST_USER_ID not in storage)
        storage.clear()

    def test_iter(self):
        page = self.layer['portal']['testpage']
        storage = IStorage(page)
        for id in ['spam', 'eggs', 'spam']:
            storage.add(id)
        ids = [ id for id in storage ]
        self.assertEqual(
            ['eggs', 'spam'],
            ids
        )
        storage.clear()

    def test_contains(self):
        page = self.layer['portal']['testpage']
        storage = IStorage(page)
        storage.add(TEST_USER_ID)
        self.assertTrue(TEST_USER_ID in storage)
        self.assertTrue('spam' not in storage)
        storage.clear()

