import streamlit as st
import streamlit as st
import numpy as np
import pandas as pd

import time


@st.cache_data
def generate_random_table(dimension):
    df = pd.DataFrame(np.random.randn(dimension, dimension))
    time.sleep(3)
    return df
