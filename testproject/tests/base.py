__copyright__ = "Copyright 2017 Renumics GmbH (http://www.renumics.com)"
import unittest

import caeml
import testproject.settings
from caeml.management import execute_from_command_line


class CAEMLTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        caeml.init(testproject.settings)
        execute_from_command_line(['manage.py', 'init_logger'])
        execute_from_command_line(['manage.py', 'init_filesystem'])
        execute_from_command_line(['manage.py', 'init_test_db'])
        execute_from_command_line(['manage.py', 'init_tools'])

    @classmethod
    def tearDownClass(self):
        execute_from_command_line(['manage.py', 'remove_test_db'])
