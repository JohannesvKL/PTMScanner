import streamlit as st
from src.workflow.WorkflowManager import WorkflowManager

class Workflow(WorkflowManager):
    # Setup pages for upload, parameter, execution and results.
    # For layout use any streamlit components such as tabs (as shown in example), columns, or even expanders.
    def __init__(self) -> None:
        # Initialize the parent class with the workflow name.
        super().__init__("TOPP Workflow", st.session_state["workspace"])

    def upload(self) -> None:
        pass

    def configure(self) -> None:
        pass

    def execution(self) -> None:
        pass

    def results(self) -> None:
        pass
