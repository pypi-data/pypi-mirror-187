"""
Unittests for gridcode module

TODO: _gridcode_filename
TODO: _add_code
TODO: _indent_block
TODO: _increment_indent_depth
TODO: _generate_grid_code
TODO: _write_gridcode_system_call
TODO: _load_grid_function
TODO: _last_grid_variable
"""

import os
import shutil
import unittest

from binarycpython.utils.functions import temp_dir

TMP_DIR = temp_dir("tests", "test_gridcode")
shutil.rmtree(TMP_DIR)
os.makedirs(TMP_DIR, exist_ok=True)


if __name__ == "__main__":
    unittest.main()
