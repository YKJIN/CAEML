#!/usr/bin/python
__copyright__ = "Copyright 2017 Renumics GmbH (http://www.renumics.com)"

import subprocess
import sys

script_file = sys.argv[1]

subprocess.Popen("/opt/salome/appli_V2016/runSession pvbatch --use-offscreen-rendering " + script_file,
                 shell=True).wait()
