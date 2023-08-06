"""
Module containing the gridcode generation functions for the binarycpython package.

This class object is an extension to the population grid object
"""

# pylint: disable=E1101

import datetime
import importlib
import os

_count = 0  # used for file symlinking (for testing only)
_numba = False  # activate experimental numba code?


class grid_sampling:
    """
    Extension to the population grid object that contains functionality to handle the metadata that will be put in the ensemble
    """

    def __init__(self, **kwargs):
        """
        Init function for the gridcode class
        """

        return

    def _grid_sampling_cleanup(self):
        """
        Clean up function for the grid-type evolution
        """

    def _grid_sampling_get_generator(self):
        """
        Function to get the generator for the grid_sampling sampling method. Called by _get_generator and used in the actual evolution loop.
        """

        # write generator
        self._generate_grid_code(dry_run=False)

        # load generator
        self._load_grid_function()
        generator = self.grid_options["_system_generator"](self, print_results=False)

        return generator

    def _grid_sampling_setup(self):
        """
        Setup function for the grid sampling sampling type
        """

        # Set up LRU cache
        self.setup_function_cache()

        ############################################################
        # Dry run and getting starcount
        ############################################################
        # Put in check
        if len(self.grid_options["_sampling_variables"]) == 0:
            print("Error: you haven't defined any grid variables! Aborting")
            raise ValueError

        # Set up the grid code with a dry run option to see total probability
        print("Do dry run? {}".format(self.grid_options["do_dry_run"]))
        if self.grid_options["do_dry_run"]:
            print("Doing dry run to calculate total starcount and probability")
            self._generate_grid_code(dry_run=True)

            # Load the grid code
            self._load_grid_function()

            # Do a dry run
            self._dry_run()

            self.verbose_print(
                self._boxed(
                    "Dry run",
                    "Total starcount is {starcount}".format(
                        starcount=self.grid_options["_total_starcount"]
                    ),
                    "Total probability is {probtot:g}".format(
                        probtot=self.grid_options["_probtot"]
                    ),
                ),
                self.grid_options["verbosity"],
                0,
            )
            if self.grid_options["exit_after_dry_run"]:
                print(
                    "Exiting after dry run {}".format(
                        self.grid_options["exit_after_dry_run"]
                    )
                )
                self.exit(code=0)
            elif self.grid_options["return_after_dry_run"]:
                print(
                    "Returning after dry run {}".format(
                        self.grid_options["exit_after_dry_run"]
                    )
                )
                return False

        #######################
        # Reset values and prepare the grid function
        self.grid_options[
            "_probtot"
        ] = 0  # To make sure that the values are reset. TODO: fix this in a cleaner way

        # # Making sure the loaded grid code isn't lingering in the main PID
        # self._generate_grid_code(dry_run=False)

        # #
        # self._load_grid_function()

        #
        self.grid_options["_system_generator"] = None

    ###################################################
    # Grid code functions
    #
    # Function below are used to run populations with
    # a variable grid
    ###################################################
    def _gridcode_filename(self):
        """
        Returns a filename for the gridcode.
        """
        if self.HPC_job():
            filename = os.path.join(
                self.grid_options["tmp_dir"],
                "binary_c_grid_{population_id}.{jobid}.py".format(
                    population_id=self.grid_options["_population_id"],
                    jobid=self.jobID(),
                ),
            )
        else:
            filename = os.path.join(
                self.grid_options["tmp_dir"],
                "binary_c_grid_{population_id}.py".format(
                    population_id=self.grid_options["_population_id"]
                ),
            )
        return filename

    def _add_code(self, *args, indent=0):
        """
        Function to add code to the grid code string

        add code to the code_string

        indent (=0) is added once at the beginning
        mindent (=0) is added for every line

        don't use both!
        """

        indent_block = self._indent_block(indent)
        for thing in args:
            self.code_string += indent_block + thing

    def _indent_block(self, n=0):
        """
        return an indent block, with n extra blocks in it
        """
        return (self.indent_depth + n) * self.indent_string

    def _increment_indent_depth(self, delta):
        """
        increment the indent indent_depth by delta
        """
        self.indent_depth += delta

    def _generate_grid_code(self, dry_run=False):
        """
        Function that generates the code from which the population will be made.

        dry_run: when True, it will return the starcount at the end so that we know
        what the total number of systems is.

        The phasevol values are handled by generating a second array

        Results in a generated file that contains a system_generator function.

        # TODO: make sure running systems with multiplicity 3+ is also possible.
        # TODO: there is a lot of things going on in this function. Make sure to describe clearly what happens here.
        """
        self.verbose_print("Generating grid code", self.grid_options["verbosity"], 1)

        total_sampling_variables = len(self.grid_options["_sampling_variables"])

        self._add_code(
            # Import packages
            "import math\n",
            "import numpy as np\n",
            "from collections import OrderedDict\n",
            "from binarycpython.utils.useful_funcs import *\n",
            "import numba" if _numba else "",
            "\n\n",
            # Make the function
            "def grid_code(self, print_results=True):\n",
        )

        # Increase indent_depth
        self._increment_indent_depth(+1)

        self._add_code(
            # Write some info in the function
            "# Grid code generated on {}\n".format(datetime.datetime.now().isoformat()),
            "# This function generates the systems that will be evolved with binary_c\n\n"
            # Set some values in the generated code:
            "# Set initial values\n",
            "_total_starcount = 0\n",
            "starcounts = [0 for i in range({})]\n".format(
                total_sampling_variables + 1
            ),
            "probabilities = {}\n",
            "probabilities_list = [0 for i in range({})]\n".format(
                total_sampling_variables + 1
            ),
            "probabilities_sum = [0 for i in range({})]\n".format(
                total_sampling_variables + 1
            ),
            "parameter_dict = {}\n",
            "phasevol = 1\n",
        )

        # Set up the system parameters
        self._add_code(
            "M_1 = None\n",
            "M_2 = None\n",
            "M_3 = None\n",
            "M_4 = None\n",
            "orbital_period = None\n",
            "orbital_period_triple = None\n",
            "orbital_period_quadruple = None\n",
            "eccentricity = None\n",
            "eccentricity2 = None\n",
            "eccentricity3 = None\n",
            "\n",
            # Prepare the probability
            "# set probability lists\n",
        )

        for sampling_variable_el in sorted(
            self.grid_options["_sampling_variables"].items(),
            key=lambda x: x[1]["sampling_variable_number"],
        ):
            # Make probabilities dict
            sampling_variable = sampling_variable_el[1]
            self._add_code(
                'probabilities["{}"] = 0\n'.format(sampling_variable["name"])
            )

        #################################################################################
        # Start of code generation
        #################################################################################
        self._add_code("\n")

        # turn vb to True to have debugging output
        vb = False

        # Generate code
        for loopnr, sampling_variable_el in enumerate(
            sorted(
                self.grid_options["_sampling_variables"].items(),
                key=lambda x: x[1]["sampling_variable_number"],
            )
        ):
            self.verbose_print(
                "Constructing/adding: {}".format(sampling_variable_el[0]),
                self.grid_options["verbosity"],
                2,
            )
            sampling_variable = sampling_variable_el[1]

            ####################
            # top code
            if sampling_variable["topcode"]:
                self._add_code(sampling_variable["topcode"])

            #########################
            # Set up the for loop
            # Add comment for for loop
            self._add_code(
                "# for loop for variable {name} gridtype {gridtype}".format(
                    name=sampling_variable["name"],
                    gridtype=sampling_variable["gridtype"],
                )
                + "\n",
                "sampled_values_{} = {}".format(
                    sampling_variable["name"], sampling_variable["samplerfunc"]
                )
                + "\n",
            )

            if vb:
                self._add_code(
                    "print('samples','{name}',':',sampled_values_{name})\n".format(
                        name=sampling_variable["name"],
                    )
                )

            if vb:
                self._add_code(
                    "print('sample {name} from',sampled_values_{name})".format(
                        name=sampling_variable["name"]
                    )
                    + "\n"
                )

            # calculate number of values and starting location
            #
            # if we're sampling a continuous variable, we
            # have one fewer grid point than the length of the
            # sampled_values list
            if sampling_variable["gridtype"] in [
                "centred",
                "centre",
                "center",
                "edge",
                "left edge",
                "left",
                "right",
                "right edge",
            ]:
                offset = -1
            elif sampling_variable["gridtype"] == "discrete":
                # discrete variables sample all the points
                offset = 0

            start = 0

            # for loop over the variable
            if vb:
                self._add_code(
                    'print("var {name} values ",sampled_values_{name}," len ",len(sampled_values_{name})+{offset}," gridtype {gridtype} offset {offset}\\n")\n'.format(
                        name=sampling_variable["name"],
                        offset=offset,
                        gridtype=sampling_variable["gridtype"],
                    )
                )

            stop = "len(sampled_values_{name})+{offset}".format(
                name=sampling_variable["name"], offset=offset
            )

            if _numba and sampling_variable["dry_parallel"]:
                # Parallel outer loop
                self._add_code("@numba.jit(parallel=True)\n")
                self._add_code("def __parallel_func(phasevol,_total_starcount):\n")
                self._increment_indent_depth(+1)
                self._add_code(
                    "for {name}_sample_number in numba.prange({stop}):\n".format(
                        name=sampling_variable["name"],
                        stop=stop,
                    )
                )
                self._increment_indent_depth(+1)
                if start > 0:
                    self._add_code(
                        "if {name}_sample_number < {start}:\n".format(
                            name=sampling_variable["name"],
                            start=start,
                        )
                    )
                    self._add_code("continue\n", indent=1)
            else:
                self._add_code(
                    "for {name}_sample_number in range({start},{stop}):\n".format(
                        name=sampling_variable["name"],
                        start=start,
                        stop=stop,
                    )
                )
                self._increment_indent_depth(+1)

            # {}_this_index is this grid point's index
            # {}_prev_index and {}_next_index are the previous and next grid points,
            # (which can be None if there is no previous or next, or if
            #  previous and next should not be used: this is deliberate)
            #

            if sampling_variable["gridtype"] == "discrete":
                # discrete grids only care about this,
                # both prev and next should be None to
                # force errors where they are used
                self._add_code(
                    "{name}_this_index = {name}_sample_number ".format(
                        name=sampling_variable["name"],
                    ),
                )
                self._add_code(
                    "\n",
                    "{name}_prev_index = None if {name}_this_index == 0 else ({name}_this_index - 1) ".format(
                        name=sampling_variable["name"],
                    ),
                    "\n",
                )
                self._add_code(
                    "\n",
                    "{name}_next_index = None if {name}_this_index >= (len(sampled_values_{name})+{offset} - 1) else ({name}_this_index + 1)".format(
                        name=sampling_variable["name"], offset=offset
                    ),
                    "\n",
                )

            elif sampling_variable["gridtype"] in [
                "centred",
                "centre",
                "center",
                "edge",
                "left",
                "left edge",
            ]:

                # left and centred grids
                self._add_code(
                    "if {}_sample_number == 0:\n".format(sampling_variable["name"])
                )
                self._add_code(
                    "{}_this_index = 0;\n".format(sampling_variable["name"]), indent=1
                )
                self._add_code("else:\n")
                self._add_code(
                    "{name}_this_index = {name}_sample_number ".format(
                        name=sampling_variable["name"]
                    ),
                    indent=1,
                )
                self._add_code("\n")
                self._add_code(
                    "{name}_prev_index = ({name}_this_index - 1) if {name}_this_index > 0 else None ".format(
                        name=sampling_variable["name"]
                    )
                )
                self._add_code("\n")
                self._add_code(
                    "{name}_next_index = {name}_this_index + 1".format(
                        name=sampling_variable["name"]
                    )
                )
                self._add_code("\n")

            elif sampling_variable["gridtype"] in ["right", "right edge"]:

                # right edged grid
                self._add_code(
                    "if {name}_sample_number == 0:\n".format(
                        name=sampling_variable["name"]
                    )
                )
                self._add_code(
                    "{name}_this_index = 1;\n".format(name=sampling_variable["name"]),
                    indent=1,
                )
                self._add_code("else:\n")
                self._add_code(
                    "{name}_this_index = {name}_sample_number + 1 ".format(
                        name=sampling_variable["name"],
                    ),
                    indent=1,
                )
                self._add_code("\n")
                self._add_code(
                    "{name}_prev_index = {name}_this_index - 1".format(
                        name=sampling_variable["name"]
                    )
                )
                self._add_code("\n")
                self._add_code(
                    "{name}_next_index = ({name}_this_index + 1) if {name}_this_index < len(sampled_values_{name}) else None".format(
                        name=sampling_variable["name"]
                    )
                )
                self._add_code("\n")

            # calculate phase volume
            if sampling_variable["dphasevol"] == -1:
                # no phase volume required so set it to 1.0
                self._add_code(
                    "dphasevol_{name} = 1.0 # 666\n".format(
                        name=sampling_variable["name"]
                    )
                )

            elif sampling_variable["gridtype"] in ["right", "right edge"]:
                # right edges always have this and prev defined
                self._add_code(
                    "dphasevol_{name} = (sampled_values_{name}[{name}_this_index] - sampled_values_{name}[{name}_prev_index])".format(
                        name=sampling_variable["name"]
                    )
                    + "\n"
                )
            elif sampling_variable["gridtype"] == "discrete":
                # discrete might have next defined, use it if we can,
                # otherwise use prev
                self._add_code(
                    "dphasevol_{name} = (sampled_values_{name}[{name}_next_index] - sampled_values_{name}[{name}_this_index]) if {name}_next_index else (sampled_values_{name}[{name}_this_index] - sampled_values_{name}[{name}_prev_index])".format(
                        name=sampling_variable["name"]
                    )
                    + "\n"
                )
            else:
                # left and centred always have this and next defined
                self._add_code(
                    "dphasevol_{name} = (sampled_values_{name}[{name}_next_index] - sampled_values_{name}[{name}_this_index])".format(
                        name=sampling_variable["name"]
                    )
                    + "\n"
                )

            ##############
            # Add phasevol check:
            self._add_code(
                "if dphasevol_{name} <= 0:\n".format(name=sampling_variable["name"])
            )

            #   n that case we need another local variable which will prevent it from being run but will track those parameters
            # Add phasevol check action:
            self._add_code(
                'print("Grid generator: dphasevol_{name} <= 0! (this=",{name}_this_index,"=",sampled_values_{name}[{name}_this_index],", next=",{name}_next_index,"=",sampled_values_{name}[{name}_next_index],") Skipping current sample.")'.format(
                    name=sampling_variable["name"]
                )
                + "\n",
                "continue\n",
                indent=1,
            )

            if vb:
                self._add_code(
                    "print('sample {name} from ',sampled_values_{name},' at this=',{name}_this_index,', next=',{name}_next_index)".format(
                        name=sampling_variable["name"]
                    )
                    + "\n"
                )

            # select sampled point location based on gridtype (left, centre or right)
            if sampling_variable["gridtype"] in [
                "edge",
                "left",
                "left edge",
                "right",
                "right edge",
                "discrete",
            ]:
                self._add_code(
                    "{name} = sampled_values_{name}[{name}_this_index]".format(
                        name=sampling_variable["name"]
                    )
                    + "\n"
                )
            elif sampling_variable["gridtype"] in ["centred", "centre", "center"]:
                self._add_code(
                    "{name} = 0.5 * (sampled_values_{name}[{name}_next_index] + sampled_values_{name}[{name}_this_index])".format(
                        name=sampling_variable["name"]
                    )
                    + "\n"
                )
            else:
                msg = "Unknown gridtype value {type}.".format(
                    type=sampling_variable["gridtype"]
                )
                raise ValueError(msg)

            if vb:
                self._add_code(
                    "print('hence {name} = ',{name})\n".format(
                        name=sampling_variable["name"]
                    )
                )

            #################################################################################
            # Check condition and generate for loop

            # If the grid variable has a condition, write the check and the action
            if sampling_variable["condition"]:
                self._add_code(
                    # Add comment
                    "# Condition for {name}\n".format(name=sampling_variable["name"]),
                    # Add condition check
                    "if not {condition}:\n".format(
                        condition=sampling_variable["condition"]
                    ),
                    indent=0,
                )

                # Add condition failed action:
                if self.grid_options["verbosity"] >= 4:
                    self._add_code(
                        'print("Grid generator: Condition for {name} not met!")'.format(
                            name=sampling_variable["name"]
                        )
                        + "\n",
                        "continue" + "\n",
                        indent=1,
                    )
                else:
                    self._add_code(
                        "continue" + "\n",
                        indent=1,
                    )
                    # Add some whitespace
                self._add_code("\n")

            # Add some whitespace
            self._add_code("\n")

            #########################
            # Set up pre-code and value in some cases
            # Add pre-code
            if sampling_variable["precode"]:
                self._add_code(
                    "{precode}".format(
                        precode=sampling_variable["precode"].replace(
                            "\n", "\n" + self._indent_block(0)
                        )
                    )
                    + "\n"
                )

            # Set phasevol
            self._add_code(
                "phasevol *= dphasevol_{name}\n".format(
                    name=sampling_variable["name"],
                )
            )

            #######################
            # Probabilities
            # Calculate probability
            self._add_code(
                "\n",
                "# Set probabilities\n",
                "dprob_{name} = dphasevol_{name} * ({probdist})".format(
                    name=sampling_variable["name"],
                    probdist=sampling_variable["probdist"],
                )
                + "\n",
                # Save probability sum
                "probabilities_sum[{n}] += dprob_{name}".format(
                    n=sampling_variable["sampling_variable_number"],
                    name=sampling_variable["name"],
                )
                + "\n",
            )

            if sampling_variable["sampling_variable_number"] == 0:
                self._add_code(
                    "probabilities_list[0] = dprob_{name}".format(
                        name=sampling_variable["name"]
                    )
                    + "\n"
                )
            else:
                self._add_code(
                    "probabilities_list[{this}] = probabilities_list[{prev}] * dprob_{name}".format(
                        this=sampling_variable["sampling_variable_number"],
                        prev=sampling_variable["sampling_variable_number"] - 1,
                        name=sampling_variable["name"],
                    )
                    + "\n"
                )

            ##############
            # postcode
            if sampling_variable["postcode"]:
                self._add_code(
                    "{postcode}".format(
                        postcode=sampling_variable["postcode"].replace(
                            "\n", "\n" + self._indent_block(0)
                        )
                    )
                    + "\n"
                )

            #######################
            # Increment starcount for this parameter
            self._add_code(
                "\n",
                "# Increment starcount for {name}\n".format(
                    name=sampling_variable["name"]
                ),
                "starcounts[{n}] += 1".format(
                    n=sampling_variable["sampling_variable_number"],
                )
                + "\n",
                # Add value to dict
                'parameter_dict["{name}"] = {name}'.format(
                    name=sampling_variable["parameter_name"]
                )
                + "\n",
                "\n",
            )

            self._increment_indent_depth(-1)

            # The final parts of the code, where things are returned, are within the deepest loop,
            # but in some cases code from a higher loop needs to go under it again
            # SO I think its better to put an if statement here that checks
            # whether this is the last loop.
            if loopnr == len(self.grid_options["_sampling_variables"]) - 1:
                self._write_gridcode_system_call(
                    sampling_variable,
                    dry_run,
                    sampling_variable["branchpoint"],
                    sampling_variable["branchcode"],
                )

            # increment indent_depth
            self._increment_indent_depth(+1)

            ####################
            # bottom code
            if sampling_variable["bottomcode"]:
                self._add_code(sampling_variable["bottomcode"])

        self._increment_indent_depth(-1)
        self._add_code("\n")

        # Write parts to write below the part that yield the results.
        # this has to go in a reverse order:
        # Here comes the stuff that is put after the deepest nested part that calls returns stuff.
        # Here we will have a
        reverse_sorted_sampling_variables = sorted(
            self.grid_options["_sampling_variables"].items(),
            key=lambda x: x[1]["sampling_variable_number"],
            reverse=True,
        )
        for loopnr, sampling_variable_el in enumerate(
            reverse_sorted_sampling_variables
        ):
            sampling_variable = sampling_variable_el[1]

            self._increment_indent_depth(+1)
            self._add_code(
                "#" * 40 + "\n",
                "# Code below is for finalising the handling of this iteration of the parameter {name}\n".format(
                    name=sampling_variable["name"]
                ),
            )

            # Set phasevol
            # TODO: fix. this isn't supposed to be the value that we give it here. discuss
            self._add_code(
                "phasevol /= dphasevol_{name}\n\n".format(
                    name=sampling_variable["name"]
                )
            )

            self._increment_indent_depth(-2)

            if _numba and sampling_variable["dry_parallel"]:
                self._add_code("__parallel_func(phasevol,_total_starcount)\n")
                self._increment_indent_depth(-1)

            # Check the branchpoint part here. The branchpoint makes sure that we can construct
            # a grid with several multiplicities and still can make the system calls for each
            # multiplicity without reconstructing the grid each time
            if sampling_variable["branchpoint"] > 0:

                self._increment_indent_depth(+1)

                self._add_code(
                    # Add comment
                    "# Condition for branchpoint at {}".format(
                        reverse_sorted_sampling_variables[loopnr + 1][1]["name"]
                    )
                    + "\n",
                    # # Add condition check
                    #     "if not {}:".format(sampling_variable["condition"])
                    #     + "\n"
                    # Add branchpoint
                    "if multiplicity=={}:".format(sampling_variable["branchpoint"])
                    + "\n",
                )

                self._write_gridcode_system_call(
                    reverse_sorted_sampling_variables[loopnr + 1][1],
                    dry_run,
                    sampling_variable["branchpoint"],
                    sampling_variable["branchcode"],
                )
                self._increment_indent_depth(-1)
                self._add_code("\n")

        ###############################
        # Finalise print statements
        #
        self._increment_indent_depth(+1)
        self._add_code("\n", "#" * 40 + "\n", "if print_results:\n")
        self._add_code(
            "print('Grid has handled {starcount} stars with a total probability of {probtot:g}'.format(starcount=_total_starcount,probtot=self.grid_options['_probtot']))\n",
            indent=1,
        )

        ################
        # Finalise return statement for dry run.
        #
        if dry_run:
            self._add_code("return _total_starcount\n")

        self._increment_indent_depth(-1)
        #################################################################################
        # Stop of code generation. Here the code is saved and written

        # Save the grid code to the grid_options
        self.verbose_print(
            "Save grid code to grid_options", self.grid_options["verbosity"], 1
        )

        self.grid_options["code_string"] = self.code_string

        # Write to file
        gridcode_filename = self._gridcode_filename()

        self.grid_options["gridcode_filename"] = gridcode_filename

        self.verbose_print(
            "{blue}Write grid code to {file} [dry_run = {dry}]{reset}".format(
                blue=self.ANSI_colours["blue"],
                file=gridcode_filename,
                dry=dry_run,
                reset=self.ANSI_colours["reset"],
            ),
            self.grid_options["verbosity"],
            1,
        )

        with self.open(gridcode_filename, "w", encoding="utf-8") as file:
            file.write(self.code_string)

        # reset the code string
        self.code_string = ""

        # perhaps create symlink
        if not self.HPC_job() and self.grid_options["symlink_latest_gridcode"]:
            global _count
            symlink = os.path.join(
                self.grid_options["tmp_dir"], "binary_c_grid-latest" + str(_count)
            )
            _count += 1
            try:
                os.unlink(symlink)
            except:
                pass

            try:
                os.symlink(gridcode_filename, symlink)
                self.verbose_print(
                    "{blue}Symlinked grid code to {symlink} {reset}".format(
                        blue=self.ANSI_colours["blue"],
                        symlink=symlink,
                        reset=self.ANSI_colours["reset"],
                    ),
                    self.grid_options["verbosity"],
                    1,
                )
            except OSError:
                print("symlink failed")

    def _write_gridcode_system_call(
        self, sampling_variable, dry_run, branchpoint, branchcode
    ):
        """
        Function to write the block of code (as string) that handles the setting the final probability, taking into account the weight and repeat settings, incrementing the total starcount and total probability.

        Then if the run is a dry run we implement the dry_run_hook or pass depending on the settings. If it is not a dry run we yield the system dict
        """

        self._increment_indent_depth(+1)
        self._add_code("#" * 40 + "\n")

        if branchcode:
            self._add_code(
                "# Branch code\nif {branchcode}:\n".format(branchcode=branchcode)
            )

        if branchpoint:
            self._add_code(
                "# Code below will get evaluated for every system at this level of multiplicity (last one of that being {name})\n".format(
                    name=sampling_variable["name"]
                )
            )
        else:
            self._add_code(
                "# Code below will get evaluated for every generated system\n"
            )

        # Factor in the custom weight input
        self._add_code(
            "\n",
            "# Weigh the probability by a custom weighting factor\n",
            'probability = self.grid_options["weight"] * probabilities_list[{n}]'.format(
                n=sampling_variable["sampling_variable_number"]
            )
            + "\n",
            # Take into account the multiplicity fraction:
            "\n",
            "# Factor the multiplicity fraction into the probability\n",
            "probability *= self._calculate_multiplicity_fraction(parameter_dict)"
            + "\n",
            # Divide by number of repeats
            "\n",
            "# Divide the probability by the number of repeats\n",
            'probability /= self.grid_options["repeat"]' + "\n",
            # Now we yield the system self.grid_options["repeat"] times.
            "\n",
            "# Loop over the repeats\n",
            'for _ in range(self.grid_options["repeat"]):' + "\n",
        )
        self._add_code(
            "_total_starcount += 1\n",
            # set probability and phasevol values into the system dict
            'parameter_dict["{p}"] = {p}'.format(p="probability") + "\n",
            'parameter_dict["{v}"] = {v}'.format(v="phasevol") + "\n",
            # Increment total probability
            "self._increment_probtot(probability)\n",
            indent=1,
        )

        if not dry_run:
            # Handle what is returned, or what is not.
            self._add_code("yield(parameter_dict)\n", indent=1)

        # If its a dry run, dont do anything with it
        else:
            # run the hook function, only if given
            if self.grid_options["dry_run_hook"]:
                self._add_code(
                    "self.grid_options['dry_run_hook'](self, parameter_dict)\n",
                    indent=1,
                )
            else:
                # or pass
                self._add_code("pass\n", indent=1)

        self._add_code("#" * 40 + "\n")

        self._increment_indent_depth(-1)

        return self.code_string

    def _load_grid_function(self):
        """
        Function that loads the grid code from file
        """

        # Code to load the
        self.verbose_print(
            message="Load grid code function from {file}".format(
                file=self.grid_options["gridcode_filename"]
            ),
            verbosity=self.grid_options["verbosity"],
            minimal_verbosity=1,
        )

        spec = importlib.util.spec_from_file_location(
            "binary_c_python_grid",
            os.path.join(self.grid_options["gridcode_filename"]),
        )
        grid_file = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(grid_file)
        generator = grid_file.grid_code

        self.grid_options["_system_generator"] = generator

        self.verbose_print("Grid code loaded", self.grid_options["verbosity"], 1)
