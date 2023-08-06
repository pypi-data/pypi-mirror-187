"""
Main script to provide the sampling variable class extension. Here the sampling variable codebase is defined.
"""

# pylint: disable=E1101
import json
from typing import Union


class sampling_variables:
    """
    Extension for the Population class containing the code for the sampling variable.
    """

    def __init__(self, **kwargs):
        """
        Init function for the spacing_functions class
        """

        return

    def _last_sampling_variable(self):
        """
        Function that returns the last sampling variable (i.e. the one with the highest sampling_variable_number)

        """

        # Get total number of sampling variables
        number = len(self.grid_options["_sampling_variables"])

        # Get dictionary of grid variable numbers
        # RGI: broken?
        #sampling_variable_dict = {
        #    sampling_variable["sampling_variable_number"]: sampling_variable
        #    for sampling_variable in self.grid_options["_sampling_variables"]
        #}

        # Get dictionary of grid variable numbers
        sampling_variable_dict = {
            self.grid_options['_sampling_variables'][sampling_variable]["sampling_variable_number"]: sampling_variable
            for sampling_variable in self.grid_options["_sampling_variables"]
        }

        #
        return sampling_variable_dict[number - 1]

    def update_sampling_variable(self, name: str, **kwargs) -> None:
        """
        Function to update the values of a sampling variable.

        Args:
            name:
                name of the grid variable to be changed.
            **kwargs:
                key-value pairs to override the existing grid variable data. See add_sampling_variable for these names.
        """

        if name in self.grid_options["_sampling_variables"]:
            sampling_variable = self.grid_options["_sampling_variables"][name]

            # Set the value and print
            for key, value in kwargs.items():
                sampling_variable[key] = value
                self.verbose_print(
                    "Updated grid variable: {}".format(
                        json.dumps(sampling_variable, indent=4, ensure_ascii=False)
                    ),
                    self.grid_options["verbosity"],
                    1,
                )
        else:
            msg = "Unknown sampling variable {} - please create it with the add_sampling_variable() method.".format(
                name
            )
            raise KeyError(msg)

    def delete_sampling_variable(
        self,
        name: str,
    ) -> None:
        """
        Function to delete a sampling variable with the given name.

        Args:
            name:
                name of the sampling variable to be deleted.
        """

        if name in self.grid_options["_sampling_variables"]:
            del self.grid_options["_sampling_variables"][name]
            self.verbose_print(
                "Deleted sampling variable: {}".format(name),
                self.grid_options["verbosity"],
                1,
            )
        else:
            msg = (
                "Failed to remove sampling variable {}: please check it exists.".format(
                    name
                )
            )
            raise ValueError(msg)

    def rename_sampling_variable(self, oldname: str, newname: str) -> None:
        """
        Function to rename a sampling variable.

        note: this does NOT alter the order
        of the self.grid_options["_sampling_variables"] dictionary.

        The order in which the sampling variables are loaded into the grid is based on their
        `sampling_variable_number` property

        Args:
            oldname:
                old name of the sampling variable
            newname:
                new name of the sampling variable
        """

        if oldname in self.grid_options["_sampling_variables"]:
            self.grid_options["_sampling_variables"][newname] = self.grid_options[
                "_sampling_variables"
            ].pop(oldname)
            self.grid_options["_sampling_variables"][newname]["name"] = newname
            self.verbose_print(
                "Rename sampling variable: {} to {}".format(oldname, newname),
                self.grid_options["verbosity"],
                1,
            )
        else:
            msg = "Failed to rename sampling variable {} to {}.".format(
                oldname, newname
            )
            raise ValueError(msg)

    def add_sampling_variable(
        self,
        name: str,
        parameter_name: str,
        longname: str,
        valuerange: Union[list, str],
        samplerfunc: str,
        probdist: str,
        dphasevol: Union[str, int] = -1,
        gridtype: str = "centred",
        branchpoint: int = 0,
        branchcode: Union[str, None] = None,
        precode: Union[str, None] = None,
        postcode: Union[str, None] = None,
        topcode: Union[str, None] = None,
        bottomcode: Union[str, None] = None,
        condition: Union[str, None] = None,
        dry_parallel: Union[bool, None] = False,
        dependency_variables: Union[list, None] = None,
    ) -> None:
        """
        Function to add sampling variables to the grid_options.

        The execution of the sampling generation will be through a nested for loop.
        Each of the grid variables will get create a deeper for loop.

        The real function that generates the numbers will get written to a new file in the TMP_DIR,
        and then loaded imported and evaluated.
        beware that if you insert some destructive piece of code, it will be executed anyway.
        Use at own risk.

        Args:
            name:
                name of parameter used in the grid Python code.
                This is evaluated as a parameter and you can use it throughout
                the rest of the function

                Examples::

                    name = 'lnM_1'

            parameter_name:
                name of the parameter in binary_c

                This name must correspond to a Python variable of the same name,
                which is automatic if parameter_name == name.

                Note: if parameter_name != name, you must set a
                      variable in "precode" or "postcode" to define a Python variable
                      called parameter_name

            longname:
                Long name of parameter

                Examples::

                    longname = 'Primary mass'

            range:
                Range of values to take. Does not get used really, the samplerfunc is used to
                get the values from

                Examples::

                    range = [math.log(m_min), math.log(m_max)]

            samplerfunc:
                Function returning a list or numpy array of samples spaced appropriately.
                You can either use a real function, or a string representation of a function call.

                Examples::

                    samplerfunc = "self.const_linear(math.log(m_min), math.log(m_max), {})".format(resolution['M_1'])

            precode:
                Extra room for some code. This code will be evaluated within the loop of the
                sampling function (i.e. a value for lnM_1 is chosen already)

                Examples::

                    precode = 'M_1=math.exp(lnM_1);'

            postcode:
                Code executed after the probability is calculated.

            probdist:
                Function determining the probability that gets assigned to the sampled parameter

                Examples::

                    probdist = 'self.Kroupa2001(M_1)*M_1'

            dphasevol:
                part of the parameter space that the total probability is calculated with. Put to -1
                if you want to ignore any dphasevol calculations and set the value to 1

                Examples::

                    dphasevol = 'dlnM_1'

            condition:
                condition that has to be met in order for the grid generation to continue

                Examples::

                    condition = "self.grid_options['binary']==1"

            gridtype:
                Method on how the value range is sampled. Can be either 'edge' (steps starting at
                the lower edge of the value range) or 'centred'
                (steps starting at ``lower edge + 0.5 * stepsize``).

            dry_parallel:
                If True, try to parallelize this variable in dry runs.

            topcode:
                Code added at the very top of the block.

            bottomcode:
                Code added at the very bottom of the block.

            dependency_variables:
                TODO: describe
        """

        # check parameters
        # if False and dphasevol != -1.0 and gridtype == "discrete":
        if dphasevol != -1.0 and gridtype == "discrete":
            print(
                "Error making grid: you have set the phasevol to be not -1 and gridtype to discrete, but a discrete grid has no phasevol calculation. You should only set the gridtype to discrete and not set the phasevol in this case."
            )

            self.exit(code=1)

        # Add sampling_variable
        sampling_variable = {
            "name": name,
            "parameter_name": parameter_name,
            "longname": longname,
            "valuerange": valuerange,
            "samplerfunc": samplerfunc,
            "precode": precode,
            "postcode": postcode,
            "probdist": probdist,
            "dphasevol": dphasevol,
            "condition": condition,
            "gridtype": gridtype,
            "branchpoint": branchpoint,
            "branchcode": branchcode,
            "topcode": topcode,
            "bottomcode": bottomcode,
            "sampling_variable_number": len(self.grid_options["_sampling_variables"]),
            "dry_parallel": dry_parallel,
            "dependency_variables": dependency_variables,
        }

        # Check for gridtype input
        allowed_gridtypes = [
            "edge",
            "right",
            "right edge",
            "left",
            "left edge",
            "centred",
            "centre",
            "center",
            "discrete",
        ]

        if gridtype not in allowed_gridtypes:
            msg = "Unknown gridtype {gridtype}. Please choose one of: ".format(
                gridtype=gridtype
            ) + ",".join(allowed_gridtypes)
            raise ValueError(msg)

        # Load it into the grid_options
        self.grid_options["_sampling_variables"][
            sampling_variable["name"]
        ] = sampling_variable

        self.verbose_print(
            "Added sampling variable: {}".format(
                json.dumps(sampling_variable, indent=4, ensure_ascii=False)
            ),
            self.grid_options["verbosity"],
            2,
        )

    ######################################################################
    # Functions to maintain compatibility with older scripts
    ######################################################################
    def _last_grid_variable(self):
        """
        NOTE: this function exists for backward compatability with older scripts. Please use _last_sampling_variable from now on.

        Function that returns the last sampling variable (i.e. the one with the highest grid_variable_number). Wrapper that calls _last_sampling_variable.
        """

        return self._last_sampling_variable()

    def update_grid_variable(self, name: str, **kwargs) -> None:
        """
        NOTE: this function exists for backward compatability with older scripts. Please use update_sampling_variable from now on.

        Function to update the values of a sampling variable. Calls update_sampling_variable().

        Args:
            name:
                name of the grid variable to be changed.
            **kwargs:
                key-value pairs to override the existing grid variable data. See add_sampling_variable for these names.
        """

        self.update_sampling_variable(name, **kwargs)

    def delete_grid_variable(
        self,
        name: str,
    ) -> None:
        """
        NOTE: this function exists for backward compatability with older scripts. Please use delete_sampling_variable from now on.

        Function to delete a sampling variable with the given name. Calls delete_sampling_variable()

        Args:
            name:
                name of the sampling variable to be deleted.
        """

        self.delete_sampling_variable(name)

    def rename_grid_variable(self, oldname: str, newname: str) -> None:
        """
        NOTE: this function exists for backward compatability with older scripts. Please use rename_sampling_variable from now on.

        Function to rename a sampling variable. Calls rename_sampling_variable()

        note: this does NOT alter the order
        of the self.grid_options["_sampling_variables"] dictionary.

        The order in which the sampling variables are loaded into the grid is based on their
        `sampling_variable_number` property

        Args:
            oldname:
                old name of the sampling variable
            newname:
                new name of the sampling variable
        """

        self.rename_sampling_variable(oldname=oldname, newname=newname)

    def add_grid_variable(
        self,
        name: str,
        parameter_name: str,
        longname: str,
        valuerange: Union[list, str],
        samplerfunc: str,
        probdist: str,
        dphasevol: Union[str, int] = -1,
        gridtype: str = "centred",
        branchpoint: int = 0,
        branchcode: Union[str, None] = None,
        precode: Union[str, None] = None,
        postcode: Union[str, None] = None,
        topcode: Union[str, None] = None,
        bottomcode: Union[str, None] = None,
        condition: Union[str, None] = None,
        dry_parallel: Union[bool, None] = False,
    ) -> None:
        """
        NOTE: this function exists for backward compatability with older scripts. Please use add_sampling_variable from now on.

        Function to add sampling variables to the grid_options. Calls add_sampling_variable().

        The execution of the sampling generation will be through a nested for loop.
        Each of the grid variables will get create a deeper for loop.

        The real function that generates the numbers will get written to a new file in the TMP_DIR,
        and then loaded imported and evaluated.
        beware that if you insert some destructive piece of code, it will be executed anyway.
        Use at own risk.

        Args:
            name:
                name of parameter used in the grid Python code.
                This is evaluated as a parameter and you can use it throughout
                the rest of the function

                Examples::

                    name = 'lnM_1'

            parameter_name:
                name of the parameter in binary_c

                This name must correspond to a Python variable of the same name,
                which is automatic if parameter_name == name.

                Note: if parameter_name != name, you must set a
                      variable in "precode" or "postcode" to define a Python variable
                      called parameter_name

            longname:
                Long name of parameter

                Examples::

                    longname = 'Primary mass'

            range:
                Range of values to take. Does not get used really, the samplerfunc is used to
                get the values from

                Examples::

                    range = [math.log(m_min), math.log(m_max)]

            samplerfunc:
                Function returning a list or numpy array of samples spaced appropriately.
                You can either use a real function, or a string representation of a function call.

                Examples::

                    samplerfunc = "self.const_linear(math.log(m_min), math.log(m_max), {})".format(resolution['M_1'])

            precode:
                Extra room for some code. This code will be evaluated within the loop of the
                sampling function (i.e. a value for lnM_1 is chosen already)

                Examples::

                    precode = 'M_1=math.exp(lnM_1);'

            postcode:
                Code executed after the probability is calculated.

            probdist:
                Function determining the probability that gets assigned to the sampled parameter

                Examples::

                    probdist = 'self.Kroupa2001(M_1)*M_1'

            dphasevol:
                part of the parameter space that the total probability is calculated with. Put to -1
                if you want to ignore any dphasevol calculations and set the value to 1

                Examples::

                    dphasevol = 'dlnM_1'

            condition:
                condition that has to be met in order for the grid generation to continue

                Examples::

                    condition = "self.grid_options['binary']==1"

            gridtype:
                Method on how the value range is sampled. Can be either 'edge' (steps starting at
                the lower edge of the value range) or 'centred'
                (steps starting at ``lower edge + 0.5 * stepsize``).

            dry_parallel:
                If True, try to parallelize this variable in dry runs.

            topcode:
                Code added at the very top of the block.

            bottomcode:
                Code added at the very bottom of the block.
        """

        self.add_sampling_variable(
            name=name,
            parameter_name=parameter_name,
            longname=longname,
            valuerange=valuerange,
            samplerfunc=samplerfunc,
            probdist=probdist,
            dphasevol=dphasevol,
            gridtype=gridtype,
            branchpoint=branchpoint,
            branchcode=branchcode,
            precode=precode,
            postcode=postcode,
            topcode=topcode,
            bottomcode=bottomcode,
            condition=condition,
            dry_parallel=dry_parallel,
        )
