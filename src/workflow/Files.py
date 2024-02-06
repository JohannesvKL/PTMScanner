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
        file_type (str, optional): The default file type/extension for the files.
        results_dir (str, optional): The directory to store processed results.
    """
    def __init__(
        self,
        files: Union[List[Union[str, Path]], Path, "Files"],
        file_type: str = None,
        results_dir: str = None,
    ):
        """
        Initializes the Files object with a collection of file paths, optional file type,
        and results directory. Converts various input formats (single path, list of paths,
        Files object) into a unified list of file paths.

        Args:
            files (Union[List[Union[str, Path]], Path, "Files"]): The initial collection
                of file paths or a Files object.
            file_type (str, optional): Default file type/extension to set for the files.
            results_dir (str, optional): Directory name for storing results. If 'auto',
                a directory name is automatically generated.
        """
        if isinstance(files, str):
            files = [files]
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
        """
        Validates and converts input items to a consistent format (string representation
        of paths). Handles conversion of Path objects to strings and ensures items are
        either strings or lists of strings.

        Args:
            item: The item to validate and convert.

        Returns:
            The converted item as a string or list of strings.

        Raises:
            ValueError: If the item is neither a string, a Path object, nor a list of these.
        """
        # Convert Path objects to strings, and ensure all items are strings or lists of strings
        if isinstance(item, Path):
            return str(item)
        elif isinstance(item, list):
            return [
                str(file) if isinstance(file, Path) else file
                for file in item
                if isinstance(file, (str, Path))
            ]
        elif isinstance(item, str):
            return item
        else:
            raise ValueError(
                "All items must be strings, lists of strings, or Path objects"
            )

    def set_type(self, file_type: str) -> None:
        """
        Sets or changes the file extension for all files in the collection to the
        specified file type.

        Args:
            file_type (str): The file extension to set for all files.
        """
        def change_extension(file_path, new_ext):
            return Path(file_path).with_suffix("." + new_ext)

        for i in range(len(self.files)):
            if isinstance(self.files[i], list):  # If the item is a list
                self.files[i] = [
                    str(change_extension(file, file_type)) for file in self.files[i]
                ]
            elif isinstance(self.files[i], str):  # If the item is a string
                self.files[i] = str(change_extension(self.files[i], file_type))

    def set_results_dir(self, subdir_name: str) -> None:
        """
        Sets the subdirectory within the results directory to store files. If the
        subdirectory name is 'auto' or empty, generates a random subdirectory name.
        Warns and overwrites if the subdirectory already exists.

        Args:
            subdir_name (str): The name of the subdirectory within the results directory.
        """
        if not subdir_name:
            subdir_name = self.create_results_sub_dir(subdir_name)
        else:
            if Path(st.session_state["workflow-dir"], "results", subdir_name).exists():
                Logger().log(
                    f"WARNING: Subdirectory already exists, will overwrite content: {subdir_name}"
                )
            subdir_name = self.create_results_sub_dir(subdir_name)

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

    def create_results_sub_dir(self, name: str = "") -> str:
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

    def flatten(self):
        """
        Flattens the files list, removing any nested lists.
        """
        flattened_files = []
        for file in self.files:
            if isinstance(file, list):
                flattened_files.extend(file)
            else:
                flattened_files.append(file)
        self.files = flattened_files

    def combine(self):
        """
        Combines all files in the files list into a single list.
        """
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
        return len(self.files)

    def __getitem__(self, index):
        return self.files[index]
