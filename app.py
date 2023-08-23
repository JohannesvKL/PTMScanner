import streamlit as st
from src.common import *
from streamlit.web import cli
from pathlib import Path

params = page_setup(page="main")

if __name__ == "__main__":
    st.title("Template App")
    st.markdown("## A template for an OpenMS streamlit app.")
    if Path("OpenMS-App.zip").exists():
        st.markdown("## Installation")
        with open("OpenMS-App.zip", "rb") as file:
            st.download_button(
                    label="Download for Windows",
                    data=file,
                    file_name="OpenMS-App.zip",
                    mime="archive/zip",
                )

save_params(params)

