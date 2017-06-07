__copyright__ = "Copyright 2017 Renumics GmbH (http://www.renumics.com)"
import caeml.common.workflow
import caeml.tools
import testproject.tests.base
from caeml.api import workflowBuilder
from caeml.api import workflowRunner


class test_simple_workflow_api(testproject.tests.base.CAEMLTestCase):
    """Test workflow: addList[1..6] => add1(x, 2) => add2(x,100)  => multiply(x,23)
                                 21 => (21,2)=23  => (23,100)=123 =>  (123,23)= 2829 """

    def setUp(self):  #
        AddDyn_WorkflowAttributes(self)

    def test_execute_a_recently_built_workflow(self):
        workflowState = workflowRunner.executeAsync(self.workflow)
        result = workflowState.findPortState(self.multiplyStep1.outputPorts['product']).getValue()
        self.assertEqual(result, self.exp, "Error! Wrong Result expected {:.2f} got {:.2f}".format(self.exp, result))

    def test_execute_a_loaded_workflow(self):
        id = self.workflow.save()
        bam = caeml.common.workflow.Workflow.load(id)
        workflowState = workflowRunner.executeAsync(bam)
        multiplyStep1Loaded = bam.steps[self.multiplyStep1.name].outputPorts['product']
        result = workflowState.findPortState(multiplyStep1Loaded).getValue()
        self.assertEqual(result, self.exp, "Error! Wrong Result expected {:.2f} got {:.2f}".format(self.exp, result))

    def test_execute_a_workflow_from_loaded_workflowState(self):
        workflowState = workflowRunner.executeAsync(self.workflow)
        result_old = workflowState.findPortState(self.multiplyStep1.outputPorts['product']).getValue()
        resID = workflowState.save()
        bam = caeml.common.states.WorkflowState.load(resID)
        workflowStateNew = workflowRunner.executeAsync(bam.workflow)
        result = workflowStateNew.stepStates['finalMulti'].outputPortStates['product'].getValue()
        self.assertEqual(result, self.exp, "Error! Wrong Result expected {:.2f} got {:.2f}".format(self.exp, result))


def AddDyn_WorkflowAttributes(something):
    something.workflow = workflowBuilder.createWorkflow('TestWorkflow')
    something.sumStep1 = workflowBuilder.createToolStep('add', something.workflow, 'Add0')
    something.sumStep2 = workflowBuilder.createToolStep('add', something.workflow)
    something.multiplyStep1 = workflowBuilder.createToolStep('multiply', something.workflow, 'finalMulti')
    something.sumListStep1 = workflowBuilder.createToolStep('addList', something.workflow)

    # set constants
    something.sumListStep1.inputPorts['addends'].fixed_value = [1, 2, 3, 4, 5, 6]
    something.sumStep1.inputPorts['addend1'].fixed_value = 2
    something.sumStep2.inputPorts['addend1'].fixed_value = 100
    something.multiplyStep1.inputPorts['factor2'].fixed_value = 23

    # connect input/output
    workflowBuilder.connectPorts(something.sumListStep1.outputPorts['sum'], something.sumStep1.inputPorts['addend2'])
    workflowBuilder.connectPorts(something.sumStep1.outputPorts['sum'], something.sumStep2.inputPorts['addend2'])
    workflowBuilder.connectPorts(something.sumStep2.outputPorts['sum'], something.multiplyStep1.inputPorts['factor1'])

    something.exp = float(2829)
