__copyright__ = "Copyright 2017 Renumics GmbH (http://www.renumics.com)"
import caeml.common.process as process
import caeml.common.tools as tools


class add(tools.PythonTool):
    name = 'add'
    inputParameters = {'addend1': process.Parameter(name='addend1', parameterType='float'),
                       'addend2': process.Parameter(name='addend2', parameterType='float')}
    outputParameters = {'sum': process.Parameter(name='sum', parameterType='float')}

    def launchCmd(self, inputs, tmpStore, stdout_file):
        return {'sum': inputs['addend1'] + inputs['addend2']}

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
