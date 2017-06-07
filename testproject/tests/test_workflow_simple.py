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
        AddDyn_WorkflowAttributes_simple(self)

    def test_execute_a_recently_built_workflow(self):
        workflowState = workflowRunner.executeAsync(self.workflow)
        assert (isinstance(workflowState, caeml.common.states.WorkflowState))
        result = float(workflowState.stepStates['multiplyStep'].outputPortStates['product'].getValue())
        self.assertEqual(result, self.exp, "Error! Wrong Result expected {:.2f} got {:.2f}".format(self.exp, result))


def AddDyn_WorkflowAttributes_simple(something):
    something.workflow = workflowBuilder.createWorkflow('TestSimpleWorkflow')

    something.sumStep = workflowBuilder.createStep(parent=something.workflow, process=getCmdTool('add'))
    something.multiplyStep = workflowBuilder.createStep(name='multiplyStep', parent=something.workflow,
                                                        process=getCmdTool('multiply'))

    # set constants
    something.sumStep.inputPorts['addend1'].fixed_value = 2
    something.sumStep.inputPorts['addend2'].fixed_value = 3
    something.multiplyStep.inputPorts['factor2'].fixed_value = 4

    # connect input/output
    workflowBuilder.connectPorts(something.sumStep.outputPorts['sum'], something.multiplyStep.inputPorts['factor1'])

    something.float = float(20)
    something.exp = something.float
