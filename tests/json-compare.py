#!/usr/bin/env python
import sys
import json

file1, file2 = sys.argv[1:]

json1 = json.load(open(file1))
json2 = json.load(open(file2))

if 'debug' in json2:
    json2.pop('debug')

def unpack_diff(json1, json2, prefix=''):
    if isinstance(json1, list) and isinstance(json2, list):
        for i, (val1, val2) in enumerate(zip(json1, json2)):
            unpack_diff(val1, val2, prefix + '[%s]' % i)
        if len(json1) != len(json2):
            print('len(%s)' % prefix, len(json1), '!=', len(json2))

    elif isinstance(json1, dict) and isinstance(json2, dict):
        if prefix:
            prefix += '.'
        for key in sorted(set(json1.keys()) | set(json2.keys())):
            val1 = json1.get(key)
            val2 = json2.get(key)
            unpack_diff(val1, val2, prefix + key)

    elif json1 != json2:
        print(prefix, json1, '!=', json2)

if json1 != json2:
    unpack_diff(json1, json2)
    sys.exit("Files do not match!")
