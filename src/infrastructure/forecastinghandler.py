import os
import json
import requests
import pandas as pd
import numpy as np

from requests.models import Response
from datetime import date, datetime, timedelta
from random import randint
from lightgbm import Booster
from typing import List, Dict
from utils import util

CREDENTIALS_PATH: str = 'cfg/api.json'
MODEL_PATH: str = 'databases/models/'
REQUEST: str = 'https://api.openweathermap.org/data/3.0/onecall?lat=40.6347&lon=-8.66038&exclude=alerts,daily,minutely,current&appid={}'

def round_date(dt: datetime) -> datetime:
    return dt.replace(second=0, microsecond=0, minute=0, hour=dt.hour) + timedelta(hours=dt.minute // 30)

def add_weather_features(data: pd.DataFrame) -> pd.DataFrame:
    
    # fetch weather data for next 48 hours
    with open(CREDENTIALS_PATH) as f:
        credentials: Dict = json.load(f)
        
    resp: Response = requests.get(REQUEST.format(credentials['key']))
    weather: Dict = resp.json()
    weather: List = [
        {
            'time_index': datetime.fromtimestamp(hour['dt']),
            'temperature': float(hour['temp']) - 272.15,
            'humidity': float(hour['humidity']),
            'precipitation': float(hour['pop'])
        }
        for hour in weather['hourly']
    ]
    weather: pd.DataFrame = pd.DataFrame(weather)
    weather: pd.DataFrame = weather.set_index('time_index')

    # filter records that don't match weather API
    data['exists']: pd.Series = data['time_index'].apply(lambda x: round_date(x) in weather.index)
    data: pd.DataFrame = data[data['exists'] == True]
    data: pd.DataFrame = data.drop(['exists'], axis=1)
    
    data["temperature"]: pd.Series =  data["time_index"].apply(lambda x: weather.temperature.loc[round_date(x)])
    data["humidity"]: pd.Series = data["time_index"].apply(lambda x: weather.humidity.loc[round_date(x)])
    data["precipitation"]:pd.Series = data["time_index"].apply(lambda x: weather.precipitation.loc[round_date(x)])
    return data

def add_time_features(data: pd.DataFrame) -> pd.DataFrame:
    data['weekday']: pd.DataFrame = data['time_index'].dt.weekday
    data["hour"]: pd.DataFrame = data["time_index"].dt.hour
    data["minute"]: pd.DataFrame = data["time_index"].dt.minute
    return data

def preprocess(data: pd.DataFrame) -> pd.DataFrame:
    data: pd.DataFrame = data.set_index('time_index')
    data: pd.DataFrame = pd.get_dummies(data, columns=['weekday', 'hour', 'minute'])

    final_cols: List[str] = [util.FORECASTING_FEATURE_MAPPING[c] for c in data.columns]
    data.columns: List[str] = final_cols
    
    # at this point dataset features don't match train, need to add remaining columns as 0 and re-order them to train order
    missing_cols: List[str] = [val for val in util.FORECASTING_FEATURE_MAPPING.values() if val not in data.columns]
    for missing_col in missing_cols:
        data[missing_col]: pd.Series = 0
        
    data: pd.DataFrame = data[final_cols + missing_cols]
    
    # re-order columns
    return data

def forecast(post: str, n_days: int= 1) -> pd.DataFrame:
    # load local regression model based on path
    fname: str = 'local_mobility_regressor_' + post + '.txt'
    fpath: str = os.path.join(MODEL_PATH, fname)
    clf: Booster = Booster(model_file=fpath)
    
    # create base dataframe for time range
    now_date: datetime = datetime.today() + timedelta(hours=1)
    initial_date: datetime = round_date(now_date)

    # round to nearest date in the future
    if initial_date < now_date:
        initial_date: datetime = initial_date + timedelta(hours=1)

    end_date: datetime = initial_date + timedelta(days=n_days)
    end_date: datetime = datetime(end_date.year, end_date.month, end_date.day)
    
    data: pd.DataFrame = pd.date_range(initial_date, end_date, freq='15min').to_frame()
    data.columns: List[str] = ['time_index']

    # feature engineering
    data: pd.DataFrame = add_weather_features(data)
    data: pd.DataFrame = add_time_features(data)
    
    # preprocess
    data: pd.DataFrame = preprocess(data)
    
    # predict 
    y_pred: np.ndarray = clf.predict(data)
    
    # append results
    data['Mobility Indicator']: pd.Series = y_pred
    data: pd.DataFrame = data.reset_index()
    data['Time']: pd.Series = data['time_index']
    
    return data

def smooth(data: pd.DataFrame, column: List) -> pd.DataFrame:
    data[column] = data[column].rolling(4).sum()
    data = data.dropna()
    return data
