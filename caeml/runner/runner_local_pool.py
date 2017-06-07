__copyright__ = "Copyright 2017 Renumics GmbH (http://www.renumics.com)"
import logging
from concurrent.futures import Future
from concurrent.futures import ThreadPoolExecutor  # , ProcessPoolExecutor

import caeml.common.states as states
import caeml.common.tools
import caeml.common.workflow
import caeml.files.storage
import caeml.runner.launcher as launcher

# deadlocks can occur if max_works < count of workflow_steps
executor = ThreadPoolExecutor(max_workers=None)


def executeAsync(workflow: caeml.common.workflow.Workflow,
                 workflowState: states.WorkflowState = None) -> states.WorkflowState:
    """submit all steps"""

    if not workflowState:  # nested workflows come with an workflowState defined from outer workflow
        workflowState = states.WorkflowState(workflow=workflow)

    remaining_work = True
    results = []
    while remaining_work:
        remaining_work = False
        for stepKey, stepState in workflowState.stepStates.items():
            if (not stepState.submitted) and stepState.isReady():
                remaining_work = True

                if not isinstance(stepState.getStep().process, caeml.common.workflow.Workflow):
                    args = [stepState]
                    future = executor.submit(funcWrapper, *args)  # args is just a stepState (data in port states)

                    for key, portStates in stepState.outputPortStates.items():
                        portStates.setValue(future)  # workaround: push same future into all outputs
                    results.append(future)
                    stepState.submitted = True

                else:  # nested workflow: push values from outer portStates to exposed ports states.
                    nestedWorkflow = stepState.getStep().process
                    nestedWorkflowState = states.WorkflowState(workflow=nestedWorkflow)

                    for wfPortName, portState in nestedWorkflowState.getExposedInputPortStates().items():
                        portState.setValue(stepState.inputPortStates[wfPortName].getEvaluation())
                    executeAsync(nestedWorkflow, nestedWorkflowState)
                    stepState.submitted = True
                    for wfPortName, portState in nestedWorkflowState.getExposedOutputPortStates().items():
                        stepState.outputPortStates[wfPortName].setValue(portState.getEvaluation())
                    stepState.submitted = True

        # TODO threading: remove
        for res in results:
            logging.getLogger('system').debug('res:' + str(res.result()))
            assert (res.result())

    return workflowState


def funcWrapper(*args) -> bool:
    """can be passed to executor, workflow step is loaded from args[0], funcWrapper wait for futures and stores values
    in steps before a launcher is started"""
    assert (len(args) == 1)
    aSWorkflowStepState = args[0]
    assert (isinstance(aSWorkflowStepState, states.WorkflowStepState))

    # wait for prior future results
    for key, input in aSWorkflowStepState.inputPortStates.items():
        currentValue = input.getEvaluation()  # future
        if isinstance(currentValue, Future):
            # Quick and dirty: blocks until port-states are written by launchTool;
            # Later: this wont work in multi-CPU / multi-node enviroments because port states might be not in sync!
            input.setValue(currentValue.result())
            logging.getLogger('system').debug(currentValue.result())
        else:
            input.setValue(currentValue)

    launcher.launchTool(aSWorkflowStepState)

    return True
