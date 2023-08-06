"""
Main script to provide the custom generator sampling class extension
"""

# pylint: disable=E1101

from collections.abc import Iterable  # drop `.abc` with Python 2.7 or lower


class custom_generator_sampling:
    """
    Extension for the Population class containing the code for custom_generator sampling functions
    """

    def __init__(self, **kwargs):
        """
        Init function for the spacing_functions class
        """

        return

    def _custom_generator_sampling_cleanup(self):
        """
        Cleanup function for the custom-generator sampling evolution type
        """

    def _custom_generator_sampling_get_generator(self):
        """
        Function to get the generator for the _custom_generator_sampling sampling method. Called by _get_generator and used in the actual evolution loop.
        """

        generator = self.grid_options["custom_generator"]

        return generator

    def _custom_generator_sampling_setup(self):
        """
        Function to prepare the class for sampling via a custom generator
        """

        if not isinstance(self.grid_options["custom_generator"], Iterable):
            print(
                "Error. provided no or wrong custom value for the system generator (custom_generator: {})".format(
                    self.grid_options["custom_generator"]
                )
            )
            raise ValueError
