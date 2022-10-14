import streamlit as st
import plotly.express as px
import pandas as pd

from PIL import Image
from typing import List
from infrastructure import datahandler, forecastinghandler
from utils import util


# ============================================================
# Data Ingestion
# ============================================================
data: pd.DataFrame = datahandler.load_base_data()

posts: List[str] = data['n_p'].unique().tolist()


# ============================================================
# Mobility Forecasting
# ============================================================
st.set_page_config(page_title="Continental_AA&AI", layout="wide")
st.markdown('## Mobility Forecasting')

st.write('This page provides a mobility forecasting service powered by Machine Learning that uses past observations \
        along with weather conditions to predict the indicator values for the next day.'
)

# select forecasting parameters
post: str = st.radio('Select post', util.POSTS.keys(), horizontal=True)
#days = st.number_input('Number of days', min_value=1, max_value=7)

# compute forecast
forecast: pd.DataFrame = forecastinghandler.forecast(util.POSTS[post], n_days=2)
forecast_smt: pd.DataFrame = forecastinghandler.smooth(forecast, ['Mobility Indicator'])

# line plot
fig = px.line(forecast, x='Time', y='Mobility Indicator', title='Mobility Forecast')
st.plotly_chart(fig, use_container_width=True)


col1, col2, col3 = st.columns([0.15, 0.7, 0.15])

with col1:
        st.write(' ')
with col2:
        with st.expander("See Explanation", expanded=True):
                image = Image.open('databases/plots/local_mobility_shap_plot_{}.png'.format(util.POSTS[post]))
                st.image(image, caption='AI explains the main driving factors of mobility for ' + post + '.')
with col3:
        st.write(' ')
