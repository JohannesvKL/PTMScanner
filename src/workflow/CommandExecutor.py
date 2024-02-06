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
    """
    Manages the execution of external shell commands such as OpenMS TOPP tools within a Streamlit application.

    This class provides a structured approach to executing shell commands, capturing
    their output, and handling errors. It is designed to facilitate running both single
    commands and batches of commands in parallel, leveraging Python's subprocess module
    for execution.
    """
    # Methods for running commands and logging
    def __init__(self):
        self.pid_dir = Path(st.session_state["workflow-dir"], "pids")
        self.logger = Logger()

    def run_multiple_commands(
        self, commands: list[str], write_log: bool = True
    ) -> None:
        """
        Executes multiple shell commands concurrently in separate threads.

        This method leverages threading to run each command in parallel, improving
        efficiency for batch command execution. Execution time and command results are
        logged if specified.

        Args:
            commands (list[str]): A list where each element is a list representing
                                        a command and its arguments.
            write_log (bool): If True, logs the execution details and outcomes of the commands.
        """
        # Log the start of command execution
        self.logger.log(f"Running {len(commands)} commands in parallel...")
        start_time = time.time()

        # Initialize a list to keep track of threads
        threads = []

        # Start a new thread for each command
        for cmd in commands:
            thread = threading.Thread(target=self.run_command, args=(cmd, write_log))
            thread.start()
            threads.append(thread)

        # Wait for all threads to complete
        for thread in threads:
            thread.join()

        # Calculate and log the total execution time
        end_time = time.time()
        self.logger.log(
            f"Total time to run {len(commands)} commands: {end_time - start_time:.2f} seconds"
        )

    def run_command(self, command: list[str], write_log: bool = True) -> None:
        """
        Executes a specified shell command and logs its execution details.

        Args:
            command (list[str]): The shell command to execute, provided as a list of strings.
            write_log (bool): If True, logs the command's output and errors.

        Raises:
            Exception: If the command execution results in any errors.
        """
        # Ensure all command parts are strings
        command = [str(c) for c in command]
        
        # Log the execution start
        self.logger.log(f"Running command:\n"+'\n'.join(command)+"\nWaiting for command to finish...")
        
        start_time = time.time()
        
        # Execute the command
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        child_pid = process.pid
        
        # Record the PID for potential management
        pid_file_path = self.pid_dir / str(child_pid)
        pid_file_path.touch()
        
        # Wait for command completion and capture output
        stdout, stderr = process.communicate()
        
        # Cleanup PID file
        pid_file_path.unlink()
        
        end_time = time.time()
        execution_time = end_time - start_time
        
        # Format the logging prefix
        prefix = f"Command finished:\n"+'\n'.join(command)+ "\nTotal time to run command: {execution_time:.2f} seconds\n"
        
        # Log stdout if present
        if stdout and write_log:
            self.logger.log(f"{prefix}Console log:\n\n{stdout.decode()}")
        
        # Log stderr and raise an exception if errors occurred
        if stderr or process.returncode != 0:
            error_message = stderr.decode().strip()
            self.logger.log(f"{prefix}ERRORS OCCURRED:\n{error_message}")
            raise Exception(f"Errors occurred while running command: {' '.join(command)}\n{error_message}")

    def run_topp(self, tool: str, input_output: dict, show_log: bool = True) -> None:
        """
        Constructs and executes commands for the specified tool OpenMS TOPP tool based on the given
        input and output configurations. Ensures that all input/output file lists
        are of the same length, or single strings, to maintain consistency in command
        execution. Supports executing commands either as single or multiple processes
        based on the input size.

        Args:
            tool (str): The executable name or path of the tool.
            input_output (dict): A dictionary specifying the input and output
                                 parameters and their corresponding files. The files
                                 can be specified as single paths (strings) or lists
                                 of paths for batch processing.
            show_log (bool): If True, enables logging of command execution details.
        
        Raises:
            ValueError: If the lengths of input/output file lists are inconsistent,
                        except for single string inputs.
        """
        # check input: any input lists must be same length, other items can be a single string
        # e.g. input_mzML : [list of n mzML files], output_featureXML : [list of n featureXML files], input_database : database.tsv
        io_lengths = [len(v) for v in input_output.values() if len(v) > 1]

        if len(set(io_lengths)) > 1:
            raise ValueError(f"ERROR in {tool} input/output.\nFile list lengths must be 1 and/or the same. They are {io_lengths}.")

        if len(io_lengths) == 0:  # all inputs/outputs are length == 1
            n_processes = 1
        else:
            n_processes = max(io_lengths)

        commands = []

        # Load parameters for non-defaults
        params = ParameterManager().load_parameters()
        # Construct commands for each process
        for i in range(n_processes):
            command = [tool]
            # Add input/output files
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
            # Add non-default TOPP tool parameters
            if tool in params.keys():
                for k, v in params[tool].items():
                    command += [f"-{k}", str(v)]
            commands.append(command)

        # Run command(s)
        if len(commands) == 1:
            self.run_command(commands[0], show_log)
        elif len(commands) > 1:
            self.run_multiple_commands(commands, show_log)
        else:
            raise Exception("No commands to execute.")

    def stop(self) -> None:
        """
        Terminates all processes initiated by this executor by killing them based on stored PIDs.
        """
        self.logger.log("Stopping all running processes...")
        pids = [Path(f).stem for f in self.pid_dir.iterdir()]
        
        for pid in pids:
            try:
                os.kill(int(pid), 9)
            except OSError as e:
                self.logger.log(f"Failed to kill process {pid}: {e}")
        
        shutil.rmtree(self.pid_dir, ignore_errors=True)
        self.logger.log("Workflow stopped.")
