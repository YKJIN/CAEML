__copyright__ = "Copyright 2017 Renumics GmbH (http://www.renumics.com)"
import os
from logging.config import dictConfig

from caeml.management.base import BaseCommand
from caeml.management.conf import settings


class Command(BaseCommand):
    help = "Initializes Logger from settings files"

    def execute(self, argv):
        # create logging directories
        logging_handlers = settings.LOGGING['handlers']
        for name, handler in logging_handlers.items():
            path = handler.get('filename', None)
            if path is not None:
                path = os.path.dirname(path)
                if not os.path.isdir(path):
                    os.makedirs(path)
        dictConfig(settings.LOGGING)
        import logging
        logging.getLogger('init').info("Logging initialized")
