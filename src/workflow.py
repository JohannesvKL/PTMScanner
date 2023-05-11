import time

import numpy as np
import pandas as pd
import streamlit as st


@st.cache_data
def generate_random_table(dimension):
    """Example for a cached table"""
    df = pd.DataFrame(np.random.randn(dimension, dimension))
    time.sleep(3)
    return df
