import streamlit as st
from src.Workflow import Workflow
from src.workflow.StreamlitUI import StreamlitUI
from src.workflow.FileManager import FileManager
from src.workflow.CommandExecutor import CommandExecutor
from src.common import page_setup
from inspect import getsource
from pathlib import Path
import requests

page_setup()


st.title("Documentation")

cols = st.columns(2)

pages = [
    "User Guide",
    "Installation",
    "Developers Guide: How to build app based on this template",
    "Developers Guide: TOPP Workflow Framework",
    "Developer Guide: Windows Executables",
    "Developers Guide: Deployment",
]
page = cols[0].selectbox(
    "**Content**",
    pages,
)

#############################################################################################
# User Guide
#############################################################################################

if page == pages[0]:
    st.markdown(
        """
# User Guide

Welcome to the OpenMS Streamlit Web Application! This guide will help you understand how to use our tools effectively.

## Advantages of OpenMS Web Apps

OpenMS web applications provide a user-friendly interface for accessing the powerful features of OpenMS. Here are a few advantages:
- **Accessibility**: Access powerful OpenMS algorithms and TOPP tools from any device with a web browser.
- **Ease of Use**: Simplified user interface makes it easy for both beginners and experts to perform complex analyses.
- **No Installation Required**: Use the tools without the need to install OpenMS locally, saving time and system resources.

## Workspaces

In the OpenMS web application, workspaces are designed to keep your analysis organized:
- **Workspace Specific Parameters and Files**: Each workspace stores parameters and files (uploaded input files and results from workflows).
- **Persistence**: Your workspaces and parameters are saved, so you can return to your analysis anytime and pick up where you left off.

## Online and Local Mode Differences

There are a few key differences between operating in online and local modes:
- **File Uploads**:
  - *Online Mode*: You can upload only one file at a time. This helps manage server load and optimizes performance.
  - *Local Mode*: Multiple file uploads are supported, giving you flexibility when working with large datasets.
- **Workspace Access**:
  - In online mode, workspaces are stored temporarily and will be cleared after seven days of inactivity.
  - In local mode, workspaces are saved on your local machine, allowing for persistent storage.

## Downloading Results

You can download the results of your analyses, including data, figures and tables, directly from the application:
- **Figures**: Click the camera icon button, appearing while hovering on the top right corner of the figure. Set the desired image format in the settings panel in the side bar.
- **Tables**: Use the download button to save tables in *csv* format, appearing while hovering on the top right corner of the table.
- **Data**: Use the download section in the sidebar to download the raw results of your analysis.

## Getting Started

To get started:
1. Select or create a new workspace.
2. Upload your data file.
3. Set the necessary parameters for your analysis.
4. Run the analysis.
5. View and download your results.

For more detailed information on each step, refer to the specific sections of this guide.
"""
    )

#############################################################################################
# Installation
#############################################################################################

if page == pages[1]:
    if Path("OpenMS-App.zip").exists():
        st.markdown(
            """
Download the latest version for **Windows** here clicking the button below.
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

"""
    )

#############################################################################################
# Developer Overview, how to build app based on Template
#############################################################################################

if page == pages[2]:
    st.markdown(
        """
# Build your own app based on this template

## App layout

- *Main page* contains explanatory text on how to use the app and a workspace selector. `app.py`
- *Pages* can be navigated via *Sidebar*. Sidebar also contains the OpenMS logo, settings panel and a workspace indicator. The *main page* contains a workspace selector as well.
- See *pages* in the template app for example use cases. The content of this app serves as a documentation.

## Key concepts

- **Workspaces**
: Directories where all data is generated and uploaded can be stored as well as a workspace specific parameter file.
- **Run the app locally and online**
: Launching the app with the `local` argument lets the user create/remove workspaces. In the online the user gets a workspace with a specific ID.
- **Parameters**
: Parameters (defaults in `assets/default-params.json`) store changing parameters for each workspace. Parameters are loaded via the page_setup function at the start of each page. To track a widget variable via parameters simply give them a key and add a matching entry in the default parameters file. Initialize a widget value from the params dictionary.

```python
params = page_setup()

st.number_input(label="x dimension", min_value=1, max_value=20,
value=params["example-y-dimension"], step=1, key="example-y-dimension")

save_params()
```

## Code structure

- **Pages** must be placed in the `pages` directory.
- It is recommended to use a separate file for defining functions per page in the `src` directory.
- The `src/common.py` file contains a set of useful functions for common use (e.g. rendering a table with download button).

## Modify the template to build your own app

1. In `src/common.py`, update the name of your app and the repository name
    ```python
    APP_NAME = "OpenMS Streamlit App"
    REPOSITORY_NAME = "streamlit-template"
    ```
2. In `clean-up-workspaces.py`, update the name of the workspaces directory to `/workspaces-<your-repository-name>`
    ```python
    workspaces_directory = Path("/workspaces-streamlit-template")
    ```
3. Update `README.md` accordingly


**Dockerfile-related**
1. Choose one of the Dockerfiles depending on your use case:
    - `Dockerfile` builds OpenMS including TOPP tools
    - `Dockerfile_simple` uses pyOpenMS only
2. Update the Dockerfile:
    - with the `GITHUB_USER` owning the Streamlit app repository
    - with the `GITHUB_REPO` name of the Streamlit app repository
    - if your main page Python file is not called `app.py`, modify the following line
        ```dockerfile
        RUN echo "mamba run --no-capture-output -n streamlit-env streamlit run app.py" >> /app/entrypoint.sh
        ```
3. Update Python package dependency files:
    - `requirements.txt` if using `Dockerfile_simple`
    - `environment.yml` if using `Dockerfile`
   
## How to build a workflow

### Simple workflow using pyOpenMS

Take a look at the example pages `Simple Workflow` or `Workflow with mzML files` for examples (on the *sidebar*). Put Streamlit logic inside the pages and call the functions with workflow logic from from the `src` directory (for our examples `src/simple_workflow.py` and `src/mzmlfileworkflow.py`).

### Complex workflow using TOPP tools

This template app features a module in `src/workflow` that allows for complex and long workflows to be built very efficiently. Check out the `TOPP Workflow Framework` page for more information (on the *sidebar*).
"""
    )

#############################################################################################
# TOPP Workflow Framework
#############################################################################################

if page == pages[3]:
    wf = Workflow()

    st.title("TOPP Workflow Framework Documentation")

    st.markdown(
        """
## Features

- streamlined methods for uploading files, setting parameters, and executing workflows
- automatic parameter handling
- quickly build parameter interface for TOPP tools with all parameters from *ini* files
- automatically create a log file for each workflow run with stdout and stderr
- workflow output updates automatically in short intervalls
- user can leave the app and return to the running workflow at any time
- quickly build a workflow with multiple steps channelling files between steps
"""
    )

    st.markdown(
        """
## Quickstart

This repository contains a module in `src/workflow` that provides a framework for building and running analysis workflows.

The `WorkflowManager` class provides the core workflow logic. It uses the `Logger`, `FileManager`, `ParameterManager`, and `CommandExecutor` classes to setup a complete workflow logic.

To build your own workflow edit the file `src/TOPPWorkflow.py`. Use any streamlit components such as tabs (as shown in example), columns, or even expanders to organize the helper functions for displaying file upload and parameter widgets.

> 💡 Simply set a name for the workflow and overwrite the **`upload`**, **`configure`**, **`execution`** and **`results`** methods in your **`Workflow`** class.

The file `content/6_TOPP-Workflow.py` displays the workflow content and can, but does not have to be modified.

The `Workflow` class contains four important members, which you can use to build your own workflow:

> **`self.params`:** dictionary of parameters stored in a JSON file in the workflow directory. Parameter handling is done automatically. Default values are defined in input widgets and non-default values are stored in the JSON file.

> **`self.ui`:** object of type `StreamlitUI` contains helper functions for building the parameter and file upload widgets.

> **`self.executor`:** object of type `CommandExecutor` can be used to run any command line tool alone or in parallel and includes a convenient method for running TOPP tools.

> **`self.logger`:** object of type `Logger` to write any output to a log file during workflow execution.

> **`self.file_manager`:** object of type `FileManager` to handle file types and creation of output directories.
"""
    )

    with st.expander("**Complete example for custom Workflow class**", expanded=False):
        st.code(getsource(Workflow))

    st.markdown(
        """
## File Upload

All input files for the workflow will be stored within the workflow directory in the subdirectory `input-files` within it's own subdirectory for the file type.

The subdirectory name will be determined by a **key** that is defined in the `self.ui.upload_widget` method. The uploaded files are available by the specific key for parameter input widgets and accessible while building the workflow.

Calling this method will create a complete file upload widget section with the following components:

- file uploader
- list of currently uploaded files with this key (or a warning if there are none)
- button to delete all files

Fallback files(s) can be specified, which will be used if the user doesn't upload any files. This can be useful for example for database files where a default is provided.
"""
    )

    st.code(getsource(Workflow.upload))

    st.info(
        "💡 Use the same **key** for parameter widgets, to select which of the uploaded files to use for analysis."
    )

    with st.expander("**Code documentation:**", expanded=True):
        st.help(StreamlitUI.upload_widget)

    st.markdown(
        """
## Parameter Input

The paramter section is already pre-defined as a form with buttons to **save parameters** and **load defaults** and a toggle to show TOPP tool parameters marked as advanced.

Generating parameter input widgets is done with the `self.ui.input` method for any parameter and the `self.ui.input_TOPP` method for TOPP tools.

**1. Choose `self.ui.input_widget` for any paramter not-related to a TOPP tool or `self.ui.select_input_file` for any input file:**

It takes the obligatory **key** parameter. The key is used to access the parameter value in the workflow parameters dictionary `self.params`. Default values do not need to be specified in a separate file. Instead they are determined from the widgets default value automatically. Widget types can be specified or automatically determined from **default** and **options** parameters. It's suggested to add a **help** text and other parameters for numerical input.

Make sure to match the **key** of the upload widget when calling `self.ui.input_TOPP`.

**2. Choose `self.ui.input_TOPP` to automatically generate complete input sections for a TOPP tool:**

It takes the obligatory **topp_tool_name** parameter and generates input widgets for each parameter present in the **ini** file (automatically created) except for input and output file parameters. For all input file parameters a widget needs to be created with `self.ui.select_input_file` with an appropriate **key**. For TOPP tool parameters only non-default values are stored.

**3. Choose `self.ui.input_python` to automatically generate complete input sections for a custom Python tool:**

Takes the obligatory **script_file** argument. The default location for the Python script files is in `src/python-tools` (in this case the `.py` file extension is optional in the **script_file** argument), however, any other path can be specified as well. Parameters need to be specified in the Python script in the **DEFAULTS** variable with the mandatory **key** and **value** parameters.
"""
    )

    with st.expander(
        "Options to use as dictionary keys for parameter definitions (see `src/python-tools/example.py` for an example)"
    ):
        st.markdown(
            """
**Mandatory** keys for each parameter
- *key:* a unique identifier
- *value:* the default value

**Optional** keys for each parameter
- *name:* the name of the parameter
- *hide:* don't show the parameter in the parameter section (e.g. for **input/output files**)
- *options:* a list of valid options for the parameter
- *min:* the minimum value for the parameter (int and float)
- *max:* the maximum value for the parameter (int and float)
- *step_size:* the step size for the parameter (int and float)
- *help:* a description of the parameter
- *widget_type:* the type of widget to use for the parameter (default: auto)
- *advanced:* whether or not the parameter is advanced (default: False)
"""
        )

    st.code(getsource(Workflow.configure))
    st.info(
        "💡 Access parameter widget values by their **key** in the `self.params` object, e.g. `self.params['mzML-files']` will give all selected mzML files."
    )

    with st.expander("**Code documentation**", expanded=True):
        st.help(StreamlitUI.input_widget)
        st.help(StreamlitUI.select_input_file)
        st.help(StreamlitUI.input_TOPP)
        st.help(StreamlitUI.input_python)
    st.markdown(
        """
## Building the Workflow

Building the workflow involves **calling all (TOPP) tools** using **`self.executor`** with **input and output files** based on the **`FileManager`** class. For TOPP tools non-input-output parameters are handled automatically. Parameters for other processes and workflow logic can be accessed via widget keys (set in the parameter section) in the **`self.params`** dictionary.

### FileManager

The `FileManager` class serves as an interface for unified input and output files with useful functionality specific to building workflows, such as **setting a (new) file type** and **subdirectory in the workflows result directory**.

Use the **`get_files`** method to get a list of all file paths as strings.

Optionally set the following parameters modify the files:

- **set_file_type** (str): set new file types and result subdirectory. 
- **set_results_dir** (str): set a new subdirectory in the workflows result directory.
- **collect** (bool): collect all files into a single list. Will return a list with a single entry, which is a list of all files. Useful to pass to tools which can handle multiple input files at once.
"""
    )

    st.code(
        """
# Get all file paths as strings from self.param entry.
mzML_files = self.file_manager.get_files(self.params["mzML-files])
# mzML_files = ['../workspaces-streamlit-template/default/topp-workflow/input-files/mzML-files/Control.mzML', '../workspaces-streamlit-template/default/topp-workflow/input-files/mzML-files/Treatment.mzML']

# Creating output files for a TOPP tool, setting a new file type and result subdirectory name.
feature_detection_out = self.file_manager.get_files(mzML_files, set_file_type="featureXML", set_results_dir="feature-detection")
# feature_detection_out = ['../workspaces-streamlit-template/default/topp-workflow/results/feature-detection/Control.featureXML', '../workspaces-streamlit-template/default/topp-workflow/results/feature-detection/Treatment.featureXML']

# Setting a name for the output directory automatically (useful if you never plan to access these files in the results section).
feature_detection_out = self.file_manager.get_files(mzML_files, set_file_type="featureXML", set_results_dir="auto")
# feature_detection_out = ['../workspaces-streamlit-template/default/topp-workflow/results/6DUd/Control.featureXML', '../workspaces-streamlit-template/default/topp-workflow/results/6DUd/Treatment.featureXML']

# Combining all mzML files to be passed to a TOPP tool in a single run. Using "collected" files as argument for self.file_manager.get_files will "un-collect" them.
mzML_files = self.file_manager.get_files(mzML_files, collect=True)
# mzML_files = [['../workspaces-streamlit-template/default/topp-workflow/input-files/mzML-files/Control.mzML', '../workspaces-streamlit-template/default/topp-workflow/input-files/mzML-files/Treatment.mzML']]
    """
    )

    with st.expander("**Code documentation**", expanded=True):
        st.help(FileManager.get_files)

    st.markdown(
        """
### Running commands

It is possible to execute any command line command using the **`self.executor`** object, either a single command or a list of commands in parallel. Furthermore a method to run TOPP tools is included.

**1. Single command**

The `self.executor.run_command` method takes a single command as input and optionally logs stdout and stderr to the workflow log (default True).
"""
    )

    st.code(
        """
self.executor.run_command(["command", "arg1", "arg2", ...])
"""
    )

    st.markdown(
        """
**2. Run multiple commands in parallel**

The `self.executor.run_multiple_commands` method takes a list of commands as inputs.

**3. Run TOPP tools**

The `self.executor.run_topp` method takes a TOPP tool name as input and a dictionary of input and output files as input. The **keys** need to match the actual input and output parameter names of the TOPP tool. The **values** should be of type `FileManager`. All other **non-default parameters (from input widgets)** will be passed to the TOPP tool automatically.

Depending on the number of input files, the TOPP tool will be run either in parallel or in a single run (using **`FileManager.collect`**).
"""
    )

    st.info(
        """💡 **Input and output file order**
        
In many tools, a single input file is processed to produce a single output file.
When dealing with lists of input or output files, the convention is that
files are paired based on their order. For instance, the n-th input file is
assumed to correspond to the n-th output file, maintaining a structured
relationship between input and output data.       
"""
    )
    st.code(
        """
# e.g. FeatureFinderMetabo takes single input files
in_files = self.file_manager.get_files(["sample1.mzML", "sample2.mzML"])
out_files = self.file_manager.get_files(in_files, set_file_type="featureXML", set_results_dir="feature-detection")

# Run FeatureFinderMetabo tool with input and output files in parallel for each pair of input/output files.
self.executor.run_topp("FeatureFinderMetabo", input_output={"in": in_files, "out": out_files})
# FeaturFinderMetabo -in sample1.mzML -out workspace-dir/results/feature-detection/sample1.featureXML
# FeaturFinderMetabo -in sample2.mzML -out workspace-dir/results/feature-detection/sample2.featureXML

# Run SiriusExport tool with mutliple input and output files.
out = self.file_manager.get_files("sirius.ms", set_results_dir="sirius-export")
self.executor.run_topp("SiriusExport", {"in": self.file_manager.get_files(in_files, collect=True),
                                        "in_featureinfo": self.file_manager.get_files(out_files, collect=True),
                                        "out": out_se})
# SiriusExport -in sample1.mzML sample2.mzML -in_featureinfo sample1.featureXML sample2.featureXML -out sirius.ms
        """
    )

    st.markdown(
        """
**4. Run custom Python scripts**

Sometimes it is useful to run custom Python scripts, for example for extra functionality which is not included in a TOPP tool.

`self.executor.run_python` works similar to `self.executor.run_topp`, but takes a single Python script as input instead of a TOPP tool name. The default location for the Python script files is in `src/python-tools` (in this case the `.py` file extension is optional in the **script_file** argument), however, any other path can be specified as well. Input and output file parameters need to be specified in the **input_output** dictionary.
"""
    )

    st.code(
        """
# e.g. example Python tool which modifies mzML files in place based on experimental design
self.ui.input_python(script_file="example", input_output={"in": in_mzML, "in_experimantal_design": FileManager(["path/to/experimantal-design.tsv"])})       
        """
    )

    st.markdown("**Example for a complete workflow section:**")

    st.code(getsource(Workflow.execution))

    with st.expander("**Code documentation**", expanded=True):
        st.help(CommandExecutor.run_command)
        st.help(CommandExecutor.run_multiple_commands)
        st.help(CommandExecutor.run_topp)
        st.help(CommandExecutor.run_python)

#############################################################################################
# Windows Executables
#############################################################################################

if page == pages[4]:
    # Define CSS styles
    css = """
<style>
    /* Add space between tabs */
    .stTabs [data-baseweb="tab-list"] button {
        margin-right: 20px;
        border-radius: 5px;
        transition: background-color 0.3s ease, color 0.3s ease; /* Add smooth transition */
    }
    /* Style active tab */
    .stTabs [data-baseweb="tab-list"] button:focus {
        background-color: #f0f0f0; /* Change background color of active tab */
        color: #333333; /* Change text color of active tab */
        border-width: 3px; /* Increase thickness of blue line */
    }
    /* Style tab text */
    .stTabs [data-baseweb="tab-list"] button [data-testid="stMarkdownContainer"] p {
        font-size: 2rem;
        font-weight: bold;
    }
    /* Add hover effect */
    .stTabs [data-baseweb="tab-list"] button:hover {
        background-color: #f8f8f8; /* Change background color on hover */
    }
</style>
"""

    st.markdown(css, unsafe_allow_html=True)

    st.markdown(
        """
# 💻  How to package everything for Windows executables

This guide explains how to package OpenMS apps into Windows executables using two different methods:
"""
    )


    def fetch_markdown_content(url):
        response = requests.get(url)
        if response.status_code == 200:
            # Remove the first line from the content
            content_lines = response.text.split("\n")
            markdown_content = "\n".join(content_lines[1:])
            return markdown_content
        else:
            return None


    tabs = ["embeddable Python", "PyInstaller"]
    tabs = st.tabs(tabs)

    # window executable with embeddable python
    with tabs[0]:
        markdown_url = "https://raw.githubusercontent.com/OpenMS/streamlit-template/main/win_exe_with_embed_py.md"

        markdown_content = fetch_markdown_content(markdown_url)

        if markdown_content:
            st.markdown(markdown_content, unsafe_allow_html=True)
        else:
            st.error(
                "Failed to fetch Markdown content from the specified URL.", markdown_url
            )

    # window executable with pyinstaller
    with tabs[1]:
        # URL of the Markdown document
        markdown_url = "https://raw.githubusercontent.com/OpenMS/streamlit-template/main/win_exe_with_pyinstaller.md"

        markdown_content = fetch_markdown_content(markdown_url)

        if markdown_content:
            st.markdown(markdown_content, unsafe_allow_html=True)
        else:
            st.error(
                "Failed to fetch Markdown content from the specified URL. ", markdown_url
            )

#############################################################################################
# Deployment
#############################################################################################

if page == pages[5]:
    url = "https://raw.githubusercontent.com/OpenMS/streamlit-deployment/main/README.md"

    response = requests.get(url)

    if response.status_code == 200:
        st.markdown(response.text)  # or process the content as needed
    else:
        st.warning("Failed to get README from streamlit-deployment repository.")