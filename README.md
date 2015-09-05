# py_amira_file_reader [![Build Status](https://travis-ci.org/strawlab/py_amira_file_reader.png?branch=master)](https://travis-ci.org/strawlab/py_amira_file_reader)

Read Amira files (AmiraMesh 3D and HyperSurface) in Python.

## API

Use from Python (2.7 or 3.x):

    import py_amira_file_reader.read_amira as read_amira

    data = read_amira.read_amira( 'filename.am' )

Use from the command line to convert a .surf file to a .obj file:

    python -m py_amira_file_reader.amira_to_obj filename.surf

See also the tests and example scripts in the `tests/` and `examples/`
directories.
