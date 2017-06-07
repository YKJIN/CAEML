__copyright__ = "Copyright 2017 Renumics GmbH (http://www.renumics.com)"
import caeml.common.process as process
import caeml.common.tools as tools


class statsTool(tools.PythonTool):
    name = 'asd'
    inputParameters = {'data': process.Parameter(name='data', parameterType='list')}
    outputParameters = {'mean': process.Parameter(name='mean', parameterType='float'),
                        'max': process.Parameter(name='max', parameterType='float'),
                        'min': process.Parameter(name='min', parameterType='float')}  # TODO:allow real tpyes

    def launchCmd(self, inputs, tmpStore, stdout_file):
        data = inputs['data']
        minval = min(data)
        maxval = max(data)
        meanval = sum(data) / len(data)
        return {'mean': meanval, 'max': maxval, 'min': minval}
