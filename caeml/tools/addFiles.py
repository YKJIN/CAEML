#!/usr/bin/python
__copyright__ = "Copyright 2017 Renumics GmbH (http://www.renumics.com)"
import csv
import sys

url = sys.argv[1]
url2 = sys.argv[2]
aSum = 0

with open(url, 'r') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
    for row in spamreader:
        for col in row:
            aSum = aSum + float(col)

with open(url2, 'r') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
    for row in spamreader:
        for col in row:
            aSum = aSum + float(col)

print(aSum)
