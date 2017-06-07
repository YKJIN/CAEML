__copyright__ = "Copyright 2017 Renumics GmbH (http://www.renumics.com)"
import testproject.tests.base
from caeml.api import workflowBuilder
from caeml.api import workflowRunner


class ArtificialDemoTestCase(testproject.tests.base.CAEMLTestCase):
    def test_workflow_in_workflow(self):
        """Test workflow:  add(1, 2) =>  (( add(x, 3) => multi(x, 4) => )) add(x, 5)
                                 3   =>   add(3,3)=6  => multi(6,4)=24 =>  add(24,5)=29"""

        # create nested workflow with one input and one output parameter
        aWorkflowABC = workflowBuilder.createWorkflow('ArtificialDemoTestCase-aWorkflowABC')
        sumStepA = workflowBuilder.createToolStep(toolId='caeml.tools.add.add', parent=aWorkflowABC)
        sumStepA.inputPorts['addend1'].fixed_value = 3
        sumStepA.inputPorts['addend2'].exposed_as = 'IN'
        multiStepB = workflowBuilder.createToolStep(toolId='multiply', parent=aWorkflowABC)
        multiStepB.inputPorts['factor2'].fixed_value = 4
        workflowBuilder.connectPorts(sumStepA.outputPorts['sum'], multiStepB.inputPorts['factor1'])
        workflowBuilder.connectPorts(sumStepA.outputPorts['sum'], multiStepB.inputPorts['factor1'])
        multiStepB.outputPorts['product'].exposed_as = 'OUT'

        # add basic workflow steps, assign values and connect parameters
        aWorkflow = workflowBuilder.createWorkflow('ArtificialDemoTestCase-aWorkflow')
        sumStep1 = workflowBuilder.createToolStep(toolId='add', parent=aWorkflow)
        sumStep3 = workflowBuilder.createToolStep(toolId='add', parent=aWorkflow)
        aWorkflowABCStep = workflowBuilder.createStep(process=aWorkflowABC, parent=aWorkflow, name='aWorkflowABCStep')

        # assign input values
        sumStep1.inputPorts['addend1'].fixed_value = 1
        sumStep1.inputPorts['addend2'].fixed_value = 2
        sumStep3.inputPorts['addend1'].fixed_value = 5

        # plug workflowABC into aWorkflow
        inPorts = aWorkflowABCStep.inputPorts
        workflowBuilder.connectPorts(sumStep1.outputPorts['sum'], inPorts['IN'])

        exPorts = aWorkflowABCStep.outputPorts
        workflowBuilder.connectPorts(exPorts['OUT'], sumStep3.inputPorts['addend2'])

        res = workflowRunner.executeAsync(aWorkflow)
        result = res.findPortState(sumStep3.outputPorts['sum']).getValue()
        exp = float(29)
        self.assertEqual(result, exp, "Error! Wrong Result expected {:.2f} got {:.2f}".format(exp, result))
