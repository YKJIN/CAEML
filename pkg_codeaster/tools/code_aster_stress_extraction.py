__copyright__ = "Copyright 2017 Renumics GmbH (http://www.renumics.com)"
from caeml.common import process
from caeml.common.tools import PythonTool


class CodeAsterStressExtractionTool(PythonTool):
    name = 'CodeAsterStressExtractionTool'
    inputParameters = {'resu_file': process.Parameter(name='mesh', parameterType='caeml.files.file.File'),
                       }
    outputParameters = {'stress_value': process.Parameter(name='comm_file', parameterType='float'),
                        }

    def launchCmd(self, inputs, tmpStore, stdout_file):
        resu_file = inputs['resu_file']

        with open(resu_file.path, 'r') as file:
            content = file.read()

        start = content.find('LA VALEUR MAXIMALE DE INVA_2   EST ') + len('LA VALEUR MAXIMALE DE INVA_2   EST    ')
        end = content.find('EN', start)
        value = float(content[start:end].strip())

        return {'stress_value': value}
