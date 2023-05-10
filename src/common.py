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
REPOSITORY_NAME = "openms-streamlit-template"
APP_NAME = "OpenMS App Template"


def page_setup(page="default"):
    # Streamlit configs
    st.set_page_config(
        page_title=APP_NAME,
        page_icon="assets/OpenMS.png",
        layout="wide",
        initial_sidebar_state="auto",
        menu_items=None,
    )

    # Determining workspace -> should run once at app start-up
    if "workspace" not in st.session_state:
        # in docker need to set working directory to repository directory
        if "docker" in sys.argv:
            os.chdir(REPOSITORY_NAME)
        # define directory where all workspaces will be stored outside of repository directory
        workspaces_dir = Path("..", "workspaces-"+REPOSITORY_NAME)
        # Local: workspace name at startup: default-workspace
        if "local" in sys.argv:
            st.session_state.location = "local"
            st.session_state["workspace"] = Path(
                workspaces_dir, "default"
            )
        # Online: create a random key as workspace name
        else:
            st.session_state.location = "online"
            st.session_state["workspace"] = Path(
                workspaces_dir, str(uuid.uuid1())
            )

    # Make sure important directories exist
    st.session_state["workspace"].mkdir(parents=True, exist_ok=True)
    Path(st.session_state["workspace"],
         "mzML-files").mkdir(parents=True, exist_ok=True)

    params = load_params()

    sidebar(params, page)
    # Load and return initial parameters
    return params


def load_params():
    path = Path(st.session_state["workspace"], "params.json")
    if path.exists():
        # Opening JSON file
        with open(path, "r") as f:
            return json.load(f)
    else:
        with open("assets/default-params.json", "r") as f:
            return json.load(f)


def save_params(params, check_sesion_state=True):
    if check_sesion_state:
        for key, value in st.session_state.items():
            if isinstance(value, (str, int, float, dict, list)):
                if not any([x in key for x in ["FormSubmitter", "location", "mzML-upload"]]):
                    params[key] = value
    with open(Path(st.session_state["workspace"], "params.json"), "w") as outfile:
        json.dump(params, outfile, indent=4)


def sidebar(params, page=""):
    with st.sidebar:
        # The main page has workspace switcher
        if page == "main":
            st.markdown("🖥️ **Workspaces**")
            workspaces_dir = Path(st.session_state["workspace"], "..")
            if st.session_state["location"] == "online":
                new_workspace = st.text_input("enter workspace", "")
                if st.button("**Enter Workspace**") and new_workspace:
                    path = Path(
                        workspaces_dir, new_workspace)
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
                    for file in workspaces_dir.iterdir()
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
                        workspaces_dir, chosen
                    )

                # Create or Remove workspaces
                create_remove = st.text_input(
                    "create/remove workspace", "")
                path = Path(
                    workspaces_dir,
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
                        workspaces_dir, "default"
                    )
                    st.experimental_rerun()

        # Workflow pages have mzML file selector, there can be multiple workflow pages which share mzML file selection
        if page == "workflow":
            st.markdown("📁 **mzML files**")
            st.multiselect("mzML files",  options=[Path(f).stem for f in Path(st.session_state["workspace"], "mzML-files").glob("*.mzML")],
                           default=params["selected-mzML-files"], key="selected-mzML-files", on_change=save_params, args=[params], label_visibility="collapsed")
            st.markdown("---")

        # All pages have logo and settings
        st.image("assets/OpenMS.png", "powered by")
        st.markdown("---")
        with st.expander("⚙️ **Settings**"):
            img_formats = ["svg", "png", "jpeg", "webp"]
            st.selectbox(
                "image export format",
                img_formats,
                img_formats.index(params["image-format"]), on_change=save_params, args=[params], key="image-format"
            )
        # Indicator for current workspace
        if page != "main":
            st.info(
                f"**{Path(st.session_state['workspace']).stem}**")


def v_space(n, col=None):
    for _ in range(n):
        if col:
            col.write("#")
        else:
            st.write("#")


def show_table(df, download_name):
    st.dataframe(df, use_container_width=True)
    st.download_button(
        "Download Table",
        df.to_csv(sep="\t").encode("utf-8"),
        download_name.replace(" ", "-") + ".tsv",
    )


def show_fig(fig, download_name, params, container_width=True):
    st.plotly_chart(
        fig,
        use_container_width=container_width,
        config={
            "displaylogo": False,
            "modeBarButtonsToRemove": [
                "zoom",
                "pan",
                "select",
                "lasso",
                "zoomin",
                "autoscale",
                "zoomout",
                "resetscale",
            ],
            "toImageButtonOptions": {
                "filename": download_name,
                "format": params["image-format"],
            },
        },
    )


def reset_directory(path: Path):
    shutil.rmtree(path)
    path.mkdir(parents=True, exist_ok=True)


# General warning/error messages
WARNINGS = {
    "missing-mzML": "Upload or select some mzML files first!",
}

ERRORS = {
    "general": "Something went wrong.",
    "workflow": "Something went wrong during workflow execution.",
    "visualization": "Something went wrong during visualization of results.",
}
