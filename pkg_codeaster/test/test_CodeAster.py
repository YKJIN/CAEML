__copyright__ = "Copyright 2017 Renumics GmbH (http://www.renumics.com)"
import os
import unittest

import caeml.common.workflow
import caeml.runner.runner_local_pool
import pkg_codeaster.tools.code_aster_stress_extraction as stress_tool
import testproject.tests.base
from caeml.common.tool_loader import getCmdTool
from caeml.files.file import File
from   pkg_codeaster.tools.code_aster_beam import CodeAsterBeamDemoTool


class CodeAsterBaseTest(testproject.tests.base.CAEMLTestCase):
    def test_input_deck_creation(self):
        aWorkflow = caeml.common.workflow.Workflow()

        deckCreationTool = CodeAsterBeamDemoTool()
        deckCreationStep = caeml.common.workflow.Step(name='step1', process=deckCreationTool, parent=aWorkflow)
        aWorkflow.steps['step1'] = deckCreationStep

        # set values
        deckCreationStep.inputPorts['mesh'].fixed_value = File(
            os.path.join(os.path.abspath(os.path.join(__file__, os.pardir)), 'test_data/beam/', 'beam.med'))
        deckCreationStep.inputPorts['youngs_modulus'].fixed_value = 2.1e+11
        deckCreationStep.inputPorts['force'].fixed_value = 1200000001

        state = caeml.runner.runner_local_pool.executeAsync(aWorkflow)
        comm_file = state.findPortState(deckCreationStep.outputPorts['comm_file']).getEvaluation()
        export_file = state.findPortState(deckCreationStep.outputPorts['export_file']).getEvaluation()

        with open(comm_file.path) as current_file:
            content = current_file.read()
            self.assertTrue('1200000001' in content)

        with open(export_file.path) as current_file:
            content = current_file.read()
            self.assertTrue('beam.med' in content)

    def test_code_aster_runner(self):
        aWorkflow = caeml.common.workflow.Workflow()

        codeAsterStep = caeml.common.workflow.Step(name='step1', process=getCmdTool('CodeAster'), parent=aWorkflow)
        aWorkflow.steps['step1'] = codeAsterStep

        # set values
        codeAsterStep.inputPorts['export_file'].fixed_value = File(
            os.path.join(os.path.abspath(os.path.join(__file__, os.pardir)), 'test_data/beam/beam.export'))
        codeAsterStep.inputPorts['comm_file'].fixed_value = File(
            os.path.join(os.path.abspath(os.path.join(__file__, os.pardir)), 'test_data/beam/beam.comm'))
        codeAsterStep.inputPorts['mesh_file'].fixed_value = File(
            os.path.join(os.path.abspath(os.path.join(__file__, os.pardir)), 'test_data/beam/beam.med'))

        # set values
        state = caeml.runner.runner_local_pool.executeAsync(aWorkflow)

        res_file = state.findPortState(codeAsterStep.outputPorts['plain_mesh']).getEvaluation()
        res_stress = state.findPortState(codeAsterStep.outputPorts['resu_file']).getEvaluation()

        # binary res_file: only check that it exists
        self.assertTrue(os.path.exists(res_file.path))

        with open(res_stress.path) as current_file:
            content = current_file.read()
            self.assertTrue('TOTAL_JOB' in content)
            self.assertTrue('VALEUR MAXIMALE DE INVA_2' in content)

        self.assertTrue(True)

    def test_whole_workflow(self):
        aWorkflow = caeml.common.workflow.Workflow()

        deckCreationTool = CodeAsterBeamDemoTool()
        deckCreationStep = caeml.common.workflow.Step(name='step1', process=deckCreationTool, parent=aWorkflow)
        aWorkflow.steps['step1'] = deckCreationStep

        # set values
        deckCreationStep.inputPorts['mesh'].fixed_value = File(
            os.path.join(os.path.abspath(os.path.join(__file__, os.pardir)), 'test_data/beam/', 'beam.med'))
        deckCreationStep.inputPorts['youngs_modulus'].fixed_value = 2.1e+11
        deckCreationStep.inputPorts['force'].fixed_value = 1200000001

        codeAsterStep = caeml.common.workflow.Step(name='step2', process=getCmdTool('CodeAster'), parent=aWorkflow)
        aWorkflow.steps['step2'] = codeAsterStep

        codeAsterStep.inputPorts['export_file'].setSource(deckCreationStep.outputPorts['export_file'])
        codeAsterStep.inputPorts['comm_file'].setSource(deckCreationStep.outputPorts['comm_file'])
        codeAsterStep.inputPorts['mesh_file'].fixed_value = File(
            os.path.join(os.path.abspath(os.path.join(__file__, os.pardir)), 'test_data/beam/', 'beam.med'))

        stressExtractionTool = stress_tool.CodeAsterStressExtractionTool()
        stressExtractionStep = caeml.common.workflow.Step(name='step3', process=stressExtractionTool,
                                                          parent=aWorkflow)
        aWorkflow.steps['step3'] = stressExtractionStep
        stressExtractionStep.inputPorts['resu_file'].setSource(codeAsterStep.outputPorts['resu_file'])

        state = caeml.runner.runner_local_pool.executeAsync(aWorkflow)

        # res_file = state.findPortState(codeAsterStep.outputPorts['results']).getEvaluation()
        stress = state.findPortState(stressExtractionStep.outputPorts['stress_value']).getEvaluation()
        print(str(stress))

        self.assertLessEqual(abs(stress - 0.07716), 1e-6)


if __name__ == '__main__':
    unittest.main()
