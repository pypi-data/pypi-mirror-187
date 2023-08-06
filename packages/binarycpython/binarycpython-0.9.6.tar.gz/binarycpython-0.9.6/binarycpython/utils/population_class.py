"""
Module containing the Population grid class object.

Here all the functionality of a Population object is defined.

TODO: the save_snapshots and save_snapshot, are they actually distinct?

Tasks:
    - TODO: add functionality to 'on-init' set arguments
    - TODO: type the private functions
    - TODO: fix the correct object types for the default values of the bse_options
    - TODO: think of a clean and nice way to unload and remove the custom_logging_info library from memory (and from disk)
    - TODO: think of a nice way to remove the loaded grid_code/ generator from memory.
    - TODO: Some of the methods that we have defined in the (mixin) class are designed to be used as a portal to information (return_binary_c_version_info for example.) The current design is that they are all instance methods, but that is not always necessary. We can decorate them with @staticmethod, or @classmethod to make it easier to use them (https://realpython.com/instance-class-and-static-methods-demystified/)
"""

import copy
import json
import multiprocessing
import os
import sys
import time
import uuid
import warnings

from colorama import init as colorama_init

from binarycpython.utils.dicts import AutoVivificationDict
from binarycpython.utils.ensemble import new_grid_ensemble_results
from binarycpython.utils.functions import (
    check_if_in_shell,
    filter_arg_dict,
    get_ANSI_colours,
    get_defaults,
    hostnames,
    mem_use,
)

# Class extensions
from binarycpython.utils.population_extensions.analytics import analytics
from binarycpython.utils.population_extensions.argument_handling import (
    argument_handling,
)
from binarycpython.utils.population_extensions.cache import cache
from binarycpython.utils.population_extensions.custom_generator_sampling import (
    custom_generator_sampling,
)
from binarycpython.utils.population_extensions.dataIO import dataIO
from binarycpython.utils.population_extensions.distribution_functions import (
    distribution_functions,
)
from binarycpython.utils.population_extensions.ensemble import ensemble
from binarycpython.utils.population_extensions.evolution_functions import (
    evolution_functions,
)
from binarycpython.utils.population_extensions.failing_systems_functions import (
    failing_systems_functions,
)
from binarycpython.utils.population_extensions.grid_logging import grid_logging
from binarycpython.utils.population_extensions.grid_options_defaults import (
    grid_options_defaults,
)
from binarycpython.utils.population_extensions.grid_sampling import grid_sampling
from binarycpython.utils.population_extensions.HPC import HPC
from binarycpython.utils.population_extensions.metadata import metadata
from binarycpython.utils.population_extensions.miscellaneous_functions import (
    miscellaneous_functions,
)
from binarycpython.utils.population_extensions.Moe_di_Stefano_2017 import (
    Moe_di_Stefano_2017,
)
from binarycpython.utils.population_extensions.monte_carlo_sampling import (
    monte_carlo_sampling,
)
from binarycpython.utils.population_extensions.return_functions import return_functions
from binarycpython.utils.population_extensions.sampling_variables import (
    sampling_variables,
)
from binarycpython.utils.population_extensions.signal_handling import signal_handling
from binarycpython.utils.population_extensions.source_file_sampling import (
    source_file_sampling,
)
from binarycpython.utils.population_extensions.spacing_functions import (
    spacing_functions,
)
from binarycpython.utils.population_extensions.termination_functions import (
    termination_functions,
)
from binarycpython.utils.population_extensions.version_info import version_info

# Initialise colorama
colorama_init()


class Population(
    analytics,
    cache,
    dataIO,
    distribution_functions,
    grid_logging,
    grid_options_defaults,
    HPC,
    metadata,
    Moe_di_Stefano_2017,
    spacing_functions,
    version_info,
    grid_sampling,
    monte_carlo_sampling,
    source_file_sampling,
    custom_generator_sampling,
    signal_handling,
    return_functions,
    ensemble,
    argument_handling,
    termination_functions,
    miscellaneous_functions,
    evolution_functions,
    failing_systems_functions,
    sampling_variables,
):
    """
    Population Object. Contains all the necessary functions to set up, run and process a
    population of systems
    """

    def __init__(self, **kwargs):
        """
        Initialisation function of the population class

        NOTE: (david): we could probably put some of these init statements in the mixin file that they belong to
        """

        # Initialise the mix-in classes
        analytics.__init__(self)
        cache.__init__(self)
        dataIO.__init__(self)
        distribution_functions.__init__(self)
        grid_logging.__init__(self)
        grid_options_defaults.__init__(self)
        grid_sampling.__init__(self)
        HPC.__init__(self)
        metadata.__init__(self)
        Moe_di_Stefano_2017.__init__(self)
        spacing_functions.__init__(self)
        version_info.__init__(self)
        monte_carlo_sampling.__init__(self)
        source_file_sampling.__init__(self)
        signal_handling.__init__(self)
        custom_generator_sampling.__init__(self)
        argument_handling.__init__(self)
        return_functions.__init__(self)
        ensemble.__init__(self)
        termination_functions.__init__(self)
        miscellaneous_functions.__init__(self)
        evolution_functions.__init__(self)
        failing_systems_functions.__init__(self)
        sampling_variables.__init__(self)

        # caches
        self.caches = {}
        self.cached_function_cache = {}
        self.original_function_cache = {}
        self.hostnameslist = hostnames()

        # TODO: put in parameter handling or something
        # Different sections of options
        # get binary_c defaults and create a cleaned up dict
        # Setting stuff will check against the defaults to see if the input is correct.
        self.defaults = get_defaults()
        self.cleaned_up_defaults = self._cleanup_defaults()
        self.available_keys = list(self.defaults.keys())
        self.special_params = [
            el for el in list(self.defaults.keys()) if el.endswith("%d")
        ]
        self.preloaded_population = None
        self.signal_count = {}

        # make the input dictionary
        self.bse_options = {}  # bse_options is just empty.

        # Grid options
        self.grid_options = copy.deepcopy(self.get_grid_options_defaults_dict())

        # Custom options
        # TODO: is this really necessary here? The custom options should be empty on start i think
        self.custom_options = {
            "save_snapshot": False,
        }

        # grid code generation
        self.indent_depth = 0
        self.indent_string = "    "
        self.code_string = ""

        # cached value of minimum stellar mass
        self._minimum_stellar_mass = None

        # logging levels
        self._LOGGER_VERBOSITY_LEVEL = 1
        self._CUSTOM_LOGGING_VERBOSITY_LEVEL = 2

        # Set the options that are passed at creation of the object
        self.set(**kwargs)

        # Load Moe and di Stefano options
        self.grid_options["Moe2017_options"] = copy.deepcopy(
            self.get_Moe_di_Stefano_2017_default_options()
        )

        # Write MOE2017 options to a file. NOTE: (david) not sure why i put this here anymore
        os.makedirs(
            os.path.join(self.grid_options["tmp_dir"], "moe_distefano"), exist_ok=True
        )
        with self.open(
            os.path.join(
                os.path.join(self.grid_options["tmp_dir"], "moe_distefano"),
                "moeopts.dat",
            ),
            "w",
        ) as f:
            json.dump(
                self.grid_options["Moe2017_options"], f, indent=4, ensure_ascii=False
            )

        # Argline dict
        self.argline_dict = {}

        # Set some memory dicts
        self.persistent_data_memory_dict = {}

        # shared memory used for logging
        self.shared_memory = {}

        # variable to test if we're running in a shell
        self.in_shell = check_if_in_shell()

        # ANSI colours: use them if in a shell
        self.ANSI_colours = get_ANSI_colours()
        if self.in_shell is False:
            for c in self.ANSI_colours:
                self.ANSI_colours[c] = ""

        # Set global (OS) process id
        self.grid_options["_main_pid"] = os.getpid()

        # local process ID
        self.process_ID = 0

        # Create location to store results. Users should write to this dictionary.
        # The AutoVivificationDict allows for Perl-like addition of possibly
        # non-existant subdicts.
        self.grid_results = AutoVivificationDict()

        # Create grid ensemble data location
        self.grid_ensemble_results = new_grid_ensemble_results()

        # add metadata
        self.add_system_metadata()

        # set up function cache.
        # NOTE: (david) I added this here to be able to test the distributions functions without actually running anything.
        self.setup_function_cache()

    def jobID(self):
        """
        Function to return the job ID number of this process as a string.

        Normal processes return their process ID (PID)
        HPC processes return whatever HPC_jobID() gives.
        """
        if self.HPC_job():
            jobID = self.HPC_jobID()
            if not jobID:
                # fallback: use process ID but with "HPC" prepended
                # (this should never happen!)
                jobID = "HPC{}".format(self.process_ID)
        else:
            jobID = "{}".format(self.process_ID)
        return jobID

    ###################################################
    # Evolution functions
    ###################################################

    def _pre_run_setup(self) -> None:
        """
        Function to clean up some stuff in the grid before a run (like results, ensemble results etc)
        """

        # empty results
        self.grid_results = AutoVivificationDict()
        self.grid_ensemble_results = new_grid_ensemble_results()

        # set number of processes/cores we want to use
        self._set_nprocesses()

        # Reset the process ID (should not have a value initially, but can't hurt if it does)
        self.process_ID = 0

        # Reset population ID:
        self.grid_options["_population_id"] = uuid.uuid4().hex

        # save number of stored log stats
        self.shared_memory["n_saved_log_stats"] = multiprocessing.Value("i", 0)

        # set previous logging time
        _t = time.time()
        self.shared_memory["prev_log_time"] = multiprocessing.Array(
            "d", [_t] * self.grid_options["n_logging_stats"]
        )

        # set previous logging system number to 0
        self.shared_memory["prev_log_system_number"] = multiprocessing.Array(
            "i", [0] * self.grid_options["n_logging_stats"]
        )

        # arrays to store memory and max memory use per-thread
        mem = 1.0 * mem_use()
        for x in ["", "max_"]:
            self.shared_memory[x + "memory_use_per_thread"] = multiprocessing.Array(
                "d", [mem] * self.grid_options["num_processes"]
            )

        ############################################################
        # set and check default directory locations
        ############################################################

        # check tmp_dir exists
        if self.grid_options["tmp_dir"] is None or not os.path.isdir(
            self.grid_options["tmp_dir"]
        ):
            print(
                "grid_options['tmp_dir'] is not set or it is not a directory : this should point to a temporary directory location, preferably local to your CPUs"
            )
            self.exit(code=1)

        # check any HPC requirements are met
        if self.HPC_job() and not self.HPC_check_requirements()[0]:
            print(self.HPC_check_requirements()[1])
            self.exit(code=1)

        # default status_dir and cache_dir to be in tmp_dir
        #
        # NOTE: binary_c-python uses its own status_dir, which is not
        #       the same dir as HPC jobs use (so tmp_dir can be local
        #       to an HPC job, while the HPC status dir is common to
        #       all jobs)
        for x in ["status", "cache"]:
            if self.grid_options[x + "_dir"] is None:
                self.grid_options[x + "_dir"] = os.path.join(
                    self.grid_options["tmp_dir"], x
                )

        # make list of directories we want to use
        dirs = ["tmp_dir", "status_dir", "cache_dir"] + self.HPC_dirs()

        for dir in dirs:
            # try to make directories if they don't exist
            path = self.grid_options[dir]
            if path is not None:
                os.makedirs(path, exist_ok=True)

            # check directories exist and can be written to
            if path is not None and self.dir_ok(path) is False:
                print(
                    "Directory {dir} currently set to {path} cannot be written to. Please check that this directory is correct and you have write access.".format(
                        dir=dir, path=path
                    )
                )
                self.exit(code=1)

        # Make sure the subdirs of the tmp dir exist
        subdirs = [
            "failed_systems",
            "process_summary",
            "runtime_systems",
            "snapshots",
        ]
        for subdir in subdirs:
            path = os.path.join(self.grid_options["tmp_dir"], subdir)
            os.makedirs(path, exist_ok=True)
            if self.dir_ok(path) is False:
                print(
                    "Sub-Directory {subdir} (in tmp_dir) currently set to {path} cannot be written to. Please check that this directory is correct and you have write access.".format(
                        subdir=subdir, path=path
                    )
                )
                self.exit(code=1)

        # make sure the arg logging directory exists if we need it
        if self.grid_options["log_args"]:
            path = os.path.join(self.grid_options["log_args_dir"])
            os.makedirs(path, exist_ok=True)
            if self.dir_ok(path) is False:
                print(
                    "Failed to make directory at {path} for output of system arguments. Please check that this directory is correct and you have write access.".format(
                        path=path
                    )
                )
                self.exit(code=1)

        # restore from existing HPC files
        self.HPC_restore()

        # set up function cache
        self.setup_function_cache()

        return

    def clean(self) -> None:
        """
        Clean the contents of the population object so it can be reused.

        Calling _pre_run_setup()

        TODO: decide to deprecate this function
        """

        self._pre_run_setup()

    def evolve(self) -> None:
        """
        Entry point function of the whole object. From here, based on the settings,
        we set up a grid and (probably) evolve the population.

        There are no direct arguments to this function, the grid_options
        contain all the relevant settings.

        Returns:
               a dictionary containing the analytics of the run.
        """

        # Just to make sure we don't have stuff from a previous run hanging around
        self._pre_run_setup()

        if self.HPC_job():
            # run HPC grid: if this returns True, then exit immediately
            self.grid_options["symlink_latest_gridcode"] = False
            if self.HPC_grid():
                self.exit(code=0)

        if self.grid_options["evolution_type"] == "join":
            # join previously calculated data and return immediately
            self.HPC_join_previous()
            return

        # Execute population evolution subroutines
        result = self._evolve_population_wrapper()

        if result is False:
            print("Error detected in _evolve_population() : stopping here")

            sys.exit()

        # make analytics information
        analytics_dict = self.make_analytics_dict()

        if self.HPC_job():
            self.HPC_dump_status("HPC grid after analytics")

        if self.custom_options["save_snapshot"]:
            # we must save a snapshot, not the population object
            # ... also save the new starting point: this has to take into
            # account where we originally started, and that the modulo may
            # not be == 1.
            self.grid_options["start_at"] = (
                self.grid_options["start_at"]
                + self.grid_options["_count"] * self.grid_options["modulo"]
            )
            # then save the snapshot
            self.save_snapshot()
            exitcode = 1 if self.was_killed() else 0
            self.exit(code=exitcode)

        # Save object to a pickle file
        elif self.grid_options["save_population_object"]:
            self.save_population_object()

        # if we're running an HPC grid, exit here
        # unless we're joining
        if self.HPC_job() and self.grid_options["evolution_type"] != "join":
            self.exit()

        ##
        # Clean up code: remove files, unset values, unload interpolators etc. This is placed in the general evolve function,
        # because that makes for easier control
        self._cleanup()

        return analytics_dict

    ############################################################
    def _setup(self):
        """
        Function to set up the necessary stuff for the population evolution.

        The idea is to do all the stuff that is necessary for a population to run.
        Since we have different methods of running a population, this setup function
        will do different things depending on different settings

        Returns:
        True if we want to continue.
        False if we should return to the original calling script.
        """

        # Check for restore
        if self.grid_options["restore_from_snapshot_file"]:
            self.load_snapshot(self.grid_options["restore_from_snapshot_file"])

        # Check for parse function
        if not self.grid_options["parse_function"]:
            print("Warning: No parse function set. Make sure you intended to do this.")

        # #######################
        # ### Custom logging code:
        self._set_custom_logging()

        # Unset some value
        self.grid_options["_probtot"] = 0

        ## check the settings and set all the warnings.
        if self.bse_options.get("ensemble", None):
            self._ensemble_setup()

        ##################
        # Call setup function for specific evolution type

        # grid type
        if self.grid_options["evolution_type"] == "grid":
            self._grid_sampling_setup()

        # user-provided custom generator
        if self.grid_options["evolution_type"] == "custom_generator":
            self._custom_generator_sampling_setup()

        # Source file
        elif self.grid_options["evolution_type"] == "source_file":
            self._source_file_sampling_setup()

        # Monte-carlo
        elif self.grid_options["evolution_type"] == "monte_carlo":
            warnings.warn(
                "Currently the Monte-Carlo implementation is not well-tested and should not be used for anything other than developing reasons."
            )
            self._monte_carlo_sampling_setup()

        #######################
        # Reset values and prepare the grid function
        self.grid_options[
            "_probtot"
        ] = 0  # To make sure that the values are reset. TODO: fix this in a cleaner way

        return True

    def _cleanup(self):
        """
        Function that handles all the cleaning up after the grid has been generated and/or run

        - reset values to 0
        - remove grid file
        - unload grid function/module
        - remove dry grid file
        - unload dry grid function/module
        """

        # Reset values
        for x in [
            "_count",
            "_probtot",
            "_failed_count",
            "_failed_prob",
            "_total_mass_run",
            "_total_probability_weighted_mass_run",
        ]:
            self.grid_options[x] = 0
        for x in ["_errors_found", "_errors_exceeded"]:
            self.grid_options[x] = False
        self.grid_options["_system_generator"] = None
        self.grid_options["_failed_systems_error_codes"] = []
        self.grid_options["_queue_done"] = False
        self.grid_options["stop_queue"] = False
        self.grid_options["_job_crashed"] = False

        ############
        # Calls to each specific evolution type cleanup functions

        # grid type
        if self.grid_options["evolution_type"] == "grid":
            self._grid_sampling_cleanup()

        # user-provided custom generator
        if self.grid_options["evolution_type"] == "custom_generator":
            self._custom_generator_sampling_cleanup()

        # Source file
        elif self.grid_options["evolution_type"] == "source_file":
            self._source_file_sampling_cleanup()

        # Monte-carlo
        elif self.grid_options["evolution_type"] == "monte_carlo":
            self._monte_carlo_sampling_cleanup()

    def _dry_run(self):
        """
        Function to dry run the grid and know how many stars it will run

        Requires the grid to be built as a dry run grid

        NOTE: (david): this is a rather general function, and I'm not sure if we want to have a general dry-run function?
        """

        self.verbose_print(
            "Doing a dry run of the grid.", self.grid_options["verbosity"], 1
        )
        system_generator = self.grid_options["_system_generator"]
        total_starcount = system_generator(self)
        self.grid_options["_total_starcount"] = total_starcount

    ###################################################
    # Unordered functions
    #
    # Functions that aren't ordered yet
    ###################################################

    def _cleanup_defaults(self):
        """
        Function to clean up the default values:

        from a dictionary, removes the entries that have the following values:
        - "NULL"
        - ""
        - "Function"

        Uses the function from utils.functions

        TODO: Rethink this functionality. seems a bit double, could also be just outside of the class
        """

        binary_c_defaults = self.return_binary_c_defaults().copy()
        cleaned_dict = filter_arg_dict(binary_c_defaults)

        return cleaned_dict

    def _increment_probtot(self, prob):
        """
        Function to add to the total probability. For now not used
        """

        self.grid_options["_probtot"] += prob

    def _increment_count(self):
        """
        Function to add to the total number of stars. For now not used
        """
        self.grid_options["_count"] += 1

    #####
    #
    def _get_generator(self):
        """
        Function to get the generator. Handles the choice of evolution method
        """

        ###
        # Get generator for different evolution methods

        # grid type
        if self.grid_options["evolution_type"] == "grid":
            generator = self._grid_sampling_get_generator()

        # user-provided custom generator
        if self.grid_options["evolution_type"] == "custom_generator":
            generator = self._custom_generator_sampling_get_generator()

        # Source file
        elif self.grid_options["evolution_type"] == "source_file":
            generator = self._source_file_sampling_get_generator()

        # Monte-carlo
        elif self.grid_options["evolution_type"] == "monte_carlo":
            generator = self._monte_carlo_sampling_get_generator()

        return generator
