__copyright__ = "Copyright 2017 Renumics GmbH (http://www.renumics.com)"
import logging

import caeml.common.base
import caeml.common.process
import caeml.common.states
import caeml.common.workflow
import caeml.tools
import testproject.tests.base
from caeml.api import workflowBuilder
from caeml.common.tool_loader import getCmdTool


class GetDictAndStorage(testproject.tests.base.CAEMLTestCase):
    def setUp(self):
        wf = workflowBuilder.createWorkflow('dummyWorkflow')
        self.sumStep1 = workflowBuilder.createStep(name='aStep', process=getCmdTool('multiply'), parent=wf)
        assert (isinstance(self.sumStep1, caeml.common.workflow.Step))

    def test_step_dict(self):
        aDict = self.sumStep1.getCaemlDict_Recursive()
        logging.getLogger('system').debug(aDict)

    def test_process_dict(self):
        aDict = self.sumStep1.process.getCaemlDict_Recursive()
        logging.getLogger('system').debug(aDict)

    def test_Parameter_dict(self):
        aProcess = self.sumStep1.process
        assert (isinstance(aProcess, caeml.common.process.Process))
        aParameter = next(iter(aProcess.inputParameters.values()))
        assert (isinstance(aParameter, caeml.common.process.Parameter))
        aDict = aParameter.getCaemlDict_Recursive()
        logging.getLogger('system').debug(aDict)

    def test_Parameter_Binding_dict(self):
        aProcess = self.sumStep1.process
        assert (isinstance(aProcess, caeml.common.process.Process))
        aParameter = next(iter(aProcess.inputParameters.values()))
        assert (isinstance(aParameter, caeml.common.process.Parameter))
        aInputBinding = aParameter.inputBinding
        aDict = aParameter.getCaemlDict_Recursive()
        logging.getLogger('system').debug(aDict)
