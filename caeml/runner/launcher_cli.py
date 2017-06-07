__copyright__ = "Copyright 2017 Renumics GmbH (http://www.renumics.com)"
import glob
import logging
import os
import shlex
from concurrent.futures import Future
from typing import List

import caeml.common.states as states
import caeml.common.tools
import caeml.common.workflow
from caeml.common import helper


def launchCmd(aWorkflowStepState: states.WorkflowStepState, tmpStore: str, stdout_file: str):
    args = createPopenArgs(aWorkflowStepState)

    helper.runFromCommandLine(args, stdout_file)

    gatherOutputFromDir(aWorkflowStepState, tmpStore)


def launchDocker(aWorkflowStepState: states.WorkflowStepState, tmpStore: str, stdout_file: str):
    args = createPopenArgs(aWorkflowStepState, '/data/input')  # TODO: get input dir name from stepPortsState.Value
    assert (isinstance(aWorkflowStepState, caeml.common.states.WorkflowStepState))

    tmpWorkdir = tmpStore

    # TODO if you debug a docker image on your local machine, be shure to push it to i61sv002 before testing, otherwise your local image will be overwritten at runtime
    helper.pullContainerImage(aWorkflowStepState.getStep().process.dockerImageId)

    # TODO added --rm to ensure the dockers filesystem does not persist after exit
    if True:  # LATER
        env_display = os.getenv('DISPLAY')
        addDockerArgs = " -e DISPLAY=unix{} -e WORK_DIR=/data".format(env_display)
    else:
        addDockerArgs = ""
    mounts = [{'hostVolume': tmpWorkdir, 'containerVolume': '/data'},
              {'hostVolume': '/tmp/.X11-unix', 'containerVolume': '/tmp/.X11-unix:rw'}]
    helper.runContainer(aWorkflowStepState.getStep().process.dockerImageId, mounts=mounts,
                        dockerArgs=addDockerArgs, args=args, stdout_file=stdout_file)

    gatherOutputFromDir(aWorkflowStepState, tmpStore)


def createPopenArgs(aWorkflowStepState: states.WorkflowStepState, replace_path_with: str = False) -> List['str']:
    argDict = dict()
    for key, portState in aWorkflowStepState.inputPortStates.items():  # gathering and command preparation
        assert (not isinstance(portState.setValue, Future))
        assert (portState.isEvaluable())
        argDict[key] = dict()
        aParameter = portState.getPort().getParameter()
        argDict[key]['prefix'] = aParameter.inputBinding.prefix if aParameter.inputBinding.prefix else ''
        argDict[key]['position'] = aParameter.inputBinding.position
        argDict[key]['value'] = portState.getEvaluation()

        if isinstance(argDict[key]['value'], list):
            argDict[key]['value'] = ' '.join(str(v) for v in argDict[key]['value'])
        if (isinstance(argDict[key]['value'], caeml.files.file.File)):
            if not replace_path_with:
                argDict[key]['value'] = argDict[key]['value'].path
            else:  # replace_path_with == true
                argDict[key]['value'] = replace_path_with + '/' + argDict[key]['value'].getFileBaseName()
                # Later: encapsulate replace_path_with in storage (e.g. a docker-storage?)

    argDict = sorted(argDict.values(), key=lambda k: k['position'])
    argsString = ' '.join([str(inp['prefix']) + ' ' + str(inp['value']) for inp in argDict])
    command_line = aWorkflowStepState.getStep().process.baseCommand + ' ' + argsString
    logging.getLogger('workflow').debug('Command:  ' + command_line)
    logging.getLogger('system').debug('workflow' 'Command:  ' + command_line)
    args = shlex.split(command_line)
    return args


def gatherOutputFromDir(aWorkflowStepState: states.WorkflowStepState, tmpStore: str):
    for key, portState in aWorkflowStepState.outputPortStates.items():
        outpara = portState.getPort().getParameter()
        if outpara.parameterType == 'caeml.files.file.File' or outpara.outputBinding.glob:
            glob_pattern = outpara.outputBinding.glob
            found_files = glob.glob(tmpStore + '/' + glob_pattern)
            # TODO : raise expeception or return list when len(..)> 1
            if (len(found_files) < 1):
                raise Exception('No output file is matching glob ' + outpara.outputBinding.glob)
            if (len(found_files) > 1):
                raise Exception('Too many output files are matching glob ' + outpara.outputBinding.glob)
            portState.setValue(caeml.files.file.File(found_files[0]))

            # Later: move file(s) from cmd line tool workdir to runners
