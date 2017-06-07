__copyright__ = "Copyright 2017 Renumics GmbH (http://www.renumics.com)"
"""
Settings and configuration for CAEML.

There are two possibilities to supply local settings two the system:
1. Set the env variable CAEML_SETTINGS_MODULE
2. Call caeml from a directory that is a python module (has__init__.py), whose parent directory is
 in the Python path and that has a settings file

If no local settings can be found, the global default settings are used.

"""

import importlib
import os

ENVIRONMENT_VARIABLE = "CAEML_SETTINGS_MODULE"


class Settings(object):
    def __init__(self, local_mod=None):
        # load global settings first

        global_mod = importlib.import_module(
            'caeml.management.conf.global_settings')

        for setting in dir(global_mod):
            if setting.isupper():
                setattr(self, setting, getattr(global_mod, setting))

        if local_mod is None:
            settings_module = os.environ.get(ENVIRONMENT_VARIABLE)

            # try to load module
            local_settings_module_loaded = False
            try:
                local_mod = importlib.import_module(settings_module)
                local_settings_module_loaded = True
            except Exception:
                pass
        else:
            local_settings_module_loaded = True

        if not local_settings_module_loaded:
            raise Exception(
                "Warning: Local settings could not be retrieved from environment variable CAEML_SETTINGS_MODULE, trying global settings!")

        if local_settings_module_loaded:
            for setting in dir(local_mod):
                if setting.isupper():
                    setattr(self, setting, getattr(local_mod, setting))
                    # TODO : make sure BASE_DIR is was assigned; is BASE_DIR the only setting not available from global settings?


class LazySettings(object):
    def __init__(self):
        self._wrapped = None

    def configure(self, local_mod=None):
        self._wrapped = Settings(local_mod)

    def __getattr__(self, name):
        if self._wrapped is None:
            raise LookupError("Settings need to be configured before they are used")
        return getattr(self._wrapped, name)

    @property
    def configured(self):
        return self._wrapped is not None
