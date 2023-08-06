"""
Main script to provide the failing systems functions class extension
"""

# pylint: disable=E1101

import datetime
import os


class failing_systems_functions:
    """
    Extension for the Population class containing the code for failing systems functionality
    """

    def __init__(self, **kwargs):
        """
        Init function for the spacing_functions class
        """

        return

    def _log_failure(
        self, system_dict=None, system_number=None, process=None, exitcode=None
    ):
        """
        Log failing or crashed system to file in log_failed_systems_dir
        """

        if (
            self.grid_options["log_failed_systems"]
            and self.grid_options["log_failed_systems_dir"] is not None
        ):
            path = os.path.join(self.grid_options["log_failed_systems_dir"])
            os.makedirs(path, exist_ok=True)
            if self.dir_ok(path):
                failed_systems_file = os.path.join(
                    self.grid_options["log_failed_systems_dir"],
                    "process_{}.txt".format(self.jobID()),
                )
                with self.open(
                    failed_systems_file, "a", encoding="utf-8"  # append
                ) as f:
                    now = datetime.datetime.now()
                    now = now.strftime("%d/%m/%Y %H:%M:%S\n")
                    if system_dict:
                        binary_c_cmdline_string = (
                            f"system {system_number} at {now} "
                            + self._return_argline(system_dict)
                            + "\n"
                        )
                        f.write(binary_c_cmdline_string)
                    if process:
                        print(f"logged crashed process to {failed_systems_file}")
                        f.write(
                            f"Process {process} crashed at {now} with exit code {exitcode}."
                        )
        return

    def _check_binary_c_error(self, system_number, binary_c_output, system_dict):
        """
        Function to check whether binary_c throws an error and handle accordingly.
        """

        if binary_c_output:
            if (binary_c_output.splitlines()[0].startswith("SYSTEM_ERROR")) or (
                binary_c_output.splitlines()[-1].startswith("SYSTEM_ERROR")
            ):
                self.verbose_print(
                    "FAILING SYSTEM FOUND",
                    self.grid_options["verbosity"],
                    0,
                )

                # Keep track of the amount of failed systems and their error codes
                self.grid_options["_failed_prob"] += system_dict.get("probability", 1)
                self.grid_options["_failed_count"] += 1
                self.grid_options["_errors_found"] = True

                try:
                    error_code = int(
                        binary_c_output.splitlines()[0]
                        .split("with error code")[-1]
                        .split(":")[0]
                        .strip()
                    )
                    self.verbose_print(
                        f"Have error code {error_code}",
                        self.grid_options["verbosity"],
                        0,
                    )
                except:
                    self.verbose_print(
                        "Failed to extract error code",
                        self.grid_options["verbosity"],
                        0,
                    )
                    pass

                # Try catching the error code and keep track of the unique ones.
                try:
                    error_code = int(
                        binary_c_output.splitlines()[0]
                        .split("with error code")[-1]
                        .split(":")[0]
                        .strip()
                    )

                    if (
                        error_code
                        not in self.grid_options["_failed_systems_error_codes"]
                    ):
                        print(f"Caught errr code {error_code}")
                        self.grid_options["_failed_systems_error_codes"].append(
                            error_code
                        )
                except ValueError:
                    error_code = None
                    self.verbose_print(
                        "Failed to extract the error-code",
                        self.grid_options["verbosity"],
                        1,
                    )

                # log failing args?
                self._log_failure(system_dict=system_dict, system_number=system_number)

                # Check if we have exceeded the number of errors
                print(
                    f"Check failed count {self.grid_options['_failed_count']} vs max {self.grid_options['failed_systems_threshold']}"
                )
                if (
                    self.grid_options["_failed_count"]
                    > self.grid_options["failed_systems_threshold"]
                ):

                    # stop evolving systems
                    self.grid_options["stop_queue"]

                    # warn the user the first time we exceed failed_systems_threshold
                    if not self.grid_options["_errors_exceeded"]:
                        self.verbose_print(
                            self._boxed(
                                "Process {} exceeded the maximum ({}) number of failing systems. Stopped logging them to files now".format(
                                    self.process_ID,
                                    self.grid_options["failed_systems_threshold"],
                                )
                            ),
                            self.grid_options["verbosity"],
                            1,
                        )
                        self.grid_options["_errors_exceeded"] = True

        else:
            self.verbose_print(
                "binary_c output nothing - this is strange. If there is ensemble output being generated then this is fine.",
                self.grid_options["verbosity"],
                3,
            )
