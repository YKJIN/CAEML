__copyright__ = "Copyright 2017 Renumics GmbH (http://www.renumics.com)"
import caeml.api.workflowBuilder as workflowBuilder
import testproject.tests.base
from caeml.api import workflowRunner


class FileBasedWorkflowTest(testproject.tests.base.CAEMLTestCase):
    def test1_FileBasedWorkflowTest_test1(self):
        # new workflow
        aWorkflow = workflowBuilder.createWorkflow('test1_FileBasedWorkflowTest_test1')

        # add new workflow steps
        # aCmdAddTool = caeml.tools.generated_tools.add()
        aStats = workflowBuilder.createToolStep('stats', aWorkflow)
        aSum = workflowBuilder.createToolStep('addFiles', aWorkflow)

        # set values
        aStats.inputPorts['data'].fixed_value = [1, 2, 3, 4, 5, 6, 7]

        # connect
        workflowBuilder.connectPorts(aStats.outputPorts['max'], aSum.inputPorts['addend1'])
        workflowBuilder.connectPorts(aStats.outputPorts['min'], aSum.inputPorts['addend2'])

        # print(yaml.dump(aWorkflow))
        state = workflowRunner.executeAsync(aWorkflow)
        x = state.findPortState(aSum.outputPorts['sum']).getEvaluation()
        self.assertEqual(x, 8)
