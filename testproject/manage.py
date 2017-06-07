#!/usr/bin/env python
__copyright__ = "Copyright 2017 Renumics GmbH (http://www.renumics.com)"
import sys

import caeml
import testproject.settings

caeml.init(testproject.settings)

if __name__ == "__main__":
    from caeml.management import execute_from_command_line

    execute_from_command_line(sys.argv)
