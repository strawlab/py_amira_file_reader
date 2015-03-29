from __future__ import print_function
import py_amira_file_reader.read_amira as read_amira
import os

def get_data_path(fname):
    tests_path = os.path.split( __file__ )[0]
    data_path = os.path.join( tests_path, 'data', fname )
    return data_path

def show_result(data):
    result = data['data']
    print('==='*20, 'RESULT')
    import pprint
    for row in result:
        if 'data' not in row:
            pprint.pprint( row )
        else:
            print('<NOT SHOWING DATA>')
        print()

def test_ascii_surf():
    fname = 'tetrahedron.surf'
    data_path = get_data_path(fname)
    data = read_amira.read_amira( data_path )
    if read_amira.is_debug():
        show_result(data)
    assert data['data'][0]['Parameters']['Materials']['Exterior']['id'] == 1
    assert data['data'][1]['Vertices'].shape == (4,3)

def test_binary_am():
    fname = 'LHMask.am'
    data_path = get_data_path(fname)
    data = read_amira.read_amira( data_path )
    if read_amira.is_debug():
        show_result(data)

    # a few spot checks
    assert data['data'][0]['define']['Lattice'] == [50, 50, 50]
