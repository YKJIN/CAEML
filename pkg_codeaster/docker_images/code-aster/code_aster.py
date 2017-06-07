#!/usr/bin/python
__copyright__ = "Copyright 2017 Renumics GmbH (http://www.renumics.com)"

import subprocess
import sys

export_file = sys.argv[1]

subprocess.Popen("/opt/salome/V2016/tools/Code_aster_frontend-20160/bin/as_run " + export_file, shell=True).wait()
