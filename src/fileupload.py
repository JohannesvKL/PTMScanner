import streamlit as st
from src.common import *
from pathlib import Path
import shutil


mzML_dir = Path(st.session_state["workspace"], "mzML-files")


@st.cache_data
def save_uploaded_mzML(uploaded_files, params):
    # Need to have a list of uploaded files to copy to the mzML dir,
    # in case of online only a single item is return, so we put it in the list
    if st.session_state.location == "online":
        uploaded_files = [uploaded_files]

    # If no files are uploaded, exit early
    if not uploaded_files:
        st.warning("Upload some files first.")
        return params

    for f in uploaded_files:
        if f.name not in [f.name for f in mzML_dir.iterdir()] and f.name.endswith("mzML"):
            with open(Path(mzML_dir, f.name), "wb") as fh:
                fh.write(f.getbuffer())
        if Path(f.name).stem not in params["selected-mzML-files"]:
            params["selected-mzML-files"].append(
                Path(f.name).stem)
    st.success("Successfully added uploaded files!")

    save_params(params, check_session_state=False)
    return params


@st.cache_data
def copy_local_mzML_files_from_directory(mzML_directory, params):
    if not any(Path(mzML_directory).glob("*.mzML")):
        st.warning("No mzML files found in specified folder.")
        return params
    files = Path(mzML_directory).glob("*.mzML")
    for f in files:
        if f.name not in mzML_dir.iterdir():
            shutil.copy(f, mzML_dir)
            if f.stem not in params["selected-mzML-files"]:
                params["selected-mzML-files"].append(
                    f.stem)
    st.success("Successfully added local files!")
    save_params(params, check_session_state=False)
    return params


def load_example_mzML_files(params):
    for f in Path("example-data", "mzML").glob("*.mzML"):
        shutil.copy(f, mzML_dir)
        if f.stem not in params["selected-mzML-files"]:
            params["selected-mzML-files"].append(f.stem)
    st.success("Example mzML files loaded!")
    save_params(params, check_session_state=False)
    return params


def remove_selected_mzML_files(to_remove, params):
    for f in to_remove:
        Path(mzML_dir, f+".mzML").unlink()
        params["selected-mzML-files"].remove(f)
    st.success("Selected mzML files removed!")
    save_params(params, check_session_state=False)
    return params


def remove_all_mzML_files(params):
    reset_directory(mzML_dir)
    params["selected-mzML-files"] = []
    st.success("All mzML files removed!")
    save_params(params, check_session_state=False)
    return params
