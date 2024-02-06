import pyopenms as poms
import json
import shutil
import streamlit as st
from pathlib import Path
from .DirectoryManager import DirectoryManager


class ParameterManager:
    # Methods related to parameter handling
    def __init__(self):
        self.ini_dir = DirectoryManager().ensure_directory_exists(
            Path(st.session_state["workflow-dir"], "ini")
        )
        self.params_file = Path(st.session_state["workflow-dir"], "params.json")
        self.param_prefix = f"{Path(st.session_state['workflow-dir']).stem}-param-"
        self.topp_param_prefix = f"{Path(st.session_state['workflow-dir']).stem}-TOPP-"

    def save_parameters(self, to_default: bool = False) -> None:
        # Everything in session state which begins with self.param_prefix is saved to a json file
        json_params = {
            k.replace(self.param_prefix, ""): v
            for k, v in st.session_state.items()
            if k.startswith(self.param_prefix)
        }
        # get a list of TOPP tools which are in session state
        current_topp_tools = list(
            set(
                [
                    k.replace(self.topp_param_prefix, "").split(":1:")[0]
                    for k in st.session_state.keys()
                    if k.startswith(f"{self.topp_param_prefix}")
                ]
            )
        )
        # for each TOPP tool, open the ini file
        for tool in current_topp_tools:
            json_params[tool] = {}
            # load the param object
            param = poms.Param()
            poms.ParamXMLFile().load(str(Path(self.ini_dir, f"{tool}.ini")), param)
            # get all session state param keys and values for this tool
            for key, value in st.session_state.items():
                if key.startswith(f"{self.topp_param_prefix}{tool}:1:"):
                    # get ini_key
                    ini_key = key.replace(self.topp_param_prefix, "").encode()
                    # get ini (default) value by ini_key
                    ini_value = param.getValue(ini_key)
                    # need to convert bool values to string values
                    if isinstance(value, bool):
                        if value == True:
                            value = "true"
                        elif value == False:
                            value = "false"
                    # convert strings with newlines to list
                    if isinstance(value, str):
                        if "\n" in value:
                            value = [v.encode() for v in value.split("\n")]
                    # check if value is different from default
                    if ini_value != value:
                        # store non-default value
                        json_params[tool][key.split(":1:")[1]] = value
        # Save to json file
        with open(self.params_file, "w", encoding="utf-8") as f:
            json.dump(json_params, f, indent=4)

    def load_parameters(self) -> None:
        # Check if parameter file exists
        if not Path(self.params_file).exists():
            return {}
        else:
            # Load parameters from json file
            with open(self.params_file, "r", encoding="utf-8") as f:
                return json.load(f)

    def reset_to_default_parameters(self) -> None:
        # Delete custom params json file
        self.params_file.unlink(missing_ok=True)
        shutil.rmtree(self.ini_dir)
        st.rerun()
