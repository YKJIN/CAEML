__copyright__ = "Copyright 2017 Renumics GmbH (http://www.renumics.com)"

import logging
from typing import Dict

import caeml.common.base
import caeml.common.process


class Workflow(caeml.common.process.Process):
    def __init__(self, name: str = None, steps: Dict['str', dict] = None, _id: str = None) -> 'Workflow':
        logging.getLogger('system').debug('Workflow creation..')
        self.steps = caeml.common.base.constructCaemlObjs_fromCaemlDicts(steps, self) if steps else {}
        super().__init__(name=name, _id=_id)

    def getExposedOutputPorts(self) -> Dict['str', 'OutPort']:
        aDict = {}
        for stepKey, step in self.steps.items():
            for portKey, port in step.outputPorts.items():
                if port.exposed_as:
                    aDict[port.exposed_as] = port
        return aDict

    def getExposedInputPorts(self) -> Dict['str', 'InputPort']:
        aDict = {}
        for stepKey, step in self.steps.items():
            for portKey, port in step.inputPorts.items():
                if port.exposed_as:
                    aDict[port.exposed_as] = port
        return aDict

    @property
    def inputParameters(self) -> Dict['str', caeml.common.process.Parameter]:
        return {k: port.getParameter() for k, port in self.getExposedInputPorts().items()}

    @property
    def outputParameters(self) -> Dict['str', caeml.common.process.Parameter]:
        return {k: port.getParameter() for k, port in self.getExposedOutputPorts().items()}


class Step(caeml.common.base.caemlNodeObj):
    def __init__(self, inputPorts: Dict['str', dict] = None, outputPorts: Dict['str', dict] = None,
                 process: caeml.common.process.Process = None, parent: Workflow = None,
                 name: str = None) -> 'Step':
        # TODO: assert (isinstance(parent, Workflow)) #this is currently blocked by tool_loader

        if issubclass(type(process), caeml.common.process.Process):
            self.process = process
        else:
            self.process = caeml.common.base.caemlDBObj.load_DBRef(process)
            if not issubclass(type(self.process), caeml.common.process.Process):
                raise Exception('load error')

        if inputPorts:
            self.inputPorts = caeml.common.base.constructCaemlObjs_fromCaemlDicts(inputPorts, self)
        else:
            self.inputPorts = {key: InputPort(name=key, parent=self)
                               for key, parameter in process.inputParameters.items()}

        if outputPorts:
            self.outputPorts = caeml.common.base.constructCaemlObjs_fromCaemlDicts(outputPorts, self)
        else:
            self.outputPorts = {key: OutPort(name=key, parent=self)
                                for key, parameter in process.outputParameters.items()}
        super().__init__(parent=parent, name=name)


class Port(caeml.common.base.caemlNodeObj):
    def __init__(self, parent: Step = None, name: str = None, source_step: Step = None,
                 source_port=None, fixed_value=None, exposed_as=None):
        assert (isinstance(parent, Step))
        self.exposed_as = exposed_as
        if not source_port is None:
            pass
        self.source_step = source_step
        self.source_port = source_port
        self.fixed_value = fixed_value
        super().__init__(parent=parent, name=name)

    def setSource(self, port: 'OutPort'):
        self.source_step = port.parent.name
        self.source_port = port.name

    def getSource(self) -> 'OutPort':
        if self.source_port or self.source_step:
            return self.parent.parent.steps[self.source_step].outputPorts[self.source_port]
        return None


class InputPort(Port):
    def getParameter(self) -> caeml.common.process.Parameter:
        parameter = self.parent.process.inputParameters[self.name]
        if not isinstance(parameter, caeml.common.process.Parameter):
            raise Exception('InputPort.getParameter could not find a parameter')
        return parameter


class OutPort(Port):
    def getParameter(self) -> caeml.common.process.Parameter:
        parameter = self.parent.process.outputParameters[self.name]
        if not isinstance(parameter, caeml.common.process.Parameter):
            raise Exception('InputPort.getParameter could not find a parameter')
        return parameter
