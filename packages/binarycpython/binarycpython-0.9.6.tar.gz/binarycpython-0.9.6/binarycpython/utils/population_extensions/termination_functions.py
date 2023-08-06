"""
Main script to provide the termination functions class extensions
"""

# pylint: disable=E1101

import sys
import traceback


class termination_functions:
    """
    Extension for the Population class containing the code for termination functions
    """

    def __init__(self, **kwargs):
        """
        Init function for the ensemble class
        """

        return

    def was_killed(self):
        """
        Function to determine if the process was killed. Returns True if so, false otherwise.
        """

        killed = self.grid_options["_killed"]

        if "_killed" in self.grid_ensemble_results.get("metadata", {}):
            killed = killed or self.grid_ensemble_results["metadata"]["_killed"]

        return killed

    def exit(self, code=None, message=True, flush=True, stacktrace=False):
        """
        Exit function: use this to exit from a Population object.
        Really it's just a wrapper for sys.exit() to return the correct exit code,
        but also to post a message (if message is True, default is True)
        and perhaps a stacktrace (if stacktrace is True, default is False).
        """
        # if we've been killed, set exit code to 1
        if self.grid_options["exit_code"] == 0 and self.grid_options["_killed"]:
            self.grid_options["exit_code"] = 1
        # but override with code passed in
        if code:
            self.grid_options["exit_code"] = code
        if message:
            print(
                "exit from binary_c-python Population with code {}".format(
                    self.grid_options["exit_code"]
                )
            )
        if flush:
            sys.stdout.flush()
        if stacktrace or self.grid_options["print_stack_on_exit"]:
            traceback.print_stack()
        sys.exit(self.grid_options["exit_code"])

    def _all_children_running(self, processes):
        """
        Function to test if all child processes are running.
        """

        for p in processes:
            if p.is_alive() is False and p.exitcode != 0:
                print(
                    "Warning: process",
                    p,
                    "is no longer alive and hasn't returned good data.",
                )
                self._log_failure(process=p, exitcode=p.exitcode)
                return False

        return True

    def _kill_child_processes(self, processes):
        """
        Function to kill all child processes.
        """

        for p in processes:
            if p.is_alive():
                p.kill()
