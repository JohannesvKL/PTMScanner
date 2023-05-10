import streamlit as st
from src.common import *
from src.workflow import *


def content():
    params = page_setup(page="workflow")
    st.title("Workflow")


if __name__ == "__main__":
    # try:
    content()
    # except:
    #     st.warning(ERRORS["visualization"])
