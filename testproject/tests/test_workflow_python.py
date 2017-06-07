__copyright__ = "Copyright 2017 Renumics GmbH (http://www.renumics.com)"
import caeml.common.workflow
import caeml.tools.statsPython
import testproject.tests.base
from caeml.api import workflowBuilder
from caeml.api import workflowRunner
from caeml.tools import statsFilePython


class PythonBasedWorkflowTest(testproject.tests.base.CAEMLTestCase):
    def test1_WorkflowPythonTool_test1(self):
        # new workflow
        aWorkflow = workflowBuilder.createWorkflow('test1_WorkflowPythonTool_test1')

        # add new workflow steps
        # aCmdAddTool = caeml.tools.generated_tools.add()
        aStatsTool = caeml.tools.statsPython.statsTool()
        aStats = workflowBuilder.createStep(name='step1', process=aStatsTool, parent=aWorkflow)
        aSum = workflowBuilder.createToolStep('add', aWorkflow)
        aWorkflow.steps['step1'] = aStats

        # set values
        aStats.inputPorts['data'].fixed_value = [1, 2, 3, 4, 5, 6, 7]

        # connect
        workflowBuilder.connectPorts(aStats.outputPorts['max'], aSum.inputPorts['addend1'])
        workflowBuilder.connectPorts(aStats.outputPorts['min'], aSum.inputPorts['addend2'])

        # print(yaml.dump(aWorkflow))
        state = workflowRunner.executeAsync(aWorkflow)
        x = state.findPortState(aSum.outputPorts['sum']).getEvaluation()
        self.assertEqual(x, 8)

    def test2_WorkflowPythonTool(self):
        # new workflow
        aWorkflow = caeml.common.workflow.Workflow()

        # add new workflow steps
        # aCmdAddTool = caeml.tools.generated_tools.add()
        aStatsTool = caeml.tools.statsFilePython.statsFileTool()
        aStats = workflowBuilder.createStep(name='step1', process=aStatsTool, parent=aWorkflow)
        aSum = workflowBuilder.createToolStep('add', aWorkflow)

        # set values
        aStats.inputPorts['data'].fixed_value = [1, 2, 3, 4, 5, 6, 7]

        # connect
        workflowBuilder.connectPorts(aStats.outputPorts['max'], aSum.inputPorts['addend1'])
        workflowBuilder.connectPorts(aStats.outputPorts['min'], aSum.inputPorts['addend2'])

        # print(yaml.dump(aWorkflow))
        state = workflowRunner.executeAsync(aWorkflow)
        x = state.findPortState(aSum.outputPorts['sum']).getEvaluation()
        self.assertEqual(x, 8)
