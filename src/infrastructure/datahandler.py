import pandas as pd

from sklearn.preprocessing import MinMaxScaler
from typing import List

SOURCE: str = 'databases/indicator.parquet'

def load_base_data() -> pd.DataFrame:
    data: pd.DataFrame = pd.read_parquet(SOURCE)
    data: pd.DataFrame = data.reset_index()
    data['time_index']: pd.Series = data['time_index'].dt.tz_localize(None)
    return data
    

def get_geo_data() -> pd.DataFrame:
    data: pd.DataFrame = load_base_data()
    data['time_index']: pd.Series = data['time_index'].astype(str)
    
    data['lat']: pd.DataFrame = data['n_p'].apply(
        lambda x: 40.63476 if x == 'p1' 
        else 40.64074 if x == 'p3' 
        else 40.63028
    )
    data['lon']: pd.DataFrame = data['n_p'].apply(
        lambda x: -8.66038 if x == 'p1' 
        else -8.65705 if x == 'p3' 
        else -8.65423
    )
    
    return data

def scale_data(data: pd.DataFrame) -> pd.DataFrame:
    numeric_cols: List[str] = data.select_dtypes(include=['float', 'int']).columns.to_list()
    temp: pd.DataFrame = data[numeric_cols]
    
    data_scaled: pd.DataFrame = pd.DataFrame(MinMaxScaler().fit_transform(temp))
    data_scaled['time_index']: pd.Series = data['time_index']
    data_scaled['n_p']: pd.Series = data['n_p']
    
    column_names: List[str] = numeric_cols + ['time_index', 'n_p']
    data_scaled.columns: List[str] = column_names
    return data_scaled