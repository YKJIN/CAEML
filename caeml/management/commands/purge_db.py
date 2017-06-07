__copyright__ = "Copyright 2017 Renumics GmbH (http://www.renumics.com)"
import logging
import os
import shutil

from caeml.management.base import BaseCommand
from caeml.management.conf import settings


class Command(BaseCommand):
    help = "ATTENTION: DELETES COMPLETE DATA DIR OF DB"

    def execute(self, argv):
        # from pymongo import MongoClient
        # client = MongoClient(
        #     settings.DATABASE['host'], settings.DATABASE['port'])
        # client.drop_database(settings.DATABASE['name'])

        response = input('THIS WILL PURGE ALL YOUR DB DATA: TYPE \"YES\" IF YOU ARE SURE!')

        if response == 'YES':
            # kill docker container

            command = "docker rm -f %s" % (settings.DATABASE['container_name'])
            os.system(command)

            # delete db dir
            fullDir = os.path.join(settings.DATA_DIR, settings.DB_DIR_SUFFIX)
            if os.path.isdir(fullDir):
                shutil.rmtree(fullDir)

            logging.getLogger('init').info("Database wiped.")

        else:
            logging.getLogger('init').info("Database wipe aborted.")
