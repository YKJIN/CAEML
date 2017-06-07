__copyright__ = "Copyright 2017 Renumics GmbH (http://www.renumics.com)"
import logging
import os

from caeml.management.base import BaseCommand
from caeml.management.conf import settings


class Command(BaseCommand):
    help = "Deletes all data on disk and all log files"

    def execute(self, argv):

        response = input('THIS WILL PURGE ALL YOUR CAEML DATA: TYPE \"YES\" IF YOU ARE SURE!')

        if response == 'YES':

            # delete data dir
            fullDir = os.path.join(settings.DATA_DIR, settings.FILES_DIR_SUFFIX)
            if os.path.isdir(fullDir):
                import shutil
                shutil.rmtree(fullDir)

            # delete logging data
            logging_handlers = settings.LOGGING['handlers']
            for name, handler in logging_handlers.items():
                path = handler.get('filename', None)
                if path:
                    os.remove(path)

            logging.getLogger('init').info("Data deleted.")

        else:
            logging.getLogger('init').info("Data delete aborted.")
