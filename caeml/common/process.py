__copyright__ = "Copyright 2017 Renumics GmbH (http://www.renumics.com)"

import logging
from pydoc import locate

import caeml.common.base as base
from caeml.common import process


class Process(base.caemlDBObj):
    def __init__(self, name: str = None, _id: str = None):
        logging.getLogger('system').debug('Process creation..')
        self.name = name  # a caemlDBObj schould not have a name.
        super().__init__(_id=_id)


class Parameter(base.caemlNodeObj):
    def __init__(self, name: str = None, parameterType: str = None, format: str = None, outputBinding: dict = None,
                 inputBinding: dict = None, parent: process.Process = None):
        logging.getLogger('system').debug('Parameter creation..')
        self.parameterType = parameterType
        if not isinstance(parameterType, str):
            raise Exception('parameterType must be of type str')
        self.format = format
        self.inputBinding = base.constructCaemlObj_fromCaemlDict(inputBinding) if inputBinding else None
        self.outputBinding = base.constructCaemlObj_fromCaemlDict(outputBinding) if outputBinding else None
        super().__init__(name=name, parent=parent)

    def getParameterClass(self) -> type:
        aType = locate(self.parameterType)
        if not aType:
            raise Exception('No python class for parameter type {0} available'.format(self.parameterType))
        return aType


class InputBinding(base.caemlBaseObj):
    def __init__(self, position: int = None, prefix: str = None):
        self.position = position
        self.prefix = prefix


class OutputBinding(base.caemlBaseObj):
    def __init__(self, glob: str = None):
        self.glob = glob
