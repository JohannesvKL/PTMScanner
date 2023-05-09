import streamlit as st
from src.common import *
from src.workflow import *


def content():
    page_setup()
    sidebar()
    st.title("Workflow")

    st.session_state["p"] = load_params()

    st.number_input("djkjd", 1, 10, st.session_state["p"]["select"],
                    key="select", on_change=save_params)  # , args=[p])


if __name__ == "__main__":
    # try:
    content()
    # except:
    #     st.warning(ERRORS["visualization"])
