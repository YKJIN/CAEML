__copyright__ = "Copyright 2017 Renumics GmbH (http://www.renumics.com)"

import concurrent.futures
from typing import Dict

import caeml.common.base
import caeml.common.workflow
import caeml.files.storage
from caeml.common.workflow import Port, Step
from caeml.management.conf import settings


class WorkflowState(caeml.common.base.caemlDBObj):
    def __init__(self, workflow: caeml.common.workflow.Workflow = None,
                 stepStates: Dict['str', 'WorkflowStepState'] = None,
                 _id: str = None, inputPortStates: Dict['str', 'InputPortState'] = None,
                 outputPortStates: Dict['str', 'OutputPortState'] = None):
        if issubclass(type(workflow), caeml.common.workflow.Workflow):
            self.workflow = workflow
        else:
            self.workflow = caeml.common.base.caemlDBObj.load_DBRef(workflow)
            if not issubclass(type(self.workflow), caeml.common.workflow.Workflow):
                raise Exception('load error')

        if stepStates:
            self.stepStates = caeml.common.base.constructCaemlObjs_fromCaemlDicts(stepStates, self)
        else:
            self.stepStates = {key: WorkflowStepState(name=key, parent=self) for key, step in workflow.steps.items()}

        self._dataStorage = None
        super().__init__(_id)

    def findPortState(self, port: 'Port') -> 'PortState':
        try:
            return self.stepStates[port.parent.name].inputPortStates[port.name]
        except:
            return self.stepStates[port.parent.name].outputPortStates[port.name]

    def findWorkflowStepState(self, workflowStep: Step):
        raise NotImplementedError()

    def getExposedInputPortStates(self) -> Dict['str', 'InputPortState']:
        return {k: self.findPortState(v) for k, v in self.workflow.getExposedInputPorts().items()}

    def getExposedOutputPortStates(self) -> Dict['str', 'OutputPortState']:
        return {k: self.findPortState(v) for k, v in self.workflow.getExposedOutputPorts().items()}

    def getDataStorage(self) -> caeml.files.storage.FileStorage:
        if not self._dataStorage:
            aStore = caeml.files.storage.FileStorage()
            workflowName = self.workflow.name
            if not workflowName:
                workflowName = "aWorkflow"
            aStore.resetBaseLocationToNewSub(workflowName)
            self._dataStorage = aStore
        return self._dataStorage


class WorkflowStepState(caeml.common.base.caemlNodeObj):
    def __init__(self, name: str = None, parent: WorkflowState = None, submitted: bool = False, analyst: str = None,
                 done: bool = False, start_time: int = 0, end_time: int = 0,
                 inputPortStates: Dict['str', 'InputPortState'] = None,
                 outputPortStates: Dict['str', 'OutputPortState'] = None):
        if analyst is None:
            analyst = settings.ANALYST  # default cant reach settings

        assert (isinstance(parent, WorkflowState))
        super().__init__(name=name, parent=parent)
        self.submitted = submitted
        self.analyst = analyst
        self.start_time = start_time
        self.end_time = end_time
        self.done = done

        if inputPortStates:
            self.inputPortStates = caeml.common.base.constructCaemlObjs_fromCaemlDicts(inputPortStates, self)
        else:
            self.inputPortStates = {key: InputPortState(name=key, parent=self)
                                    for key, port in self.getStep().inputPorts.items()}
        if outputPortStates:
            self.outputPortStates = caeml.common.base.constructCaemlObjs_fromCaemlDicts(outputPortStates, self)
        else:
            self.outputPortStates = {key: OutputPortState(name=key, parent=self)
                                     for key, port in self.getStep().outputPorts.items()}

    def getStep(self) -> caeml.common.workflow.Step:
        step = self.parent.workflow.steps[self.name]
        if not (isinstance(step, caeml.common.workflow.Step)):
            print(isinstance(step, caeml.common.workflow.Step))
        assert (isinstance(step, caeml.common.workflow.Step))
        return step

    def isReady(self) -> bool:
        """A process in ready for execution when all input parameters are evaluable (futures are sufficient)"""
        ready = True
        for input in self.inputPortStates.values():
            if not input.isEvaluable():
                ready = False
        return ready


class PortState(caeml.common.base.caemlNodeObj):
    def __init__(self, parent: WorkflowStepState = None, name: str = None, rawValue=None):
        assert (parent)
        super().__init__(name=name, parent=parent)
        self.rawValue = rawValue

    def getValue(self):
        return self.rawValue

    def setValue(self, value):  # cares for conversion
        if value and not isinstance(value, concurrent.futures.Future):
            aParameterClass = self.getPort().getParameter().getParameterClass()
            if not aParameterClass:
                raise Exception('ParameterType mus be set before a value is assigned.')

            # read file when parameter when value is file and parameter is not.
            if (isinstance(value, caeml.files.file.File) and not issubclass(aParameterClass, caeml.files.file.File)):
                with open(value.path) as f:
                    self.setValue(f.read())  # recursive call, now with file content

            else:  # conversion, later: refactor to new file and extend it
                if not issubclass(type(value), aParameterClass):
                    self.rawValue = aParameterClass(value)  # convert by calling c'tor
                else:
                    self.rawValue = value

    def isEvaluable(self) -> bool:  # might contain an empty future
        if self.getPort().fixed_value:
            return True
        if self.getValue():
            return True
        if self.getPort().getSource():
            wfState = self.parent.parent
            sourceState = wfState.findPortState(self.getPort().getSource())
            return sourceState.isEvaluable()
        return False

    def getEvaluation(self):  # this might block.
        if self.getValue():
            return self.getValue()
        if self.getPort().fixed_value:
            return self.getPort().fixed_value
        if self.getPort().getSource():
            wfState = self.parent.parent
            sourceState = wfState.findPortState(self.getPort().getSource())
            return sourceState.getEvaluation()
        raise Exception('{input} with id={id} could not be evaluated'.format(input=input, id=id))


class InputPortState(PortState):
    def getPort(self) -> caeml.common.workflow.InputPort:
        port = self.parent.getStep().inputPorts[self.name]
        assert (isinstance(port, caeml.common.workflow.Port))
        return port


class OutputPortState(PortState):
    def getPort(self) -> caeml.common.workflow.OutPort:
        port = self.parent.getStep().outputPorts[self.name]
        assert (isinstance(port, caeml.common.workflow.Port))
        return port
