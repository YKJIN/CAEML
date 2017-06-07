__copyright__ = "Copyright 2017 Renumics GmbH (http://www.renumics.com)"
import os

from jinja2 import Environment, PackageLoader

from caeml.common import process
from caeml.common.tools import PythonTool
from pkg_codeaster.data_model.code_aster_model import CodeAster_commFile_Model


# Builds Code aster input deck
class CodeAsterBeamDemoTool(PythonTool):
    name = 'codeAsterBeamDemo'
    inputParameters = {'youngs_modulus': process.Parameter(name='youngs_modulus', parameterType='float'),
                       'mesh': process.Parameter(name='mesh', parameterType='caeml.files.file.File'),
                       'force': process.Parameter(name='force', parameterType='float'), }
    outputParameters = {'comm_file': process.Parameter(name='comm_file', parameterType='caeml.files.file.File'),
                        'export_file': process.Parameter(name='export_file', parameterType='caeml.files.file.File'),
                        }

    def launchCmd(self, inputs, tmpStore, stdout_file):
        mesh = inputs['mesh']

        this_folder = os.path.dirname(__file__)
        aModel = CodeAster_commFile_Model(os.path.join(this_folder, 'templates/comm/comm_beam.comm'))

        beam_data_model_dict = aModel.beam_data_model.asDict()

        # build .comm file
        material_defintions = [p for p in beam_data_model_dict['paragraphs'].paragraphs if
                               p.operator_name == 'DEFI_MATERIAU']
        youngs = material_defintions[0].keyword_arguments.findValueForKeyRecursive('E').expression
        youngs.value = inputs['youngs_modulus']
        meca_def = [p for p in beam_data_model_dict['paragraphs'].paragraphs if
                    p.operator_name == 'AFFE_CHAR_MECA']
        FY = meca_def[0].keyword_arguments.findValueForKeyRecursive('FY').expression
        FY.value = inputs['force']

        output = beam_data_model_dict['paragraphs'].ca_repr()

        with open('beam_bending_aster.comm', 'w') as file:
            file.write(output)

        # build .export file
        env = Environment(loader=PackageLoader('pkg_codeaster.tools', 'templates'))
        templateExport = env.get_template('export_template.export')
        with open('beam_bending_aster.export', 'w') as file:
            file.write(templateExport.render(input_deck='F comm /data/input/beam_bending_aster.comm D  1', \
                                             input_mesh='F mmed /data/' + mesh.path + ' D  20', \
                                             output_1='F mess /data/output.mess R  6', \
                                             output_2='F resu /data/output.resu R  8', \
                                             output_3='F rmed /data/output.rmed R  80', \
                                             output_4='R base /data/output.base RC 0'))

        return {'comm_file': 'beam_bending_aster.comm',
                'export_file': 'beam_bending_aster.export'
                }
