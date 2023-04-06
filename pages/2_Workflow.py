import streamlit as st
from src.workflow import *
from src.view import *
import plotly.graph_objects as go

# st.markdown(
#     "The result for each table dimension will be cached and not re-calculated again."
# )
# dimension = st.number_input("table dimension", 1, 10, 3)
# data = generate_random_table(dimension)

# st.dataframe(data)

import numpy as np
from pyopenms import *


@st.cache_resource
def plot_2D_map(df_ms1):

    ints = np.concatenate([df_ms1.loc[index, "intarray"] for index in df_ms1.index])
    mzs = np.concatenate([df_ms1.loc[index, "mzarray"] for index in df_ms1.index])
    rts = np.concatenate(
        [
            np.full(len(df_ms1.loc[index, "mzarray"]), df_ms1.loc[index, "RT"])
            for index in df_ms1.index
        ]
    )

    sort = np.argsort(ints)
    ints = ints[sort]
    mzs = mzs[sort]
    rts = rts[sort]

    st.write(len(rts))

    fig = go.Figure()

    fig.add_trace(
        go.Scattergl(
            name="peaks",
            x=rts,
            y=mzs,
            mode="markers",
            marker_color=ints,
            marker_symbol="square",
        )
    )
    fig.update_layout(
        # title="peak map 2D",
        xaxis_title="retention time",
        yaxis_title="m/z",
        plot_bgcolor="rgb(255,255,255)",
        showlegend=False,
        # width=1000,
        # height=800,
    )
    fig.layout.template = "plotly_white"

    color_scale = [
        (0.00, "rgba(233, 233, 233, 1.0)"),
        (0.01, "rgba(243, 236, 166, 1.0)"),
        (0.1, "rgba(255, 168, 0, 1.0)"),
        (0.2, "rgba(191, 0, 191, 1.0)"),
        (0.4, "rgba(68, 0, 206, 1.0)"),
        (1.0, "rgba(33, 0, 101, 1.0)"),
    ]

    fig.update_traces(
        marker_colorscale=color_scale,
        hovertext=ints.round(),
        selector=dict(type="scattergl"),
    )
    return fig


df = get_df("example-data/mzML/Pool.mzML")
st.dataframe(df)

st.write(df.shape)

# df["mzarray"] = df["mzarray"].apply(
#     lambda x: np.array([np.mean(part) for part in np.array_split(x, 50)])
# )

# df["intarray"] = df["intarray"].apply(
#     lambda x: np.array([np.mean(part) for part in np.array_split(x, 50)])
# )

step_size = round(df.shape[0] / 200)
df = df.iloc[
    ::step_size,
]
# df["RT"] = df["RT"].apply(
#     lambda x: np.array([np.mean(part) for part in np.array_split(x, 20)])
# )

fig = plot_2D_map(df)
st.plotly_chart(fig)
