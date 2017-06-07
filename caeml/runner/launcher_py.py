__copyright__ = "Copyright 2017 Renumics GmbH (http://www.renumics.com)"
import os

import caeml.common.states as states
import caeml.common.tools as tools


def launchCmd(aWorkflowStepState: states.WorkflowStepState, tmpStore: str, stdout_file: str):
    aProcess = aWorkflowStepState.getStep().process
    assert (isinstance(aProcess, tools.PythonTool))
    assert (isinstance(aWorkflowStepState, states.WorkflowStepState))
    inputs = {}
    for k, v in aWorkflowStepState.inputPortStates.items():
        inputs[k] = v.getValue()
    outputs = aProcess.launchCmd(inputs, tmpStore, stdout_file)
    for k, v in outputs.items():
        outpara = aWorkflowStepState.outputPortStates[k].getPort().getParameter()
        if outpara.parameterType == 'caeml.files.file.File':
            aWorkflowStepState.outputPortStates[k].setValue(os.path.abspath(v))
            assert (os.path.isfile(aWorkflowStepState.outputPortStates[k].getValue().path))
        else:
            aWorkflowStepState.outputPortStates[k].setValue(v)
