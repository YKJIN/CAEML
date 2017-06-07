#!/usr/bin/python
__copyright__ = "Copyright 2017 Renumics GmbH (http://www.renumics.com)"

import argparse

parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('--addends', dest="addends", type=float, nargs='+')

args = parser.parse_args()

print(sum(args.addends))
