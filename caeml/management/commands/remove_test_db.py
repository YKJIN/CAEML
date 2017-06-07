__copyright__ = "Copyright 2017 Renumics GmbH (http://www.renumics.com)"
import logging

from caeml.management.base import BaseCommand
from caeml.management.conf import settings


class Command(BaseCommand):
    help = "ATTENTION: DELETES COMPLETE DATA DIR OF DB"

    def execute(self, argv):

        if settings.DATABASE['name'].startswith("test_"):
            from pymongo import MongoClient
            client = MongoClient(
                settings.DATABASE['host'], settings.DATABASE['port'])
            client.drop_database(settings.DATABASE['name'])
            logging.getLogger('init').info("Test db %s deleted" % (settings.DATABASE['name']))

        else:
            logging.getLogger('init').info(
                "DB %s cannot be deleted, because it does not start with \"test_\"" % (settings.DATABASE['name']))
