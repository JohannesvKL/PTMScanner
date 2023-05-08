import streamlit as st
from src.common import *
from src.workflow import *

def content():
    page_setup()
    sidebar()
    st.title("Workflow")

if __name__ == "__main__":
    # try:
    content()
    # except:
    #     st.warning(ERRORS["visualization"])