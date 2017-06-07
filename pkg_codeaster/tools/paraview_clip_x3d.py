__copyright__ = "Copyright 2017 Renumics GmbH (http://www.renumics.com)"
import os

from jinja2 import Environment, PackageLoader

from caeml.common import process
from caeml.common.tools import PythonTool


# Later: Refactor to meta tool.
class ParaviewClipX3DTool(PythonTool):
    name = 'ParaviewStressWarpX3DTool'
    inputParameters = {'mesh': process.Parameter(name='mesh', parameterType='caeml.files.file.File')
                       }

    outputParameters = {'script_file': process.Parameter(name='script_file', parameterType='caeml.files.file.File')
                        }

    def launchCmd(self, inputs, tmpStore, stdout_file):
        mesh = inputs['mesh']

        absPath = os.path.abspath(os.path.join('/data', mesh.path))

        env = Environment(
            loader=PackageLoader('pkg_codeaster.tools', 'templates')
        )

        templatePara = env.get_template('paraview_clip_template.py')

        with open('clip_output_script.py', 'w') as file:
            file.write(templatePara.render(input_mesh=absPath))

        return {'script_file': 'clip_output_script.py'
                }
