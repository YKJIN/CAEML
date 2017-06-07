__copyright__ = "Copyright 2017 Renumics GmbH (http://www.renumics.com)"
if __name__ == "__main__":
    import sys
    import os
    import unittest

    path = os.path.dirname(__file__)

    suite = unittest.TestLoader().discover(path, pattern="test_*.py")
    runner = unittest.TextTestRunner(verbosity=0)
    res = not runner.run(suite).wasSuccessful()

    sys.exit(res)
