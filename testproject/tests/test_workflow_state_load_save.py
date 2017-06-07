__copyright__ = "Copyright 2017 Renumics GmbH (http://www.renumics.com)"
import testproject.tests.base
import testproject.tests.test_workflow_simple


class TestWorkflowLoadSave(testproject.tests.base.CAEMLTestCase):
    """Test workflow: addList[1..6] => add1(x, 2) => add2(x,100)  => multiply(x,23)
                                 21 => (21,2)=23  => (23,100)=123 =>  (123,23)= 2829 """

    def setUp(self):
        testproject.tests.test_workflow_simple.AddDyn_WorkflowAttributes_simple(self)
        # TODO add test for workflow sate (save load)
