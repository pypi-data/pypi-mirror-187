"""
Main script to provide the signal handling class extensions
"""

# pylint: disable=E1101
import os
import signal


class signal_handling:
    """
    Extension for the Population class containing the code for source-file sampling functions
    """

    def __init__(self, **kwargs):
        """
        Init function for the spacing_functions class
        """

        return

    def _child_signal_handler(self, signal_data, signum, frame):
        """
        Signal handler for child processes.
        """
        sigstring = signal.Signals(signum).name

        if sigstring in self.signal_count:
            self.signal_count[sigstring] += 1
        else:
            self.signal_count[sigstring] = 1

        # if we receive the signal three times, exit
        if self.signal_count[sigstring] > 3:
            print("caught > 3 times : exit")
            self.exit(code=2)

        print(
            "Child signal {} caught (count {}) handler set in {} [ keys {} ]".format(
                sigstring,
                self.signal_count[sigstring],
                signal_data["where"],
                ",".join(signal_data.keys()),
            )
        )

        # SIGINT should stop the queue nicely
        if signum == signal.SIGINT:
            self.grid_options["stop_queue"] = True
            self.grid_options["_killed"] = True

        # propagate signal to parent
        os.kill(self.grid_options["_main_pid"], signum)

    def _parent_signal_handler(self, signal_data, signum, frame):
        """
        Signal handling function for the parent process.
        """

        # this function is called by both queues when they
        # catch a signal
        sigstring = signal.Signals(signum).name

        if sigstring in self.signal_count:
            self.signal_count[sigstring] += 1
        else:
            self.signal_count[sigstring] = 1

        if self.signal_count[sigstring] > 3:
            print("caught > 3 times : exit")
            self.exit(code=2)

        # tell the user what has happened
        print(
            "Parent signal {} caught (count {}) handler set in {} [ keys {} ]".format(
                sigstring,
                self.signal_count[sigstring],
                signal_data["where"],
                ",".join(signal_data.keys()),
            )
        )

        # set status files
        self.set_status("signal {sig}".format(sig=sigstring))

        if signum == signal.SIGINT:
            # caught SIGINT: e.g. CTRL-C or HPC job manager
            # shutting us down
            print("Parent set stop_queue to True")
            self.grid_options["stop_queue"] = True
            self.custom_options["save_snapshot"] = True
            self.grid_options["_killed"] = True
            return
        else:
            # what to do?
            return
