__copyright__ = "Copyright 2017 Renumics GmbH (http://www.renumics.com)"
"""
Performs test for the settings mechanism
"""

import os
import unittest


class SettingsTestCase(unittest.TestCase):  # dont use caeml test here (it wraps settings)

    def setUp(self):
        self._settings_backup = os.environ.get("CAEML_SETTINGS_MODULE")
        self._working_dir_backup = os.getcwd()
        if os.environ.get("CAEML_SETTINGS_MODULE") is not None:
            del os.environ["CAEML_SETTINGS_MODULE"]

    def test_one(self):
        """
        Emulate settings call without setting env variable or calling from directory with settings
        :return:
        """
        if os.environ.get("CAEML_SETTINGS_MODULE") is not None:
            del os.environ["CAEML_SETTINGS_MODULE"]
        self.assertRaises(Exception)  # TODO: why? this is lazy evaluated!?

    def doCleanups(self):
        os.chdir(self._working_dir_backup)
        if self._settings_backup is not None:
            os.environ.setdefault(
                "CAEML_SETTINGS_MODULE",
                self._settings_backup)
        else:
            if os.environ.get("CAEML_SETTINGS_MODULE") is not None:
                del os.environ["CAEML_SETTINGS_MODULE"]

    def test_two(self):
        """
        Emulate settings call with env variable
        :return:
        """
        from caeml.management.conf import settings
        settings._wrapped = None
        os.environ.setdefault(
            "CAEML_SETTINGS_MODULE",
            'testproject.settings')
        from caeml.management.conf import settings
        # configure settings with none
        settings.configure()
        val = settings.SETTINGS_TEST
        self.assertTrue(val)
