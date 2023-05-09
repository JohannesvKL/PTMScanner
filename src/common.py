import streamlit as st
import pandas as pd
import io
from pathlib import Path
import shutil
import sys
import os
import uuid
import json

# things to do depending on the repository:
# set the repository name in case of running with docker
# set the name for the workspaces directory


def page_setup():
    # Streamlit configs
    st.set_page_config(
        page_title="OpenMS App Template",
        page_icon="assets/OpenMS.png",
        # layout="wide",
        initial_sidebar_state="auto",
        menu_items=None,
    )

    # Should run once at app start-up
    if "workspace" not in st.session_state:
        # in docker need to set working directory to repository directory
        if "docker" in sys.argv:
            os.chdir("streamlit-template")
        # define directory where all workspaces will be stored
        st.session_state["workspaces-dir"] = Path("..", "workspaces-template")
        # Local: workspace name at startup: default-workspace
        if "local" in sys.argv:
            st.session_state.location = "local"
            st.session_state["workspace"] = Path(
                st.session_state["workspaces-dir"], "default"
            )
        # Online: create a random key as workspace name
        else:
            st.session_state.location = "online"
            st.session_state["workspace"] = Path(
                st.session_state["workspaces-dir"], str(uuid.uuid1())
            )

    # Make sure important directories exist
    st.session_state["workspace"].mkdir(parents=True, exist_ok=True)
    st.session_state["mzML-files"] = Path(
        st.session_state["workspace"], "mzML-files")
    st.session_state["mzML-files"].mkdir(parents=True, exist_ok=True)

    # Keep track of selected mzML files across all pages
    path = Path(st.session_state["workspace"], "selected-mzML.txt")
    path.touch(exist_ok=True)

    # Global variables
    if "image-format" not in st.session_state:
        st.session_state["image-format"] = "svg"


def load_params():
    # path = Path(st.session_state["workspace"], "params.json")
    # if path.exists():
    #     # Opening JSON file
    #     with open(path, "r") as f:
    #         return json.load(f)
    # else:
    #     return {}
    path = Path(st.session_state["workspace"], "params.json")
    if path.exists():
        # Opening JSON file
        with open(path, "r") as f:
            st.session_state["p"] = json.load(f)
    else:
        st.session_state["p"] = {}


def save_params(params):
    for key, value in st.session_state["p"].items():
        if isinstance(value, (str, int, float, dict, list)) and key != "p":
            st.session_state["p"][key] = value
    with open(Path(st.session_state["workspace"], "params.json"), "w") as outfile:
        json.dump(st.session_state["p"], outfile)


def v_space(n, col=None):
    for _ in range(n):
        if col:
            col.write("#")
        else:
            st.write("#")


def open_df(file):
    separators = {"txt": "\t", "tsv": "\t", "csv": ","}
    try:
        if type(file) == str:
            ext = file.split(".")[-1]
            if ext != "xlsx":
                df = pd.read_csv(file, sep=separators[ext])
            else:
                df = pd.read_excel(file)
        else:
            ext = file.name.split(".")[-1]
            if ext != "xlsx":
                df = pd.read_csv(file, sep=separators[ext])
            else:
                df = pd.read_excel(file)
        # sometimes dataframes get saved with unnamed index, that needs to be removed
        if "Unnamed: 0" in df.columns:
            df.drop("Unnamed: 0", inplace=True, axis=1)
        return df
    except:
        return pd.DataFrame()


def show_table(df, title, col=""):
    text = f"##### {title}\n{df.shape[0]} rows, {df.shape[1]} columns"
    if col:
        col.download_button(
            "Download Table",
            df.to_csv(sep="\t").encode("utf-8"),
            title.replace(" ", "-") + ".tsv",
        )
        col.dataframe(df)
    else:
        st.download_button(
            "Download Table",
            df.to_csv(sep="\t").encode("utf-8"),
            title.replace(" ", "-") + ".tsv",
        )
        st.dataframe(df)


def download_plotly_figure(fig, col=None, filename=""):
    buffer = io.BytesIO()
    fig.write_image(file=buffer, format="png")

    if col:
        col.download_button(
            label=f"Download Figure",
            data=buffer,
            file_name=filename,
            mime="application/png",
        )
    else:
        st.download_button(
            label=f"Download Figure",
            data=buffer,
            file_name=filename,
            mime="application/png",
        )


def reset_directory(path: Path):
    shutil.rmtree(path)
    path.mkdir(parents=True, exist_ok=True)


# Functionality to update the text file with selected mzML files
def update_selected_mzML():
    with open(Path(st.session_state["workspace"], "selected-mzML.txt"), "w") as f:
        f.write(
            "\n".join([file+".mzML" for file in st.session_state.selected]))


def remove_selected_mzML(to_remove=[]):
    with open(Path(st.session_state["workspace"], "selected-mzML.txt"), "r") as f:
        keep = [line.strip() for line in f.readlines()
                if line.strip() not in to_remove]
    with open(Path(st.session_state["workspace"], "selected-mzML.txt"), "w") as f:
        f.write("\n".join(keep))
    # empty list means remove all
    if not to_remove:
        Path(st.session_state["workspace"], "selected-mzML.txt").unlink()
        Path(st.session_state["workspace"],
             "selected-mzML.txt").touch(exist_ok=True)


def add_mzML_file(name):
    if name and name.endswith(".mzML"):
        with open(Path(st.session_state["workspace"], "selected-mzML.txt"), "r") as f:
            files = [l.strip() for l in f.readlines()]
            if name not in files:
                files.append(name)
        with open(Path(st.session_state["workspace"], "selected-mzML.txt"), "w") as f:
            f.write("\n".join(files))


def get_selected_mzML_files():
    with open(Path(st.session_state["workspace"], "selected-mzML.txt"), "r") as f:
        return [name.strip() for name in f.readlines()]


def update_img_format():
    st.session_state["image-format"] = st.session_state.img_format


def sidebar(page=""):
    with st.sidebar:
        if page == "main":
            st.markdown("🖥️ **Workspaces**")
            if st.session_state["location"] == "online":
                new_workspace = st.text_input("enter workspace", "")
                if st.button("**Enter Workspace**") and new_workspace:
                    path = Path(
                        st.session_state["workspaces-dir"], new_workspace)
                    if path.exists():
                        st.session_state["workspace"] = path
                    else:
                        st.warning("⚠️ Workspace does not exist.")
                st.info(
                    f"""💡 Your workspace ID:

**{st.session_state['workspace'].name}**

You can share this unique workspace ID with other people.

⚠️ Anyone with this ID can access your data!"""
                )
            elif st.session_state["location"] == "local":
                # Show available workspaces
                options = [
                    file.name
                    for file in st.session_state["workspaces-dir"].iterdir()
                    if file.is_dir()
                ]

                # Let user chose an already existing workspace
                chosen = st.selectbox(
                    "choose existing workspace",
                    options,
                    index=options.index(
                        str(st.session_state["workspace"].stem)),
                )
                if chosen:
                    st.session_state["workspace"] = Path(
                        st.session_state["workspaces-dir"], chosen
                    )

                # Create or Remove workspaces
                create_remove = st.text_input(
                    "create/remove workspace", "")
                path = Path(
                    st.session_state["workspaces-dir"],
                    create_remove,
                )
                # Create new workspace
                if st.button("**Create Workspace**"):
                    path.mkdir(parents=True, exist_ok=True)
                    st.session_state["workspace"] = path
                    st.experimental_rerun()
                # Remove existing workspace and fall back to default
                if st.button("⚠️ Delete Workspace") and path.exists:
                    shutil.rmtree(path)
                    st.session_state["workspace"] = Path(
                        st.session_state["workspaces-dir"], "default"
                    )
                    st.experimental_rerun()

        if page == "":
            st.markdown("📁 **mzML files**")
            with open(Path(st.session_state["workspace"], "selected-mzML.txt"), "r") as f:
                selected_files = [
                    Path(mzML_file.strip()).stem for mzML_file in f.readlines()]
            st.multiselect("mzML files",  options=[Path(f).stem for f in Path(st.session_state["mzML-files"]).glob("*.mzML")],
                           default=selected_files, key="selected", on_change=update_selected_mzML, label_visibility="collapsed")

        st.markdown("---")
        st.image("assets/OpenMS.png", "powered by")
        st.markdown("---")

        with st.expander("⚙️ **Settings**"):
            img_formats = ["svg", "png", "jpeg", "webp"]
            st.selectbox(
                "image export format",
                img_formats,
                img_formats.index(
                    st.session_state["image-format"]), on_change=update_img_format, key="img_format"
            )


WARNINGS = {
    "no-workspace": "No online workspace ID found, please visit the start page first.",
    "missing-mzML": "Upload or select some mzML files first!",
}

ERRORS = {
    "general": "Something went wrong.",
    "workflow": "Something went wrong during workflow execution.",
    "visualization": "Something went wrong during visualization of results.",
}
