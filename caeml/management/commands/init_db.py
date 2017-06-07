__copyright__ = "Copyright 2017 Renumics GmbH (http://www.renumics.com)"
import logging
import os
import shlex
import time

import caeml.common.helper
from caeml.common.exceptions import InitDBException
from caeml.management.base import BaseCommand
from caeml.management.conf import settings


class Command(BaseCommand):
    help = "Spins up the MongoDB DB"

    def execute(self, argv):
        # There is only be one container. The settings.DATA_DIR must be the same for all running dbs
        # What happens if a second container is started with a differen settings.DATABASE['container_name']?
        # TODO: What happens if a container is running and a new one is initialized with a different DATA_DIR?
        # TODO: ....

        # filesystem hast to be initialized before init_db, throw error if this is not the case
        fullDir = os.path.join(settings.DATA_DIR, settings.DB_DIR_SUFFIX)
        if not os.path.isdir(fullDir):
            logging.getLogger('init').error(
                "Filesystem not initialized, please run \"manage.py init_filesystem\" before initializing db")
            raise InitDBException(
                "Filesystem not initialized, please run \"manage.py init_filesystem\" before initializing db")

        # search only for running containers
        command = "docker ps -q --filter \"ancestor=mongo\""
        containerIds = caeml.common.helper.runFromCommandLine(args=shlex.split(command))

        if containerIds == "":
            # init mongodb
            if not caeml.common.helper.containerImageExists('mongo'):
                caeml.common.helper.pullContainerImage('mongo', wait=True, logger='init')

            logging.getLogger('init').info("Spinning up db, settings: ")
            logging.getLogger('init').debug(settings.DATABASE)

            # no container is running check if one with the same name is suspended and rename it
            # check for exact name with ^/...$
            exists = caeml.common.helper.containerWithNameExists(settings.DATABASE['container_name'])

            if exists:
                # find name that is not already taken
                newName = settings.DATABASE['container_name'] + '_backup_'
                i = 0
                while (exists):
                    i += 1
                    exists = caeml.common.helper.containerWithNameExists(newName + str(i))
                newName += str(i)

                # rename old container
                logging.getLogger('init').info("Container with name: {} already exists! Renaming it to {}".format(
                    settings.DATABASE['container_name'], newName))
                command = "docker rename {} {}".format(settings.DATABASE['container_name'], newName)
                logging.getLogger('init').debug(command)
                commandArgs = shlex.split(command)
                response = caeml.common.helper.runFromCommandLine(args=commandArgs, logger_name='init')

            userId = os.getuid()

            if settings.DATABASE['docker_net'] is not None:
                command = "docker run -u %s -d --restart=always --name %s --net %s " % (
                    str(userId), settings.DATABASE['container_name'], settings.DATABASE['docker_net'])
                logging.getLogger('init').info("Linking db to gitlab docker net")
                logging.getLogger('init').info(command)
            else:
                command = "-d -u %s --restart=always --name %s -p 127.0.0.1:27017:27017 " % (
                    str(userId), settings.DATABASE['container_name'])
                logging.getLogger('init').info(command)

            mounts = [{'hostVolume': fullDir, 'containerVolume': '/data/db'}]

            caeml.common.helper.runContainer(imageId='mongo', mounts=mounts,
                                             dockerArgs=command, logger='init', rm=False)

            time.sleep(1)

        else:
            # check if everything is alright
            logging.getLogger('init').debug('Following container found ' + containerIds)

            containerList = containerIds.split()
            # assures that only one container is run at a time
            if len(containerList) != 1:
                raise InitDBException("More than one container is currently running from mongo image")

            # check if the container is already there, get info on it
            resJSON = caeml.common.helper.inspectDocker(containerIds)

            bind = resJSON[0]['HostConfig']['Binds'][0]
            mountDirs = bind.split(':')

            if mountDirs[0] != fullDir:
                logging.getLogger('init').error(
                    "Docker container %s present, running with wrong data dir. Consider purging DB with \"manage.py purge_db\" if you want to permanently remove it" % (
                        settings.DATABASE['container_name']))
                raise InitDBException("DB container is running with wrong data dir")

            # check if docker is already running, return if this is the case

            if resJSON[0]['State']['Status'] == 'running':
                logging.getLogger('init').info("DB is already running, no need to initialize it")
            # check if docker container with name already exists, if so throw error and exit
            else:
                logging.getLogger('init').warning(
                    "Docker container %s present, but not running. Consider purging DB with \"manage.py purge_db\" if you want to permanently remove it" % (
                        settings.DATABASE['container_name']))
                raise InitDBException(
                    "DB container is present, but not running. Consider purging DB with \"manage.py purge_db\" if you want to permanently remove it")
