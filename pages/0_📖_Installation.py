import streamlit as st 
from pathlib import Path
from src.common import page_setup

page_setup()

if Path("OpenMS-App.zip").exists():
    st.markdown("""
Download the latest version for **Windows** here clicking the button below.
""")
    with open("OpenMS-App.zip", "rb") as file:
        st.download_button(
            label="Download for Windows",
            data=file,
            file_name="OpenMS-App.zip",
            mime="archive/zip",
            type="primary",
        )

st.markdown("""
# Installation

## Windows

The app is available as pre-packaged Windows executable, including all dependencies.

The windows executable is built by a GitHub action and can be downloaded [here](https://github.com/OpenMS/streamlit-template/actions/workflows/build-windows-executable-app.yaml).
Select the latest successfull run and download the zip file from the artifacts section, while signed in to GitHub.

## Python

Clone the [streamlit-template repository](https://github.com/OpenMS/streamlit-template). It includes files to install dependencies via pip or conda.

### via pip in an existing Python environment

To install all required depdencies via pip in an already existing Python environment, run the following command in the terminal:

`pip install -r requirements.txt`

### create new environment via conda/mamba

Create and activate the conda environment:

`conda env create -f environment.yml`

`conda activate streamlit-env`

### run the app

Run the app via streamlit command in the terminal with or without *local* mode (default is *online* mode). Learn more about *local* and *online* mode in the documentation page 📖 **OpenMS Template App**.

`streamlit run app.py [local]`

## Docker

This repository contains two Dockerfiles.

1. `Dockerfile`: This Dockerfile builds all dependencies for the app including Python packages and the OpenMS TOPP tools. Recommended for more complex workflows where you want to use the OpenMS TOPP tools for instance with the **TOPP Workflow Framework**.
2. `Dockerfile_simple`: This Dockerfile builds only the Python packages. Recommended for simple apps using pyOpenMS only.

""")