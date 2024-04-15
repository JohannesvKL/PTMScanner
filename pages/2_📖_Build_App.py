import streamlit as st 

from src.common import page_setup

page_setup()

st.markdown("""
# Build your own app based on this template

## Key concepts

**Workspaces** 

Directories where all data generated and uploaded can be stored as well as a workspace specific parameter file.

**Run the app locally and online**

Launching the app with the `local` argument let's the user create/remove workspaces. In the online the user gets a workspace with a specific ID.

**Parameters**

Parameters (defaults in `assets/default-params.json`) store changing parameters for each workspace. Parameters are loaded via the page_setup function at the start of each page. To track a widget variable via parameters simply give them a key and add a matching entry in the default parameters file. Initialize a widget value from the params dictionary.

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

## App layout

- Main page contains explanatory text on how to use the app and a workspace selector.
- Sidebar contains the OpenMS logo, settings panel and a workspace indicator. The main page contains a workspace selector as well.
- See pages in the template app for example use cases. The content of this app serves as a documentation.

## Modify the template to build your own app

- in `src/common.py` update the name of your app and the repository name
- in `clean-up-workspaces.py` update the name of the workspaces directory to `/workspaces-<your-repository-name>`
    - e.g. for the streamlit template it's "/workspaces-streamlit-template"
- chose one of the Dockerfiles depending on your use case:
    - `Dockerfile` build OpenMS including TOPP tools
    - `Dockerfile_simple` uses pyOpenMS only
- update the Dockerfile:
    - with the `GITHUB_USER` owning the streamlit app repository
    - with the `GITHUB_REPO` name of the streamlit app repository
    - if your main streamlit file is not called `app.py` modfify the following line
        - `RUN echo "mamba run --no-capture-output -n streamlit-env streamlit run app.py" >> /app/entrypoint.sh`
- update Python package dependency files:
    - `requirements.txt` if using `Dockerfile_simple`
    - `environment.yml` if using `Dockerfile`
- update `README.md`
- for the Windows executable package:
    - update `datas` in `run_app_temp.spec` with the Python packages required for your app
    - update main streamlit file name to run in `run_app.py`
    
## How to build a workflow

### Simple workflow using pyopenms

Take a look at the example pages `Simple Workflow` or `Workflow with mzML files` for examples. Put streamlit logic inside the pages and call the functions with workflow logic from from the `src` directory (for our examples `src/simple_workflow.py` and `src/mzmlfileworkflow.py`).

### Complex workflow using TOPP tools

This template app features a module in `src/workflow` that allows for complex and long workflows to be built very efficiently. Check out the `TOPP Workflow Framework` page for more information.
""")

