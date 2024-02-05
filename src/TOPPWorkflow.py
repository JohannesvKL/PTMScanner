import streamlit as st
from pathlib import Path
from .workflow.WorkflowManager import WorkflowManager
from .workflow.Files import Files


class TOPPWorkflow(WorkflowManager):

    def __init__(self):
        super().__init__("TOPP Workflow")

    def define_file_upload_section(self) -> None:
        tabs = st.tabs(
            ["**mzML files**"])
        with tabs[0]:
            self.ui.upload("mzML-files", "mzML")

    def define_input_section(self) -> None:
        self.ui.select_input_file("mzML-files", multiple=True)
        
        tabs = st.tabs(
            ["**Feature Detection**", "**Adduct Detection**", "**SIRIUS Export**", "**Mass Search**"])
        with tabs[0]:
            self.ui.input_TOPP("FeatureFinderMetabo")
        with tabs[1]:
            self.ui.input_TOPP("MetaboliteAdductDecharger")
        with tabs[2]:
            self.ui.input_TOPP("SiriusExport")
        # with tabs[3]:
        #     self.ui.input_TOPP("AccurateMassSearch")

    def define_workflow_steps(self) -> None:
        # Input files
        in_mzML = Files(self.params["mzML-files"])
        self.logger.log(f"Number of input mzML files: {len(in_mzML)}")

        # Feature Detection
        out_ffm = Files(in_mzML, "featureXML", "feature-detection")
        self.executor.run_topp("FeatureFinderMetabo", {
                               "in": in_mzML, "out": out_ffm}, False)

        # Adduct Detection
        self.executor.run_topp("MetaboliteAdductDecharger", {
                               "in": out_ffm, "out_fm": out_ffm}, False)

        # SiriusExport
        in_mzML.combine()
        out_ffm.combine()
        out_se = Files(["sirius-export.ms"], None, "sirius-export")
        self.executor.run_topp(
            "SiriusExport", {"in": in_mzML, "in_featureinfo": out_ffm, "out": out_se}, False)

        # SIRIUS
        out_sirius = Files("sirius-project", None, "sirius")
        self.executor.run_command(["sirius", "--input", out_se[0], "--project", out_sirius[0], "--maxmz", "300",
                                   "--no-compression", "formula", "passatutto", "write-summaries"], False)
