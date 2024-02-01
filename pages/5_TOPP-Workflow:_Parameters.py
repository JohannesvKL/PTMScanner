import streamlit as st
from pathlib import Path
from src.TOPPWorkflow import TOPPWorkflow
from src.common import page_setup

params = page_setup()

wf = TOPPWorkflow()


# Everything else can be left unchanged

st.title(f"{wf.name}: Parameters")

wf.show_input_section()
