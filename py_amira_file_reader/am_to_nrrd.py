#!/usr/bin/env python
from __future__ import print_function

import py_amira_file_reader.read_amira as read_amira
import numpy as np
import sys

import nrrd # called pynrrd on PyPI

import argparse

def convert_file(fname):
    data = read_amira.read_amira( fname )
    dlist = data['data']
    merged = {}
    for row in dlist:
        merged.update(row)
    if 'data' not in merged:
        print('Only binary .am files are supported',file=sys.stderr)
        sys.exit(1)
    arr = merged['data']
    nrrd.write(fname+'.nrrd', arr)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('FILE', type=str, help='The file to show')
    args = parser.parse_args()
    convert_file(args.FILE)

if __name__=='__main__':
    main()
