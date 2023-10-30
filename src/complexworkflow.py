import streamlit as st
from pathlib import Path
import pyopenms as poms
import pandas as pd
import time
from src.common import reset_directory


def run_workflow(params, result_dir):
    """Load each mzML file into pyOpenMS Experiment and get the number of spectra."""

    # delete old workflow results and set new directory
    reset_directory(result_dir)

    # collect spectra numbers
    num_spectra = []

    # use st.status to print info while running the workflow
    with st.status(
        "Loading mzML files and getting number of spectra...", expanded=True
    ) as status:
        # get selected mzML files from parameters
        for file in params["example-workflow-selected-mzML-files"]:
            # logging file name in status
            st.write(f"Reading mzML file: {file} ...")

            # reading mzML file, getting num spectra and adding some extra time
            path = str(
                Path(st.session_state["workspace"], "mzML-files", file + ".mzML")
            )
            exp = poms.MSExperiment()
            poms.MzMLFile().load(path, exp)
            num_spectra.append(exp.size())
            time.sleep(2)

        # set status as complete and collapse box
        status.update(label="Complete!", expanded=False)

    # create and save result dataframe
    df = pd.DataFrame(
        {
            "filenames": params["example-workflow-selected-mzML-files"],
            "number of spectra": num_spectra,
        }
    )
    df.to_csv(Path(result_dir, "result.tsv"), sep="\t", index=False)
