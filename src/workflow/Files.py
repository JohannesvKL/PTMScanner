from pathlib import Path
import string
import random
import shutil
import streamlit as st
from typing import Union, List
from .Logger import Logger


class Files:
    def __init__(self, files: Union[List[Union[str, Path]], Path, "Files"],
                 file_type: str = None,
                 results_dir: str = None):
        if isinstance(files, Files):
            files = files.files
        if isinstance(files, Path):
            if files.is_dir():
                self.files = [str(f) for f in files.iterdir()]
            else:
                self.files = [str(files)]
        else:
            # Validate and convert each item in the files list
            self.files = [self._validate_and_convert(item) for item in files]
        if file_type is not None:
            self.set_type(file_type)
        if results_dir is not None:
            if results_dir == "auto":
                results_dir = ""
            self.set_results_dir(results_dir)

    def _validate_and_convert(self, item):
        # Convert Path objects to strings, and ensure all items are strings or lists of strings
        if isinstance(item, Path):
            return str(item)
        elif isinstance(item, list):
            return [str(file) if isinstance(file, Path) else file for file in item if isinstance(file, (str, Path))]
        elif isinstance(item, str):
            return item
        else:
            raise ValueError(
                "All items must be strings, lists of strings, or Path objects")

    def set_type(self, file_type: str) -> None:
        def change_extension(file_path, new_ext):
            return Path(file_path).with_suffix('.' + new_ext)

        for i in range(len(self.files)):
            if isinstance(self.files[i], list):  # If the item is a list
                self.files[i] = [str(change_extension(file, file_type))
                                 for file in self.files[i]]
            elif isinstance(self.files[i], str):  # If the item is a string
                self.files[i] = str(change_extension(self.files[i], file_type))

    def set_results_dir(self, subdir_name: str) -> None:
        if not subdir_name:
            subdir_name = self.create_results_sub_dir(subdir_name)
        else:
            if Path(st.session_state["workflow-dir"], "results", subdir_name).exists():
                Logger().log(
                    f"WARNING: Subdirectory already exists, will overwrite content: {subdir_name}")
            subdir_name = self.create_results_sub_dir(subdir_name)

        def change_subdir(file_path, subdir):
            return Path(subdir, Path(file_path).name)
        
        for i in range(len(self.files)):
            if isinstance(self.files[i], list):  # If the item is a list
                self.files[i] = [str(change_subdir(file, subdir_name))
                                 for file in self.files[i]]
            elif isinstance(self.files[i], str):  # If the item is a string
                self.files[i] = str(change_subdir(self.files[i], subdir_name))


    def _generate_random_code(self, length):
        # Define the characters that can be used in the code
        # Includes both letters and numbers
        characters = string.ascii_letters + string.digits

        # Generate a random code of the specified length
        random_code = ''.join(random.choice(characters) for _ in range(length))

        return random_code

    def create_results_sub_dir(self, name: str = "") -> str:
        # create a directory (e.g. for results of a TOPP tool) within the results directory
        # if name is empty string, auto generate a name
        if not name:
            name = self._generate_random_code(4)
            # make sure the subdirectory does not exist in results yet
            while Path(st.session_state["workflow-dir"], "results", name).exists():
                name = self._generate_random_code(4)
        path = Path(st.session_state["workflow-dir"], "results", name)
        shutil.rmtree(path, ignore_errors=True)
        path.mkdir()
        return str(path)

    def channel(self, input_channel: list, out_file_type: str, subdir_name: str = "") -> list:
        # modify file name to include the file type and different subdir within results directory
        # if subdir_name is empty string, auto generate a name
        if not subdir_name:
            subdir_name = self.create_results_sub_dir(subdir_name)
        else:
            if Path(st.session_state["workflow-dir"], "results", subdir_name).exists():
                Logger().log(
                    f"WARNING: Subdirectory already exists, will overwrite content: {subdir_name}")
            subdir_name = self.create_results_sub_dir(subdir_name)
        # create a list of files to return
        output_channel = []

        for entry in input_channel:
            if isinstance(entry, list):
                output_channel.append(
                    [str(Path(subdir_name, f"{Path(f).stem}.{out_file_type}")) for f in entry])
            elif isinstance(entry, str):
                output_channel.append(
                    str(Path(subdir_name, f"{Path(entry).stem}.{out_file_type}")))
            else:
                raise TypeError(f"Input type {type(entry)} not supported.")

        return output_channel

    def flatten(self):
        flattened_files = []
        for file in self.files:
            if isinstance(file, list):
                flattened_files.extend(file)
            else:
                flattened_files.append(file)
        self.files = flattened_files
        
    def combine(self):
        combined_files = [[]]
        for file in self.files:
            if isinstance(file, list):
                combined_files[0].extend(file)
            else:
                combined_files[0].append(file)
        self.files = combined_files     

    def __repr__(self):
        return self.files

    def __str__(self):
        return str(self.files)

    def __len__(self):
        return sum(1 if isinstance(file, str) else len(file) for file in self.files)
