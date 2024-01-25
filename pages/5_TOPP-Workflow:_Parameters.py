import streamlit as st
from pathlib import Path
import time
from workflows.TOPPWorkflow import TOPPWorkflow
from src.common import page_setup

# """
# This code sets up a workflow directory, log file, and process ID (pid) directory. 
# It allows the user to start and stop a multiprocessing workflow, 
# displaying the log and tracking process IDs.

# The workflow_dir is created if needed. The log_file and pid_dir are constructed
# within it. An instance of the workflow class is created with the log and pid dirs. 

# The user can start the workflow, which launches it in a separate process. The 
# process ID is tracked in the pid dir. The user can also stop a running workflow.

# If the log file exists, its contents are displayed. It checks for a pid dir 
# to see if the workflow is running. The page reruns periodically to update the log.
# """
params = page_setup()

wf = TOPPWorkflow()


# Everything else can be left unchanged

st.title(f"{wf.name}: Parameters")

wf.show_input_section()

