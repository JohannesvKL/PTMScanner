import streamlit as st
from pathlib import Path
from .WorkflowBase import WorkflowBase


class TOPPWorkflow(WorkflowBase):

    def __init__(self):
        super().__init__("TOPP Workflow")

    def define_workflow_steps(self, results_dir: str, params: dict) -> None:

        self.log("Starting example workflow using TOPP tools...")

        # Get input file paths
        mzML_files = [str(Path(st.session_state["workspace"], "mzML-files", f))
                      for f in st.session_state["mzML_files"]]
        self.log("Number of mzML files: " + str(len(mzML_files)))

        # Feature Detection
        tmp_results = self.ensure_directory_exists(
            Path(results_dir, "FeatureFinderMetabo"))
        self.log(
            "Detecting features with FeatureFinderMetabo for all files in parallel.")
        # Create a list of commands to run in parallel
        commands = [["FeatureFinderMetabo", "-in", f, "-out", str(Path(
            tmp_results, Path(f.replace(".mzML", ".featureXML")).name))] for f in mzML_files]
        # Run commands in parallel without logs
        self.run_multiple_commands(commands, False)


    def define_input_section(self, params) -> None:
            # input mzML files...
            st.multiselect("Select mzML files", 
                        options=[f.name for f in Path(st.session_state["workspace"], "mzML-files").iterdir()],
                        default=params["mzML_files"],
                        key=f"{self.name}-param-mzML_files")

            # TOPP tools
            self.show_input_TOPP("FeatureFinderMetabo",
                                 num_cols=3,
                                 exclude_parameters=["outpairs",
                                                    "positive_adducts",
                                                    "negative_adducts",
                                                    "mapping",
                                                    "struct"])