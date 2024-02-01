import streamlit as st
from .workflow.WorkflowManager import WorkflowManager


class TOPPWorkflowTemplate(WorkflowManager):
    ###############################################
    # parameter are available as self.params
    # ui function are vaiable as self.ui
    # run command function with self.executor
    # log messages with self.logger.log()
    ###############################################

    def __init__(self):
        super().__init__("TOPP Workflow Template")

    def define_input_section(self) -> None:
        pass

    def define_workflow_steps(self) -> None:
        pass
