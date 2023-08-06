"""
Main script to provide the source-file sampling class extensions.
"""

# pylint: disable=E1101

import os


class source_file_sampling:
    """
    Extension for the Population class containing the code for source-file sampling functions
    """

    def __init__(self, **kwargs):
        """
        Init function for the spacing_functions class
        """

        return

    ###################################################
    # Population from file functions
    #
    # Functions below are used to run populations from
    # a file containing binary_c calls
    ###################################################

    def _source_file_sampling_cleanup(self):
        """
        Cleanup function for the evolution type source file sampling
        """

        # Terminate and close the filehandle
        source_file_filehandle = self.grid_options["_system_generator"]

        source_file_filehandle.close()

    def _source_file_dry_run(self):
        """
        Function to go through the source_file and count the number of lines and the total probability
        """

        system_generator = self.grid_options["_system_generator"]
        total_starcount = 0

        for _ in system_generator:
            total_starcount += 1

        total_starcount = system_generator(self)
        self.grid_options["_total_starcount"] = total_starcount

    def _load_source_file(self, check=False):
        """
        Function that loads the source_file that contains a binary_c calls
        """

        if not os.path.isfile(self.grid_options["source_file_filename"]):
            self.verbose_print(
                "Source file doesnt exist", self.grid_options["verbosity"], 0
            )

        self.verbose_print(
            message="Loading source file from {}".format(
                self.grid_options["gridcode_filename"]
            ),
            verbosity=self.grid_options["verbosity"],
            minimal_verbosity=1,
        )

        # We can choose to perform a check on the source file, which checks if the lines start with 'binary_c'
        if check:
            source_file_check_filehandle = self.open(
                self.grid_options["source_file_filename"], "r", encoding="utf-8"
            )
            for line in source_file_check_filehandle:
                if not line.startswith("binary_c"):
                    failed = True
                    break
            if failed:
                self.verbose_print(
                    "Error, sourcefile contains lines that do not start with binary_c",
                    self.grid_options["verbosity"],
                    0,
                )
                raise ValueError

        source_file_filehandle = self.open(
            self.grid_options["source_file_filename"], "r", encoding="utf-8"
        )

        self.grid_options["_system_generator"] = source_file_filehandle

        self.verbose_print("Source file loaded", self.grid_options["verbosity"], 1)

    def _dict_from_line_source_file(self, line):
        """
        Function that creates a dict from a binary_c arg line
        """
        if line.startswith("binary_c "):
            line = line.replace("binary_c ", "")

        split_line = line.split()
        arg_dict = {}

        for i in range(0, len(split_line), 2):
            if "." in split_line[i + 1]:
                arg_dict[split_line[i]] = float(split_line[i + 1])
            else:
                arg_dict[split_line[i]] = int(split_line[i + 1])

        return arg_dict

    def _source_file_sampling_setup(self):
        """
        setup function for the source file sampling evolution method
        """

        if self.grid_options["do_dry_run"]:
            # Do a dry run
            self._source_file_dry_run()

        print(
            "Total starcount will be: {}".format(self.grid_options["_total_starcount"])
        )

        raise ValueError("This functionality is not available yet")

    def _source_file_sampling_get_generator(self):
        """
        Function to get the generator for the source_file sampling method. Called by _get_generator and used in the actual evolution loop.
        """

        # load source-file
        self._load_source_file()

        generator = self.grid_options["_system_generator"]

        return generator
