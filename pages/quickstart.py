"""
Main page for the OpenMS Template App.

This module sets up and displays the Streamlit app for the OpenMS Template App.
It includes:
- Setting the app title.
- Displaying a description.
- Providing a download button for the Windows version of the app.

Usage:
Run this script to launch the OpenMS Template App.

Note:
- If run in local mode, the CAPTCHA control is not applied.
- If not in local mode, CAPTCHA control is applied to verify the user.

Returns:
    None
"""

from pathlib import Path
import streamlit as st

from src.common import page_setup

page_setup(page="main")

st.title("OpenMS Web App Template")
c1, c2 = st.columns(2)
c1.info(
    """
**💡 Template app for OpenMS workflows in a web application using the **streamlit** framework.**
            
- Simple workflows with **pyOpenMS** 
- Complex workflows utilizing **OpenMS TOPP tools** with parallel execution.
- Workspaces for user data with unique shareable IDs
- Persistent parameters and input files within a workspace
- Captcha control
- Packaged executables for Windows
- Deploy multiple apps easily with [docker-compose](https://github.com/OpenMS/streamlit-deployment)
"""
)
c2.image("assets/pyopenms_transparent_background.png", width=300)
st.markdown("## 👋 Quick Start")
if Path("OpenMS-App.zip").exists():
    st.subsubheader(
        """
Download the latest version for Windows here by clicking the button below.
"""
    )
    with open("OpenMS-App.zip", "rb") as file:
        st.download_button(
            label="Download for Windows",
            data=file,
            file_name="OpenMS-App.zip",
            mime="archive/zip",
            type="primary",
        )
    st.markdown(
        """
Extract the zip file and run the executable (.exe) file to launch the app. Since every dependency is compressed and packacked the app will take a while to launch (up to one minute).
"""
    )

st.markdown("### 📖 Documentation")
st.markdown(
    f"""
This template app includes documentation for **users** including **installation** and introduction to template specific concepts such as **workspaces** and developers with detailed instructions on **how to create and deploy your own app** based on this template.
"""
)
st.page_link(
    "pages/documentation.py",
    label="Read documentation here, select chapter in the content menu.",
    icon="➡️",
)
st.markdown("### Example pages: workflows, visualization and more")
st.markdown(
    """
This app serves both as documentation and showcase what's possible with OpenMS web apps. 
            
In general there are two options for building workflows.
            
#### 1. 🚀 **TOPP Workflow Framework**
            
Use this option if you want a standardized framework for building your workflow.

- **pre-defined user interface** all in one streamlit page with all steps in different tabs:
    - **File Upload**: upload, download and delete input files
    - **Configure**: Automatically display input widgets for all paramters in TOPP tools and custom Python scripts
    - **Run**: Start and stop workflow execution, includes continous log
    - **Results**: Interactive result dashboard
- **write less code**: everything from file upload, input widget generation and execution of tools is handled via convenient functions
- **fast and performant workflows**: Automatic parallel execution of TOPP tools ensures great speed, comparable with workflows written in bash

"""
)
st.page_link(
    "pages/documentation.py",
    label="Check out extensive documentation on the TOPP tool framework.",
    icon="➡️",
)
st.page_link(
    "pages/topp_workflow.py", label="Play around with the example workflow.", icon="➡️"
)
st.markdown(
    """
#### 2. 🐍 **Flexible, custom workflow with pyOpenMS on multiple pages**
            
Use this option if you want full control over your workflow implementation and user interface.

Uses the integrated parameter handling with global parameters across pages, including uploaded files.
            
To get an idea check out the following pages from the example worklfow (file upload first!).
"""
)
st.page_link(
    "pages/file_upload.py",
    label="Upload your own mzML files or use the provided example data set.",
    icon="➡️",
)
st.page_link(
    "pages/raw_data_viewer.py",
    label="Visualize mzML file content in an interactive dashboard.",
    icon="➡️",
)
st.page_link(
    "pages/run_example_workflow.py",
    label="Run a small example workflow with mzML files and check out results.",
    icon="➡️",
)

st.markdown(
    """
#### Other Topics
            
Includes other example pages which are independent to showcase other functionalities.
"""
)
st.page_link(
    "pages/simple_workflow.py",
    label="A very simple worklfow explaining the concepts of data caching in streamlit.",
    icon="➡️",
)
st.page_link(
    "pages/run_subprocess.py",
    label="How to run any command line tool as subprocess from within the OpenMS web app.",
    icon="➡️",
)