__copyright__ = "Copyright 2017 Renumics GmbH (http://www.renumics.com)"

import caeml.common.base as base
import caeml.common.process as caeml_process


class PythonTool(caeml_process.Process):
    def __init__(self, name: str = 'unknownName', ____baseCommand: str = 'unknownBaseCommand', stdout: str = 'None',
                 processClass: str = 'unknownProcessClass', inputParameters: dict = None, outputParameters: dict = None,
                 _id=None):
        self.stdout = stdout  # can we handle this?
        self.processClass = processClass
        self.inputParameters = type(self).inputParameters
        self.outputParameters = type(self).outputParameters
        super().__init__(_id=_id, name=name)

    # TODO: How to load from DB?

    def launchCmd(self, aSWorkflowStepState, tmpStore, stdout_file):
        # TDOD: how to store in DB?
        raise NotImplementedError()


class CommandLineTool(caeml_process.Process):
    def __init__(self, name: str = 'unknownName', baseCommand: str = 'unknownBaseCommand', stdout: str = 'None',
                 processClass: str = 'unknownProcessClass', inputParameters: dict = None, outputParameters: dict = None,
                 _id=None):
        self.baseCommand = baseCommand
        self.stdout = stdout
        self.processClass = processClass
        self.outputParameters = base.constructCaemlObjs_fromCaemlDicts(outputParameters, self) \
            if outputParameters else {}
        self.inputParameters = base.constructCaemlObjs_fromCaemlDicts(inputParameters, self) \
            if inputParameters else {}
        super().__init__(_id=_id, name=name)


class DockerizedCommandLineTool(CommandLineTool):
    def __init__(self, name: str = 'unknownName', baseCommand: str = 'unknownBaseCommand', stdout: str = 'None',
                 processClass: str = 'unknownProcessClass', inputParameters: dict = None, outputParameters: dict = None,
                 _id=None, dockerImageId=''):
        self.dockerImageId = dockerImageId
        super().__init__(name=name, baseCommand=baseCommand, stdout=stdout, processClass=processClass,
                         inputParameters=inputParameters, outputParameters=outputParameters, _id=_id)
