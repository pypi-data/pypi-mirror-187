"""
Main script to provide the Monte-Carlo sampling class extensions

Some tasks to consider doing soon
TODO: add option to add a secondary probability distribution to each parameter. This enables adaptive importance sampling
"""

import datetime
import importlib
import os

import numpy as np

from binarycpython.utils.functions import calculate_total_mass_system

# pylint: disable=E1101

_numba = False
comment_line = "###########\n"


class monte_carlo_sampling:
    """
    Extension for the Population class containing the code for Monte-Carlo sampling functions
    """

    def __init__(self, **kwargs):
        """
        Init function for the spacing_functions class
        """

        return

    def _monte_carlo_sampling_cleanup(self):
        """
        Cleanup function for the Monte-Carlo sampling evolution type
        """

        self.grid_options["_monte_carlo_threshold_reached"] = False
        self.grid_options["_monte_carlo_current_total_mass_evolved"] = 0

    def _monte_carlo_sampling_check_mass_threshold(self, system_dict):
        """
        Function to handle checking the total mass evolved and signal to stop
        """

        # Only if the monte_carlo_mass_threshold is positive (default = -1)
        if self.grid_options["monte_carlo_mass_threshold"] > 0:

            # Add total mass of current system tot total mass evolved
            self.grid_options[
                "_monte_carlo_current_total_mass_evolved"
            ] += calculate_total_mass_system(system_dict)

            # Check if exceeds threshold
            if (
                self.grid_options["_monte_carlo_current_total_mass_evolved"]
                > self.grid_options["monte_carlo_mass_threshold"]
            ):
                self.grid_options["_monte_carlo_threshold_reached"] = True

    def _monte_carlo_sampling_check_custom_threshold(self, result_queue):
        """
        Function to handle checking the content of the result queue and look for a
        TODO: put in the user-defined custom threshold function
        """

        # raise NotImplementedError("Functionality in not implemented")
        pass

    ##############
    # Generator functions

    # Management
    def _monte_carlo_sampling_get_generator_filename(self):
        """
        Returns a filename for the gridcode.
        """

        if self.HPC_job():
            filename = os.path.join(
                self.grid_options["tmp_dir"],
                "binary_c_monte_carlo_sampling_generator_{population_id}.{jobid}.py".format(
                    population_id=self.grid_options["_population_id"],
                    jobid=self.jobID(),
                ),
            )
        else:
            filename = os.path.join(
                self.grid_options["tmp_dir"],
                "binary_c_monte_carlo_sampling_generator_{population_id}.py".format(
                    population_id=self.grid_options["_population_id"]
                ),
            )
        return filename

    def _monte_carlo_sampling_write_generator_file(self, dry_run=False):
        """
        Function to write the function that can generate the sample for the parameter

        Contrary to the grid sampling variable generator code, this code is not nested, but is linear.
        """

        #########
        # Set up header and start of function
        self._add_code(
            # Import packages
            "import math\n",
            "import copy\n",
            "import numpy as np\n",
            "from collections import OrderedDict\n",
            "from binarycpython.utils.useful_funcs import *\n",
            "\n\n",
            # Make the function
            "def monte_carlo_generator(self, print_results=True):\n",
        )

        # Increase indent_depth
        self._increment_indent_depth(+1)

        # Code to set up some parameters
        self._add_code(
            # Write some info in the function
            "# Grid code generated on {}\n".format(datetime.datetime.now().isoformat()),
            "# This function generates the systems that will be evolved with binary_c\n\n",
            # Set some values in the generated code:
            "# Set initial values\n",
            "_total_starcount = 0\n",
            "generating = True\n",
            "default_system_dict = {'multiplicity': 0}\n\n",
        )

        # Add method for the pre-calculation of the arrays
        if self.grid_options["monte_carlo_use_pre_calculated_distributions"]:
            self._add_code("self.handle_pre_calc(self)\n")

        #########
        # Set up the loop and yield calls
        self._add_code(
            # Comment
            comment_line,
            "# Start of the while loop\n",
            # while loop
            "while generating:\n",
        )

        # Increase indent_depth
        self._increment_indent_depth(+1)
        self._add_code("system_dict = copy.copy(default_system_dict)\n\n")

        #########
        # Run loop of sampling variable setup
        for loopnr, sampling_variable_el in enumerate(
            sorted(
                self.grid_options["_sampling_variables"].items(),
                key=lambda x: x[1]["sampling_variable_number"],
            )
        ):
            sampling_variable = sampling_variable_el[1]

            #########
            # Generate parameter lines
            self._monte_carlo_sampling_write_generator_parameter(sampling_variable)

            #########
            # Generate yield call if branchpoint
            self._monte_carlo_sampling_write_system_call(
                sampling_variable,
                dry_run,
                sampling_variable["branchpoint"],
                sampling_variable["branchcode"],
            )

        #########
        # Write to file
        monte_carlo_sampling_generator_filename = (
            self._monte_carlo_sampling_get_generator_filename()
        )

        self.grid_options[
            "_monte_carlo_sampling_generator_filename"
        ] = monte_carlo_sampling_generator_filename

        self.verbose_print(
            "{blue}Write grid code to {file} {reset}".format(
                blue=self.ANSI_colours["blue"],
                file=monte_carlo_sampling_generator_filename,
                reset=self.ANSI_colours["reset"],
            ),
            self.grid_options["verbosity"],
            1,
        )

        with self.open(
            monte_carlo_sampling_generator_filename, "w", encoding="utf-8"
        ) as file:
            file.write(self.code_string)
        self.code_string = ""

    # Construction
    def _monte_carlo_sampling_write_system_call(
        self, sampling_variable, dry_run, branchpoint, branchcode
    ):
        """
        Function to write the block of code (as string) that handles the setting the final probability, taking into account the weight and repeat settings, incrementing the total starcount and total probability.

        Then if the run is a dry run we implement the dry_run_hook or pass depending on the settings. If it is not a dry run we yield the system dict
        """

        if branchpoint:
            self._add_code(comment_line)
            if branchcode:
                self._add_code(
                    "# Branch code\n",
                    "if {branchcode}:\n".format(branchcode=branchcode),
                )
                self._increment_indent_depth(+1)

            # Factor in the custom weight input
            self._add_code(
                "\n",
                "# Loop over the repeats\n",
                'for _ in range(self.grid_options["repeat"]):' + "\n",
            )
            self._add_code(
                "_total_starcount += 1\n",
                indent=1,
            )

            if not dry_run:
                # Handle what is returned, or what is not.
                self._add_code("yield system_dict\n\n", indent=1)

            # If its a dry run, dont do anything with it
            else:
                # run the hook function, only if given
                if self.grid_options["dry_run_hook"]:
                    self._add_code(
                        "self.grid_options['dry_run_hook'](self, system_dict)\n\n",
                        indent=1,
                    )
                else:
                    # or pass
                    self._add_code("pass\n\n", indent=1)

            self._increment_indent_depth(-1)

        return self.code_string

    def _monte_carlo_sampling_write_generator_parameter(self, sampling_variable):
        """
        Function to write the parameter lines and the pre and postcode around it to the monte carlo sampling generator function.
        """

        self.verbose_print(
            "Constructing/adding: {}".format(sampling_variable["parameter_name"]),
            self.grid_options["verbosity"],
            2,
        )

        ####################
        # Write comment
        self._add_code(
            comment_line, "# Sampling variable {}\n\n".format(sampling_variable["name"])
        )

        self.verbose_print(
            "Writing sampling variable {} to monte-carlo sampling generator".format(
                sampling_variable["parameter_name"]
            ),
            self.grid_options["verbosity"],
            1,
        )

        ####################
        # Generate top code
        if sampling_variable["topcode"]:
            self._add_code(
                comment_line,
                sampling_variable["topcode"],
                "\n\n",
            )

        #########
        # Generate call to pdf-cdf function to generate the parameter value
        self._add_code(
            comment_line,
            "{} = self.handle_calc_sampled_value(self, sampling_variable={}{})\n".format(
                sampling_variable["parameter_name"],
                sampling_variable,
                ", "
                + ",".join(
                    [
                        "{}={}".format(dependency_variable, dependency_variable)
                        for dependency_variable in sampling_variable[
                            "dependency_variables"
                        ]
                    ]
                )
                if sampling_variable["dependency_variables"]
                else "",
            ),
            "system_dict['{}'] = {}\n\n".format(
                sampling_variable["parameter_name"], sampling_variable["parameter_name"]
            ),
        )

        ####################
        # bottom code
        if sampling_variable["bottomcode"]:
            self._add_code(
                comment_line,
                sampling_variable["bottomcode"] + "\n\n",
            )

    ##############
    # Sampling functions

    # Management
    def _monte_carlo_sampling_get_sampling_functions_filename(self):
        """
        Returns a filename for the file containing the function to generate values for the variables.
        """

        filename = os.path.join(
            "binary_c_monte_carlo_sampling_sampling_functions_{population_id}.py".format(
                population_id=self.grid_options["_population_id"]
            ),
        )

        return filename

    def _monte_carlo_sampling_load_sampling_functions_file(self):
        """
        Function to load the sampling functions
        """

        # Code to load the generator code
        self.verbose_print(
            message="Load monte-carlo sampling functions from {file}".format(
                file=self.grid_options[
                    "_monte_carlo_sampling_sampling_functions_filename"
                ]
            ),
            verbosity=self.grid_options["verbosity"],
            minimal_verbosity=1,
        )

        # Load the module from file and the functions in it.
        spec = importlib.util.spec_from_file_location(
            "binary_c_python_monte_carlo_sampling_functions",
            os.path.join(
                self.grid_options["_monte_carlo_sampling_sampling_functions_filename"]
            ),
        )
        monte_carlo_sampling_functions_file = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(monte_carlo_sampling_functions_file)

        # NOTE: the way we are loading and dynamically is i think not fully correct. I have to pass the self in twice.
        # TODO: fix the setting of these functions properly

        # Create dictionary to hold the calc_sampled_value functions
        self.monte_carlo_calc_sampled_value_functions = {}
        for obj in dir(monte_carlo_sampling_functions_file):
            if obj.startswith("calc_sampled_value"):
                # Set function as class function
                setattr(self, obj, getattr(monte_carlo_sampling_functions_file, obj))
                # Add to dict
                self.monte_carlo_calc_sampled_value_functions[
                    obj.replace("calc_sampled_value_", "")
                ] = getattr(monte_carlo_sampling_functions_file, obj)

        # Create dictionary to hold the calc_pdf_cdf_value_array_dict functions
        self.monte_carlo_calc_pdf_cdf_value_array_dict_functions = {}
        for obj in dir(monte_carlo_sampling_functions_file):
            if obj.startswith("calc_pdf_cdf_value_array_dict"):
                # Set function as class function
                setattr(self, obj, getattr(monte_carlo_sampling_functions_file, obj))
                # Add to dict
                self.monte_carlo_calc_pdf_cdf_value_array_dict_functions[
                    obj.replace("calc_pdf_cdf_value_array_dict_", "")
                ] = getattr(monte_carlo_sampling_functions_file, obj)

        # Load handler function
        for obj in dir(monte_carlo_sampling_functions_file):
            if obj.startswith("handle_calc_sampled_value"):
                self.handle_calc_sampled_value = getattr(
                    monte_carlo_sampling_functions_file, obj
                )
                break

        # Load handler function
        for obj in dir(monte_carlo_sampling_functions_file):
            if obj.startswith("handle_pre_calc"):
                self.handle_pre_calc = getattr(monte_carlo_sampling_functions_file, obj)
                # setattr(self, obj, getattr(monte_carlo_sampling_functions_file, obj))
                # MethodType(func, obj)
                # MethodType(getattr(monte_carlo_sampling_functions_file, obj), self)

                break

    def _monte_carlo_sampling_write_sampling_functions_file(self, dry_run=False):
        """
        Function to write the functions that handle generating the values for each variable
        """

        #########
        # Set up header and start of function
        self._add_code(
            # Import packages
            "import math\n",
            "import copy\n",
            "import numpy as np\n",
            "from collections import OrderedDict\n",
            "from binarycpython.utils.useful_funcs import *\n",
            "\n\n",
        )

        #########
        # Write functions to calculate the values for each parameter.
        for loopnr, sampling_variable_el in enumerate(
            sorted(
                self.grid_options["_sampling_variables"].items(),
                key=lambda x: x[1]["sampling_variable_number"],
            )
        ):

            sampling_variable = sampling_variable_el[1]

            ######################
            # Call to function to write the calc_sample_value function
            self._monte_carlo_sampling_write_calc_pdf_cdf_value_array_dict_function(
                sampling_variable
            )

            ######################
            # Call to function to write the calc_sample_value function
            self._monte_carlo_sampling_write_calc_sampled_value_function(
                sampling_variable
            )

            ######################
            # Call to function to write the pre_calc_sample_value function
            if self.grid_options["monte_carlo_use_pre_calculated_distributions"]:
                self._monte_carlo_sampling_write_pre_calc_function(sampling_variable)

        ######################
        # Call to function to write the handle_calc_sample_value wrapper function
        self._monte_carlo_sampling_write_handle_calc_sampled_value_function()

        ######################
        # Call to function to write the handle_pre_calc function and other functions
        if self.grid_options["monte_carlo_use_pre_calculated_distributions"]:
            self._monte_carlo_sampling_write_handle_pre_calc_function()

            self._monte_carlo_sampling_write_bin_function()

            self._monte_carlo_sampling_write_center_function()

        #########
        # Write to file
        monte_carlo_sampling_sampling_functions_filename = (
            self._monte_carlo_sampling_get_sampling_functions_filename()
        )

        self.grid_options[
            "_monte_carlo_sampling_sampling_functions_filename"
        ] = monte_carlo_sampling_sampling_functions_filename

        self.verbose_print(
            "{blue}Write sampling functions code to {file} {reset}".format(
                blue=self.ANSI_colours["blue"],
                file=monte_carlo_sampling_sampling_functions_filename,
                reset=self.ANSI_colours["reset"],
            ),
            self.grid_options["verbosity"],
            1,
        )

        with self.open(
            monte_carlo_sampling_sampling_functions_filename, "w", encoding="utf-8"
        ) as file:
            file.write(self.code_string)

        # Reset indentation
        self.code_string = ""

    # Construction
    def _monte_carlo_sampling_write_pdf_cdf_value_array_block(self, sampling_variable):
        """
        Function to write the code-block for the pdf/cdf value array functions
        """

        #######
        # Set up lists
        self._add_code(
            comment_line,
            "value_array = {}\n".format(
                sampling_variable["samplerfunc"]
            ),  # Line for the sampler func value array sampling (not the same as parameter value array)
            "parameter_value_array = []\n",
            "probability_array = [0]\n\n",
        )

        #######
        # Set up first parameter value array adding
        self._add_code(
            comment_line,
            "{} = value_array[0]\n".format(sampling_variable["name"]),
            "{}\n".format(
                sampling_variable["precode"].replace("\n", "\n" + self._indent_block(0))
            )
            if sampling_variable["precode"]
            else "\n",
            "parameter_value_array.append({})\n\n".format(
                sampling_variable["parameter_name"]
            ),
        )

        #######
        # Set up loop for sampling the distribution function
        self._add_code(
            comment_line,
            "for {} in value_array[1:]:\n".format(sampling_variable["name"]),
        )
        self._increment_indent_depth(+1)

        #######
        # Set up conversion with precode
        self._add_code(
            comment_line,
            "{}\n".format(
                sampling_variable["precode"].replace("\n", "\n" + self._indent_block(0))
            )
            if sampling_variable["precode"]
            else "\n",
            "parameter_value_array.append({})\n\n".format(
                sampling_variable["parameter_name"]
            ),
        )

        #######
        # Set up calculation of probability
        # TODO: implement the call to a second pdf here (could be anything, but perhaps a likelihood or AIS)
        self._add_code(
            comment_line,
            "probability = {}\n".format(sampling_variable["probdist"]),
            "probability_array.append(probability)\n\n",
        )
        self._increment_indent_depth(-1)

        #######
        # Construct method to calculate pdf/cdf and value array
        self._add_code(
            comment_line,
            "probability_array = np.array(probability_array)\n",
            "cdf_array = np.cumsum(probability_array) / np.sum(probability_array)\n",
            "parameter_value_array = np.array(parameter_value_array)\n\n",
        )

        #######
        # Construct pdf/cdf and array dict and return
        self._add_code(
            comment_line,
            "pdf_cdf_value_array_dict = {'probability_array': probability_array, 'cdf_array': cdf_array, 'value_array': value_array, 'parameter_value_array': parameter_value_array}\n\n",
        )

    def _monte_carlo_sampling_write_bin_function(self):
        """
        Function to write the bin function
        """

        self._add_code(
            comment_line,
            "def bin(parameter_value_array, parameter_value):\n",
            "    index = np.digitize(parameter_value, bins=parameter_value_array, right=False)-1\n",
            "    center_value = (parameter_value_array[index+1]+parameter_value_array[index])/2\n",
            "    return center_value\n",
        )

    def _monte_carlo_sampling_write_center_function(self):
        """
        Function to write the center function
        """

        self._add_code(
            comment_line,
            "def center(sampling_func):\n",
            "    value_array = sampling_func\n",
            "    center_value_array = (value_array[1:]+value_array[:-1])/2\n",
            "    return center_value_array\n",
        )

    def _monte_carlo_sampling_write_handle_pre_calc_function(self):
        """
        Function to write then handler function for the calc_sampled_value
        """

        #######
        # Construct function
        self._add_code(
            "def handle_pre_calc(self):\n".format(),
        )
        self._increment_indent_depth(+1)

        #######
        # Initialise dict
        self._add_code(
            "self.pre_calculated_pdf_cdf_value_array_dicts = {}\n",
        )

        #######
        # Loop over variables and call them to set the pre-calculated pdf cdf information in the dictionary
        for loopnr, sampling_variable_el in enumerate(
            sorted(
                self.grid_options["_sampling_variables"].items(),
                key=lambda x: x[1]["sampling_variable_number"],
            )
        ):
            sampling_variable = sampling_variable_el[1]

            #######
            # Write call to specific functions to pre-calculate each pdf/cdf dict
            self._add_code(
                "self.pre_calculated_pdf_cdf_value_array_dicts['{}'] = pre_calculate_pdf_cdf_value_array_dict_{}(self)\n".format(
                    sampling_variable["parameter_name"],
                    sampling_variable["parameter_name"],
                ),
            )

        #######
        # De-dent and padd
        self._increment_indent_depth(-1)
        self._add_code("\n\n")

    def _monte_carlo_sampling_write_calc_sampled_value_function(
        self, sampling_variable
    ):
        """
        Function to write the calc_sampled_value call
        """

        #######
        # Construct function
        self._add_code(
            "def calc_sampled_value_{}(self{}):\n".format(
                sampling_variable["parameter_name"],
                ", "
                + ",".join(
                    [
                        "{}".format(dependency_variable)
                        for dependency_variable in sampling_variable[
                            "dependency_variables"
                        ]
                    ]
                )
                if sampling_variable["dependency_variables"]
                else "",
            ),
        )
        self._increment_indent_depth(+1)

        #######
        # Call to pdf_cdf_value_array_dict function
        self._add_code(
            comment_line,
            "if self.grid_options['monte_carlo_use_pre_calculated_distributions']:\n",
        )

        ######
        # Add calls to the dependency variable's pre-calculated parameter_value_array
        if sampling_variable["dependency_variables"]:
            for dependency_variable in sampling_variable["dependency_variables"]:
                # Create string for getting the parameter value array
                string = "self.pre_calculated_pdf_cdf_value_array_dicts['{}']".format(
                    dependency_variable
                )

                if self.grid_options["_sampling_variables_parameter_names"][
                    dependency_variable
                ]["dependency_variables"]:
                    for depth in range(
                        0,
                        len(
                            self.grid_options["_sampling_variables_parameter_names"][
                                dependency_variable
                            ]["dependency_variables"]
                        ),
                    ):
                        string += "['{{:.6f}}'.format(binned_{})]".format(
                            sampling_variable["dependency_variables"][depth]
                        )

                # Add code to get the binned value of the current dependency value
                self._add_code(
                    "    binned_{} = bin({}['parameter_value_array'], {})\n".format(
                        dependency_variable, string, dependency_variable
                    )
                )

        self._add_code(
            "    pdf_cdf_value_array_dict = self.pre_calculated_pdf_cdf_value_array_dicts['{}']{}\n".format(
                sampling_variable["parameter_name"],
                "".join(
                    [
                        "['{{:.6f}}'.format(binned_{})]".format(dependency_variable)
                        for dependency_variable in sampling_variable[
                            "dependency_variables"
                        ]
                    ]
                )
                if sampling_variable["dependency_variables"]
                else "",
            ),
            "else:\n",
            "    pdf_cdf_value_array_dict = self.monte_carlo_calc_pdf_cdf_value_array_dict_functions['{}'](self{})\n\n".format(
                sampling_variable["parameter_name"],
                ", "
                + ",".join(
                    [
                        "{}".format(dependency_variable)
                        for dependency_variable in sampling_variable[
                            "dependency_variables"
                        ]
                    ]
                )
                if sampling_variable["dependency_variables"]
                else "",
            ),
            comment_line,
            "cdf_array = pdf_cdf_value_array_dict['cdf_array']\n",
            "value_array = pdf_cdf_value_array_dict['value_array']\n",
            "parameter_value_array = pdf_cdf_value_array_dict['parameter_value_array']\n\n",
        )

        #######
        # Get random sample
        self._add_code(
            comment_line,
            "random_sample = np.random.uniform(low=0.0, high=1.0, size=(1))\n\n",
        )

        #######
        # Calculate indices and edge points
        self._add_code(
            comment_line,
            "left_index = np.digitize(random_sample, bins=cdf_array, right=False)-1\n",
            "right_index = left_index + 1\n\n",
        )

        #######
        # Get probabilities of bin-edges and set
        self._add_code(
            comment_line,
            "left_cdf = cdf_array[left_index]\n",
            "right_cdf = cdf_array[right_index]\n",
            "dcdf = right_cdf - left_cdf\n\n",
        )

        #######
        # Get values of bin-edges and set
        self._add_code(
            comment_line,
            "left_value = parameter_value_array[left_index]\n",
            "right_value = parameter_value_array[right_index]\n",
            "dvalue = right_value - left_value\n\n",
        )

        #######
        # Calculate new point by interpolation
        self._add_code(
            comment_line,
            "dvalue_dcdf = dvalue/dcdf\n",
            "dist_to_left = random_sample - left_cdf\n",
            "{} = left_value + (dvalue_dcdf) * dist_to_left\n\n".format(
                sampling_variable["parameter_name"]
            ),
        )

        #######
        # Turn the new point into the actual parameter if we have post-code
        if sampling_variable["postcode"]:
            self._add_code(
                comment_line,
                sampling_variable["postcode"] + "\n\n",
            )

        #######
        # return value
        self._add_code(
            comment_line,
            "return {}[0]\n".format(sampling_variable["parameter_name"]),
        )

        #######
        # De-dent and padd
        self._increment_indent_depth(-1)
        self._add_code("\n\n")

    def _monte_carlo_sampling_write_calc_pdf_cdf_value_array_dict_function(
        self, sampling_variable
    ):
        """
        Function to write the calc_pdf_cdf_value_array_dict_function call
        """

        #######
        # Construct function
        self._add_code(
            "def calc_pdf_cdf_value_array_dict_{}(self{}):\n".format(
                sampling_variable["parameter_name"],
                ", "
                + ",".join(
                    [
                        "{}".format(dependency_variable)
                        for dependency_variable in sampling_variable[
                            "dependency_variables"
                        ]
                    ]
                )
                if sampling_variable["dependency_variables"]
                else "",
            ),
        )
        self._increment_indent_depth(+1)

        #######
        # Write the pdf cdf value array code block
        self._monte_carlo_sampling_write_pdf_cdf_value_array_block(sampling_variable)

        #######
        # Construct pdf/cdf and array dict and return
        self._add_code(
            "return pdf_cdf_value_array_dict\n",
        )

        #######
        # De-dent and pad
        self._increment_indent_depth(-1)
        self._add_code("\n\n")

    def _monte_carlo_sampling_write_handle_calc_sampled_value_function(self):
        """
        Function to write then handler function for the calc_sampled_value
        """

        #######
        # Construct function
        self._add_code(
            "def handle_calc_sampled_value(self, sampling_variable, **kwargs):\n".format(),
        )
        self._increment_indent_depth(+1)

        #######
        # Get correct function and call the function with the arguments
        self._add_code(
            "calc_sampled_value_function = self.monte_carlo_calc_sampled_value_functions[sampling_variable['parameter_name']]\n",
            "sampled_value = calc_sampled_value_function(self, **kwargs)\n\n",
            "return sampled_value\n",
        )

        #######
        # De-dent and padd
        self._increment_indent_depth(-1)
        self._add_code("\n\n")

    def _monte_carlo_sampling_write_pre_calc_function(self, sampling_variable):
        """
        Function to write the pre_calc function for each variable
        """

        #######
        # Construct function
        self._add_code(
            "def pre_calculate_pdf_cdf_value_array_dict_{}(self):\n".format(
                sampling_variable["parameter_name"]
            ),
        )
        self._increment_indent_depth(+1)

        #######
        # Handle construction if we have dependency variables
        if sampling_variable["dependency_variables"]:

            #######
            # Construct nested pdf cdf dict
            self._add_code(
                comment_line,
                "nested_pdf_cdf_value_array_dict = {}\n\n",
            )

            sampling_variable_dict_based_on_parameter_name = {
                sampling_variable_el["parameter_name"]: sampling_variable_el
                for sampling_variable_el in self.grid_options[
                    "_sampling_variables"
                ].values()
            }
            dependency_variable_list = [
                sampling_variable_dict_based_on_parameter_name[dependency_variable_key]
                for dependency_variable_key in sampling_variable["dependency_variables"]
            ]

            #######
            # Loop over all dependency variables
            for dependency_variable_i, dependency_variable_key in enumerate(
                sampling_variable["dependency_variables"]
            ):
                dependency_variable = sampling_variable_dict_based_on_parameter_name[
                    dependency_variable_key
                ]

                ################
                # Create dict if we are in
                if (
                    not dependency_variable_i
                    == len(sampling_variable["dependency_variables"])
                ) and (not dependency_variable_i == 0):
                    self._add_code(
                        comment_line,
                        "nested_pdf_cdf_value_array_dict['{{:.6f}}'.format({})] = {{}}\n".format(
                            sampling_variable["dependency_variables"][
                                dependency_variable_i - 1
                            ]
                        ),
                    )

                #######
                # Construct the loop over the
                self._add_code(
                    comment_line,
                    "value_array_{} = {}\n\n".format(
                        dependency_variable["name"], dependency_variable["samplerfunc"]
                    ),
                )

                #######
                # Set up loop for sampling the distribution function
                self._add_code(
                    comment_line,
                    "for {} in center(value_array_{}):\n\n".format(
                        dependency_variable["name"], dependency_variable["name"]
                    ),
                )
                self._increment_indent_depth(+1)

                self._add_code(
                    "{}\n".format(
                        dependency_variable["precode"].replace(
                            "\n", "\n" + self._indent_block(0)
                        )
                    )
                    if dependency_variable["precode"]
                    else "\n"
                )

            #######
            # Construct parts to build the pdf cdf function
            self._monte_carlo_sampling_write_pdf_cdf_value_array_block(
                sampling_variable
            )

            #######
            # Write code to store the dict in the nested dict
            nested_dict_calls = "".join(
                [
                    "['{{:.6f}}'.format({})]".format(
                        cur_dependency_variable["parameter_name"]
                    )
                    for cur_dependency_variable in dependency_variable_list
                ]
            )
            self._add_code(
                comment_line,
                "nested_pdf_cdf_value_array_dict{} = pdf_cdf_value_array_dict\n\n".format(
                    nested_dict_calls
                ),
            )

            #######
            # de-dent the code
            for dependency_variable_i, dependency_variable_key in enumerate(
                sampling_variable["dependency_variables"][::-1]
            ):
                self._increment_indent_depth(-1)

            #######
            # Construct dictionary to hold the other dictionaries
            self._add_code(
                "return nested_pdf_cdf_value_array_dict\n",
            )

        #######
        # Handle construction if we don't have dependency variables
        else:
            #######
            # Construct parts to build the pdf cdf function
            self._monte_carlo_sampling_write_pdf_cdf_value_array_block(
                sampling_variable
            )

            #######
            # Write return statement
            self._add_code(
                "return pdf_cdf_value_array_dict\n",
            )

        #######
        # De-dent and padd
        self._increment_indent_depth(-1)
        self._add_code("\n\n")

    # Misc
    def _sample_multiplicity(self, system_dict):
        """
        Function to calculate the multiplicity based on grid choices and random guess
        """

        ##############
        # If we choose to use no multiplicity fraction function then we always return multiplicity of 1
        if self.grid_options["multiplicity_fraction_function"] in [0, "None"]:
            return 1

        # Otherwise we will get the multiplicity fraction dict sample a random value to determine which multiplicty we have
        multiplicity_dict = self._get_multiplicity_dict(system_dict)

        # TODO: this can probably be a oneliner
        multiplicity_list, probability_list = [], []
        for multiplicity, probability in sorted(
            multiplicity_dict.items(), key=lambda x: x[0]
        ):
            multiplicity_list.append(multiplicity)
            probability_list.append(probability)
        multiplicity_array = np.array(multiplicity_list)
        probability_array = np.array(probability_list)

        ##############
        # Calculate CDF and sample
        probability_cdf = np.cumsum(probability_array)
        random_number = np.random.uniform()
        indices = np.digitize(random_number, bins=probability_cdf, right=False)

        # Get multiplicity and return
        multiplicity = multiplicity_array[indices]

        return multiplicity

    ##############
    # Management functions
    def _monte_carlo_sampling_load_generator(self):
        """
        Function to load the monte_carlo grid
        """

        # Code to load the generator code
        self.verbose_print(
            message="Load monte-carlo generator function from {file}".format(
                file=self.grid_options["_monte_carlo_sampling_generator_filename"]
            ),
            verbosity=self.grid_options["verbosity"],
            minimal_verbosity=1,
        )

        spec = importlib.util.spec_from_file_location(
            "binary_c_python_monte_carlo_sampling_generator",
            os.path.join(self.grid_options["_monte_carlo_sampling_generator_filename"]),
        )
        monte_carlo_sampling_generator_file = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(monte_carlo_sampling_generator_file)
        generator = monte_carlo_sampling_generator_file.monte_carlo_generator

        self.grid_options["_monte_carlo_sampling_generator"] = generator

        self.verbose_print("Grid code loaded", self.grid_options["verbosity"], 1)

        # raise NotImplementedError("This functionality is not available yet")

    def _monte_carlo_sampling_setup(self):
        """
        Function to prepate the class for a monte-carlo sampling simulation
        """

        print("setup mc sampling")

        # raise NotImplementedError("This functionality is not available yet")

    def _monte_carlo_sampling_get_generator(self):
        """
        Function to get the generator for the source_file sampling method. Called by _get_generator and used in the actual evolution loop.
        """

        # Write the sampling functions file
        self._monte_carlo_sampling_write_sampling_functions_file()

        # Load the sampling functions
        self._monte_carlo_sampling_load_sampling_functions_file()

        # Write generator file
        self._monte_carlo_sampling_write_generator_file()

        # Load generator
        self._monte_carlo_sampling_load_generator()

        # Get generator file
        generator = self.grid_options["_monte_carlo_sampling_generator"](
            self, print_results=False
        )

        return generator

    ##############
    # misc

    ##############
    # Writing binary_c calls to file:
    def monte_carlo_sampling_write_binary_c_calls_to_file(
        self, output_file, include_defaults
    ):
        """
        Function to write the generated grid to a file.
        TODO: this can be merged with the original write_binary_c_calls to file ... Have the get_generator handle the setup
        """

        #######
        # Start up the generator
        generator = self._get_generator()

        if not self.grid_options["monte_carlo_mass_threshold"] > 0:
            raise ValueError("Cant write MC sampling to file without a mass threshold")

        # then if the _system_generator is present, we go through it
        if generator:
            # Write to file
            with self.open(output_file, "w", encoding="utf-8") as file:
                # Get defaults and clean them, then overwrite them with the set values.
                if include_defaults:
                    # TODO: make sure that the defaults here are cleaned up properly
                    cleaned_up_defaults = self.cleaned_up_defaults
                    full_system_dict = cleaned_up_defaults.copy()
                    full_system_dict.update(self.bse_options.copy())
                else:
                    full_system_dict = self.bse_options.copy()

                for system_number, system_dict in enumerate(generator):
                    # update values with current system values
                    full_system_dict.update(system_dict)

                    ######
                    # Handle monte-carlo threshold based on evolved mass
                    if self.grid_options["evolution_type"] == "monte_carlo":
                        # Check based on mass threshold
                        self._monte_carlo_sampling_check_mass_threshold(
                            full_system_dict
                        )

                        ######
                        # Check if evolution threshold is reached.
                        if self.grid_options["_monte_carlo_threshold_reached"]:
                            break

                    #
                    binary_cmdline_string = self._return_argline(full_system_dict)
                    file.write(binary_cmdline_string + "\n")
        else:
            print("Error. No grid function found!")
            raise ValueError

        return output_file
