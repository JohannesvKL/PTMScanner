import streamlit as st
from src.workflow import *

st.markdown(
    "The result for each table dimension will be cached and not re-calculated again."
)
dimension = st.number_input("table dimension", 1, 10, 3)
data = generate_random_table(dimension)

st.dataframe(data)
