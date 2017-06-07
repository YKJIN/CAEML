__copyright__ = "Copyright 2017 Renumics GmbH (http://www.renumics.com)"
"""
Settings for CAEML
"""

DATA_DIR = "~/caeml_data"

DB_DIR_SUFFIX = "db"

FILES_DIR_SUFFIX = "files"

DATABASE = {
    # 'directory': "~/filestorage/db",
    'host': 'localhost',
    'port': 27017,
    'name': 'caeml-db',
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
            'level': 'DEBUG'
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

SETTINGS_TEST = False

ANALYST = "Anonymous"
