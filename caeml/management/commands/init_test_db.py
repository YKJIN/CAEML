__copyright__ = "Copyright 2017 Renumics GmbH (http://www.renumics.com)"
import logging

from caeml.management import execute_from_command_line
from caeml.management.base import BaseCommand
from caeml.management.conf import settings


class Command(BaseCommand):
    help = "ATTENTION: DELETES COMPLETE DATA DIR OF DB"

    def execute(self, argv):

        if settings.DATABASE['name'].startswith("test_"):
            execute_from_command_line(['manage.py', 'init_db'])

        else:
            logging.getLogger('init').info(
                "DB %s cannot be initialized, because it does not start with \"test_\"" % (settings.DATABASE['name']))
