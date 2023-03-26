import streamlit as st
from src.common import *
from pathlib import Path
import os
import shutil


def content():
    page_setup()

    # make directory to store mzML files
    if not os.path.isdir(st.session_state["mzML-files"]):
        os.mkdir(st.session_state["mzML-files"])

    c1, c2 = st.columns([0.8, 0.2])
    c1.title("File Upload")

    # Load Example Data
    v_space(1, c2)
    if c2.button("Load Example Data"):
        for file in Path("example-data", "mzML").glob("*.mzML"):
            shutil.copy(file, Path(st.session_state["mzML-files"]))

    # Display info how to upload files
    st.info(
        """
    **💡 How to upload files**

    1. Browse files on your computer
    2. Click the **Add the uploaded mzML files** button to use them in the workflows

    Select data for anaylsis from the uploaded files shown in the sidebar."""
    )

    # Online accept only one file per upload, local is unrestricted
    accept_multiple = True
    if st.session_state.location == "online":
        accept_multiple = False

    # Upload files via upload widget
    st.markdown("**Upload files**")
    with st.form("my-form", clear_on_submit=True):
        uploaded_mzML = st.file_uploader(
            "mzML files", accept_multiple_files=accept_multiple
        )
        _, c2, _ = st.columns(3)
        # User needs to click button to upload selected files
        submitted = c2.form_submit_button("Add the uploaded mzML files")
        if submitted:
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
                            Path(st.session_state["mzML-files"], file.name), "wb"
                        ) as f:
                            f.write(file.getbuffer())
                st.success("Successfully added uploaded files!")
            else:
                st.warning("Upload some files before adding them.")

    # Local file upload option: via directory path
    if st.session_state.location == "local":
        st.markdown("**OR specify the path to a folder containing your mzML files**")
        c1, c2 = st.columns([0.8, 0.2])
        upload_dir = c1.text_input("path to folder with mzML files")
        upload_dir = r"{}".format(upload_dir)
        c2.markdown("##")
        if c2.button("Upload"):
            uploaded_mzML = Path("example-data", "mzML").glob("*.mzML")
            with st.spinner("Uploading files..."):
                for file in Path(upload_dir).glob("*.mzML"):
                    if file.name not in st.session_state["mzML-files"].iterdir():
                        shutil.copy(file, st.session_state["mzML-files"])
                st.success("Successfully added uploaded files!")

    sidebar(page="files")


if __name__ == "__main__":
    # try:
    content()
# except:
#     st.error(ERRORS["general"])
