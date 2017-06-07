__copyright__ = "Copyright 2017 Renumics GmbH (http://www.renumics.com)"
import caeml.common.process
import caeml.common.states
import caeml.common.workflow
import caeml.common.workflow
import testproject.tests.base
from caeml.api import workflowBuilder
from caeml.api import workflowRunner
from caeml.api.workflowBuilder import getCmdTool


class TestSimpleWorkflow(testproject.tests.base.CAEMLTestCase):
    """Test workflow: addList[1..6] => add1(x, 2) => add2(x,100)  => multiply(x,23)
                                 21 => (21,2)=23  => (23,100)=123 =>  (123,23)= 2829 """

    def setUp(self):
        AddDyn_WorkflowAttributes_NoAPI(self)

    def test_execute_a_recently_built_workflow(self):
        workflowState = workflowRunner.executeAsync(self.workflow)
        assert (isinstance(workflowState, caeml.common.states.WorkflowState))
        result = float(workflowState.stepStates['step3'].outputPortStates['product'].getValue())
        self.assertEqual(result, self.exp, "Error! Wrong Result expected {:.2f} got {:.2f}".format(self.exp, result))

    def test_execute_a_workflow_from_db(self):
        id = self.workflow.save()
        bam = caeml.common.workflow.Workflow.load(id)
        workflowState = workflowRunner.executeAsync(bam)
        result = float(workflowState.stepStates['step3'].outputPortStates['product'].getValue())
        self.assertEqual(result, self.exp, "Error! Wrong Result expected {:.2f} got {:.2f}".format(self.exp, result))

    def test_execute_a_workflow_from_loaded_workflowState(self):
        workflowState = workflowRunner.executeAsync(self.workflow)
        assert (isinstance(workflowState, caeml.common.states.WorkflowState))
        result = float(workflowState.stepStates['step3'].outputPortStates['product'].getValue())
        self.assertEqual(result, result, "Error! Wrong Result expected {:.2f} got {:.2f}".format(self.exp, result))

        # error: this writes workflow steps with processes as dicts
        resID = workflowState.save()
        bam = caeml.common.states.WorkflowState.load(resID)
        workflowStateNew = workflowRunner.executeAsync(bam.workflow)
        result = float(workflowStateNew.stepStates['step3'].outputPortStates['product'].getValue())
        self.assertEqual(result, self.exp, "Error! Wrong Result expected {:.2f} got {:.2f}".format(self.exp, result))


def AddDyn_WorkflowAttributes_NoAPI(something):
    something.workflow = workflowBuilder.createWorkflow('TestWorkflow')

    something.sumStep1 = workflowBuilder.createStep(name='step1', parent=something.workflow, process=getCmdTool('add'))
    something.sumStep2 = workflowBuilder.createStep(name='step2', parent=something.workflow, process=getCmdTool('add'))
    something.multiplyStep1 = workflowBuilder.createStep(name='step3', parent=something.workflow,
                                                         process=getCmdTool('multiply'))
    something.sumListStep1 = workflowBuilder.createStep(name='step10', parent=something.workflow,
                                                        process=getCmdTool('addList'))

    # set constants
    something.sumListStep1.inputPorts['addends'].fixed_value = [1, 2, 3, 4, 5, 6]
    something.sumStep1.inputPorts['addend1'].fixed_value = 2
    something.sumStep2.inputPorts['addend1'].fixed_value = 100
    something.multiplyStep1.inputPorts['factor2'].fixed_value = 23

    # connect input/output
    workflowBuilder.connectPorts(something.sumListStep1.outputPorts['sum'], something.sumStep1.inputPorts['addend2'])
    workflowBuilder.connectPorts(something.sumStep1.outputPorts['sum'], something.sumStep2.inputPorts['addend2'])
    workflowBuilder.connectPorts(something.sumStep2.outputPorts['sum'], something.multiplyStep1.inputPorts['factor1'])

    something.exp = 2829
