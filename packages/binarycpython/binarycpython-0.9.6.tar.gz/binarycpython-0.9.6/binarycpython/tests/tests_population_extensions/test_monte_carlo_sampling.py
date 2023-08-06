"""
Test routines for the monte-carlo sampling
"""

import unittest

from binarycpython import Population
from binarycpython.utils.functions import Capturing, temp_dir

TMP_DIR = temp_dir("tests", "test_monte_carlo_sampling")


class test_mass_treshold_class(unittest.TestCase):
    """
    Class for unit test of mass treshold
    """

    def test_mass_treshold(self):
        with Capturing() as _:
            self._test_mass_treshold()

    def _test_mass_treshold(self):
        """
        Unittest for the function flat
        """

        monte_carlo_pop = Population(tmp_dir=TMP_DIR, evolution_type="monte_carlo")

        #
        monte_carlo_pop.set(
            monte_carlo_mass_threshold=10, _actually_evolve_system=False
        )

        # run systems
        print(monte_carlo_pop.grid_options["_total_mass_run"])

        monte_carlo_pop.evolve()


if __name__ == "__main__":
    print("yo")
    test = test_mass_treshold_class()
    test.test_mass_treshold()
