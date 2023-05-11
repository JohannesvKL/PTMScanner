import streamlit as st

from src.common import *
from src.workflow import *

params = page_setup(page="workflow")
st.title("Workflow")

save_params(params)
