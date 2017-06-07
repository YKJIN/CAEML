__copyright__ = "Copyright 2017 Renumics GmbH (http://www.renumics.com)"
import caeml.common.process as process
import caeml.common.tools as tools


class statsFileTool(tools.PythonTool):
    name = 'asd'
    inputParameters = {'data': process.Parameter(name='data', parameterType='list')}
    outputParameters = {'mean': process.Parameter(name='mean', parameterType='caeml.files.file.File'),
                        'max': process.Parameter(name='max', parameterType='caeml.files.file.File'),
                        'min': process.Parameter(name='min', parameterType='caeml.files.file.File')}

    def launchCmd(self, inputs, tmpStore, stdout_file):
        data = inputs['data']
        minval = min(data)
        maxval = max(data)
        meanval = sum(data) / len(data)

        with open('min.txt', 'w') as fileWriter:
            fileWriter.write(str(minval) + "\n")

        with open('max.txt', 'w') as fileWriter:
            fileWriter.write(str(maxval) + "\n")

        with open('mean.txt', 'w') as fileWriter:
            fileWriter.write(str(meanval) + "\n")

        return {'min': 'min.txt', 'max': 'max.txt', 'mean': 'mean.txt'}
