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

# set up the workflow directory and page name
workflow_dir = Path(st.session_state.workspace, "TOPP-workflow")
st.title("TOPP Workflow")

# if not workflow_dir.exists():
#     workflow_dir.mkdir(parents=True, exist_ok=True)

# log_file = Path(workflow_dir, "log.txt")
# pid_dir = Path(workflow_dir, "pids")

# Everything else can be left unchanged
wf = TOPPWorkflow(workflow_dir)

if not wf.pid_dir.exists():
    wf.show_input_section()
else:
    if st.button("Stop Workflow", type="primary", use_container_width=True):
        wf.stop()
        st.rerun()

if wf.log_file.exists():
    if wf.pid_dir.exists():
        with st.spinner("**Workflow running...**"):
            with open(wf.log_file, "r") as f:
                st.code(f.read(), language="neon", line_numbers=True)
            time.sleep(5)
            st.rerun()
    else:
        with st.expander("**Log file content of last run**"):
            with open(wf.log_file, "r") as f:
                st.code(f.read(), language="neon", line_numbers=True)
    

