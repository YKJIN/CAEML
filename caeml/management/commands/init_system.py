__copyright__ = "Copyright 2017 Renumics GmbH (http://www.renumics.com)"
from caeml.management import execute_from_command_line
from caeml.management.base import BaseCommand


class Command(BaseCommand):
    help = "Initialized complete CAEML system"

    def execute(self, argv):
        execute_from_command_line(['manage.py', 'init_logger'])
        execute_from_command_line(['manage.py', 'init_filesystem'])
        execute_from_command_line(['manage.py', 'init_db'])
        # execute_from_command_line(['manage.py', 'init_tools'])
        # execute_from_command_line(['manage.py', 'init_api'])
