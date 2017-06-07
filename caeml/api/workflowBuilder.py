__copyright__ = "Copyright 2017 Renumics GmbH (http://www.renumics.com)"
from caeml.common import tool_loader
from caeml.common.process import Process
from caeml.common.tools import CommandLineTool
from caeml.common.workflow import Port
from caeml.common.workflow import Step
from caeml.common.workflow import Workflow


def createWorkflow(name: str) -> Workflow:
    return Workflow(name=name)


def connectPorts(source: Port, target: Port):
    assert (target.parent.parent == source.parent.parent)
    target.setSource(source)


def getCmdTool(id: str) -> CommandLineTool:
    return tool_loader.getCmdTool(id)


def createStep(process: Process, parent: Workflow, name: str = None) -> Step:
    if not name:
        i = 0
        name = process.name + str(i)
        while name in parent.steps:
            i = i + 1
            name = process.name + str(i)

    step = Step(process=process, parent=parent, name=name)
    parent.steps[step.name] = step
    return step


def createToolStep(toolId: str, parent: Workflow, name: str = None) -> Step:
    step = createStep(getCmdTool(toolId), parent, name)
    return step
