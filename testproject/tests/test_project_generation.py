__copyright__ = "Copyright 2017 Renumics GmbH (http://www.renumics.com)"
# TODO: running this test alone give an error:
# ERROR: test_init_db (test_project_generation.TestProjectGeneration)
# ----------------------------------------------------------------------
# Traceback (most recent call last):
#   File "/home/markus/caeml/testproject/tests/test_project_generation.py", line 19, in setUp
#     if hasattr(settings, 'TEST_PROJECT_DIRECTORY'):
#   File "/home/markus/caeml/caeml/management/conf/base.py", line 88, in __getattr__
#     raise LookupError("Settings need to be configured before they are used")
# LookupError: Settings need to be configured before they are used

import logging
import os
import shutil

from jinja2 import Template

import caeml
import caeml.management.commands.init_project as init_project
import testproject.tests.base


class TestProjectGeneration(testproject.tests.base.CAEMLTestCase):
    def setUp(self):
        self.directory = os.path.dirname(__file__)
        from caeml.management.conf import settings
        self.test_directory = os.path.join(self.directory, 'test_project_directory')
        if hasattr(settings, 'TEST_PROJECT_DIRECTORY'):
            self.test_directory = settings.TEST_PROJECT_DIRECTORY
        self.settings_file = os.path.join(self.test_directory, 'settings.py')
        self.caeml_path = os.path.abspath(os.path.join(os.path.dirname(caeml.__file__), os.path.pardir))
        if os.path.exists(self.test_directory):
            shutil.rmtree(self.test_directory)

        script_file = os.path.abspath(init_project.__file__)
        proj_creation_command = "python3 {} {}".format(script_file, self.test_directory)
        logging.getLogger('system').debug(proj_creation_command)
        os.system(proj_creation_command)

        shutil.copyfile(src=os.path.abspath(os.path.join(self.directory, os.pardir, 'settings.py')),
                        dst=self.settings_file)

    # TODO test_a the a is necessary to ensure that settings.py is changed before it is loaded by the system
    def test_a_local_settings_file(self):
        test_var_name = "TEST_LOCAL_SETTINGS_FILE_STRING"
        test_var_val = "Local Settings Setup Test File String Content"
        with open(self.settings_file, "a") as myfile:
            myfile.write("\n")
            myfile.write("{} = '{}'".format(test_var_name, test_var_val))
            myfile.write("\n")

        file_template = Template("""
import caeml
import logging
import settings as local_settings
from caeml.management.conf import settings

caeml.init(local_settings)

logging.getLogger('system').debug("Testing Settings Mechanism")

exitcode = 1
if settings.{{ var_name }} == "{{ var_value }}":
    exitcode = 0
exit(exitcode)
""")
        settings_file_path = os.path.join(self.test_directory, 'settings_test_script.py')
        with open(settings_file_path, 'w') as file:
            file_content = file_template.render({'var_name': test_var_name, 'var_value': test_var_val})
            file.write(file_content)

        py_command = "PYTHONPATH={}:{} python3 {}".format(self.test_directory, self.caeml_path, settings_file_path)
        logging.getLogger('system').debug(py_command)
        exit_code = (os.system(py_command))
        res = exit_code >> 8
        # signal_num = exit_code % 256

        self.assertEqual(res, 0, "Settings File was not set correctly")

    def test_init_db(self):
        file_template = Template("""
import unittest
import os
import settings as local_settings
import caeml
from caeml.management.conf import settings
caeml.init(local_settings)
import caeml.common.process
from caeml.management import execute_from_command_line
import caeml.common.states
import caeml.common.workflow
import caeml.common.workflow
import testproject.tests.base
from caeml.api import workflowBuilder
from caeml.api import workflowRunner
from caeml.api.workflowBuilder import getCmdTool

#caeml.init(local_settings)
execute_from_command_line(['manage.py', 'init_filesystem'])
execute_from_command_line(['manage.py', 'init_logger'])
execute_from_command_line(['manage.py', 'init_db'])

exp=2829

class dummy(object):
    @classmethod
    def start(self):

        ###########copy paste from test_simple_workflow.setUP#########
        self.workflow = workflowBuilder.createWorkflow('TestWorkflow')

        self.sumStep1 = workflowBuilder.createStep(name='step1', parent=self.workflow, process=getCmdTool('add'))
        self.sumStep2 = workflowBuilder.createStep(name='step2', parent=self.workflow, process=getCmdTool('add'))
        self.multiplyStep1 = workflowBuilder.createStep(name='step3', parent=self.workflow,
                                                        process=getCmdTool('multiply'))
        self.sumListStep1 = workflowBuilder.createStep(name='step10', parent=self.workflow,
                                                       process=getCmdTool('addList'))

        # set constants
        self.sumListStep1.inputPorts[
            'addends'].fixed_value = [1, 2, 3, 4, 5, 6]
        self.sumStep1.inputPorts['addend1'].fixed_value = 2
        self.sumStep2.inputPorts['addend1'].fixed_value = 100
        self.multiplyStep1.inputPorts['factor2'].fixed_value = 23

        # create steps (not needed when caeml_api is used
        # why is this necessary at all --> ISSUE?
        self.workflow.steps['step1'] = self.sumStep1
        self.sumStep1.name = 'step1'
        self.workflow.steps['step2'] = self.sumStep2
        self.sumStep2.name = 'step2'
        self.workflow.steps['step3'] = self.multiplyStep1
        self.multiplyStep1.name = 'step3'
        self.workflow.steps['step10'] = self.sumListStep1
        self.sumListStep1.name = 'step10'

        # connect input/output
        workflowBuilder.connectPorts(self.sumListStep1.outputPorts['sum'], self.sumStep1.inputPorts['addend2'])
        workflowBuilder.connectPorts(self.sumStep1.outputPorts['sum'], self.sumStep2.inputPorts['addend2'])
        workflowBuilder.connectPorts(self.sumStep2.outputPorts['sum'], self.multiplyStep1.inputPorts['factor1'])

        self.exp = float(2829)

        ##########copy paste from test_simple_workflow.test_execute_a_recently_built_workflow########
        workflowState = workflowRunner.executeAsync(
            self.workflow)
        assert (isinstance(workflowState, caeml.common.states.WorkflowState))
        result = float(workflowState.stepStates['step3'].outputPortStates['product'].getValue())

        return result

result = dummy.start()

exit_code = 1
if result == exp:
    exit_code = 0

exit(exit_code)
""")
        settings_file_path = os.path.join(self.test_directory, 'workflow_test_script.py')
        with open(settings_file_path, 'w') as file:
            file.write(file_template.render())

        py_command = "PYTHONPATH={}:{} python3 {}".format(self.test_directory, self.caeml_path, settings_file_path)
        logging.getLogger('system').debug(py_command)
        exit_code = (os.system(py_command))
        res = exit_code >> 8
        # signal_num = exit_code % 256

        self.assertEqual(res, 0, "Workflow was not set correctly")

    def tearDown(self):
        if os.path.exists(self.test_directory):
            shutil.rmtree(self.test_directory)
