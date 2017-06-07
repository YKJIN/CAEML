__copyright__ = "Copyright 2017 Renumics GmbH (http://www.renumics.com)"
from caeml.common.states import WorkflowState
from caeml.common.workflow import Workflow
from caeml.runner import runner_local_pool


def executeAsync(aWorkflow: Workflow) -> WorkflowState:
    return runner_local_pool.executeAsync(aWorkflow)
