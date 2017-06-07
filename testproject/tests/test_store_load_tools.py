__copyright__ = "Copyright 2017 Renumics GmbH (http://www.renumics.com)"
import pymongo.database

from caeml.common.db import get_db
from caeml.common.tool_loader import getCmdTool
from caeml.common.tools import CommandLineTool
from testproject.tests.base import CAEMLTestCase


class TestToolStoreLoadDB(CAEMLTestCase):
    def setUp(self):
        self.skipTest('getCmdTool rewrite (YAML)')
        db = get_db()
        assert isinstance(db, pymongo.database.Database)
        self.tools_collection = db.get_collection('caeml.common.tools.CommandLineTool')
        self.tools_collection.remove()

    def test_loading_non_existing_tools(self):
        self.assertEqual(self.tools_collection.count(), 0, "Tools collection was not empty")
        tool = getCmdTool('add')
        self.assertEqual(self.tools_collection.count(), 1, "Add tool was not added to Tools collection")
        tool = getCmdTool('add')
        self.assertLessEqual(self.tools_collection.count(), 1, "Add tool was added to Tools collection again")
        tool = getCmdTool('addList')
        self.assertEqual(self.tools_collection.count(), 2, "addlist tool was not added to Tools collection")

    def test_saved_name_of_tool(self):
        tool = getCmdTool('multiply')
        loaded_tool = self.tools_collection.find_one({'name': 'multiply'})
        self.assertEqual(loaded_tool['name'], tool.name)

    def test_saved_dict_of_tool(self):
        tool = getCmdTool('post_processing/x3dexport_clip')
        loaded_tool = self.tools_collection.find_one({'name': 'x3dExport_Clip'})
        assert isinstance(tool, CommandLineTool)
        self.assertEqual(tool._id, loaded_tool['_id'])
        self.assertEqual(tool.name, loaded_tool['name'])
        self.assertEqual(tool.baseCommand, loaded_tool['baseCommand'])
        self.assertEqual(tool.processClass, loaded_tool['processClass'])
        tool_dict = tool.getCaemlDict_Recursive()
        self.assertTrue(tool_dict['inputParameters'] == loaded_tool['inputParameters'])
        self.assertTrue(tool_dict['outputParameters'] == loaded_tool['outputParameters'])
