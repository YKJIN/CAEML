__copyright__ = "Copyright 2017 Renumics GmbH (http://www.renumics.com)"
import caeml.management.conf.base
from caeml.management import execute_from_command_line


def init(settings_mod):
    """

    caeml init takes care of all initialization and needs to be called before other caeml modules are imported
    :param settings_mod: include path of local settings.py
    :return:
    """

    from caeml.management.conf import settings
    settings.configure(settings_mod)
