import streamlit as st
import pyopenms as poms
from pathlib import Path
import shutil
import subprocess
from .ParameterManager import ParameterManager
from .Files import Files
from typing import Any, Union, Dict, List
import json


class StreamlitUI:
    """
    Provides an interface for Streamlit applications to handle file uploads, 
    input selection, and parameter management for analysis workflows. It includes 
    methods for uploading files, selecting input files from available ones, and 
    generating various input widgets dynamically based on the specified parameters.

    The class is designed to work with pyOpenMS for mass spectrometry data analysis, 
    leveraging the ParameterManager for parameter persistence and the Files class 
    for file management.
    """
    # Methods for Streamlit UI components
    def __init__(self):
        self.ini_dir = Path(st.session_state["workflow-dir"], "ini")
        self.params = ParameterManager().load_parameters()

    def upload(
        self,
        key: str,
        file_type: str,
        name: str = "",
        fallback_files: Union[List, str] = None,
    ) -> None:
        """
        Handles file uploads through the Streamlit interface, supporting both direct
        uploads and local directory copying for specified file types. It allows for
        specifying fallback files to ensure essential files are available.

        Args:
            key (str): A unique identifier for the upload component.
            file_type (str): Expected file type for the uploaded files.
            name (str, optional): Display name for the upload component. Defaults to the key if not provided.
            fallback_files (Union[List, str], optional): Default files to use if no files are uploaded.
        """
        # streamlit uploader can't handle file types with upper and lower case letters
        files_dir = Path(st.session_state["workflow-dir"], "input-files", key)

        if not name:
            name = key.replace("-", " ")

        c1, c2 = st.columns(2)
        c1.markdown("**Upload file(s)**")
        with c1.form(f"{key}-upload", clear_on_submit=True):
            if any(c.isupper() for c in file_type) and (c.islower() for c in file_type):
                file_type_for_uploader = None
            else:
                file_type_for_uploader = [file_type]
            files = st.file_uploader(
                f"{name}",
                accept_multiple_files=(st.session_state.location == "local"),
                type=file_type_for_uploader,
                label_visibility="collapsed",
            )
            if st.form_submit_button(
                f"Add **{name}**", use_container_width=True, type="primary"
            ):
                if files:
                    files_dir.mkdir(parents=True, exist_ok=True)
                    for f in files:
                        if f.name not in [
                            f.name for f in files_dir.iterdir()
                        ] and f.name.endswith(file_type):
                            with open(Path(files_dir, f.name), "wb") as fh:
                                fh.write(f.getbuffer())
                    st.success("Successfully added uploaded files!")
                else:
                    st.error("Nothing to add, please upload file.")

        # Local file upload option: via directory path
        if st.session_state.location == "local":
            c2.markdown("**OR copy files from local folder**")
            with c2.form(f"{key}-local-file-upload"):
                local_dir = st.text_input(f"path to folder with **{name}** files")
                if st.form_submit_button(
                    f"Copy **{name}** files from local folder", use_container_width=True
                ):
                    # raw string for file paths
                    if not any(Path(local_dir).glob(f"*.{file_type}")):
                        st.warning(
                            f"No files with type **{file_type}** found in specified folder."
                        )
                    else:
                        files_dir.mkdir(parents=True, exist_ok=True)
                        # Copy all mzML files to workspace mzML directory, add to selected files
                        files = list(Path(local_dir).glob("*.mzML"))
                        my_bar = st.progress(0)
                        for i, f in enumerate(files):
                            my_bar.progress((i + 1) / len(files))
                            shutil.copy(f, Path(files_dir, f.name))
                        st.success("Successfully copied files!")

        if fallback_files:
            files_dir.mkdir(parents=True, exist_ok=True)
            if isinstance(fallback_files, str):
                fallback_files = [fallback_files]
            for f in fallback_files:
                if not Path(files_dir, f).exists():
                    shutil.copy(f, Path(files_dir, Path(f).name))
                    st.info(f"Adding default file: **{f}**")
            current_files = [
                f.name
                for f in files_dir.iterdir()
                if f.name not in [Path(f).name for f in fallback_files]
            ]
        else:
            if files_dir.exists():
                current_files = [f.name for f in files_dir.iterdir()]
            else:
                current_files = []

        if files_dir.exists() and not any(files_dir.iterdir()):
            shutil.rmtree(files_dir)

        c1, c2 = st.columns(2)
        if current_files:
            c1.info(f"Current **{name}** files:\n\n" + "\n\n".join(current_files))
            if c2.button(
                f"🗑️ Remove all files.",
                use_container_width=True,
                key=f"remove-files-{key}",
            ):
                shutil.rmtree(files_dir)
                st.rerun()
        elif not fallback_files:
            st.warning(f"No **{name}** files!")

    def select_input_file(
        self,
        key: str,
        name: str = "",
        multiple: bool = False,
        display_file_path: bool = False,
    ) -> None:
        """
        Presents a widget for selecting input files from those that have been uploaded. 
        Allows for single or multiple selections.

        Args:
            key (str): A unique identifier related to the specific input files.
            name (str, optional): The display name for the selection widget. Defaults to the key if not provided.
            multiple (bool, optional): If True, allows multiple files to be selected.
            display_file_path (bool, optional): If True, displays the full file path in the selection widget.
        """
        if not name:
            name = f"**{key}**"
        path = Path(st.session_state["workflow-dir"], "input-files", key)
        if not path.exists():
            st.warning(f"No **{name}** files!")
            return
        options = Files([f for f in path.iterdir()])
        if key in self.params.keys():
            self.params[key] = [f for f in self.params[key] if f in options]

        widget_type = "multiselect" if multiple else "selectbox"
        self.input(
            key,
            name=name,
            widget_type=widget_type,
            options=options,
            display_file_path=display_file_path,
        )

    def input(
        self,
        key: str,
        default: Any = None,
        name: str = "input widget",
        help: str = None,
        widget_type: str = "auto", # text, textarea, number, selectbox, slider, checkbox, multiselect
        options: Union[List[str], "Files"] = None,
        min_value: Union[int, float] = None,
        max_value: Union[int, float] = None,
        step_size: Union[int, float] = 1,
        display_file_path: bool = False,
    ) -> None:
        """
        Creates and displays a Streamlit widget for user input based on specified 
        parameters. Supports a variety of widget types including text input, number 
        input, select boxes, and more. Default values will be read in from parameters
        if they exist. The key is modified to be recognized by the ParameterManager class
        as a custom parameter (distinct from TOPP tool parameters).

        Args:
            key (str): Unique identifier for the widget.
            default (Any, optional): Default value for the widget.
            name (str, optional): Display name of the widget.
            help (str, optional): Help text to display alongside the widget.
            widget_type (str, optional): Type of widget to create ('text', 'textarea', 
                                         'number', 'selectbox', 'slider', 'checkbox', 
                                         'multiselect', 'password', or 'auto').
            options (Union[List[str], "Files"], optional): Options for select/multiselect widgets.
            min_value (Union[int, float], optional): Minimum value for number/slider widgets.
            max_value (Union[int, float], optional): Maximum value for number/slider widgets.
            step_size (Union[int, float], optional): Step size for number/slider widgets.
            display_file_path (bool, optional): Whether to display the full file path for file options.
        """
        def convert_files_to_str(input: Any) -> List[str]:
            if isinstance(input, Files):
                return input.files
            else:
                return input

        def format_files(input: Any) -> List[str]:
            if not display_file_path and Path(input).exists():
                return Path(input).name
            else:
                return input

        default = convert_files_to_str(default)
        options = convert_files_to_str(options)

        if key in self.params.keys():
            value = self.params[key]
        else:
            value = default
            # catch case where options are given but default is None
            if options is not None and value is None:
                if widget_type == "multiselect":
                    value = []
                elif widget_type == "selectbox":
                    value = options[0]

        if key not in self.params.keys():
            self.params[key] = value
            with open(ParameterManager().params_file, "w", encoding="utf-8") as f:
                json.dump(self.params, f, indent=4)

        key = f"{ParameterManager().param_prefix}{key}"

        if widget_type == "text":
            st.text_input(name, value=value, key=key, help=help)

        elif widget_type == "textarea":
            st.text_area(name, value=value, key=key, help=help)

        elif widget_type == "number":
            number_type = float if isinstance(value, float) else int
            step_size = number_type(step_size)
            if min_value is not None:
                min_value = number_type(min_value)
            if max_value is not None:
                max_value = number_type(max_value)
            help = str(help)
            st.number_input(
                name,
                min_value=min_value,
                max_value=max_value,
                value=value,
                step=step_size,
                format=None,
                key=key,
                help=help,
            )

        elif widget_type == "checkbox":
            st.checkbox(name, value=value, key=key, help=help)

        elif widget_type == "selectbox":
            if options is not None:
                st.selectbox(
                    name,
                    options=options,
                    index=options.index(value) if value in options else 0,
                    key=key,
                    format_func=format_files,
                    help=help,
                )
            else:
                st.warning(f"Select widget '{name}' requires options parameter")

        elif widget_type == "multiselect":
            if options is not None:
                st.multiselect(
                    name,
                    options=options,
                    default=value,
                    key=key,
                    format_func=format_files,
                    help=help,
                )
            else:
                st.warning(f"Select widget '{name}' requires options parameter")

        elif widget_type == "slider":
            if min_value is not None and max_value is not None:
                slider_type = float if isinstance(value, float) else int
                step_size = slider_type(step_size)
                if min_value is not None:
                    min_value = slider_type(min_value)
                if max_value is not None:
                    max_value = slider_type(max_value)
                st.slider(
                    name,
                    min_value=min_value,
                    max_value=max_value,
                    value=value,
                    step=step_size,
                    key=key,
                    format=None,
                    help=help,
                )
            else:
                st.warning(
                    f"Slider widget '{name}' requires min_value and max_value parameters"
                )

        elif widget_type == "password":
            st.text_input(name, value=value, type="password", key=key, help=help)

        elif widget_type == "auto":
            # Auto-determine widget type based on value
            if isinstance(value, bool):
                st.checkbox(name, value=value, key=key, help=help)
            elif isinstance(value, (int, float)):
                self.input(
                    key,
                    value,
                    widget_type="number",
                    name=name,
                    min_value=min_value,
                    max_value=max_value,
                    step_size=step_size,
                    help=help,
                )
            elif (isinstance(value, str) or value == None) and options is not None:
                self.input(
                    key,
                    value,
                    widget_type="selectbox",
                    name=name,
                    options=options,
                    help=help,
                )
            elif isinstance(value, list) and options is not None:
                self.input(
                    key,
                    value,
                    widget_type="multiselect",
                    name=name,
                    options=options,
                    help=help,
                )
            elif isinstance(value, bool):
                self.input(key, value, widget_type="checkbox", name=name, help=help)
            else:
                self.input(key, value, widget_type="text", name=name, help=help)

        else:
            st.error(f"Unsupported widget type '{widget_type}'")

    def input_TOPP(
        self,
        topp_tool_name: str,
        num_cols: int = 3,
        exclude_parameters: [str] = [],
        exclude_input_out: bool = True
    ) -> None:
        """
        Generates input widgets for TOPP tool parameters dynamically based on the tool's
        .ini file. Supports excluding specific parameters and adjusting the layout.

        Args:
            topp_tool_name (str): The name of the TOPP tool for which to generate inputs.
            num_cols (int, optional): Number of columns to use for the layout. Defaults to 3.
            exclude_parameters (List[str], optional): List of parameter names to exclude from the widget.
            exclude_input_out (bool, optional): If True, excludes input and output file parameters.
        """
        # write defaults ini files
        ini_file_path = Path(self.ini_dir, f"{topp_tool_name}.ini")
        if not ini_file_path.exists():
            subprocess.call([topp_tool_name, "-write_ini", str(ini_file_path)])
        # read into Param object
        param = poms.Param()
        poms.ParamXMLFile().load(str(ini_file_path), param)

        excluded_keys = [
            "log",
            "debug",
            "threads",
            "no_progress",
            "force",
            "version",
            "test",
        ] + exclude_parameters

        param_dicts = []
        for key in param.keys():
            # Determine if the parameter should be included based on the conditions
            if (
                exclude_input_out
                and (
                    b"input file" in param.getTags(key)
                    or b"output file" in param.getTags(key)
                )
            ) or (key.decode().split(":")[-1] in excluded_keys):
                continue
            entry = param.getEntry(key)
            param_dict = {
                "name": entry.name.decode(),
                "key": key,
                "value": entry.value,
                "valid_strings": [v.decode() for v in entry.valid_strings],
                "description": entry.description.decode(),
                "advanced": (b"advanced" in param.getTags(key)),
            }
            param_dicts.append(param_dict)

        # Update parameter values from the JSON parameters file
        json_params = self.params
        if topp_tool_name in json_params:
            for p in param_dicts:
                name = p["key"].decode().split(":1:")[1]
                if name in json_params[topp_tool_name]:
                    p["value"] = json_params[topp_tool_name][name]

        # input widgets in n number of columns
        cols = st.columns(num_cols)
        i = 0

        # show input widgets
        for p in param_dicts:

            # skip avdanced parameters if not selected
            if not st.session_state["advanced"] and p["advanced"]:
                continue

            key = f"{ParameterManager().topp_param_prefix}{p['key'].decode()}"

            try:
                # bools
                if p["value"] == "true" or p["value"] == "false":
                    cols[i].markdown("##")
                    cols[i].checkbox(
                        p["name"],
                        value=(p["value"] == "true"),
                        help=p["description"],
                        key=key,
                    )

                # string options
                elif isinstance(p["value"], str) and p["valid_strings"]:
                    cols[i].selectbox(
                        p["name"],
                        options=p["valid_strings"],
                        index=p["valid_strings"].index(p["value"]),
                        help=p["description"],
                        key=key,
                    )

                # strings
                elif isinstance(p["value"], str):
                    cols[i].text_input(
                        p["name"], value=p["value"], help=p["description"], key=key
                    )

                # ints
                elif isinstance(p["value"], int):
                    cols[i].number_input(
                        p["name"], value=int(p["value"]), help=p["description"], key=key
                    )

                # floats
                elif isinstance(p["value"], float):
                    cols[i].number_input(
                        p["name"],
                        value=float(p["value"]),
                        step=1.0,
                        help=p["description"],
                        key=key,
                    )

                # lists
                elif isinstance(p["value"], list):
                    p["value"] = [
                        v.decode() if isinstance(v, bytes) else v for v in p["value"]
                    ]
                    cols[i].text_area(
                        p["name"],
                        value="\n".join(p["value"]),
                        help=p["description"],
                        key=key,
                    )

                # increment number of columns, create new cols object if end of line is reached
                i += 1
                if i == num_cols:
                    i = 0
                    cols = st.columns(num_cols)
            except:
                cols[i].error(f"Error in parameter **{p['name']}**.")
