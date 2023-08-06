"""
Unittests for spacing_functions module


TODO: const_linear
TODO: const_int
TODO: const_ranges
TODO: peak_normalized_gaussian_func
TODO: gaussian_zoom
TODO: const_dt
"""

import os
import shutil
import unittest

import numpy as np

from binarycpython.utils.functions import Capturing, temp_dir
from binarycpython.utils.population_class import Population

TMP_DIR = temp_dir("tests", "test_spacing_functions")

shutil.rmtree(TMP_DIR)
os.makedirs(TMP_DIR, exist_ok=True)
distribution_functions_pop = Population()


class test_spacing_functions(unittest.TestCase):
    """
    Unit test for spacing functions
    """

    def test_const(self):
        with Capturing() as _:
            self._test_const()

    def _test_const(self):
        """
        Unittest for function const
        """

        const_return = distribution_functions_pop.const_linear(1, 10, 10)
        self.assertTrue(
            (const_return == np.linspace(1, 10, 10 + 1)).all(),
        )


if __name__ == "__main__":
    unittest.main()
