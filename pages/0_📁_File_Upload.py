import streamlit as st
from src.common import *
from pathlib import Path
import shutil


def content():
    page_setup()

    st.title("File Upload")

    tabs = ["File Upload", "Example Data", "Remove mzML files"]

    tabs = st.tabs(tabs)

    # Online accept only one file per upload, local is unrestricted
    with tabs[0]:
        accept_multiple = True
        if st.session_state.location == "online":
            accept_multiple = False

        with st.form("my-form", clear_on_submit=True):
            uploaded_mzML = st.file_uploader(
                "mzML files", accept_multiple_files=accept_multiple
            )
            # User needs to click button to upload selected files
            cols = st.columns(3)
            if cols[1].form_submit_button("Add to workspace", type="primary"):
                # Need to have a list of uploaded files to copy to the mzML dir,
                # in case of online only a single item is return, so we put it in the list
                if st.session_state.location == "online":
                    uploaded_mzML = [uploaded_mzML]
                # Copy uploaded mzML files to mzML-files directory
                if uploaded_mzML:
                    # opening file dialog and closing without choosing a file results in None upload
                    for file in uploaded_mzML:
                        if file.name not in st.session_state[
                            "mzML-files"
                        ].iterdir() and file.name.endswith("mzML"):
                            with open(
                                Path(
                                    st.session_state["mzML-files"], file.name), "wb"
                            ) as f:
                                f.write(file.getbuffer())
                        add_mzML_file(file.name)
                    st.success("Successfully added uploaded files!")
                else:
                    st.warning("Upload some files before adding them.")

        # Local file upload option: via directory path
        if st.session_state.location == "local":
            v_space(2)
            upload_dir = st.text_input("path to folder with mzML files")
            upload_dir = r"{}".format(upload_dir)
            cols = st.columns(3)
            if cols[1].button("Copy files to workspace", type="primary"):
                uploaded_mzML = Path("example-data", "mzML").glob("*.mzML")
                with st.spinner("Uploading files..."):
                    for file in Path(upload_dir).glob("*.mzML"):
                        if file.name not in st.session_state["mzML-files"].iterdir():
                            shutil.copy(file, st.session_state["mzML-files"])
                            add_mzML_file(file.name)
                    st.success("Successfully added uploaded files!")

    with tabs[1]:
        st.markdown("Short information text about the example data.")
        cols = st.columns(3)
        if cols[1].button("Load Example Data", type="primary"):
            for file in Path("example-data", "mzML").glob("*.mzML"):
                shutil.copy(file, Path(st.session_state["mzML-files"]))
                add_mzML_file(file.name)
            st.experimental_rerun()

    with tabs[2]:
        st.multiselect("remove selected mzML files",  options=[f.name for f in sorted(st.session_state["mzML-files"].iterdir(
        ))], key="to-remove")
        c1, c2 = st.columns(2)
        if c2.button("Remove **selected** mzML files!", type="primary"):
            for name in st.session_state["to-remove"]:
                Path(st.session_state["mzML-files"], name).unlink()
            remove_selected_mzML(st.session_state["to-remove"])
            st.experimental_rerun()

        if c1.button("⚠️ Remove **all** mzML files!"):
            reset_directory(st.session_state["mzML-files"])
            remove_selected_mzML()
            st.experimental_rerun()

    sidebar()


if __name__ == "__main__":
    # try:
    content()
# except:
#     st.error(ERRORS["general"])
