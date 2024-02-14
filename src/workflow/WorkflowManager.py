from pathlib import Path
from .Logger import Logger
from .ParameterManager import ParameterManager
from .CommandExecutor import CommandExecutor
from .StreamlitUI import StreamlitUI
import multiprocessing
import shutil
import streamlit as st

class WorkflowManager:
    # Core workflow logic using the above classes
    def __init__(self, name: str = "Workflow Base"):
        self.name = name
        self.workflow_dir = Path(st.session_state["workspace"], self.name.replace(" ", "-").lower())
        self.parameter_manager = ParameterManager(self.workflow_dir)
        self.logger = Logger(self.workflow_dir)
        self.executor = CommandExecutor(self.workflow_dir, self.logger, self.parameter_manager)
        self.ui = StreamlitUI(self)
        self.params = self.parameter_manager.load_parameters()

    def start_workflow(self) -> None:
        # Delete the log file if it already exists
        self.logger.log_file.unlink(missing_ok=True)
        # Start workflow process
        workflow_process = multiprocessing.Process(target=self.workflow_process)
        workflow_process.start()
        # Add workflow process id to pid dir
        self.executor.pid_dir.mkdir()
        Path(self.executor.pid_dir, str(workflow_process.pid)).touch()

    def workflow_process(self) -> None:
        try:
            self.logger.log("Starting workflow...")
            results_dir = Path(self.workflow_dir, "results")
            if results_dir.exists():
                shutil.rmtree(results_dir)
            results_dir.mkdir(parents=True)
            self.execution()
            self.logger.log("COMPLETE")
        except Exception as e:
            self.logger.log(f"ERROR: {e}")
        # Delete pid dir path to indicate workflow is done
        shutil.rmtree(self.executor.pid_dir, ignore_errors=True)


    def upload(self) -> None:
        ###################################
        # Add your file upload widgets here
        ###################################
        pass

    def configure(self) -> None:
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