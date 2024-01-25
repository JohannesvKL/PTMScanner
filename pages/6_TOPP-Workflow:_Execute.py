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

st.title(f"{wf.name}: Execute")

cols = st.columns(3)

if wf.pid_dir.exists():
    if cols[1].button("Stop Workflow", type="primary", use_container_width=True):
        wf.stop()
        st.rerun()
else:
    cols[1].button("Start Workflow", type="primary", use_container_width=True,
                                on_click=wf.start_workflow_process)

if wf.log_file.exists():
    if wf.pid_dir.exists():
        with st.spinner("**Workflow running...**"):
            with open(wf.log_file, "r") as f:
                st.code(f.read(), language="neon", line_numbers=True)
            time.sleep(2)
            st.rerun()
    else:
        with st.expander("**Log file content of last run**"):
            with open(wf.log_file, "r") as f:
                st.code(f.read(), language="neon", line_numbers=True)
    

