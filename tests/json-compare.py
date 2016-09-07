#!/usr/bin/env python
import sys
import json

file1, file2 = sys.argv[1:]

json1 = json.load(open(file1))
json2 = json.load(open(file2))

if json1 != json2:
    sys.exit("Files do not match!")
