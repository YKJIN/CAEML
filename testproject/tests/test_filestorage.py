__copyright__ = "Copyright 2017 Renumics GmbH (http://www.renumics.com)"
import unittest

import testproject.tests.base
from caeml.files.storage import FileStorage


class TestFileStorage(testproject.tests.base.CAEMLTestCase):
    def setUp(self):
        self.filestorage = FileStorage("")
        self.filestorage.resetBaseLocationToNewSub('TestFileStorage')
        content = "asdasdasd"
        with open(self.filestorage.path('test_setup.yml'), 'w') as test_file:
            test_file.write(content)

    def test_exists(self):
        self.assertTrue(self.filestorage.exists("test_setup.yml"))
        self.assertFalse(self.filestorage.exists("not_test.yml"))

    def test_ls(self):
        self.assertEqual(1, len(self.filestorage.ls()))
        self.assertEqual(1, len(self.filestorage.ls(ext=".yml")))
        self.assertEqual(0, len(self.filestorage.ls(ext=".yaml")))

    def test_load(self):
        with open(self.filestorage.path('test_setup.yml')) as test_file:
            content = test_file.read()
        self.assertEqual(content, "asdasdasd")

    def test_load_save(self):
        with open(self.filestorage.path('test_setup.yml')) as test_file:
            content = test_file.read()

        with open(self.filestorage.path('test_setup_copy.yml'), 'w') as test_file:
            test_file.write(content)

        with open(self.filestorage.path('test_setup_copy.yml')) as test_file:
            content_new = test_file.read()

        self.assertEqual(content, content_new)

    def test_save_override(self):
        with open(self.filestorage.path('test_setup.yml')) as test_file:
            content = test_file.read()

        with open(self.filestorage.path('test_setup_copy.yml'), 'w') as test_file:
            test_file.write(content + "asd")

        with open(self.filestorage.path('test_setup_copy.yml')) as test_file:
            content_new = test_file.read()

        self.assertEqual(content + "asd", content_new)


if __name__ == '__main__':
    unittest.main()
