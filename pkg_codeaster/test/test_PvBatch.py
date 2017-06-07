__copyright__ = "Copyright 2017 Renumics GmbH (http://www.renumics.com)"
import os
import unittest

import caeml.common.workflow
import caeml.runner.runner_local_pool
import pkg_codeaster.tools.paraview_clip_x3d as pvclip
import pkg_codeaster.tools.paraview_disp_warp_x3d as pvdispwarp
import pkg_codeaster.tools.paraview_stress_warp_x3d as pvwarp
import pkg_codeaster.tools.paraview_surfacegrid_x3d as pvsurf
import testproject.tests.base
from caeml.common.tool_loader import getCmdTool
from caeml.files.file import File


class CodeAsterBaseTest(testproject.tests.base.CAEMLTestCase):
    def setUp(self):
        # TODO
        self.skipTest(
            'Ci does not support the X-Server yet: vtkXOpenGLRenderWindow (0x4cb7380): bad X server connection. DISPLAY=unixNone. Aborting.')

    def test_stress_warp_deck(self):
        aWorkflow = caeml.common.workflow.Workflow()

        deckCreationTool = pvwarp.ParaviewStressWarpX3DTool()
        deckCreationStep = caeml.common.workflow.Step(name='step1', process=deckCreationTool, parent=aWorkflow)
        aWorkflow.steps['step1'] = deckCreationStep

        # set values
        deckCreationStep.inputPorts['mesh'].fixed_value = File(
            os.path.join(os.path.abspath(os.path.join(__file__, os.pardir)), 'test_data/beam/', 'beam_output.rmed'))

        state = caeml.runner.runner_local_pool.executeAsync(aWorkflow)
        script_file = state.findPortState(deckCreationStep.outputPorts['script_file']).getEvaluation()

        self.assertTrue(True)

    def test_paraview_stress_run(self):
        aWorkflow = caeml.common.workflow.Workflow()

        deckCreationTool = pvwarp.ParaviewStressWarpX3DTool()
        deckCreationStep = caeml.common.workflow.Step(name='step1', process=deckCreationTool, parent=aWorkflow)
        aWorkflow.steps['step1'] = deckCreationStep

        # set values
        deckCreationStep.inputPorts['mesh'].fixed_value = File(
            os.path.join(os.path.abspath(os.path.join(__file__, os.pardir)), 'test_data/beam/', 'beam_output.rmed'))

        paraviewStep = caeml.common.workflow.Step(name='step2', process=getCmdTool('PvBatch'), parent=aWorkflow)
        aWorkflow.steps['step2'] = paraviewStep

        # set values
        paraviewStep.inputPorts['script_file'].setSource(deckCreationStep.outputPorts['script_file'])
        paraviewStep.inputPorts['mesh_file'].fixed_value = File(
            os.path.join(os.path.abspath(os.path.join(__file__, os.pardir)), 'test_data/beam/', 'beam_output.rmed'))

        # set values

        state = caeml.runner.runner_local_pool.executeAsync(aWorkflow)

        res_file = state.findPortState(paraviewStep.outputPorts['results']).getEvaluation()

        self.assertTrue(True)

    def test_paraview_clip_run(self):
        aWorkflow = caeml.common.workflow.Workflow()

        deckCreationTool = pvclip.ParaviewClipX3DTool()
        deckCreationStep = caeml.common.workflow.Step(name='step1', process=deckCreationTool, parent=aWorkflow)
        aWorkflow.steps['step1'] = deckCreationStep

        # set values
        deckCreationStep.inputPorts['mesh'].fixed_value = File(
            os.path.join(os.path.abspath(os.path.join(__file__, os.pardir)), 'test_data/beam/', 'beam_output.rmed'))

        paraviewStep = caeml.common.workflow.Step(name='step2', process=getCmdTool('PvBatch'), parent=aWorkflow)
        aWorkflow.steps['step2'] = paraviewStep

        # set values
        paraviewStep.inputPorts['script_file'].setSource(deckCreationStep.outputPorts['script_file'])
        paraviewStep.inputPorts['mesh_file'].fixed_value = File(
            os.path.join(os.path.abspath(os.path.join(__file__, os.pardir)), 'test_data/beam/', 'beam_output.rmed'))

        # set values

        state = caeml.runner.runner_local_pool.executeAsync(aWorkflow)

        res_file = state.findPortState(paraviewStep.outputPorts['results']).getEvaluation()

        self.assertTrue(True)

    def test_paraview_disp_run(self):
        aWorkflow = caeml.common.workflow.Workflow()

        deckCreationTool = pvdispwarp.ParaviewDispWarpX3DTool()
        deckCreationStep = caeml.common.workflow.Step(name='step1', process=deckCreationTool, parent=aWorkflow)
        aWorkflow.steps['step1'] = deckCreationStep

        # set values
        deckCreationStep.inputPorts['mesh'].fixed_value = File(
            os.path.join(os.path.abspath(os.path.join(__file__, os.pardir)), 'test_data/beam/', 'beam_output.rmed'))

        paraviewStep = caeml.common.workflow.Step(name='step2', process=getCmdTool('PvBatch'), parent=aWorkflow)
        aWorkflow.steps['step2'] = paraviewStep

        # set values
        paraviewStep.inputPorts['script_file'].setSource(deckCreationStep.outputPorts['script_file'])
        paraviewStep.inputPorts['mesh_file'].fixed_value = File(
            os.path.join(os.path.abspath(os.path.join(__file__, os.pardir)), 'test_data/beam/', 'beam_output.rmed'))

        # set values

        state = caeml.runner.runner_local_pool.executeAsync(aWorkflow)

        res_file = state.findPortState(paraviewStep.outputPorts['results']).getEvaluation()

        self.assertTrue(True)

    def test_paraview_surfacegrid_run(self):
        aWorkflow = caeml.common.workflow.Workflow()

        deckCreationTool = pvsurf.ParaviewSurfaceGridX3DTool()
        deckCreationStep = caeml.common.workflow.Step(name='step1', process=deckCreationTool, parent=aWorkflow)
        aWorkflow.steps['step1'] = deckCreationStep

        # set values
        deckCreationStep.inputPorts['mesh'].fixed_value = File(
            os.path.join(os.path.abspath(os.path.join(__file__, os.pardir)), 'test_data/beam/', 'beam_output.rmed'))

        paraviewStep = caeml.common.workflow.Step(name='step2', process=getCmdTool('PvBatch'), parent=aWorkflow)
        aWorkflow.steps['step2'] = paraviewStep

        # set values
        paraviewStep.inputPorts['script_file'].setSource(deckCreationStep.outputPorts['script_file'])
        paraviewStep.inputPorts['mesh_file'].fixed_value = File(
            os.path.join(os.path.abspath(os.path.join(__file__, os.pardir)), 'test_data/beam/', 'beam_output.rmed'))

        # set values

        state = caeml.runner.runner_local_pool.executeAsync(aWorkflow)

        res_file = state.findPortState(paraviewStep.outputPorts['results']).getEvaluation()

        self.assertTrue(True)


if __name__ == '__main__':
    unittest.main()
