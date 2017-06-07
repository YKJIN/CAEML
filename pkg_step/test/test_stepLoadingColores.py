__copyright__ = "Copyright 2017 Renumics GmbH (http://www.renumics.com)"
import os
import unittest

from caeml.api import workflowBuilder
from caeml.api import workflowRunner
from testproject.tests.base import CAEMLTestCase

from pkg_step.tools.coloredStepAnalyzer import StepAnalyzer

from pkg_step.data_model.types import StepGeometry

class ColoredStepMeshingTest(CAEMLTestCase):

    def setUp(self):
        self.workflow = workflowBuilder.createWorkflow('StepLoadingWorkflow')
        self.stepStep = workflowBuilder.createStep(name='stepAnalyze', parent=self.workflow,
                                              process=StepAnalyzer())

    def test_load_colored_step_1(self):

        step_file_path = os.path.join(os.path.dirname(__file__), 'test_data', 'baseketball_part_colored.step')

        self.stepStep.inputPorts['input_step'].fixed_value = step_file_path


        aWorkflowState = workflowRunner.executeAsync(self.workflow)
        x = aWorkflowState.findPortState(self.stepStep.outputPorts['step']).getValue()

        assert isinstance(x, StepGeometry)
        self.assertEqual(len(x.surfaceGroups), 4,
                         "Error! Number of surface Groups is not correct got {:d} but expected{:d}"
                         .format(len(x.surfaceGroups), 4))
        self.assertEqual(len(x.surfaces), 8,
                         "Error! Number of surfaces is not correct got {:d} but expected{:d}"
                         .format(len(x.surfaces), 8))

    def test_load_partly_colored_step(self):

        step_file_path = os.path.join(os.path.dirname(__file__), 'test_data', 'baseketball_part_colored_partly.step')

        self.stepStep.inputPorts['input_step'].fixed_value = step_file_path


        aWorkflowState = workflowRunner.executeAsync(self.workflow)
        x = aWorkflowState.findPortState(self.stepStep.outputPorts['step']).getValue()

        assert isinstance(x, StepGeometry)
        self.assertEqual(len(x.surfaceGroups), 4,
                         "Error! Number of surface Groups is not correct got {:d} but expected{:d}"
                         .format(len(x.surfaceGroups), 3))
        self.assertEqual(len(x.surfaces), 42,
                         "Error! Number of surfaces is not correct got {:d} but expected{:d}"
                         .format(len(x.surfaces), 42))


    def test_load_colored_step_2(self):

        step_file_path = os.path.join(os.path.dirname(__file__), 'test_data', 'bar2.step')

        self.stepStep.inputPorts['input_step'].fixed_value = step_file_path


        aWorkflowState = workflowRunner.executeAsync(self.workflow)
        x = aWorkflowState.findPortState(self.stepStep.outputPorts['step']).getValue()

        assert isinstance(x, StepGeometry)
        self.assertEqual(len(x.surfaceGroups), 3,
                         "Error! Number of surface Groups is not correct got {:d} but expected{:d}"
                         .format(len(x.surfaceGroups), 3))
        self.assertEqual(len(x.surfaces), 6,
                         "Error! Number of surfaces is not correct got {:d} but expected{:d}"
                         .format(len(x.surfaces), 6))


if __name__ == '__main__':
    unittest.main()
