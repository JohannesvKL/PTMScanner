import time
import os
import shutil
import subprocess
import threading
from pathlib import Path
import streamlit as st
from .Logger import Logger
from .Files import Files
from .ParameterManager import ParameterManager


class CommandExecutor:
    # Methods for running commands and logging
    def __init__(self):
        self.pid_dir = Path(st.session_state["workflow-dir"], "pids")
        self.logger = Logger()

    def run_multiple_commands(
        self, commands: list[list[str]], write_log: bool = True
    ) -> None:
        self.logger.log(f"Running {len(commands)} commands in parallel...")
        start_time = time.time()
        threads = []
        for cmd in commands:
            thread = threading.Thread(target=self.run_command, args=(cmd, write_log))
            thread.start()
            threads.append(thread)
        for thread in threads:
            thread.join()
        end_time = time.time()
        self.logger.log(
            f"Total time to run {len(commands)} commands: {end_time - start_time} seconds"
        )

    def run_command(self, command: list[str], write_log: bool = True) -> None:
        # make sure all entries in command are str
        command = [str(c) for c in command]
        self.logger.log(
            "Running command:\n"
            + " ".join(command)
            + "\nWaiting for command to finish..."
        )
        start_time = time.time()
        process = subprocess.Popen(
            command, stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
        # Get the process ID (PID) of the child process
        child_pid = process.pid
        # # Write the PID to a file
        pid_file_path = Path(self.pid_dir, str(child_pid))
        pid_file_path.touch()
        # Wait for the process to finish
        stdout, stderr = process.communicate()
        # Remove pid from pid file
        pid_file_path.unlink()
        end_time = time.time()
        prefix = (
            "Command finished:\n"
            + " ".join(command)
            + f"\nTotal time to run command: {end_time - start_time} seconds\n"
        )
        # Write the output to the log file
        if stdout:
            if write_log:
                self.logger.log(f"{prefix}Console log:\n\n{stdout.decode()}")
        # Always log and raise error to interrupt workflow
        if stderr or process.returncode == 1:
            self.logger.log(f"{prefix}ERRORS OCCURED: {' '.join(command)}")
            self.logger.log(stderr.decode())
            raise Exception(f"Errors occurred while running command: {command}")

    def run_topp(self, tool: str, input_output: dict, show_log: bool = True) -> None:
        # check input: any input lists must be same length, other items can be a single string
        # e.g. input_mzML : [list of n mzML files], output_featureXML : [list of n featureXML files], input_database : database.tsv

        io_lengths = [len(v) for v in input_output.values()]

        while 1 in io_lengths:
            io_lengths.remove(1)
        if len(set(io_lengths)) > 1:
            self.logger.log("ERROR IN IOLENGTH")
            raise ValueError(f"ERROR in {tool} input/output.\nFile list lengths must be 1 and/or the same. They are {io_lengths}.")

        if len(io_lengths) == 0:  # all one i/o length
            n_processes = 1
        else:
            n_processes = max(io_lengths)

        commands = []

        params = ParameterManager().load_parameters()
        for i in range(n_processes):
            command = [tool]
            for k in input_output.keys():
                command += [f"-{k}"]
                value = input_output[k]
                if isinstance(value, Files):
                    value = value.files
                if len(value) == 1:
                    i = 0
                if isinstance(value[i], list):
                    command += value[i]
                else:
                    command += [value[i]]

            if tool in params.keys():
                for k, v in params[tool].items():
                    command += [f"-{k}", str(v)]

            commands.append(command)

        if len(commands) == 1:
            self.run_command(commands[0], show_log)
        elif len(commands) > 1:
            self.run_multiple_commands(commands, show_log)
        else:
            self.logger.log(f"No commands to run for {tool}.")

    def stop(self) -> None:
        self.logger.log(f"Stopping all running processes...")
        # Read the pids
        pids = [f.stem for f in self.pid_dir.iterdir()]
        print(pids)
        # Kill the processes
        for pid in pids:
            os.kill(int(pid), 9)
        # Delete the pid dir
        shutil.rmtree(self.pid_dir, ignore_errors=True)
        self.logger.log("Workflow stopped.")
