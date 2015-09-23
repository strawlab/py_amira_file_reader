#!/usr/bin/env python
from __future__ import print_function

import py_amira_file_reader.read_amira as read_amira
import numpy as np
import sys, os

import nrrd # called pynrrd on PyPI

import argparse

def convert_file(fname,csv_fname,nrrd_fname):
    data = read_amira.read_amira( fname )
    dlist = data['data']
    merged = {}
    for row in dlist:
        merged.update(row)
    if 'data' not in merged:
        print('Only binary .am files are supported',file=sys.stderr)
        sys.exit(1)
    arr = merged['data']
    with open( csv_fname, mode='w' ) as fd:
        fd.write('id,name\n')
        for name in merged['Parameters']['Materials']:
            this_dict = merged['Parameters']['Materials'][name]
            if 'Id' in this_dict:
                this_id = this_dict['Id']
                fd.write('%d,%r\n'%(this_id,name))
    nrrd.write(nrrd_fname, arr)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('FILE', type=str, help='The file to show')
    args = parser.parse_args()

    fname = args.FILE
    csv_fname = fname+'.csv'
    nrrd_fname = fname+'.nrrd'

    for test_fname in [csv_fname, nrrd_fname]:
        if os.path.exists(test_fname):
            print('ERROR: will not overwrite output file %r'%test_fname, file=sys.stderr)
            sys.exit(1)

    convert_file( fname, csv_fname, nrrd_fname)

if __name__=='__main__':
    main()
