import streamlit as st
import plotly.express as px
import pandas as pd

from PIL import Image
from datetime import datetime, date
from typing import List
from infrastructure import datahandler, forecastinghandler
from utils import util

# ============================================================
# Data Ingestion
# ============================================================
data: pd.DataFrame = datahandler.load_base_data()
data.columns: List[str] = ['time_index', 'n_p'] + list(util.MAPPING.keys()) 

criterion: List = util.MAPPING.keys()
dates: List[str] = data['time_index'].astype(str).unique().tolist()
posts: List[str] = data['n_p'].unique().tolist()

data_scaled: pd.DataFrame = datahandler.scale_data(data)


# ============================================================
# Mobility Details
# ============================================================
st.set_page_config(page_title="Continental_AA&AI", layout="wide")
st.markdown('## Mobility Indicator Details')

st.write('The composed mobility indicator was built resorting to the Principal Component Analysis (PCA), \
         algorithm, summarizing the trend of multiple observations over time. This dashboard provides \
         an overview on how this value was calculated by the AI method.'
)

#st.markdown('#### Configuration')
with st.expander("Dashboard Configuration"):
        # 1. filter by post
        post: str = st.radio('Select post', util.POSTS.keys(), horizontal=True)
        data_scaled: pd.DataFrame = data_scaled[data['n_p'] == util.POSTS[post]]
        
        # 2. select which series to display
        series: List[str] = st.multiselect('Select series', criterion, default=['Mobility Indicator', 'Nº of Light Vehicles', 'Speed of Light Vehicles (km/h)'])

        #date: str = st.select_slider('Select a specific date and time to inspect', options=dates, value=('2022-09-20 00:00:00', '2022-09-20 23:45:00'))
        default_first_date: datetime = datetime(2022, 9, 20)
        first_date: date = st.date_input("1st Date", default_first_date)
        first_date: datetime = datetime(first_date.year, first_date.month, first_date.day)
        
        default_second_date: datetime = datetime(2022, 9, 21)
        second_date: date = st.date_input("2nd Date", default_second_date)
        second_date: datetime = datetime(second_date.year, second_date.month, second_date.day)
        
        if first_date >= second_date:
                st.error("Error: 2nd Date should always be posterior to 1st Date.")
                data_scaled: pd.DataFrame = data_scaled[(data_scaled['time_index'] >= default_first_date) & (data_scaled['time_index'] <= default_second_date)]
        else:
                data_scaled: pd.DataFrame = data_scaled[(data_scaled['time_index'] >= first_date) & (data_scaled['time_index'] <= second_date)]

#smoothing
forecast_smt: pd.DataFrame = forecastinghandler.smooth(data_scaled, series)
# line plot
data_scaled['Time']: pd.Series = data['time_index']
fig = px.line(data_scaled, x="Time", y=series, title='Mobility Factors Over Time for ' + post)
fig.update_layout(legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1))
st.plotly_chart(fig, use_container_width=True)

col1, col2, col3 = st.columns([0.15, 0.7, 0.15])

with col1:
        st.write(' ')
with col2:
        with st.expander("See Explanation", expanded=True):
                image = Image.open('databases/plots/global_mobility_shap_plot.png')
                st.image(image, caption='AI explains the main driving factors of mobility across different ares of the city.')
with col3:
        st.write(' ')
