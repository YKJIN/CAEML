#!/usr/bin/python
__copyright__ = "Copyright 2017 Renumics GmbH (http://www.renumics.com)"

import argparse

parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('--data', dest="data", type=float, nargs='+')

args = parser.parse_args()

min = min(args.data)
max = max(args.data)
mean = sum(args.data) / len(args.data)

with open('min.txt', 'w') as fileWriter:
    fileWriter.write(str(min) + "\n")

with open('max.txt', 'w') as fileWriter:
    fileWriter.write(str(max) + "\n")

with open('mean.txt', 'w') as fileWriter:
    fileWriter.write(str(mean) + "\n")
