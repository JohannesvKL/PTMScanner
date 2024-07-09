import streamlit as st
from pathlib import Path

pages = {
    "OpenMS Web App" : [
        st.Page(Path("pages", "quickstart.py"), title="Quickstart", icon="👋"),
        st.Page(Path("pages", "documentation.py"), title="Documentation", icon="📖"),
    ],
    "TOPP Workflow Framework": [
        st.Page(Path("pages", "topp_workflow.py"), title="TOPP Workflow", icon="🚀"),
    ],
    "Example MS Workflow" : [
        st.Page(Path("pages", "file_upload.py"), title="File Upload", icon="📂"),
        st.Page(Path("pages", "raw_data_viewer.py"), title="View MS data", icon="👀"),
        st.Page(Path("pages", "run_example_workflow.py"), title="Run Workflow", icon="⚙️"),
    ],
    "Others Topics": [
        st.Page(Path("pages", "simple_workflow.py"), title="Simple Workflow", icon="⚙️"),
        st.Page(Path("pages", "run_subprocess.py"), title="Run Subprocess", icon="🖥️"),
    ]
}

pg = st.navigation(pages)
pg.run()