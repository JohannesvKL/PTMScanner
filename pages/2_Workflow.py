import streamlit as st
import numpy as np
import pandas as pd
import holoviews as hv
from holoviews import dim, opts

hv.extension("bokeh")


data = pd.DataFrame(np.random.randn(2, 100000), columns=["RT", "mz"])

st.dataframe(data)
