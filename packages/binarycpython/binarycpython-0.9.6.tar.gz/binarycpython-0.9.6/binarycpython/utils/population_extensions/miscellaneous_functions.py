"""
Main script to provide some extra miscellaneous functions that are not part of any of the other mixins yet
"""

# pylint: disable=E1101
import sys

import psutil

import binarycpython


class miscellaneous_functions:
    """
    Extension for the Population class containing some miscellaneous functions
    """

    def __init__(self, **kwargs):
        """
        Init function for the spacing_functions class
        """

        return

    def my_hostnames(self):
        """
        Function to find the hostnames of the current filesystem
        """

        if self.hostnameslist is None:
            self.hostnameslist = binarycpython.utils.functions.hostnames()
        return self.hostnameslist

    def expand_args_by_hostname(self, cmdline_args):
        """
        Expand a set of arguments by scanning each of them
        for host-specific dicts.

        Given each arg, either as a string "x=y" or dict {x:y},
        determine whether y is a dict and if so does one of the keys
        match the current hostname or "default", if so use the
        corresponding value for the current machine.
        """

        new_cmdline_args = None

        # loop over list of cmdline args
        if isinstance(cmdline_args, list):
            new_cmdline_args = []
            for cmdline_arg in cmdline_args:
                new_arg = self._match_arg_to_host(arg=cmdline_arg)
                new_cmdline_args.append(new_arg)

        # loop over a dict of cmdline args
        elif isinstance(cmdline_args, dict):
            new_cmdline_args = {}
            for parameter, value in cmdline_args.items():
                new_arg = self._match_arg_to_host(arg={parameter: value})
                new_cmdline_args[parameter] = new_arg

        return new_cmdline_args

    def _match_arg_to_host(self, arg=None, hostnameslist=None, vb=False):
        """
        Given an arg, either as a string "x=y" or dict {x:y},
        determine whether y is a dict and if so does one of the keys
        match the current hostname or "default", if so use the
        corresponding value. If not, return the original arg's value.

        NOTE: (david): this function could probably be a normal function (hardly any self. calls)
        """
        if arg is None:
            return None

        if hostnameslist is None:
            hostnameslist = self.my_hostnames()

        if isinstance(arg, dict):
            # {parameter: value} dict arg
            parameter = list(arg.keys())[0]
            value = list(arg.values())[0]
            argtype = "dict"
        else:
            # scalar x=y arg
            split = arg.split("=")
            if len(split) == 2:
                parameter = split[0]
                value = split[1]
                argtype = "list"
            else:
                parameter = None
                value = None
                argtype = None

        if parameter:
            if vb:
                print(
                    f"_match_arg_to_host: {parameter} = {value} (argtype = {argtype})"
                )
            try:
                if vb:
                    print("Try to eval", value)
                if isinstance(value, str):
                    # string : eval it
                    _x = eval(value)
                else:
                    _x = value

                # if dict, match to hostnames or 'default'
                if isinstance(_x, dict):
                    _match = None
                    for host in hostnameslist:
                        if vb:
                            print(f"check host={host}")
                        _match = _x.get(host, None)
                        if _match:
                            if vb:
                                print(
                                    f"Parameter {parameter} matches a value set by host={host} -> {_match}"
                                )
                            break

                    # no match? try 'default'
                    if not _match:
                        _match = _x.get("default", None)

                    # no match? error
                    if not _match:
                        print(
                            f"Parameter {parameter} is a dict {value} none of the keys or which matches our hostname ({hostnameslist}) or 'default'. Please update this parameter."
                        )
                        sys.exit(1)
                    else:
                        if vb:
                            print(f"Parameter {parameter} set to value {_match}")
                        value = _match
            except:
                pass

            if argtype == "list":
                # return x=y type argument
                new_arg = f"{parameter}={value}"
            else:
                new_arg = value

        if vb:
            print("return arg", new_arg, "of type", type(value))
        return new_arg

    def _set_nprocesses(self):
        """
        Function to set the number of processes used in multiprocessing.

        Test the value of grid_options['num_cores']:

        * If 0 or 'logical' or 'all logical', use all logical cores.

        * If -1 or 'physical' or 'all physical', use all physical cores.

        * If integer >=1 use the number of cores given.

        * If  a dict, (key,value) pairs are (hostname,num_cores)
          for particular machines. We then try to match this machine to
          the (hostname,num_cores) pairs to set num_cores. If not found,
          default to either the dict "default" setting, or the number
          of logical cores available.

        * If grid_options['num_cores'] is missing, all logical cores are used.

        Exit if none of the above are satisfied.

        """
        _vb = self.grid_options["verbosity"] >= 2

        def __nprocs(ncores):
            """
            Function to determine the number of processes
            """

            if type(ncores) is str:
                if ncores == "all" or ncores == "logical" or ncores == "all logical":
                    # use all logical cores available to us
                    return max(1, psutil.cpu_count(logical=True))
                elif ncores == "all physical" or ncores == "physical":
                    # use all physical cores available to us
                    return max(1, psutil.cpu_count(logical=False))
                else:
                    # unknown string : fall back to one CPU
                    print(
                        f"grid_option['num_cores'] = \"{ncores}\" is not recognised.\nPlease consider either setting this option to a number, 'physical' or 'logical', or a dict of (host,num_cores) pairs."
                    )
                    self.exit(code=1)

            if type(ncores) is int:
                if ncores == -1:
                    return max(1, psutil.cpu_count(logical=False))
                elif ncores == 0:
                    return max(1, psutil.cpu_count(logical=True))
                else:
                    return ncores
            else:
                # ncores should be int or string, oops
                print(
                    f"grid_option['num_cores'] = \"{ncores}\" is not recognised.\nPlease consider either setting this option to a number, 'physical' or 'logical', or a dict of (host,num_cores) pairs."
                )
                self.exit(code=1)

        if _vb:
            print(
                f"NPROC: pre-eval \"{self.grid_options['num_cores']}\" type \"{type(self.grid_options['num_cores'])}\""
            )

        # eval the incoming string if possible, it may be a JSON
        # representation of a dict, and if this works we
        # set the num_cores option to the eval'd version.
        # It may also be a normal string or int, so we can't just
        # use the JSON parser.
        try:
            _x = eval(self.grid_options["num_cores"])
            self.grid_options["num_cores"] = _x
        except:
            pass

        # backwards compatibility
        if "amt_cores" in self.grid_options:
            self.grid_options["num_cores"] = self.grid_options["amt_cores"]

        if _vb:
            print(
                f"NPROC: \"{self.grid_options['num_cores']}\" type \"{type(self.grid_options['num_cores'])}\""
            )

        if "num_cores" in self.grid_options:
            if _vb:
                print("NPROC found in grid options")
            if type(self.grid_options["num_cores"]) is dict:
                # try to match hostname to the dict keys
                hostnameslist = self.my_hostnames()
                for host, ncores in self.grid_options["num_cores"].items():
                    # check if we are this host
                    if host in hostnameslist:
                        self.grid_options["num_processes"] = __nprocs(ncores)
                        if _vb:
                            print(
                                f"SET NPROC = {self.grid_options['num_processes']} FROM HOST {host}"
                            )
                        return

                # no host match : use default number of cores
                if "default" in self.grid_options["num_cores"]:
                    self.grid_options["num_processes"] = __nprocs(
                        self.grid_options["num_cores"]["default"]
                    )
                    if _vb:
                        print(
                            f"SET NPROC = {self.grid_options['num_processes']} FROM default"
                        )
                    return
            elif type(self.grid_options["num_cores"]) is str:
                # just use int passed in
                self.grid_options["num_processes"] = __nprocs(
                    self.grid_options["num_cores"]
                )
                if _vb:
                    print(
                        f"SET NPROC = {self.grid_options['num_processes']} from string passed in"
                    )
                return
            elif type(self.grid_options["num_cores"]) is int:
                # just use int passed in
                self.grid_options["num_processes"] = __nprocs(
                    self.grid_options["num_cores"]
                )
                if _vb:
                    print(
                        f"SET NPROC = {self.grid_options['num_processes']} from int passed in"
                    )
                return

        # no host matched or no 'num_cores' option provided: use all available logical cores
        self.grid_options["num_processes"] = max(1, psutil.cpu_count(logical=True))
        if _vb:
            print(
                f"SET NPROC = {self.grid_options['num_processes']} because no option given"
            )

        return
