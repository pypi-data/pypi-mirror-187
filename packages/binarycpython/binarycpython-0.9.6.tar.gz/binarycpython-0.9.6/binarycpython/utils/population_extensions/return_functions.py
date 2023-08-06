"""
Main script to provide the return functions class extension.

This consists of the following class methods:
- return_population_settings
- return_binary_c_defaults
- return_all_info
- export_all_info
"""

import copy
import json

# pylint: disable=E1101
import os
from typing import Union

from binarycpython.utils.ensemble import binaryc_json_serializer
from binarycpython.utils.functions import get_help_all, now


class return_functions:
    """
    Extension for the Population class containing the code for return function
    """

    def __init__(self, **kwargs):
        """
        Init function for the spacing_functions class
        """

        return

    ###################################################
    # Return functions
    ###################################################

    def return_population_settings(self) -> dict:
        """
        Function that returns all the options that have been set.

        Can be combined with JSON to make a nice file.

        Returns:
            dictionary containing "bse_options", "grid_options", "custom_options"
        """
        options = {
            "bse_options": self.bse_options,
            "grid_options": self.grid_options,
            "custom_options": self.custom_options,
        }

        return options

    def return_binary_c_defaults(self):
        """
        Function that returns the defaults of the binary_c version that is used.
        """

        return self.defaults

    def return_all_info(
        self,
        include_population_settings: bool = True,
        include_binary_c_defaults: bool = True,
        include_binary_c_version_info: bool = True,
        include_binary_c_help_all: bool = True,
    ) -> dict:
        """
        Function that returns all the information about the population and binary_c

        Args:
            include_population_settings:
                whether to include the population_settings (see function return_population_settings)
            include_binary_c_defaults:
                whether to include a dict containing the binary_c parameters and their default
                values
            include_binary_c_version_info:
                whether to include a dict containing all the binary_c version info
                (see return_binary_c_version_info)
            include_binary_c_help_all:
                whether to include a dict containing all the information about
                the binary_c parameters (see get_help_all)

        Return:
            dictionary containing all, or part of, the above dictionaries
        """

        #
        all_info = {}
        #
        if include_population_settings:
            population_settings = self.return_population_settings()
            all_info["population_settings"] = population_settings

        #
        if include_binary_c_defaults:
            binary_c_defaults = self.return_binary_c_defaults()
            all_info["binary_c_defaults"] = binary_c_defaults

        if include_binary_c_version_info:
            binary_c_version_info = self.return_binary_c_version_info(parsed=True)
            all_info["binary_c_version_info"] = binary_c_version_info

        if include_binary_c_help_all:
            binary_c_help_all_info = get_help_all(print_help=False)
            all_info["binary_c_help_all"] = binary_c_help_all_info

        return all_info

    def export_all_info(
        self,
        use_datadir: bool = True,
        outfile: Union[str, None] = None,
        include_population_settings: bool = True,
        include_binary_c_defaults: bool = True,
        include_binary_c_version_info: bool = True,
        include_binary_c_help_all: bool = True,
        ensure_ascii: str = False,
        indent: int = 4,
    ) -> Union[str, None]:
        """
        Function that exports the all_info to a JSON file

        Tasks:
            - TODO: Fix to write things to the directory. which options do which etc
            - TODO: there's flawed logic here. rewrite this part pls
            - TODO: consider actually just removing the whole 'output to file' part and let the
                user do this.

        Args:
            include_population_settings: whether to include the population_settings
                (see function return_population_settings)
            include_binary_c_defaults: whether to include a dict containing the binary_c parameters
                and their default values
            include_binary_c_version_info: whether to include a dict containing all the binary_c
                version info (see return_binary_c_version_info)
            include_binary_c_help_all: whether to include a dict containing all the information
                about the binary_c parameters (see get_help_all)
            use_datadir: Boolean whether to use the custom_options['data_dir'] to write the file to.
                If the  custom_options["base_filename"] is set, the output file will be called
                <custom_options["base_filename"]>_settings.json. Otherwise a file called
                simulation_<date+time>_settings.json will be created
            outfile: if use_datadir is false, a custom filename will be used
            ensure_ascii: the ensure_ascii flag passed to json.dump and/or json.dumps
                           (Default: False)
            indent: indentation passed to json.dump and/or json.dumps (default 4)
        """

        all_info = self.return_all_info(
            include_population_settings=include_population_settings,
            include_binary_c_defaults=include_binary_c_defaults,
            include_binary_c_version_info=include_binary_c_version_info,
            include_binary_c_help_all=include_binary_c_help_all,
        )

        # Copy dict
        all_info_cleaned = copy.deepcopy(all_info)

        if use_datadir:
            if self.custom_options.get("data_dir", None):
                if not self.custom_options.get("base_filename", None):
                    base_name = "simulation_{}".format(now(style="nospace"))
                else:
                    base_name = os.path.splitext(self.custom_options["base_filename"])[
                        0
                    ]

                # save settings as gzipped JSON
                settings_name = base_name + "_settings.json.gz"

                # Check directory, make if necessary
                os.makedirs(self.custom_options["data_dir"], exist_ok=True)

                settings_fullname = os.path.join(
                    self.custom_options["data_dir"], settings_name
                )

                print("ok")

                # open locked settings file, then output if we get the lock
                (f, lock) = self.locked_open_for_write(settings_fullname, vb=True)
                print("ok")

                if lock and f:
                    self.verbose_print(
                        "Writing settings to {}".format(settings_fullname),
                        self.grid_options["verbosity"],
                        1,
                    )
                    json.dump(
                        all_info_cleaned,
                        f,
                        indent=indent,
                        default=binaryc_json_serializer,
                        ensure_ascii=ensure_ascii,
                    )
                self.locked_close(f, lock)
                return settings_fullname

            # TODO: turn it around and have the exception be within the if statement
            msg = "Exporting all info without passing a value for `outfile` requires custom_options['data_dir'] to be present. That is not the cause. Either set the `data_dir` or pass a value for `outfile` "
            raise ValueError(msg)

        else:
            self.verbose_print(
                "Writing settings to {}".format(outfile),
                self.grid_options["verbosity"],
                1,
            )
            if not outfile.endswith("json"):
                self.verbose_print(
                    "Error: outfile ({}) must end with .json".format(outfile),
                    self.grid_options["verbosity"],
                    0,
                )
                raise ValueError

            with self.open(outfile, "w") as file:
                json.dump(
                    all_info_cleaned,
                    file,
                    indent=indent,
                    default=binaryc_json_serializer,
                    ensure_ascii=ensure_ascii,
                )
            return outfile
