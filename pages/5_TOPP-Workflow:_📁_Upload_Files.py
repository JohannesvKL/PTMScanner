import streamlit as st
from pathlib import Path
from src.TOPPWorkflow import TOPPWorkflow
from src.common import page_setup

params = page_setup()

wf = TOPPWorkflow()


# Everything else can be left unchanged
st.title(f"📁 Upload Files")

wf.show_file_upload_section()
