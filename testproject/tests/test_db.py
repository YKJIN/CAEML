__copyright__ = "Copyright 2017 Renumics GmbH (http://www.renumics.com)"
from bson import DBRef

import caeml.common.db as db
import testproject.tests.base


class FileBasedWorkflowTest(testproject.tests.base.CAEMLTestCase):
    def test_queryWithKnownCollection(self):
        toolDict = db.get_dictByQuery({'name': 'multiply'}, collection_name='caeml.common.tools')
        self.assertIsNotNone(toolDict, "Tool Dict was None")
        self.assertEqual(toolDict['name'], 'multiply')
        self.assertIsNone(db.get_dictByQuery({'name': 'caeml.common.tools'}))

    def test_queryWithUnKnownCollection(self):
        toolDict = db.get_dictByQuery({'name': 'multiply'})
        self.assertIsNotNone(toolDict, "Tool Dict was None")
        self.assertEqual(toolDict['name'], 'multiply')
        self.assertIsNone(db.get_dictByQuery({'name': 'no.tool.will.ever.be.called.like.this'}))

    def test_addToCollection(self):
        db.create_collection('test.collection')
        data = {'_id': '1234567890', 'content': 'testcontent'}
        db.add_oneDictIntoCollection(data, 'test.collection')
        db.get_db().drop_collection('test.collection')

        db.add_oneDictIntoCollection(data, 'test.collection')

    def test_dereference(self):
        data = {'_id': '1234567890', 'content': 'testcontent'}
        ref = DBRef('test.collection', '1234567890')
        db.add_oneDictIntoCollection(data, 'test.collection')

        self.assertEqual(data, db.dereference(ref))

    def test_replace(self):
        data = {'_id': '1234567890', 'content': 'testcontent'}
        db.add_oneDictIntoCollection(data, 'test.collection')

        first_load = db.get_dictById(data['_id'])

        data = {'_id': '1234567890', 'content': 'newtestcontent'}

        db.replace_oneDictInCollection(data, 'test.collection')

        second_load = db.get_dictById(data['_id'])

        self.assertEqual(second_load['_id'], first_load['_id'])
        self.assertEqual(first_load['content'], 'testcontent')
        self.assertEqual(second_load['content'], 'newtestcontent')

    def test_oneDictByIdWithUnKnownCollection(self):
        data = {'_id': '1234567890', 'content': 'testcontent'}
        db.add_oneDictIntoCollection(data, 'test.collection')
        aDict = db.get_dictById('1234567890')
        self.assertIsNotNone(aDict)
        self.assertEqual(data['_id'], aDict['_id'])

        self.assertIsNone(db.get_dictById('no.tool.will.ever.have.an.id.like.this'))

    def test_oneDictByIdWithKnownCollection(self):
        data = {'_id': '1234567890', 'content': 'testcontent'}
        db.add_oneDictIntoCollection(data, 'test.collection')
        aDict = db.get_dictById('1234567890', 'test.collection')
        self.assertIsNotNone(aDict)
        self.assertEqual(data['_id'], aDict['_id'])

        self.assertIsNone(db.get_dictById('no.tool.will.ever.have.an.id.like.this', 'test.collection'))

    def tearDown(self):
        db.get_db().drop_collection('test.collection')
