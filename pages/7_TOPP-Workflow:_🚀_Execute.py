import streamlit as st
from src.TOPPWorkflow import TOPPWorkflow
from src.common import page_setup

params = page_setup()

wf = TOPPWorkflow()

st.title(f"🚀 Execute")

wf.show_execution_section()


    

