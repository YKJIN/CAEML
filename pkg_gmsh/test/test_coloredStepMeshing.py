__copyright__ = "Copyright 2017 Renumics GmbH (http://www.renumics.com)"
import os
import unittest

from caeml.api import workflowBuilder
from caeml.api import workflowRunner
from caeml.api.workflowBuilder import getCmdTool
from testproject.tests.base import CAEMLTestCase

from pkg_gmsh.tools.surfaceGroupsToGeo import SurfaceGroupsToGeo
from pkg_gmsh.tools.meshGeoGmsh import MeshGeoGmsh
from pkg_step.tools.coloredStepAnalyzer import StepAnalyzer

class ColoredStepMeshingTest(CAEMLTestCase):


    def test_geo_to_msh_py(self):

        step_file_path = os.path.join(os.path.dirname(__file__), 'test_data', 'bar2.step')

        workflow = workflowBuilder.createWorkflow('MeshingTestWorkflow')

        stepStep = workflowBuilder.createStep(name='stepAnalyze', parent=workflow,
                                              process=StepAnalyzer())
        meshGeoStep = workflowBuilder.createStep(name='geoStep', parent=workflow,
                                              process=SurfaceGroupsToGeo())

        meshStep = workflowBuilder.createStep(name='meshStep', parent=workflow,
                                              process=MeshGeoGmsh())

        stepStep.inputPorts['input_step'].fixed_value = step_file_path
        meshStep.inputPorts['mergedFile'].fixed_value = step_file_path
        meshStep.inputPorts['clscale'].fixed_value = 1.

        workflowBuilder.connectPorts(stepStep.outputPorts['step'], meshGeoStep.inputPorts['geom_desc'])
        workflowBuilder.connectPorts(meshGeoStep.outputPorts['geo_file'], meshStep.inputPorts['geo'])

        aWorkflowState = workflowRunner.executeAsync(workflow)
        vertsCount = aWorkflowState.findPortState(meshStep.outputPorts['vertCount']).getValue()
        elemCount = aWorkflowState.findPortState(meshStep.outputPorts['elemCount']).getValue()
        self.assertEqual(vertsCount, 106, "Wrong number of Vertices after meshing")
        self.assertLessEqual(elemCount, 513, "No Elements after meshing")
        self.assertGreaterEqual(elemCount, 508, "No Elements after meshing")

    def test_geo_to_msh_py_2(self):

        step_file_path = os.path.join(os.path.dirname(__file__), 'test_data', 'baseketball_part_colored_partly.step')

        workflow = workflowBuilder.createWorkflow('MeshingTestWorkflow')

        stepStep = workflowBuilder.createStep(name='stepAnalyze', parent=workflow,
                                              process=StepAnalyzer())
        meshGeoStep = workflowBuilder.createStep(name='geoStep', parent=workflow,
                                              process=SurfaceGroupsToGeo())

        meshStep = workflowBuilder.createStep(name='meshStep', parent=workflow,
                                              process=MeshGeoGmsh())

        stepStep.inputPorts['input_step'].fixed_value = step_file_path
        meshStep.inputPorts['mergedFile'].fixed_value = step_file_path
        meshStep.inputPorts['clscale'].fixed_value = 1.

        workflowBuilder.connectPorts(stepStep.outputPorts['step'], meshGeoStep.inputPorts['geom_desc'])
        workflowBuilder.connectPorts(meshGeoStep.outputPorts['geo_file'], meshStep.inputPorts['geo'])

        aWorkflowState = workflowRunner.executeAsync(workflow)
        vertsCount = aWorkflowState.findPortState(meshStep.outputPorts['vertCount']).getValue()
        elemCount = aWorkflowState.findPortState(meshStep.outputPorts['elemCount']).getValue()
        self.assertGreater(vertsCount, 0, "No Vertices after meshing")
        self.assertGreater(elemCount, 0, "No Elements after meshing")


if __name__ == '__main__':
    unittest.main()
