from pathlib import Path
from .Logger import Logger
from .DirectoryManager import DirectoryManager
from .ParameterManager import ParameterManager
from .CommandExecutor import CommandExecutor
from .StreamlitUI import StreamlitUI
import multiprocessing
import shutil
import time
import streamlit as st


class WorkflowManager:
    # Core workflow logic using the above classes
    def __init__(self, name: str = "Workflow Base"):
        self.name = name
        # workflow-dir should be accessible globally via st.session_state
        st.session_state["workflow-dir"] = Path(
            st.session_state["workspace"], self.name.replace(" ", "-").lower()
        )
        self.result_dir = Path(st.session_state["workflow-dir"], "results")
        self.input_dir = Path(st.session_state["workflow-dir"], "input-files")
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
        try:
            self.logger.log("Starting workflow...")
            DirectoryManager().ensure_directory_exists(self.result_dir, reset=True)
            self.execution()
            self.logger.log("COMPLETE")
        except Exception as e:
            self.logger.log(f"ERROR: {e}")
        # Delete pid dir path to indicate workflow is done
        shutil.rmtree(self.executor.pid_dir, ignore_errors=True)

    def show_file_upload_section(self) -> None:
        self.upload()
        if st.button("⬇️ Download all uploaded files", use_container_width=True):
            DirectoryManager().zip_and_download_files(self.input_dir)

    def show_parameter_section(self) -> None:
        # c1.title(f"⚙️ Parameters")
        st.toggle("Show advanced parameters", value=False, key="advanced")

        pm = ParameterManager()
        form = st.form(
            key=f"{st.session_state['workflow-dir'].stem}-input-form",
            clear_on_submit=True,
        )

        with form:
            cols = st.columns(2)

            cols[0].form_submit_button(
                label="Save parameters",
                on_click=pm.save_parameters,
                type="primary",
                use_container_width=True,
            )

            if cols[1].form_submit_button(
                label="Load default parameters", use_container_width=True
            ):
                pm.reset_to_default_parameters()

            # Load parameters
            self.parameter()
        # Save parameters
        pm.save_parameters()

    def show_execution_section(self) -> None:
        if self.executor.pid_dir.exists():
            if st.button("Stop Workflow", type="primary", use_container_width=True):
                self.executor.stop()
                st.rerun()
        else:
            st.button(
                "Start Workflow",
                type="primary",
                use_container_width=True,
                on_click=self.start_workflow_process,
            )

        if self.logger.log_file.exists():
            if self.executor.pid_dir.exists():
                with st.spinner("**Workflow running...**"):
                    with open(self.logger.log_file, "r", encoding="utf-8") as f:
                        st.code(f.read(), language="neon", line_numbers=True)
                    time.sleep(2)
                st.rerun()
            else:
                st.markdown("**Workflow log file**")
                with open(self.logger.log_file, "r", encoding="utf-8") as f:
                    st.code(f.read(), language="neon", line_numbers=True)

    def show_results_section(self) -> None:
        self.results()

    def upload(self) -> None:
        ###################################
        # Add your file upload widgets here
        ###################################
        pass

    def parameter(self) -> None:
        ###################################
        # Add your input widgets here
        ###################################
        pass

    def execution(self) -> None:
        ###################################
        # Add your workflow steps here
        ###################################
        pass

    def results(self) -> None:
        ###################################
        # Display results here
        ###################################
        pass