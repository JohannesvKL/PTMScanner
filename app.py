import streamlit as st
from pathlib import Path

pages = {
    "OpenMS Web App" : [
        st.Page(Path("content", "quickstart.py"), title="Quickstart", icon="👋"),
        st.Page(Path("content", "documentation.py"), title="Documentation", icon="📖"),
    ],
    "TOPP Workflow Framework": [
        st.Page(Path("content", "topp_workflow.py"), title="TOPP Workflow", icon="🚀"),
    ],
    "pyOpenMS Workflow" : [
        st.Page(Path("content", "file_upload.py"), title="File Upload", icon="📂"),
        st.Page(Path("content", "raw_data_viewer.py"), title="View MS data", icon="👀"),
        st.Page(Path("content", "run_example_workflow.py"), title="Run Workflow", icon="⚙️"),
    ],
    "Others Topics": [
        st.Page(Path("content", "simple_workflow.py"), title="Simple Workflow", icon="⚙️"),
        st.Page(Path("content", "run_subprocess.py"), title="Run Subprocess", icon="🖥️"),
    ]
}

pg = st.navigation(pages)
pg.run()