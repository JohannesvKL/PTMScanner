import streamlit as st
from .workflow.WorkflowManager import WorkflowManager
from .workflow.Files import Files


class TOPPWorkflow(WorkflowManager):

    def __init__(self):
        super().__init__("TOPP Workflow")

    def define_file_upload_section(self) -> None:
        tabs = st.tabs(
            [
                "**mzML files**",
                "**Mass Search: mapping**",
                "**Mass Search: struct**",
                "**Mass Search: positive adducts**",
                "**Mass Search: negative adducts**",
            ]
        )
        with tabs[0]:
            self.ui.upload("mzML-files", "mzML")
        with tabs[1]:
            self.ui.upload(
                "ams-mapping",
                "tsv",
                "mapping",
                fallback_files="example-data/AccurateMassSearch/HMDBMappingFile.tsv",
            )
        with tabs[2]:
            self.ui.upload(
                "ams-struct",
                "tsv",
                "struct",
                fallback_files="example-data/AccurateMassSearch/HMDB2StructMapping.tsv",
            )
        with tabs[3]:
            self.ui.upload(
                "ams-positive-adducts",
                "tsv",
                "positive adducts",
                fallback_files="example-data/AccurateMassSearch/PositiveAdducts.tsv",
            )
        with tabs[4]:
            self.ui.upload(
                "ams-negative-adducts",
                "tsv",
                "negative adducts",
                fallback_files="example-data/AccurateMassSearch/NegativeAdducts.tsv",
            )

    def define_input_section(self) -> None:
        self.ui.select_input_file("mzML-files", multiple=True)
        tabs = st.tabs(
            [
                "**Feature Detection**",
                "**Adduct Detection**",
                "**SIRIUS Export**",
                "**SIRIUS**",
                "**Mass Search**",
            ]
        )
        with tabs[0]:
            self.ui.input_TOPP("FeatureFinderMetabo")
        with tabs[1]:
            self.ui.input_TOPP("MetaboliteAdductDecharger")
        with tabs[2]:
            self.ui.input_TOPP("SiriusExport")
        with tabs[3]:
            cols = st.columns(3)
            with cols[0]:
                st.markdown("##")
                self.ui.input("run-sirius", True, "run SIRIUS", help="Run SIRIUS.")
            with cols[1]:
                self.ui.input(
                    "sirius-username",
                    name="SIRIUS username",
                    help="SIRIUS login username.",
                )
            with cols[2]:
                self.ui.input(
                    "sirius-password",
                    name="SIRIUS password",
                    help="SIRIUS login password",
                    widget_type="password",
                )
            cols = st.columns(3)
            with cols[0]:
                self.ui.input(
                    "sirius-maxmz",
                    300,
                    "max mz",
                    step_size=50,
                    help="Max precursor m/z to search for.",
                )
            with cols[1]:
                self.ui.input(
                    "sirius-profile",
                    "default",
                    "instrument type",
                    options=["default", "qtof", "orbitrap", "fticr"],
                )
        with tabs[4]:
            cols = st.columns(2)
            with cols[0]:
                self.ui.select_input_file("ams-mapping")
            with cols[1]:
                self.ui.select_input_file("ams-struct")
            with cols[0]:
                self.ui.select_input_file("ams-positive-adducts")
            with cols[1]:
                self.ui.select_input_file("ams-negative-adducts")
            self.ui.input_TOPP("AccurateMassSearch", num_cols=4)

    def define_workflow_steps(self) -> None:
        # Input files
        in_mzML = Files(self.params["mzML-files"])
        self.logger.log(f"Number of input mzML files: {len(in_mzML)}")

        # Feature Detection
        out_ffm = Files(in_mzML, "featureXML", "feature-detection")
        self.executor.run_topp(
            "FeatureFinderMetabo", {"in": in_mzML, "out": out_ffm}, False
        )

        # Adduct Detection
        self.executor.run_topp(
            "MetaboliteAdductDecharger", {"in": out_ffm, "out_fm": out_ffm}, False
        )

        self.executor.run_topp(
            "AccurateMassSearch",
            {
                "in": out_ffm,
                "out": Files(out_ffm, "mzTab", ""),
                "out_annotation": out_ffm,
                "db:mapping": Files(self.params["ams-mapping"]),
                "db:struct": Files(self.params["ams-struct"]),
                "positive_adducts": Files(self.params["ams-positive-adducts"]),
                "negative_adducts": Files(self.params["ams-negative-adducts"]),
            },
            False,
        )

        # SiriusExport
        in_mzML.combine()
        out_ffm.combine()
        out_se = Files(["sirius-export.ms"], None, "sirius-export")
        self.executor.run_topp(
            "SiriusExport",
            {"in": in_mzML, "in_featureinfo": out_ffm, "out": out_se},
            False,
        )

        # SIRIUS
        if self.params["run-sirius"]:
            out_sirius = Files("sirius-project", None, "sirius")
            self.executor.run_command(
                [
                    "sirius",
                    "--input",
                    out_se[0],
                    "--project",
                    out_sirius[0],
                    "--maxmz",
                    self.params["sirius-maxmz"],
                    "--no-compression",
                    "formula",
                    "--profile",
                    self.params["sirius-profile"],
                    "passatutto",
                    "write-summaries",
                ],
                False,
            )
