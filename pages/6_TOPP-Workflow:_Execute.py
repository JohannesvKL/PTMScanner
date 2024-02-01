import streamlit as st
from src.TOPPWorkflow import TOPPWorkflow
from src.common import page_setup

params = page_setup()

wf = TOPPWorkflow()

st.title(f"{wf.name}: Execute")

wf.show_execution_section()


    

