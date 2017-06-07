__copyright__ = "Copyright 2017 Renumics GmbH (http://www.renumics.com)"
import logging
import os

from caeml.management.base import BaseCommand
from caeml.management.conf import settings


class Command(BaseCommand):
    help = "Creates folders on file system for caeml file storage"

    def execute(self, argv):
        logger = logging.getLogger('init')
        # create db data if not present
        if not os.path.isdir(settings.DATA_DIR):
            logger.info("DATA_DIR: {} is not present and will be created".format(settings.DATA_DIR))
            os.makedirs(settings.DATA_DIR)

        fullDir = os.path.join(settings.DATA_DIR, settings.DB_DIR_SUFFIX)
        if not os.path.isdir(fullDir):
            logger.info("DB_DIR_SUFFIX: {} is not present and will be created".format(fullDir))
            os.makedirs(fullDir)

        fullDir = os.path.join(settings.DATA_DIR, settings.FILES_DIR_SUFFIX)
        if not os.path.isdir(fullDir):
            logger.info("FILES_DIR_SUFFIX: {} is not present and will be created".format(fullDir))
            os.makedirs(fullDir)
