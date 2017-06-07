__copyright__ = "Copyright 2017 Renumics GmbH (http://www.renumics.com)"
from caeml.management.base import ManagementUtilityCall


def execute_from_command_line(argv=None):
    """
    A simple method that runs a ManagementUtilityCall.
    """
    utility = ManagementUtilityCall(argv)
    utility.execute()
