import streamlit as st
from pathlib import Path
import shutil
from .WorkflowBase import WorkflowBase

class TOPPWorkflow(WorkflowBase):

    def __init__(self, workflow_dir: str):
        super().__init__(workflow_dir)

    def run(self) -> None:
        # Make sure results directory exits and reset
        results = self.ensure_directory_exists(
            Path(self.workflow_dir, "results"), reset=True)

        self.log("Starting example workflow using TOPP tools...")

        # Get input file paths
        mzML_files = [str(Path(st.session_state["workspace"], "mzML-files", f))
                      for f in st.session_state["mzML_files"]]
        self.log("Number of mzML files: " + str(len(mzML_files)))

        # Feature Detection
        tmp_results = self.ensure_directory_exists(
            Path(results, "FeatureFinderMetabo"))
        self.log(
            "Detecting features with FeatureFinderMetabo for all files in parallel.")
        # Create a list of commands to run in parallel
        commands = [["FeatureFinderMetabo", "-in", f, "-out", str(Path(
            tmp_results, Path(f.replace(".mzML", ".featureXML")).name))] for f in mzML_files]
        # Run commands in parallel without logs
        self.run_multiple_commands(commands, False)

        # Workflow complete
        self.log("COMPLETE")
        # Delete pid dir path to indicate workflow is done
        shutil.rmtree(self.pid_dir, ignore_errors=True)

    def show_input_section(self) -> None:

        form = st.form("topp-workflow-parameters")
        cols = form.columns(3)
        # cols[0].form_submit_button("Save Parameters", use_container_width=True)
        cols[1].form_submit_button("Start Workflow", type="primary", use_container_width=True,
                                on_click=self.start_workflow_process, args=(form,))

        # input mzML files...
        form.multiselect("Select mzML files", options=[f.name for f in Path(
            st.session_state["workspace"], "mzML-files").iterdir()], key="mzML_files")
