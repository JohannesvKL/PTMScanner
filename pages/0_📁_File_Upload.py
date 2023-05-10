import streamlit as st
from src.common import *
from src.fileupload import *
from pathlib import Path


def content():
    params = page_setup()

    st.title("File Upload")

    tabs = ["File Upload", "Example Data"]
    if st.session_state["location"] == "local":
        tabs.append("Files from local folder")

    tabs = st.tabs(tabs)

    mzML_dir = Path(st.session_state["workspace"], "mzML-files")

    with tabs[0]:
        with st.form("mzML-upload", clear_on_submit=True):
            files = st.file_uploader(
                "mzML files", accept_multiple_files=(st.session_state.location == "local"))
            cols = st.columns(3)
            if cols[1].form_submit_button("Add files to workspace", type="primary"):
                save_uploaded_mzML(files, params)

    # Example mzML files
    with tabs[1]:
        st.markdown("Short information text about the example data.")
        cols = st.columns(3)
        if cols[1].button("Load Example Data", type="primary"):
            load_example_mzML_files(params)

    # Local file upload option: via directory path
    if st.session_state.location == "local":
        with tabs[2]:
            # with st.form("local-file-upload"):
            local_mzML_dir = st.text_input(
                "path to folder with mzML files")
            # raw string for file paths
            local_mzML_dir = r"{}".format(local_mzML_dir)
            cols = st.columns(3)
            if cols[1].button("Copy files to workspace", type="primary", disabled=(local_mzML_dir == "")):
                params = copy_local_mzML_files_from_directory(
                    local_mzML_dir, params)

    # Two columns to display and delete files
    v_space(1)
    cols = st.columns([0.45, 0.10, 0.45])
    # Display all mzML files currently in workspace
    with cols[2]:
        df = pd.DataFrame(
            {"file name": [f.name for f in Path(mzML_dir).iterdir()]})
        st.markdown("##### mzML files in current workspace:")
        show_table(
            df, f"mzML-files-in-workspace-{Path(st.session_state['workspace']).stem}")
    # Remove files
    with cols[0]:
        with st.expander("remove mzML files"):
            to_remove = st.multiselect("select mzML files",
                                       options=[f.stem for f in sorted(mzML_dir.iterdir())])
            c1, c2 = st.columns(2)
            if c2.button("Remove **selected**", type="primary", disabled=not any(to_remove)):
                remove_selected_mzML_files(to_remove, params)

            if c1.button("⚠️ Remove **all**", disabled=not any(mzML_dir.iterdir())):
                remove_all_mzML_files(params)


if __name__ == "__main__":
    # try:
    content()
    # except:
    #     st.error(ERRORS["general"])
