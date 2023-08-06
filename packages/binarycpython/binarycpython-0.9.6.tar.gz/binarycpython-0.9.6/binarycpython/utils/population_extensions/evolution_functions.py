"""
The class extension for the population object that contains the evolution functionality
"""

import datetime
import functools
import gc
import json
import multiprocessing

# pylint: disable=E1101
import os
import queue
import signal
import sys
import time
from collections import OrderedDict
from typing import Any

import setproctitle

from binarycpython import _binary_c_bindings
from binarycpython.utils.dicts import keys_to_floats, merge_dicts
from binarycpython.utils.ensemble import format_ensemble_results
from binarycpython.utils.functions import (
    calculate_total_mass_system,
    mem_use,
    now,
    timedelta,
)

# Set method to fork.
multiprocessing.set_start_method("fork")


class evolution_functions:
    """
    Extension for the Population class to extend it with general evolution functions
    """

    def __init__(self, **kwargs):
        """
        Init function for the evolution_functions class
        """

        return

    ###################
    # Evolution functions

    def _evolve_population_wrapper(self):
        """
        Function to evolve populations. This handles the setting up, evolving
        and cleaning up of a population of stars.

        Returns True if the grid runs, False on error.
        """

        ############################################################
        # Prepare code/initialise grid.
        # set custom logging, set up store_memaddr, build grid code. dry run grid code.
        if self._setup() is False:
            return

        ############################################################
        # Evolve systems
        self.set_time("start")
        if (
            self.grid_options["evolution_type"]
            in self.grid_options["_evolution_type_options"]
        ):
            if self.grid_options["evolution_type"] in [
                "grid",
                "custom_generator",
                "monte_carlo",
            ]:
                if self._evolve_population_core() is False:
                    return False
        else:
            print(
                "Warning. you chose a wrong option for the grid evolution types.\
                Please choose from the following: {}.".format(
                    self.grid_options["_evolution_type_options"]
                )
            )
            raise ValueError()
        self.set_time("end")

        ############################################################
        # Log and print some information
        string1 = "Population-{} finished!\nThe total probability is {:g}.".format(
            self.grid_options["_population_id"], self.grid_options["_probtot"]
        )
        string2 = "It took a total of {dtsecs} to run {starcount} systems on {ncores} cores\n = {CPUtime} of CPU time.\nMaximum memory use {memuse:.3f} MB".format(
            dtsecs=timedelta(self.grid_options["_time_elapsed"]),
            starcount=self.grid_options[
                "_count"
            ],  # not _total_count! we may have ended the run early...
            ncores=self.grid_options["num_processes"],
            CPUtime=timedelta(self.CPU_time()),
            memuse=sum(self.shared_memory["max_memory_use_per_thread"]),
        )

        ############################################################
        # add warning about a grid that was killed
        ############################################################
        if self.was_killed():
            string2 += "\n>>> Grid was killed <<<"
            self.set_status("killed")

        self.verbose_print(
            self._boxed(string1, string2), self.grid_options["verbosity"], 0
        )

        ############################################################
        # handle errors
        ############################################################
        if self.grid_options["_errors_found"]:
            # Some information afterwards
            self.verbose_print(
                self._boxed(
                    "During the run {} failed systems were found\nwith a total probability of {:g}\nwith the following unique error codes: {} ".format(
                        self.grid_options["_failed_count"],
                        self.grid_options["_failed_prob"],
                        self.grid_options["_failed_systems_error_codes"],
                    )
                ),
                self.grid_options["verbosity"],
                0,
            )
            # Some information on where we logged the systems
            if (
                self.grid_options["log_failed_systems"]
                and self.grid_options["log_failed_systems_dir"] is not None
            ):

                self.verbose_print(
                    "The full failed arglines have been written to {self.grid_options['log_failed_systems_dir']}/process_{self.jobID()}.txt",
                    self.grid_options["verbosity"],
                    0,
                )
        else:
            self.verbose_print(
                "No failed systems were found in this run.",
                self.grid_options["verbosity"],
                0,
            )

        return True

    def _evolve_population_core(self):
        """
        Function that handles running the population using multiprocessing.

        First we set up the multiprocessing manager and the job and result queue.

        Then we spawn <self.grid_options["num_processes"]> number of process instances,
        and signal them to start.

        While the processes are waiting for their instructions, we start the queue filler,
        which goes over the grid code and puts all the tasks in a queue until its full.

        The processes take these jobs, evolve the and store results.

        When all the systems have been put in the queue we pass a STOP signal
        that will make the processes wrap up.

        We then add any previous population

        We read out the information in the result queue and store them in the grid object

        Returns True if things go well, False on error.
        """

        # Set process name
        setproctitle.setproctitle("binarycpython parent process")

        # if max_queue_size is zero, calculate automatically
        # to be double the number of processes - you don't want to
        # make the queue too large because when it's killed you
        # want to end quickly
        if self.grid_options["max_queue_size"] == 0:
            self.grid_options["max_queue_size"] = 2 * self.grid_options["num_processes"]

        ############
        # Set up the manager object and queues
        manager = multiprocessing.Manager()
        job_queue = manager.Queue(maxsize=self.grid_options["max_queue_size"])
        result_queue = manager.Queue(maxsize=self.grid_options["max_queue_size"])
        final_result_queue = manager.Queue(maxsize=self.grid_options["num_processes"])

        ############
        # data to be sent to signal handlers
        signal_data = {
            "where": "_evolve_population_core",
            "queue": job_queue,
        }

        ############
        # Create process instances to run the stars
        processes = []
        for ID in range(self.grid_options["num_processes"]):
            processes.append(
                multiprocessing.Process(
                    target=self._process_queue,
                    args=(job_queue, result_queue, final_result_queue, ID),
                )
            )

        ############
        # Activate the processes
        for p in processes:
            p.start()

        ############
        # activate signal handlers
        # * the child processes ignore these signals
        # * the parent will be in _system_queue_handler when these are caught
        signal.signal(
            signal.SIGTERM, functools.partial(self._parent_signal_handler, signal_data)
        )
        signal.signal(
            signal.SIGINT, functools.partial(self._parent_signal_handler, signal_data)
        )

        # Set up the system_queue in the parent process
        self.grid_options["_job_crashed"] = False
        self._system_queue_handler(
            job_queue,
            result_queue,
            processes,
            num_processes=self.grid_options["num_processes"],
        )

        ############
        # Handle killing of processes or join and clean up
        if self.grid_options["_job_crashed"] is True:
            # job crashed while in system_queue_filler : kill children
            # and return False
            print(
                "A child process crashed or was killed : I will not join incomplete data"
            )
            self._kill_child_processes(processes)
            return False

        else:
            # Join the processes after the queue filler has finished
            print("Do join of subprocesses ...")

            while self.grid_options["_job_crashed"] is False and processes:
                if self._all_children_running(processes) is False:
                    # job crashed: stop children and return False
                    self.grid_options["_job_crashed"] = True
                else:
                    # join first process: it should finish work soon
                    p = processes.pop(0)
                    p.join()

            if self.grid_options["_job_crashed"] is True:
                print(
                    "A child process crashed or was killed : I will not join incomplete data"
                )
                self._kill_child_processes(processes)
                return False
            else:
                print("Joined all subprocesses.")

        ############
        # Handle the results by merging all the dictionaries. How that merging happens exactly is
        # described in the merge_dicts description.
        #
        # If there is a preloaded_population, we add this first,
        # then we add the populations run just now

        # 1)
        # use preloaded population's data as a basis
        # for our combined_output_dict
        if self.preloaded_population:
            combined_output_dict = {
                "ensemble_results": keys_to_floats(
                    self.preloaded_population.grid_ensemble_results
                ),
                "results": keys_to_floats(self.preloaded_population.grid_results),
            }

            for x in self._metadata_keylist():
                try:
                    combined_output_dict[x] = self.preloaded_population.grid_options[x]
                except Exception as e:
                    print(
                        "Tried to set combined_output_dict key",
                        x,
                        "from preloaded_popuation, but this failed:",
                        e,
                    )
            print(
                "Pre-loaded data from {} stars".format(combined_output_dict["_count"])
            )

            # do not propagate _killed
            # combined_output_dict['results']['_killed'] = False
            # combined_output_dict['_killed'] = False

            self.preloaded_population = None
            gc.collect()
        else:
            # new empty combined output
            combined_output_dict = OrderedDict()
            combined_output_dict["ensemble_results"] = OrderedDict()
            combined_output_dict["results"] = OrderedDict()

        # 2)
        # combine the dicts that were output from our
        # subprocesses
        sentinel = object()
        for output_dict in iter(final_result_queue.get, sentinel):
            if output_dict:
                # don't let Xinit be added
                try:
                    del combined_output_dict["ensemble_results"]["ensemble"]["Xinit"]
                except:
                    pass

                # merge dicts
                combined_output_dict = merge_dicts(
                    combined_output_dict, keys_to_floats(output_dict)
                )
            if final_result_queue.empty():
                break

        # Extra ensemble result manipulation:
        if "ensemble_results" in combined_output_dict:
            combined_output_dict["ensemble_results"][
                "ensemble"
            ] = format_ensemble_results(
                combined_output_dict["ensemble_results"].get("ensemble", {})
            )
        gc.collect()

        # Put the values back as object properties
        self.grid_results = combined_output_dict["results"]

        #################################
        # Put Ensemble results
        self.grid_ensemble_results = combined_output_dict[
            "ensemble_results"
        ]  # Ensemble results are also passed as output from that dictionary

        # Add metadata
        self.add_ensemble_metadata(combined_output_dict)

        # if we were killed, save snapshot
        if self.grid_options["save_snapshots"] and self.grid_options["_killed"]:
            self.custom_options["save_snapshot"] = True

        # return True because all seems well
        return True

    def _evolve_system_mp(self, system_number, full_system_dict):
        """
        Function that the multiprocessing evolution method calls to evolve a system

        this function is called by _process_queue
        """

        binary_cmdline_string = self._return_argline(full_system_dict)

        persistent_data_memaddr = -1
        if self.bse_options.get("ensemble", 0) == 1:
            persistent_data_memaddr = self.persistent_data_memory_dict[self.process_ID]
            # print("thread {}: persistent_data_memaddr: ".format(self.process_ID), persistent_data_memaddr)

        # vb2 logging
        if self.grid_options["verbosity"] >= 2:
            self.vb2print(full_system_dict, binary_cmdline_string)

        # Get results binary_c
        # print("running: {}".format(binary_cmdline_string))
        out = _binary_c_bindings.run_system(
            argstring=binary_cmdline_string,
            custom_logging_func_memaddr=self.grid_options[
                "custom_logging_func_memaddr"
            ],
            store_memaddr=self.grid_options["_store_memaddr"],
            population=1,  # since this system is part of a population, we set this flag to prevent the store from being freed
            persistent_data_memaddr=persistent_data_memaddr,
        )

        # Check for errors
        _ = self._check_binary_c_error(system_number, out, full_system_dict)

        # Have some user-defined function do stuff with the data.
        if self.grid_options["parse_function"]:
            self.custom_options["parameter_dict"] = full_system_dict
            system_result = self.grid_options["parse_function"](self, out)

            return system_result

    def evolve_single(self, clean_up_custom_logging_files: bool = True) -> Any:
        """
        Function to run a single system, based on the settings in the grid_options

        The output of the run gets returned, unless a parse function is given to this function.

        Args:
            clean_up_custom_logging_files: whether the clean up all the custom_logging files.

        returns:
            either returns the raw binary_c output, or whatever the parse_function does
        """

        ######
        # Set custom logging functionality
        self._set_custom_logging()

        ######
        # Handle single system evolution

        # Check if there are actually arguments passed:
        if self.bse_options:
            # Get argument line
            argline = self._return_argline(self.bse_options)

            self.verbose_print(
                "Running {}".format(argline), self.grid_options["verbosity"], 1
            )

            # Run system
            out = _binary_c_bindings.run_system(
                argstring=argline,
                custom_logging_func_memaddr=self.grid_options[
                    "custom_logging_func_memaddr"
                ],
                store_memaddr=self.grid_options["_store_memaddr"],
                population=0,
            )

            # Clean up custom logging
            if clean_up_custom_logging_files:
                self._clean_up_custom_logging(evol_type="single")

            # Parse output and return the result
            if self.grid_options["parse_function"]:
                return self.grid_options["parse_function"](self, out)

            # Otherwise just return the raw output
            return out

        # Raise error if no evolution options are passed
        msg = "No actual evolution options passed to the evolve call. Aborting"
        raise ValueError(msg)

    ###################
    # queue and worker functions

    def _system_queue_handler(self, job_queue, result_queue, processes, num_processes):
        """
        Function that is responsible for keeping the queue filled.

        This will generate the systems until it is full, and then keeps trying to fill it.
        Will have to play with the size of this.

        This function is called as part of the parent process.
        """

        #######
        # Set up logging
        stream_logger = self._get_stream_logger()
        if self.grid_options["verbosity"] >= self._LOGGER_VERBOSITY_LEVEL:
            stream_logger.debug("setting up the system_queue_filler now")

        #######
        # Start up the generator
        generator = self._get_generator()

        #######
        # Start and handle start_at value

        # start_at can be an expression : we should eval it
        # prior to running the loop
        self.grid_options["start_at"] = eval(str(self.grid_options["start_at"]))
        if self.grid_options["start_at"] > 0:
            print("Starting at model {} ".format(self.grid_options["start_at"]))

        prev_process_check = None

        #######
        # Continuously fill the queue while we are allowed to.
        #   The loop terminates when:
        #       - the generator is exhausted
        #       - a signal to stop the queue is passed
        #       - TODO: mass threshold met when monte_carlo sampling
        #       - TODO: custom threshold (e.g. type of system)
        for system_number, system_dict in enumerate(generator):
            # on stop, quit this loop
            if self.grid_options["stop_queue"]:
                break

            ########
            # Handle start_at and modulo

            # skip systems before start_at
            elif system_number < self.grid_options["start_at"]:
                self.verbose_print(
                    "skip system {n} because < start_at = {start}".format(
                        n=system_number, start=self.grid_options["start_at"]
                    ),
                    self.grid_options["verbosity"],
                    3,
                )
                continue

            # apply modulo
            if not (
                (system_number - self.grid_options["start_at"])
                % self.grid_options["modulo"]
                == 0
            ):
                self.verbose_print(
                    "skip system {n} because modulo {mod} == {donemod}".format(
                        n=system_number,
                        mod=self.grid_options["modulo"],
                        donemod=(system_number - self.grid_options["start_at"])
                        % self.grid_options["modulo"],
                    ),
                    self.grid_options["verbosity"],
                    3,
                )

                continue

            ######
            # check children are running every 1s
            # TODO: allow frequency change?
            _now = time.time()
            if prev_process_check is None or _now - prev_process_check > 1:
                prev_process_check = _now
                if self._all_children_running(processes) is False:
                    self.grid_options["_job_crashed"] = True
                    return

            ######
            # Handle monte-carlo threshold based on evolved mass
            elif self.grid_options["evolution_type"] == "monte_carlo":
                # Check based on mass threshold
                self._monte_carlo_sampling_check_mass_threshold(system_dict)

                # Check based on custom threshold, which uses the result_queue
                # TODO: process the result_queue and pass this. How we do this (get only one, or get until the result queue is empty again)
                self._monte_carlo_sampling_check_custom_threshold(result_queue)

            ######
            # Check if evolution threshold is reached.
            #   this can be set in the _monte_carlo_sampling_check_mass_threshold function or via _monte_carlo_sampling_check_custom_threshold
            if self.grid_options["_monte_carlo_threshold_reached"]:
                self.verbose_print(
                    "Monte-Carlo threshold reached. Signaling to stop processing the queue{}",
                    self.grid_options["verbosity"],
                    2,
                )

                # Queue is done:
                self.grid_options["_queue_done"] = True

            ########
            # Put system in the job queue
            try:
                job_queue.put((system_number, system_dict), block=True)
            except Exception:
                # error on queueing : stop the queue
                self.grid_options["stop_queue"] = True

            # Print some info
            self.verbose_print(
                "Queue produced system {}".format(system_number),
                self.grid_options["verbosity"],
                3,
            )

            ########
            # Handle stopping
            if self.grid_options["_queue_done"]:
                break

        # Signal queue is done
        self.grid_options["_queue_done"] = True

        #######
        # Send closing signal to workers. When they receive this they will terminate
        if True:  # not self.grid_options['stop_queue']:
            for _ in range(num_processes):
                job_queue.put("STOP")

        if self.grid_options["verbosity"] >= self._LOGGER_VERBOSITY_LEVEL:
            stream_logger.debug("Signalling processes to stop")  # DEBUG

    def _process_queue(self, job_queue, result_queue, final_result_queue, ID):
        """
        Worker process that gets items from the job_queue and runs those systems.
        It keeps track of several things like failed systems, total time spent on systems etc.

        Input:
            job_queue: Queue object containing system dicts
            result_queue: Queue object where some results passed via the parse_function can be placed in to process in the monte-carlo sampling
            final_result_queue: Queue where the resulting analytic dictionaries will be put in
            ID: id of the worker process
        """

        ############
        # Handle signals

        # ignore SIGINT and SIGTERM : these are
        # handled by our parent process (hence in
        # _evolve_population_core)
        signal.signal(
            signal.SIGTERM,
            functools.partial(self._child_signal_handler, {"where": "_process_queue"}),
        )
        signal.signal(
            signal.SIGINT,
            functools.partial(self._child_signal_handler, {"where": "_process_queue"}),
        )

        #########
        # Start up process function and set local variations and memory

        # Set to starting up
        self.set_status("starting")

        # set start timer
        start_process_time = datetime.datetime.now()

        # set the process ID
        self.process_ID = ID

        # Set the process names
        name_proc = "binarycpython population process {}".format(ID)
        setproctitle.setproctitle(name_proc)

        # Set up local variables
        localcounter = (
            0  # global counter for the whole loop. (need to be ticked every loop)
        )
        probability_of_systems_run = (
            0  # counter for the probability of the actual systems this tread ran
        )
        number_of_systems_run = (
            0  # counter for the actual number of systems this thread ran
        )
        zero_prob_stars_skipped = 0
        total_time_calling_binary_c = 0
        total_mass_run = 0
        total_probability_weighted_mass_run = 0

        # variables for the statu bar prints
        start_grid_time = time.time()
        next_log_time = (
            self.shared_memory["prev_log_time"][0] + self.grid_options["log_dt"]
        )
        next_mem_update_time = start_grid_time + self.grid_options["log_dt"]

        # Load store memory adress: TODO: this might be prohibitive if we run with MINT
        self.grid_options["_store_memaddr"] = _binary_c_bindings.return_store_memaddr()

        # Set the ensemble memory address
        if self.bse_options.get("ensemble", 0) == 1:
            # set persistent data memory address if necessary.
            persistent_data_memaddr = (
                _binary_c_bindings.return_persistent_data_memaddr()
            )

            self.persistent_data_memory_dict = {
                self.process_ID: persistent_data_memaddr
            }

            self.verbose_print(
                "\tUsing persistent_data memaddr: {}".format(persistent_data_memaddr),
                self.grid_options["verbosity"],
                3,
            )

        #########
        # Log the starting of the process

        # Set up stream logger for the worker processes
        stream_logger = self._get_stream_logger()
        if self.grid_options["verbosity"] >= self._LOGGER_VERBOSITY_LEVEL:
            stream_logger.debug(f"Setting up processor: process-{self.process_ID}")

        self.verbose_print(
            "Process {} started at {}.\tUsing store memaddr {}".format(
                ID,
                now(),
                self.grid_options["_store_memaddr"],
            ),
            self.grid_options["verbosity"],
            3,
        )

        # Set status to running
        self.set_status("running")

        ############################################################
        # Run stellar systems in the queue
        ############################################################
        for system_number, system_dict in iter(job_queue.get, "STOP"):

            if False:
                print(
                    "Child: Job Queue system_number = {}, dict={}, n={} check {}".format(
                        system_number,
                        system_dict,
                        number_of_systems_run,
                        self.grid_options["stop_queue"],
                    )
                )
                sys.stdout.flush()

            #########
            # Create full system dict and perform check
            full_system_dict = self.bse_options.copy()
            full_system_dict.update(system_dict)

            # Check if all keys are known to binary_c.
            if number_of_systems_run == 0:
                # Check if keys match known binary_c arguments
                self._check_full_system_dict_keys(full_system_dict)

            ######################
            # Handle logging of progress

            # save the current time (used often)
            time_now = time.time()

            # update memory use stats every log_dt seconds (not every time, this is likely a bit expensive)
            if time_now > next_mem_update_time:
                m = mem_use()
                self.shared_memory["memory_use_per_thread"][ID] = m
                next_mem_update_time = time_now + self.grid_options["log_dt"]
                if m > self.shared_memory["max_memory_use_per_thread"][ID]:
                    self.shared_memory["max_memory_use_per_thread"][ID] = m

            # calculate the next logging time
            next_log_time = (
                self.shared_memory["prev_log_time"][0] + self.grid_options["log_dt"]
            )

            # Check if we need to log info again
            # TODO: Check if we can put this functionality elsewhere
            if time_now > next_log_time:
                # we have exceeded the next log time : output and update timers
                # Lock the threads. TODO: Do we need to release this?
                lock = multiprocessing.Lock()  # noqa: F841

                # Do the printing itself
                self.vb1print(ID, time_now, system_number, system_dict)

                # Set some values for next time
                next_log_time = time_now + self.grid_options["log_dt"]

                # print("PREV ",self.shared_memory["prev_log_time"])
                # print("N LOG STATS",self.shared_memory["n_saved_log_stats"].value)

                # shift the arrays
                self.shared_memory["prev_log_time"][
                    -(self.grid_options["n_logging_stats"] - 1) :
                ] = self.shared_memory["prev_log_time"][
                    : (self.grid_options["n_logging_stats"] - 1)
                ]
                self.shared_memory["prev_log_system_number"][
                    -(self.grid_options["n_logging_stats"] - 1) :
                ] = self.shared_memory["prev_log_system_number"][
                    : (self.grid_options["n_logging_stats"] - 1)
                ]

                # set the current time and system number
                self.shared_memory["prev_log_time"][0] = time_now
                self.shared_memory["prev_log_system_number"][0] = system_number

                # increase the number of stats
                self.shared_memory["n_saved_log_stats"].value = min(
                    self.shared_memory["n_saved_log_stats"].value + 1,
                    self.grid_options["n_logging_stats"],
                )

                # print("FIRST (0) ",self.shared_memory["prev_log_time"][0])
                # print("LAST (",self.shared_memory["n_saved_log_stats"].value-1,")",self.shared_memory["prev_log_time"][self.shared_memory["n_saved_log_stats"].value-1])

            ###############
            # Log current system info

            # In some cases, the whole run crashes. To be able to figure out which system
            # that was on, we log each current system to a file (each thread has one).
            # Each new system overrides the previous
            if self.grid_options["log_args"]:
                argfile = os.path.join(
                    self.grid_options["log_args_dir"],
                    "process_{}.txt".format(self.jobID()),
                )
                with self.open(
                    argfile,
                    "w",
                    encoding="utf-8",
                ) as f:
                    binary_c_cmdline_string = self._return_argline(full_system_dict)
                    f.write(binary_c_cmdline_string)
                    f.close()

            ##############
            # Running the system
            start_runtime_binary_c = time.time()

            # If we want to actually evolve the systems
            if self.grid_options["_actually_evolve_system"]:
                run_system = True

                # Check option to ignore 0 probability systems
                if not self.grid_options["run_zero_probability_system"]:
                    if full_system_dict.get("probability", 1) == 0:
                        run_system = False
                        zero_prob_stars_skipped += 1

                if run_system:
                    # Evolve the system
                    _ = self._evolve_system_mp(system_number, full_system_dict)

                    # # If we're doing monte-carlo sampling with a custom
                    # if system_result is not None:
                    #     # TODO: fix that this is only handle if user-defined function is given
                    #     # TODO: perhaps we should always put things in the system_result dict if the parse_function gives back something
                    #     # result_queue.put(
                    #     #     {
                    #     #         "system_result": system_result,
                    #     #         "system_number": system_number,
                    #     #         "full_system_dict": full_system_dict,
                    #     #     }
                    #     # )

                    #     raise NotImplementedError("Functionality not implemented")

            end_runtime_binary_c = time.time()

            # keep track of total binary_c call time
            total_time_calling_binary_c += end_runtime_binary_c - start_runtime_binary_c

            ############
            # Logging runtime

            # Debug line: logging all the lines
            if self.grid_options["log_runtime_systems"] == 1:
                with self.open(
                    os.path.join(
                        self.grid_options["tmp_dir"],
                        "runtime_systems",
                        "process_{}.txt".format(self.process_ID),
                    ),
                    "a+",
                    encoding="utf-8",
                ) as f:
                    binary_cmdline_string = self._return_argline(full_system_dict)
                    f.write(
                        "{} {} '{}'\n".format(
                            start_runtime_binary_c,
                            end_runtime_binary_c - start_runtime_binary_c,
                            binary_cmdline_string,
                        )
                    )
                    f.close()

            ####################
            # Tallying system information

            # Keep track of systems:
            probability_of_systems_run += full_system_dict.get("probability", 1)
            number_of_systems_run += 1
            localcounter += 1

            # Tally up some numbers
            total_mass_system = calculate_total_mass_system(full_system_dict)
            total_mass_run += total_mass_system
            total_probability_weighted_mass_run += (
                total_mass_system * full_system_dict.get("probability", 1)
            )

            if self.grid_options["stop_queue"]:
                print("Child: Stop queue at system {n}".format(n=number_of_systems_run))
                break

        ####################
        # Handle stopping of queue

        if self.grid_options["stop_queue"]:
            # any remaining jobs should be ignored
            try:
                while True:
                    job_queue.get_nowait()
            except queue.Empty:
                pass

        ##########################
        # Clean up and return

        # Set status to finishing
        self.set_status("finishing")
        if self.grid_options["verbosity"] >= self._LOGGER_VERBOSITY_LEVEL:
            stream_logger.debug(f"Process-{self.process_ID} is finishing.")

        # free store memory:
        _binary_c_bindings.free_store_memaddr(self.grid_options["_store_memaddr"])

        self.verbose_print(
            "process {} free memory and return ".format(ID),
            self.grid_options["verbosity"],
            1,
        )

        # Handle ensemble outut
        ensemble_json = self._process_handle_ensemble_output(ID=ID)

        # Return a set of results and errors
        output_dict = {
            "results": self.grid_results,
            "ensemble_results": ensemble_json,
            "_failed_count": self.grid_options["_failed_count"],
            "_failed_prob": self.grid_options["_failed_prob"],
            "_failed_systems_error_codes": self.grid_options[
                "_failed_systems_error_codes"
            ],
            "_errors_exceeded": self.grid_options["_errors_exceeded"],
            "_errors_found": self.grid_options["_errors_found"],
            "_probtot": probability_of_systems_run,
            "_count": number_of_systems_run,
            "_total_mass_run": total_mass_run,
            "_total_probability_weighted_mass_run": total_probability_weighted_mass_run,
            "_zero_prob_stars_skipped": zero_prob_stars_skipped,
            "_killed": self.grid_options["_killed"],
        }

        end_process_time = datetime.datetime.now()

        killed = self.was_killed()

        # thread end message
        colour = "cyan on black"
        self.verbose_print(
            self._boxed(
                "{colour}Process {ID} finished:\ngenerator started at {start}\ngenerator finished at {end}\ntotal: {timesecs}\nof which {binary_c_secs} with binary_c\nRan {nsystems} systems\nwith a total probability of {psystems:g}\n{failcolour}This thread had {nfail} failing systems{colour}\n{failcolour}with a total failed probability of {pfail}{colour}\n{zerocolour}Skipped a total of {nzero} zero-probability systems{zeroreset}\n{failednotice}".format(
                    colour=self.ANSI_colours[colour],
                    ID=ID,
                    start=start_process_time.isoformat(),
                    end=end_process_time.isoformat(),
                    timesecs=timedelta(
                        (end_process_time - start_process_time).total_seconds()
                    ),
                    binary_c_secs=timedelta(total_time_calling_binary_c),
                    nsystems=number_of_systems_run,
                    psystems=probability_of_systems_run,
                    failcolour=self.ANSI_colours["red"]
                    if self.grid_options["_failed_count"] > 0
                    else "",
                    # failreset=self.ANSI_colours[colour]
                    # if self.grid_options["_failed_count"] > 0
                    # else "",
                    nfail=self.grid_options["_failed_count"],
                    pfail=self.grid_options["_failed_prob"],
                    nzero=zero_prob_stars_skipped,
                    zerocolour=self.ANSI_colours["yellow"]
                    if zero_prob_stars_skipped > 0
                    else "",
                    zeroreset=self.ANSI_colours[colour]
                    if zero_prob_stars_skipped > 0
                    else "",
                    failednotice=">>> Process was killed <<<\n" if killed else "",
                ),
                colour=colour,
            ),
            self.grid_options["verbosity"],
            1,
        )

        # Write summary
        summary_dict = {
            "population_id": self.grid_options["_population_id"],
            "process_id": self.process_ID,
            "start_process_time": start_process_time.timestamp(),
            "end_process_time": end_process_time.timestamp(),
            "total_time_calling_binary_c": total_time_calling_binary_c,
            "number_of_systems_run": number_of_systems_run,
            "probability_of_systems_run": probability_of_systems_run,
            "failed_systems": self.grid_options["_failed_count"],
            "failed_probability": self.grid_options["_failed_prob"],
            "failed_system_error_codes": self.grid_options[
                "_failed_systems_error_codes"
            ],
            "zero_prob_stars_skipped": zero_prob_stars_skipped,
        }
        with self.open(
            os.path.join(
                self.grid_options["tmp_dir"],
                "process_summary",
                "process_{}.json".format(self.process_ID),
            ),
            "w",
            encoding="utf-8",
        ) as f:
            json.dump(summary_dict, f, indent=4, ensure_ascii=False)

        # Set status to finished
        if self.was_killed():
            self.set_status("killed")
        else:
            self.set_status("finished")

        self.verbose_print(
            "process {} queue put output_dict ".format(ID),
            self.grid_options["verbosity"],
            1,
        )

        final_result_queue.put(output_dict)

        if self.grid_options["verbosity"] >= self._LOGGER_VERBOSITY_LEVEL:
            stream_logger.debug(f"Process-{self.process_ID} is finished.")

        self.verbose_print(
            "process {} return ".format(ID),
            self.grid_options["verbosity"],
            1,
        )
        return
