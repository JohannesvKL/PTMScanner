import streamlit as st
from pathlib import Path
from .workflow.WorkflowManager import WorkflowManager
from .workflow.Files import Files

class TOPPWorkflow(WorkflowManager):

    def __init__(self):
        super().__init__("TOPP Workflow")

    def define_input_section(self) -> None:
        mzML_files = [f.name for f in Path(
            st.session_state["workspace"], "mzML-files").iterdir()]

        mzML_files = Files(Path(st.session_state["workspace"], "mzML-files"))

        self.ui.input("mzML-files", mzML_files, "mzML files", "multiselect")

        tabs = st.tabs(
            ["**Feature Detection**", "**Adduct Detection**", "**SIRIUS Export**"])

        with tabs[0]:
            self.ui.input_TOPP("FeatureFinderMetabo")
        with tabs[1]:
            self.ui.input_TOPP("MetaboliteAdductDecharger")
        with tabs[2]:
            self.ui.input_TOPP("SiriusExport")

    def define_workflow_steps(self) -> None:
        # Input files
        in_mzML = Files(self.params["mzML-files"])
        self.logger.log(f"Number of input mzML files: {len(in_mzML)}")
        
        # Feature Detection
        out_ffm = Files(in_mzML, "featureXML", "feature-detection")
        self.executor.run_topp("FeatureFinderMetabo", {"in": in_mzML, "out": out_ffm})
        
        # Adduct Detection
        self.executor.run_topp("MetaboliteAdductDecharger", {"in": out_ffm, "out_fm": out_ffm})

        # SiriusExport
        in_mzML.combine()
        out_ffm.combine()
        out_se = Files(["sirius-export.ms"], None, "sirius-export")
        self.executor.run_topp("SiriusExport", {"in": in_mzML, "in_featureinfo": out_ffm, "out": out_se})
