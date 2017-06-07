__copyright__ = "Copyright 2017 Renumics GmbH (http://www.renumics.com)"
import os

TEST = 'this is from local test file'
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
"""
Real Settings for CAEML
"""
TEST_PROJECT_DIRECTORY = "/tmp/caeml_tests"
DATA_DIR = "/tmp/caeml-test-data/"

DB_DIR_SUFFIX = "test-db"

FILES_DIR_SUFFIX = "test-files"

DATABASE = {
    # 'directory': "~/filestorage/db",
    'host': 'localhost',
    'port': 27017,
    'name': 'test_caeml-db',
    'docker_net': None,
    'container_name': 'caeml-db-docker'
}

LOGGING = {
    'version': 1,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(module)s %(message)s'
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
            'level': 'INFO'
        },

        'workflow_file_handler': {
            'class': 'logging.handlers.RotatingFileHandler',
            'formatter': 'verbose',
            'filename': '/tmp/caeml-test-data/logging/workflow.log'
        },
        'process_file_handler': {
            'class': 'logging.handlers.RotatingFileHandler',
            'formatter': 'verbose',
            'filename': '/tmp/caeml-test-data/logging/process.log'
        },
        'system_file_handler': {
            'class': 'logging.handlers.RotatingFileHandler',
            'formatter': 'verbose',
            'filename': '/tmp/caeml-test-data/logging/system.log',
            'level': 'DEBUG'
        },
        'init_file_handler': {
            'class': 'logging.handlers.RotatingFileHandler',
            'formatter': 'verbose',
            'filename': '/tmp/caeml-test-data/logging/init.log',
            'level': 'DEBUG'
        }
    },
    'loggers': {
        'init': {
            'handlers': ['console', 'init_file_handler'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'system': {
            'handlers': ['console', 'system_file_handler'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'workflow': {
            'handlers': ['workflow_file_handler'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'process_data': {
            'handlers': ['process_file_handler'],
            'level': 'DEBUG',
            'propagate': False,
        }
    }
}

TOOLS = [
    'caeml.tools',
    'pkg_gmsh.tools',
    'pkg_step.tools',
    'pkg_codeaster.tools'
]

ANALYST = "Tests"
SETTINGS_TEST = True
