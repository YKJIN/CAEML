__copyright__ = "Copyright 2017 Renumics GmbH (http://www.renumics.com)"
import datetime
import os
import shutil

import caeml.common.states as states
import caeml.common.tools
import caeml.common.workflow
import caeml.files.file
import caeml.runner.launcher_cli as launcher_cli
import caeml.runner.launcher_py as launcher_py


def launchTool(aWorkflowStepState: states.WorkflowStepState):
    assert (isinstance(aWorkflowStepState, states.WorkflowStepState))

    aWorkflowStepState.start_time = (datetime.datetime.now() - datetime.datetime(1970, 1, 1)).total_seconds()

    cwd_backup = os.getcwd()
    workflowStorage = aWorkflowStepState.parent.getDataStorage()
    subdirName = aWorkflowStepState.name
    workflowStorage.addSub(subdirName)
    os.chdir(workflowStorage.path(subdirName))  # TODO threading: fix error, cwd is shared between
    workingDirectory = workflowStorage.path(subdirName)
    os.mkdir('input')  # TODO threading
    for key, input in aWorkflowStepState.inputPortStates.items():
        if isinstance(input.getValue(), caeml.files.file.File):
            src = input.getValue().path
            dest = './input/' + os.path.basename(src)
            shutil.copyfile(src, dest)
            input.setValue(dest)

    # chose launcher method by step type
    stdout_file = aWorkflowStepState.getStep().process.stdout
    process = aWorkflowStepState.getStep().process
    if isinstance(process, caeml.common.tools.DockerizedCommandLineTool):
        launcher_cli.launchDocker(aWorkflowStepState, workingDirectory, stdout_file)
    elif isinstance(process, caeml.common.tools.CommandLineTool):
        launcher_cli.launchCmd(aWorkflowStepState, workingDirectory, stdout_file)
    elif isinstance(process, caeml.common.tools.PythonTool):
        launcher_py.launchCmd(aWorkflowStepState, workingDirectory, stdout_file)
    else:
        raise NotImplementedError()

    aWorkflowStepState.done = True
    aWorkflowStepState.end_time = (datetime.datetime.now() - datetime.datetime(1970, 1, 1)).total_seconds()

    os.chdir(cwd_backup)
