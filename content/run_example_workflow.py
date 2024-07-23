import streamlit as st
import pandas as pd
import plotly.express as px

from pathlib import Path

from src.common import page_setup, save_params, show_fig, show_table
from src import mzmlfileworkflow

# Page name "workflow" will show mzML file selector in sidebar
params = page_setup()

st.title("Workflow")
st.markdown(
    """
More complex workflow with mzML files and input form.
             
Changing widgets within the form will not trigger the execution of the script immediatly.
This is great for large parameter sections.
"""
)

with st.form("workflow-with-mzML-form"):
    st.markdown("**Parameters**")
    st.multiselect(
        "**input mzML files**",
        [f.stem for f in Path(st.session_state.workspace, "mzML-files").glob("*.mzML")],
        params["example-workflow-selected-mzML-files"],
        key="example-workflow-selected-mzML-files",
    )

    c1, _, c3 = st.columns(3)
    if c1.form_submit_button(
        "Save Parameters", help="Save changes made to parameter section."
    ):
        params = save_params(params)
    run_workflow_button = c3.form_submit_button("Run Workflow", type="primary")

result_dir = Path(st.session_state["workspace"], "mzML-workflow-results")

if run_workflow_button:
    params = save_params(params)
    if params["example-workflow-selected-mzML-files"]:
        mzmlfileworkflow.run_workflow(params, result_dir)
    else:
        st.warning("Select some mzML files.")

result_dirs = [f.name for f in Path(result_dir).iterdir() if f.is_dir()]

run_dir = st.selectbox("select result from run", result_dirs)

result_dir = Path(result_dir, run_dir)
# visualize workflow results if there are any
result_file_path = Path(result_dir, "result.tsv")

if result_file_path.exists():
    df = pd.read_csv(result_file_path, sep="\t", index_col="filenames")

    if not df.empty:
        tabs = st.tabs(["📁 data", "📊 plot"])

        with tabs[0]:
            show_table(df, "mzML-workflow-result")

        with tabs[1]:
            fig = px.bar(df)
            st.info(
                "💡 Download figure with camera icon in top right corner. File format can be specified in settings."
            )
            show_fig(fig, "mzML-workflow-results")
