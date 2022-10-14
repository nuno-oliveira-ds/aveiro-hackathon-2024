from typing import Dict, List

# ============================================================
# CONSTANTS
# ============================================================

MAPPING: Dict = {
    'Mobility Indicator': {'alias': 'indicator'},
    'Nº of People': {'alias': 'class_count'},
    'Nº of Light Vehicles': {'alias': 'vehiclelight'}, 
    'Speed of Light Vehicles (km/h)': {'alias': 'speedlight'}, 
    'Nº of Heavy Vehicles': {'alias': 'vehicleheavy'}, 
    'Speed of Heavy Vehicles (km/h)': {'alias': 'speedheavy'}, 
    'Nº of Others': {'alias': 'vehicleothers'}, 
    'Speed of Others (km/h)': {'alias': 'speedothers'}, 
}

OTHER_COLS: List[str] = {
    'temperature': 'temperature',
    'humidity': 'humidity',
    'precipitation': 'precipitation',
}

POSTS: List[str] = {
    'Instituto de Telecomunicações (p1)': 'p1',
    'Ponte Dobadoura (p3)': 'p3',
    'ISCA-UA (p35)': 'p35'
}

WEEKDAYS: List[str] = {
    'weekday_0': 'Monday',
    'weekday_1': 'Tuesday',
    'weekday_2': 'Wednesday',
    'weekday_3': 'Thursday',
    'weekday_4': 'Friday',
    'weekday_5': 'Saturday',
    'weekday_6': 'Sunday'
}

HOURS: List[str] = {'hour_{}'.format(h): '{:02d}h'.format(h) for h in range(0, 24)}
MINUTES: List[str] = {'minute_{}'.format(m): '{:02d}m'.format(m) for m in range(0, 60, 15)}

FORECASTING_FEATURE_MAPPING: Dict = {}
FORECASTING_FEATURE_MAPPING.update(OTHER_COLS)
FORECASTING_FEATURE_MAPPING.update(WEEKDAYS)
FORECASTING_FEATURE_MAPPING.update(HOURS)
FORECASTING_FEATURE_MAPPING.update(MINUTES)