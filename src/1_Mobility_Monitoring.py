import streamlit as st
import numpy as np
import pydeck as pdk
import pandas as pd

from typing import List, Dict
from infrastructure import datahandler
from utils import util


# ============================================================
# Data Ingestion
# ============================================================
data: pd.DataFrame = datahandler.get_geo_data()

criterion: List[str] = util.MAPPING.keys()
dates: List[str] = data['time_index'].unique().tolist()
midpoint = (np.average(data['lat']), np.average(data['lon']))


# ============================================================
# Mobility Monitoring
# ============================================================
st.set_page_config(page_title="Continental_AA&AI", layout="wide")

st.markdown('## Mobility Monitoring')

st.write('Through the following map it is possible to inspect the mobility within \
        different areas of the city of Aveiro. Mobility can be measured in different ways. \
        Therefore, we computed a single comprehensive indicator that comprises several factors such as \
        the number of people observed in the streets as well as the count and \
        average velocity of vehicles.'
)

with st.expander("Dashboard Configuration"):
    # 1. adjust display for criteria
    criteria: str = st.radio('Select a criteria', criterion, horizontal=True)

    numeric_cols: List[str] = data.select_dtypes(include=['float', 'int']).columns.to_list()
    temp: pd.DataFrame = data[data[numeric_cols] > 0]
    quantiles: pd.DataFrame = temp.quantile([0.25, 0.75])

    selected_col: str = util.MAPPING[criteria]['alias']

    r: str = "{} >= {} ? 255 : 0".format(
        selected_col,
        quantiles.loc[0.25][selected_col]
    )
    g: str = "{} <= {} ? 255 : 0".format(
        selected_col,
        quantiles.loc[0.75][selected_col]
    )
    b: str = "0"

    # select subset of data to be displayed dependening on selection
    date: str = st.select_slider('Select a specific date and time to inspect', options=dates, value='2022-09-20 17:00:00')
    df: pd.DataFrame = data[data['time_index'] == date]

st.pydeck_chart(pdk.Deck(
        map_style='road',
        initial_view_state=pdk.ViewState(
            latitude= midpoint[0],
            longitude=  midpoint[1],
            zoom= 14,
            #pitch=50,
        ),
        layers=[
            pdk.Layer(
                'ScatterplotLayer',
                data=df,
                get_position='[lon, lat]',
                get_fill_color=[
                    r,
                    g,
                    b,
                    "140"
                ],
                auto_highlight=True,
                get_radius=250, # in meters
                pickable=True
            ),
            pdk.Layer(
                'TextLayer',
                data=df,
                get_position='[lon, lat]',
                get_text='n_p',
                get_size=18,
                get_text_anchor='"middle"',
                get_alignment_baseline='"center"'
            )
        ]
    )
)
