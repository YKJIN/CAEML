__copyright__ = "Copyright 2017 Renumics GmbH (http://www.renumics.com)"

import json
import logging
import os
import shlex
import subprocess
from typing import List

import yaml


def pullContainerImage(imageId: str, version: str = 'latest', stdout_file: str = '', wait=False,
                       logger: str = 'system') -> None:
    dockerPullArg = "docker pull {}:{}".format(imageId, version)

    theDockerArgs = shlex.split(dockerPullArg)

    logging.getLogger(logger).info('Pulling docker image {}:{}'.format(imageId, version))

    runFromCommandLine(theDockerArgs, stdout_file=stdout_file, logger_name=logger)


def containerImageExists(imageId: str, version: str = 'latest') -> bool:
    """Checks if the specified version of an image exists
    when no tag or the tag latest is provided return value is always False
    because due to the property of the tag latest one can not assert that local latest is also remote latest"""
    infoArg = "docker inspect --type=image {}:{}".format(imageId, version)
    theDockerArgs = shlex.split(infoArg)

    info = runFromCommandLine(theDockerArgs)

    if info.find('Error') > -1:
        return False

    # TODO check what happens when asked for version *.2 but *.21 is present
    infoYaml = yaml.load(info)[0]

    return True


def containerWithNameExists(containerName: str) -> bool:
    command = 'docker ps -aqf "name=^/{}$"'.format(containerName)
    response = ""
    commandArgs = shlex.split(command)
    response = runFromCommandLine(commandArgs, logger_name='init')

    return len(response) > 0


def runContainer(imageId: str, version: str = 'latest', mounts: list = [],
                 dockerArgs: str = None, args: list = None, stdout_file: str = None, wait=True,
                 logger: str = 'system', rm=True):
    dockerCmd = "docker run -i -e LOCAL_USER_ID=" + str(os.getuid())
    if rm:
        dockerCmd += ' --rm'
    for mount in mounts:
        dockerCmd += " -v  " + mount['hostVolume'] + ':' + mount['containerVolume'] + ' '

    if not dockerArgs is None:
        dockerCmd += ' ' + dockerArgs

    dockerCmd += " {}:{}".format(imageId, version)
    if not args is None:
        dockerCmd += ' ' + ' '.join(args)

    logging.getLogger(logger).debug('Running docker argument: {}'.format(dockerCmd))
    theDockerArgs = shlex.split(dockerCmd)
    runFromCommandLine(theDockerArgs, stdout_file=stdout_file, logger_name=logger)


def inspectDocker(containerId: str) -> dict:
    command = "docker inspect %s" % (containerId)

    commandArgs = shlex.split(command)
    response = runFromCommandLine(commandArgs, logger_name='init')
    return json.loads(response)


def dockerMountDict(hostVolume='', containerVolume=''):
    return {'hostVolume': hostVolume, 'containerVolume': containerVolume}


def runFromCommandLine(args: List['str'], stdout_file: str = None, logger_name: str = None, wait=True) -> str:
    response = ""
    # Popen should never be used with shell=true
    with subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=1,
                          universal_newlines=True) as p:
        if (stdout_file):
            with open(stdout_file, 'w') as aStdout:
                for line in p.stdout:
                    if (logger_name):
                        logging.getLogger(logger_name).debug('stdout: ' + line)
                    response += line + "\n"
                    aStdout.write(line)
        else:
            for line in p.stdout.read().splitlines():
                if (logger_name):
                    logging.getLogger('init').debug('stdout: ' + line)
                response += line + "\n"
    if (wait):
        p.wait()
    return response


def runFromCommandLineWithConsoleOutput(args: List['str']):
    with subprocess.Popen(args, bufsize=1, universal_newlines=True) as p:
        p.wait()
