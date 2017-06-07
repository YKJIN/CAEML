__copyright__ = "Copyright 2017 Renumics GmbH (http://www.renumics.com)"
import time
import unittest

from bson.objectid import ObjectId

from caeml.common import db
from testproject.tests import base


class MyTestCase(base.CAEMLTestCase):
    def setUp(self):
        self.db = db.get_db()

    def test_insert_speed(self):

        for no in [1, 10, 100, 1000]:  # , 10000, 100000]:
            for size in [1, 10, 100]:  # , 1000, 10000, 100000]:
                data = {"_id": ObjectId(), "data": {"{:d}".format(n): n * n for n in range(size)}}
                start = time.time()
                for i in range(no):
                    data['_id'] = ObjectId()
                    result = self.db.workflows.insert(data)
                duration = time.time() - start
                print("{:10.5f}s;".format(duration), end="", flush=True)
                self.assertTrue(duration < 5)  # typical values on t460p notebook:< 0.25s
            print("")


if __name__ == '__main__':
    unittest.main()
