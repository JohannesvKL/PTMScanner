from pathlib import Path
import streamlit as st
import multiprocessing
import subprocess
import threading
import shutil
import os
import time


class WorkflowBase:

    def __init__(self, workflow_dir: str):
        # Make sure results directory exits
        self.workflow_dir = self.ensure_directory_exists(workflow_dir)
        self.log_file = Path(workflow_dir, "log.txt")
        self.pid_dir = Path(workflow_dir, "pids")

    def ensure_directory_exists(self, directory: str, reset: bool = False) -> str:
        if reset:
            shutil.rmtree(directory, ignore_errors=True)
        if not Path(directory).exists():
            Path(directory).mkdir(parents=True, exist_ok=True)
        return directory

    def log(self, message: str) -> None:
        # Write the message to the log file.
        with open(self.log_file, "a") as f:
            f.write(f"{message}\n\n")

    def run_multiple_commands(self, commands: list[list[str]], write_log: bool = True) -> None:
        self.log(f"Running {len(commands)} commands in parallel...")
        start_time = time.time()
        threads = []
        for cmd in commands:
            thread = threading.Thread(
                target=self.run_command, args=(cmd, write_log))
            thread.start()
            threads.append(thread)
        for thread in threads:
            thread.join()
        end_time = time.time()
        self.log(f"Total time to run {len(commands)} commands: {end_time - start_time} seconds")

    def run_command(self, command: list[str], write_log: bool = True) -> None:
        self.log(" ".join(command))
        start_time = time.time()
        process = subprocess.Popen(
            command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        # Get the process ID (PID) of the child process
        child_pid = process.pid
        # Write the PID to a file
        pid_file_path = Path(self.pid_dir, str(child_pid))
        pid_file_path.touch()
        # Wait for the process to finish
        stdout, stderr = process.communicate()
        # Remove pid from pid file
        pid_file_path.unlink()
        # Write the output to the log file
        if write_log:
            if stdout:
                self.log(stdout.decode())
            if stderr:
                self.log(stderr.decode())
            if process.returncode == 1:
                self.log(f"Process failed: {' '.join(command)}")
        end_time = time.time()
        self.log(f"Total time to run command: {end_time - start_time} seconds")

    def stop(self) -> None:
        self.log(f"Stopping all running processes...")
        # Read the pids
        pids = [f.stem for f in self.pid_dir.iterdir()]
        # Kill the processes
        for pid in pids:
            os.kill(int(pid), 9)
        # Delete the pid dir
        shutil.rmtree(self.pid_dir)
        self.log("Workflow stopped.")

    def run(self) -> None:
        self.log("Starting workflow...")
        #############################################
        # Add your workflow code here.
        #############################################
        self.log("COMPLETE")
        # Delete pid dir path to indicate workflow is done
        shutil.rmtree(self.pid_dir, ignore_errors=True)

    def start_workflow_process(self, form) -> None:
        form.empty()
        # Delete the log file if it already exists
        self.log_file.unlink(missing_ok=True)
        # Start workflow process
        workflow_process = multiprocessing.Process(target=self.run)
        workflow_process.start()
        # Add workflow process id to pid dir
        self.pid_dir.mkdir()
        Path(self.pid_dir, str(workflow_process.pid)).touch()

    def show_input_section(self) -> None:
        form = st.form("topp-workflow-parameters")

        ###################################
        # Add your input widgets here
        ###################################

        form.form_submit_button("Start Workflow", type="primary", use_container_width=True,
                                on_click=self.start_workflow_process, args=(form,))
