from pathlib import Path
import string
import random
import shutil
import streamlit as st
from typing import Union, List
from .Logger import Logger


class Files:
    """
    Manages file paths for operations such as changing file extensions, organizing files
    into result directories, and handling file collections for processing tools. Designed
    to be flexible for handling both individual files and lists of files, with integration
    into a Streamlit workflow.

    Attributes:
        files (List[str]): A list of file paths, initialized from various input formats.
        
    Methods:
        collect: Collects all files in a single list (e.g. to pass to tools which can handle multiple input files at once).
    """
    def __init__(
        self,
        files: Union[List[Union[str, Path]], Path, "Files"],
        set_file_type: str = None,
        set_results_dir: str = None,
    ):
        """
        Initializes the Files object with a collection of file paths, optional file type,
        and results directory. Converts various input formats (single path, list of paths,
        Files object) into a unified list of file paths.

        Args:
            files (Union[List[Union[Union[str, Path]], Path, "Files"]): The initial collection
                of file paths or a Files object.
            set_file_type (str, optional): Set the file type/extension for the files.
            _set_dir (str, optional): Set the directory to store processed results (creates a sub-directory of workflow results directory). If set to "auto", a name will be auto-generated.
        """
        if isinstance(files, str):
            self.files = [files]
        elif isinstance(files, Files):
            self.files = files.files.copy()
        elif isinstance(files, Path):
            if files.is_dir():
                self.files = [str(f) for f in files.iterdir()]
            else:
                self.files = [str(files)]
        elif isinstance(files, list):
            self.files = [str(f) for f in files if isinstance(f, Path) or isinstance(f, str)]
        if set_file_type is not None:
            self._set_type(set_file_type)
        if set_results_dir is not None:
            if set_results_dir == "auto":
                set_results_dir = ""
            self._set_dir(set_results_dir)
        if not self.files:
            raise ValueError(f"No files found with type {set_file_type}")

    def _set_type(self, set_file_type: str) -> None:
        """
        Sets or changes the file extension for all files in the collection to the
        specified file type.

        Args:
            set_file_type (str): The file extension to set for all files.
        """
        def change_extension(file_path, new_ext):
            return Path(file_path).with_suffix("." + new_ext)

        for i in range(len(self.files)):
            if isinstance(self.files[i], list):  # If the item is a list
                self.files[i] = [
                    str(change_extension(file, set_file_type)) for file in self.files[i]
                ]
            elif isinstance(self.files[i], str):  # If the item is a string
                self.files[i] = str(change_extension(self.files[i], set_file_type))

    def _set_dir(self, subdir_name: str) -> None:
        """
        Sets the subdirectory within the results directory to store files. If the
        subdirectory name is 'auto' or empty, generates a random subdirectory name.
        Warns and overwrites if the subdirectory already exists.

        Args:
            subdir_name (str): The name of the subdirectory within the results directory.
        """
        if not subdir_name:
            subdir_name = self._create_results_sub_dir(subdir_name)
        else:
            if Path(st.session_state["workflow-dir"], "results", subdir_name).exists():
                Logger().log(
                    f"WARNING: Subdirectory already exists, will overwrite content: {subdir_name}"
                )
            subdir_name = self._create_results_sub_dir(subdir_name)

        def change_subdir(file_path, subdir):
            return Path(subdir, Path(file_path).name)

        for i in range(len(self.files)):
            if isinstance(self.files[i], list):  # If the item is a list
                self.files[i] = [
                    str(change_subdir(file, subdir_name)) for file in self.files[i]
                ]
            elif isinstance(self.files[i], str):  # If the item is a string
                self.files[i] = str(change_subdir(self.files[i], subdir_name))

    def _generate_random_code(self, length: int) -> int:
        """Generate a random code of the specified length.

        Args:
            length (int): Length of the random code.

        Returns:
            int: Random code of the specified length.
        """
        # Define the characters that can be used in the code
        # Includes both letters and numbers
        characters = string.ascii_letters + string.digits

        # Generate a random code of the specified length
        random_code = "".join(random.choice(characters) for _ in range(length))

        return random_code

    def _create_results_sub_dir(self, name: str = "") -> str:
        """
        Creates a subdirectory within the results directory for storing files. If the
        name is not specified or empty, generates a random name for the subdirectory.

        Args:
            name (str, optional): The desired name for the subdirectory.

        Returns:
            str: The path to the created subdirectory as a string.
        """
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

    def collect(self):
        """
        Combines all files in the files list into a single list (e.g. to pass to tools which can handle multiple input files at once).
        
        Does not change the file collection.
        
        Returns:
            List[List[str]]: The combined files list.
        """
        return [self.files]

    def __repr__(self):
        return self.files

    def __str__(self):
        return str(self.files)

    def __len__(self):
        return len(self.files)

    def __getitem__(self, index):
        return self.files[index]
