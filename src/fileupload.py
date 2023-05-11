import shutil
from pathlib import Path

import streamlit as st

from src.common import reset_directory


# Specify mzML file location in workspace
mzML_dir: Path = Path(st.session_state.workspace, "mzML-files")


def add_to_selected_mzML(filename: str):
    """
    Add the given filename to the list of selected mzML files.

    Args:
        filename (str): The filename to be added to the list of selected mzML files.

    Returns:
        None
    """
    # Check if file in params selected mzML files, if not add it
    if filename not in st.session_state["selected-mzML-files"]:
        st.session_state["selected-mzML-files"].append(filename)


@st.cache_data
def save_uploaded_mzML(uploaded_files: list[bytes]) -> None:
    """
    Saves uploaded mzML files to the mzML directory.

    Args:
        uploaded_files (List[bytes]): List of uploaded mzML files.

    Returns:
        None
    """
    # A list of files is required, since online allows only single upload, create a list
    if st.session_state.location == "online":
        uploaded_files = [uploaded_files]
    # If no files are uploaded, exit early
    if not uploaded_files:
        st.warning("Upload some files first.")
        return
    # Write files from buffer to workspace mzML directory, add to selected files
    for f in uploaded_files:
        if f.name not in [f.name for f in mzML_dir.iterdir()] and f.name.endswith("mzML"):
            with open(Path(mzML_dir, f.name), "wb") as fh:
                fh.write(f.getbuffer())
        add_to_selected_mzML(Path(f.name).stem)
    st.success("Successfully added uploaded files!")


@st.cache_data
def copy_local_mzML_files_from_directory(local_mzML_directory: str) -> None:
    """
    Copies local mzML files from a specified directory to the mzML directory.

    Args:
        local_mzML_directory (str): Path to the directory containing the mzML files.

    Returns:
        None
    """
    # Check if local directory contains mzML files, if not exit early
    if not any(Path(local_mzML_directory).glob("*.mzML")):
        st.warning("No mzML files found in specified folder.")
        return
    # Copy all mzML files to workspace mzML directory, add to selected files
    files = Path(local_mzML_directory).glob("*.mzML")
    for f in files:
        if f.name not in mzML_dir.iterdir():
            shutil.copy(f, mzML_dir)
        add_to_selected_mzML(f.stem)
    st.success("Successfully added local files!")


def load_example_mzML_files() -> None:
    """
    Copies example mzML files to the mzML directory.

    Args:
        None

    Returns:
        None
    """
    # Copy files from example-data/mzML to workspace mzML directory, add to selected files
    for f in Path("example-data", "mzML").glob("*.mzML"):
        shutil.copy(f, mzML_dir)
        add_to_selected_mzML(f.stem)
    st.success("Example mzML files loaded!")


def remove_selected_mzML_files(to_remove: list[str]) -> None:
    """
    Removes selected mzML files from the mzML directory.

    Args:
        to_remove (List[str]): List of mzML files to remove.

    Returns:
        None
    """
    # remove all given files from mzML workspace directory and selected files
    for f in to_remove:
        Path(mzML_dir, f+".mzML").unlink()
        st.session_state.params["selected-mzML-files"].remove(f)
    st.success("Selected mzML files removed!")


def remove_all_mzML_files() -> None:
    """
    Removes all mzML files from the mzML directory.

    Args:
        None

    Returns:
        None
    """
    # reset (delete and re-create) mzML directory in workspace
    reset_directory(mzML_dir)
    # reset selected mzML list
    st.session_state.params["selected-mzML-files"] = []
    st.success("All mzML files removed!")
