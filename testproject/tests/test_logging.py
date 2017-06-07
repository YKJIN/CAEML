__copyright__ = "Copyright 2017 Renumics GmbH (http://www.renumics.com)"
import logging
import os

import testproject.tests.base
from caeml.management.conf import settings


class LoggingTestCase(testproject.tests.base.CAEMLTestCase):
    def setUp(self):
        logging_handlers = settings.LOGGING['handlers']
        handler = logging_handlers.get('system_file_handler')
        self.log_dir = os.path.abspath(os.path.dirname(handler['filename']))

    def test_init_logger(self):
        self.assertTrue(
            os.path.isfile(os.path.join(self.log_dir, 'system.log')),
            "system.log file not found")
        self.assertTrue(
            os.path.isfile(os.path.join(self.log_dir, 'process.log')),
            "process.log file not found")
        self.assertTrue(
            os.path.isfile(os.path.join(self.log_dir, 'workflow.log')),
            "workflow.log file not found")
        self.assertTrue(
            os.path.isfile(os.path.join(self.log_dir, 'init.log')),
            "init.log file not found")

    def test_logg(self):
        system_logger = logging.getLogger('system')

        log_str = "System Test Logg String"
        system_logger.debug(log_str)

        with open(os.path.join(self.log_dir, 'system.log')) as log_file:
            last_line = log_file.readlines()[-1]
            self.assertTrue(last_line.endswith(log_str + '\n'))

        process_logger = logging.getLogger('process_data')

        log_str = "System Test Logg String"
        process_logger.debug(log_str)

        with open(os.path.join(self.log_dir, 'process.log')) as log_file:
            last_line = log_file.readlines()[-1]
            self.assertTrue(last_line.endswith(log_str + '\n'))

        workflow_logger = logging.getLogger('workflow')

        log_str = "System Test Logg String"
        workflow_logger.debug(log_str)

        with open(os.path.join(self.log_dir, 'workflow.log')) as log_file:
            last_line = log_file.readlines()[-1]
            self.assertTrue(last_line.endswith(log_str + '\n'))

        init_logger = logging.getLogger('init')

        log_str = "System Test Logg String"
        init_logger.debug(log_str)

        with open(os.path.join(self.log_dir, 'init.log')) as log_file:
            last_line = log_file.readlines()[-1]
            self.assertTrue(last_line.endswith(log_str + '\n'))
