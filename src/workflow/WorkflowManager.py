from pathlib import Path
from .Logger import Logger
from .DirectoryManager import DirectoryManager
from .ParameterManager import ParameterManager
from .CommandExecutor import CommandExecutor
from .Logger import Logger
from .Files import Files
from .StreamlitUI import StreamlitUI
import multiprocessing
import shutil
import time
import streamlit as st

class WorkflowManager():
    # Core workflow logic using the above classes
    def __init__(self, name: str = "Workflow Base"):
        self.name = name
        # workflow-dir should be accessible globally via st.session_state
        st.session_state["workflow-dir"] = Path(st.session_state["workspace"], self.name.replace(" ", "-").lower())
        self.result_dir = Path(st.session_state["workflow-dir"], "results")
        self.params = ParameterManager().load_parameters()
        self.logger = Logger()
        self.executor = CommandExecutor()
        self.ui = StreamlitUI()
        
    def start_workflow_process(self) -> None:
        # Delete the log file if it already exists
        self.logger.log_file.unlink(missing_ok=True)
        # Start workflow process
        workflow_process = multiprocessing.Process(target=self.run)
        workflow_process.start()
        # Add workflow process id to pid dir
        self.executor.pid_dir.mkdir()
        Path(self.executor.pid_dir, str(workflow_process.pid)).touch()
        
    def run(self) -> None:
        self.logger.log("Starting workflow...")
        DirectoryManager().ensure_directory_exists(
            self.result_dir, reset=True)
        self.define_workflow_steps()
        self.logger.log("COMPLETE")
        # Delete pid dir path to indicate workflow is done
        shutil.rmtree(self.executor.pid_dir, ignore_errors=True)
        
    def show_input_section(self) -> None:
        pm = ParameterManager()
        cols = st.columns(3)
        cols[0].toggle("Show advanced parameters", value=False, key="advanced")

        form = st.form(key=f"{st.session_state['workflow-dir'].stem}-input-form", clear_on_submit=True)

        with form:
            cols = st.columns(3)

            cols[1].form_submit_button(label="Save parameters",
                                       on_click=pm.save_parameters,
                                       type="primary",
                                       use_container_width=True)

            if cols[2].form_submit_button(label="Load default parameters",
                                          use_container_width=True):
                pm.reset_to_default_parameters()

            # Load parameters
            self.define_input_section()

    def show_execution_section(self) -> None:
        cols = st.columns(3)

        if self.executor.pid_dir.exists():
            if cols[1].button("Stop Workflow", type="primary", use_container_width=True):
                self.executor.stop()
                st.rerun()
        else:
            cols[1].button("Start Workflow", type="primary", use_container_width=True,
                                        on_click=self.start_workflow_process)

        if self.logger.log_file.exists():
            if self.executor.pid_dir.exists():
                with st.spinner("**Workflow running...**"):
                    with open(self.logger.log_file, "r") as f:
                        st.code(f.read(), language="neon", line_numbers=True)
                    time.sleep(2)
                    st.rerun()
            else:
                with st.expander("**Log file content of last run**", expanded=True):
                    with open(self.logger.log_file, "r") as f:
                        st.code(f.read(), language="neon", line_numbers=True)

    def define_input_section(self) -> None:
        ###################################
        # Add your input widgets here
        ###################################
        pass

    def define_workflow_steps(self) -> None:
        ###################################
        # Add your workflow steps here
        ###################################
        pass
