from pathlib import Path
import streamlit as st
import pyopenms as poms
import multiprocessing
import subprocess
import threading
import shutil
import os
import time
import json


class WorkflowBase:

    def __init__(self, name: str):
        # Make sure results directory exits
        self.name = name
        self.workflow_dir = self.ensure_directory_exists(
            Path(st.session_state.workspace, self.name.replace(" ", "-").lower()))
        self.log_file = Path(self.workflow_dir, "log.txt")
        self.pid_dir = Path(self.workflow_dir, "pids")
        self.ini_dir = self.ensure_directory_exists(
            Path(self.workflow_dir, "ini"))
        self.params_file = Path(self.workflow_dir, "params.json")
        self.default_params_file = Path(
            "assets", f"{self.name.replace(' ', '-').lower()}-default-params.json")

    def ensure_directory_exists(self, directory: str, reset: bool = False) -> str:
        if reset:
            shutil.rmtree(directory, ignore_errors=True)
        if not Path(directory).exists():
            Path(directory).mkdir(parents=True, exist_ok=True)
        return directory

    def save_parameters(self) -> None:
        # Everything in session state which begins with f"{self.name}-param-" is saved to a json file
        json_params = {k.replace(f"{self.name}-param-", ""): v for k,
                  v in st.session_state.items() if k.startswith(f"{self.name}-param-")}
        # get a list of TOPP tools which are in session state
        current_topp_tools = list(set([k.split("##")[1].split(":1:")[0] for k in st.session_state.keys() if k.startswith(f"{self.name}##")]))
        # for each TOPP tool, open the ini file
        for tool in current_topp_tools:
            json_params[tool] = {}
            # load the param object
            param = poms.Param()
            poms.ParamXMLFile().load(
                str(Path(self.ini_dir, f"{tool}.ini")), param)
            # get all session state param keys and values for this tool
            for key, value in st.session_state.items():
                if key.startswith(f"{self.name}##{tool}:1:"):
                    # get ini_key
                    ini_key = key.split("##")[1].encode()
                    # get ini (default) value by ini_key
                    ini_value = param.getValue(ini_key)
                    # need to convert bool values to string values
                    if isinstance(value, bool):
                        if value == True:
                            value = "true"
                        elif value == False:
                            value = "false"
                    # check if value is different from default
                    if ini_value!= value:
                        # store non-default value
                        json_params[tool][key.split(":1:")[1]] = value
        # Save to json file
        with open(self.params_file, "w", encoding="utf-8") as f:
            json.dump(json_params, f, indent=4)

    def load_parameters(self) -> None:
        # Check if parameter file exists
        if not Path(self.params_file).exists():
            # Load defautls from f"assets/{self.workflow_dir}-default-params.json"
            with open(self.default_params_file, "r", encoding="utf-8") as f:
                params = json.load(f)
        else:
            # Load parameters from json file
            with open(self.params_file, "r", encoding="utf-8") as f:
                params = json.load(f)
        return params

    def reset_to_default_parameters(self) -> None:
        # Delete custom params json file
        self.params_file.unlink(missing_ok=True)
        shutil.rmtree(self.ini_dir)
        st.rerun()

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
        self.log(
            f"Total time to run {len(commands)} commands: {end_time - start_time} seconds")

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

    def start_workflow_process(self) -> None:
        # Delete the log file if it already exists
        self.log_file.unlink(missing_ok=True)
        # Start workflow process
        workflow_process = multiprocessing.Process(target=self.run)
        workflow_process.start()
        # Add workflow process id to pid dir
        self.pid_dir.mkdir()
        Path(self.pid_dir, str(workflow_process.pid)).touch()

    def show_input_TOPP(self, topp_tool_name: str, num_cols: int = 2, exclude_parameters: [str] = []) -> None:

        # write defaults ini files
        ini_file_path = Path(self.ini_dir, f"{topp_tool_name}.ini")
        if not ini_file_path.exists():
            subprocess.call([topp_tool_name, "-write_ini", str(ini_file_path)])
        # read into Param object
        param = poms.Param()
        poms.ParamXMLFile().load(str(ini_file_path), param)

        # parse into dict
        param_dicts = [{
            "name": param.getEntry(key).name.decode(),
            "key": key,
            "value": param.getEntry(key).value,
            "valid_strings": [v.decode() for v in param.getEntry(key).valid_strings],
            "description": param.getEntry(key).description.decode(),
            "advanced": (b"advanced" in param.getTags(key)),
        } for key in param.keys()]

        # exclude some parameters such as input/output and general
        excluded_keys = ["out", "in", "log", "debug", "threads", "no_progress", "force", "version",
                         "test"] + [p["name"] for p in param_dicts if p["name"].startswith("in_") or p["name"].startswith("out_")] + exclude_parameters
        param_dicts = [
            p for p in param_dicts if p["name"] not in excluded_keys]
        
        # if a parameter is already saved as non-default in json parameter file, update value
        json_params = self.load_parameters()
        if topp_tool_name in json_params.keys():
            for p in param_dicts:
                name = p["key"].decode().split(":1:")[1]
                if name in json_params[topp_tool_name].keys():
                    p["value"] = json_params[topp_tool_name][name]

        # input widgets in n number of columns
        cols = st.columns(num_cols)
        i = 0

        # show input widgets
        for p in param_dicts:
        
            # skip avdanced parameters if not selected
            if not st.session_state["advanced"] and p["advanced"]:
                continue

            # bools
            if p["value"] == "true" or p["value"] == "false":
                cols[i].markdown("##")
                cols[i].checkbox(
                    p["name"],
                    value=(p["value"] == "true"),
                    help=p["description"],
                    key=f"{self.name}##{p['key'].decode()}"
                )

            # string options
            elif isinstance(p["value"], str) and p["valid_strings"]:
                cols[i].selectbox(
                    p["name"],
                    options=p["valid_strings"],
                    index=p["valid_strings"].index(p["value"]),
                    help=p["description"],
                    key=f"{self.name}##{p['key'].decode()}"
                )

            # strings
            elif isinstance(p["value"], str):
                cols[i].text_input(
                    p["name"],
                    value=p["value"],
                    help=p["description"],
                    key=f"{self.name}##{p['key'].decode()}"
                )

            # ints
            elif isinstance(p["value"], int):
                cols[i].number_input(
                    p["name"],
                    value=int(p["value"]),
                    help=p["description"],
                    key=f"{self.name}##{p['key'].decode()}"
                )

            # floats
            elif isinstance(p["value"], float):
                cols[i].number_input(
                    p["name"],
                    value=float(p["value"]),
                    step=1.0,
                    help=p["description"],
                    key=f"{self.name}##{p['key'].decode()}"
                )

            # lists
            elif isinstance(p["value"], list):
                cols[i].text_area(
                    p["name"],
                    value="\n".join([e.decode() for e in p["value"]]),
                    help=p["description"],
                    key=f"{self.name}##{p['key'].decode()}"
                ).split("\n")

            # increment number of columns, create new cols object if end of line is reached
            i += 1
            if i == num_cols:
                i = 0
                cols = st.columns(num_cols)

    def run(self) -> None:
        self.log("Starting workflow...")
        results_dir = self.ensure_directory_exists(
            Path(self.workflow_dir, "results"), reset=True)
        params = self.load_parameters()
        self.define_workflow_steps(results_dir, params)
        self.log("COMPLETE")
        # Delete pid dir path to indicate workflow is done
        shutil.rmtree(self.pid_dir, ignore_errors=True)

    def show_input_section(self) -> None:
        cols = st.columns(3)
        cols[0].toggle("Show advanced parameters", value=False, key="advanced")

        form = st.form(key=f"{self.name}-input-form", clear_on_submit=True)

        with form:
            cols = st.columns(3)

            cols[1].form_submit_button(label="Save parameters",
                                       on_click=self.save_parameters,
                                       type="primary",
                                       use_container_width=True)

            if cols[2].form_submit_button(label="Load default parameters",
                                        use_container_width=True):
                self.reset_to_default_parameters()

            # Load parameters
            params = self.load_parameters()
            self.define_input_section(params)

    def define_input_section(self, params: dict) -> None:
        ###################################
        # Add your input widgets here
        ###################################
        pass

    def define_workflow_steps(self, results_dir: str, params: dict) -> None:
        ###################################
        # Add your workflow steps here
        ###################################
        pass
