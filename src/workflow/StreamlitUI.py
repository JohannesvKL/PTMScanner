import streamlit as st
import pyopenms as poms
from pathlib import Path
import subprocess
from .ParameterManager import ParameterManager
from .Files import Files
from typing import Any, Union, List


class StreamlitUI:
    # Methods for Streamlit UI components
    def __init__(self):
        self.ini_dir = Path(st.session_state["workflow-dir"], "ini")
        self.params = ParameterManager().load_parameters()

    def input(self,
              key: str,
              default: Any = None,
              name: str = "input widget",
              # text, textarea, number, selectbox, slider, checkbox, multiselect
              widget_type: str = "auto",
              options: Union[List[str], "Files"] = None,
              min_value: Union[int, float] = None,
              max_value: Union[int, float] = None,
              step_size: Union[int, float] = 1,
              display_file_path: bool = False
              ) -> None:
        """
        Generates a Streamlit input widget based on the specified parameters.

        :param key: Unique identifier for the widget.
        :param default: Default value of the widget.
        :param name: Display name of the widget.
        :param widget_type: Type of widget ('text', 'textarea', 'number', 'selectbox', 'multiselect', 'slider', 'checkbox' or 'auto').
        :param options: List of options for select widget.
        :param min_value: Minimum value for number or slider widget.
        :param max_value: Maximum value for number or slider widget.
        :param step_size: Step size for number or slider widget.
        :param display_file_path: Display full path or just the name of 'default' and 'option' parameters if they are passed as 'Files' object.
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
        key = f"{ParameterManager().param_prefix}{key}"

        if widget_type == 'text':
            st.text_input(name, value=value, key=key)

        elif widget_type == 'textarea':
            st.text_area(name, value=value, key=key)

        elif widget_type == 'number':
            number_type = float if isinstance(value, float) else int
            step_size = number_type(step_size)
            if min_value is not None:
                min_value = number_type(min_value)
            if max_value is not None:
                max_value = number_type(max_value)

            st.number_input(name, min_value=min_value, max_value=max_value,
                            value=value, step=step_size, format=None, key=key)

        elif widget_type == 'checkbox':
            st.checkbox(name, value=value, key=key)

        elif widget_type == 'selectbox':
            if options is not None:
                st.selectbox(name, options=options, index=options.index(
                    value) if value in options else 0, key=key)
            else:
                st.warning(
                    f"Select widget '{name}' requires options parameter")

        elif widget_type == 'multiselect':
            if options is not None:
                st.multiselect(name, options=options, default=value, key=key, format_func=format_files)
            else:
                st.warning(
                    f"Select widget '{name}' requires options parameter")

        elif widget_type == 'slider':
            if min_value is not None and max_value is not None:
                slider_type = float if isinstance(value, float) else int
                step_size = slider_type(step_size)
                if min_value is not None:
                    min_value = slider_type(min_value)
                if max_value is not None:
                    max_value = slider_type(max_value)
                st.slider(name, min_value=min_value, max_value=max_value,
                          value=value, step=step_size, key=key, format=None)
            else:
                st.warning(
                    f"Slider widget '{name}' requires min_value and max_value parameters")

        elif widget_type == 'auto':
            # Auto-determine widget type based on value
            if isinstance(value, bool):
                st.checkbox(name, value=value, key=key)
            elif isinstance(value, (int, float)):
                self.input(key, value, widget_type='number', name=name,
                           min_value=min_value, max_value=max_value, step_size=step_size)
            elif (isinstance(value, str) or value == None) and options is not None:
                self.input(
                    key, value, widget_type='selectbox', name=name, options=options)
            elif isinstance(value, list) and options is not None:
                self.input(
                    key, value, widget_type='multiselect', name=name, options=options)
            elif isinstance(value, bool):
                self.input(
                    key, value, widget_type='checkbox', name=name)
            else:
                self.input(key, value, widget_type='text', name=name)

        else:
            st.error(f"Unsupported widget type '{widget_type}'")

    def input_TOPP(self,
                   topp_tool_name: str,
                   num_cols: int = 3,
                   exclude_parameters: [str] = [],
                   exclude_input_out: bool = True) -> None:

        # write defaults ini files
        ini_file_path = Path(self.ini_dir, f"{topp_tool_name}.ini")
        if not ini_file_path.exists():
            subprocess.call([topp_tool_name, "-write_ini", str(ini_file_path)])
        # read into Param object
        param = poms.Param()
        poms.ParamXMLFile().load(str(ini_file_path), param)

        excluded_keys = ["log", "debug", "threads", "no_progress",
                         "force", "version", "test"] + exclude_parameters

        param_dicts = []
        for key in param.keys():
            # Determine if the parameter should be included based on the conditions
            if (exclude_input_out and (b"input file" in param.getTags(key) or b"output file" in param.getTags(key))) or (key.decode().split(":")[-1] in excluded_keys):
                continue
            entry = param.getEntry(key)
            param_dict = {
                "name": entry.name.decode(),
                "key": key,
                "value": entry.value,
                "valid_strings": [v.decode() for v in entry.valid_strings],
                "description": entry.description.decode(),
                "advanced": (b"advanced" in param.getTags(key))
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
                        key=key
                    )

                # string options
                elif isinstance(p["value"], str) and p["valid_strings"]:
                    cols[i].selectbox(
                        p["name"],
                        options=p["valid_strings"],
                        index=p["valid_strings"].index(p["value"]),
                        help=p["description"],
                        key=key
                    )

                # strings
                elif isinstance(p["value"], str):
                    cols[i].text_input(
                        p["name"],
                        value=p["value"],
                        help=p["description"],
                        key=key
                    )

                # ints
                elif isinstance(p["value"], int):
                    cols[i].number_input(
                        p["name"],
                        value=int(p["value"]),
                        help=p["description"],
                        key=key
                    )

                # floats
                elif isinstance(p["value"], float):
                    cols[i].number_input(
                        p["name"],
                        value=float(p["value"]),
                        step=1.0,
                        help=p["description"],
                        key=key
                    )

                # lists
                elif isinstance(p["value"], list):
                    p["value"] = [v.decode() if isinstance(v, bytes) else v for v in p["value"]]
                    cols[i].text_area(
                        p["name"],
                        value="\n".join(p["value"]),
                        help=p["description"],
                        key=key
                    )

                # increment number of columns, create new cols object if end of line is reached
                i += 1
                if i == num_cols:
                    i = 0
                    cols = st.columns(num_cols)
            except:
                cols[i].error(
                    f"Error in parameter **{p['name']}**.")
