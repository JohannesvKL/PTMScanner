import streamlit as st
from pathlib import Path
# For some reason the windows version only works if this is imported here
import pyopenms

if __name__ == '__main__':
    pages = {
        "Sage Adapter App " : [
            st.Page(Path("content", "quickstart.py"), title="Quickstart", icon="👋"),
            st.Page(Path("content", "file_upload.py"), title="File Upload", icon="📂"),
            st.Page(Path("content", "Analyze_1.py"), title="Analysis", icon="⚙️"),
            st.Page(Path("content", "Result_2.py"), title="Output", icon="📊"),
        ]
    }

    pg = st.navigation(pages)
    pg.run()