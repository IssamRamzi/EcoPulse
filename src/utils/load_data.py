import pandas as pd
from .globals import *

class DataLoader:
    def __init__(self):
        self._electricity_dataframe : pd.DataFrame = None
        self._pollution_dataframe : pd.DataFrame = None

    def loadElectricityData(self):
        df = pd.read_csv(os.path.join(DATA_CLEANED_DIR, "elec_production.csv"))
        df['Date'] = pd.to_datetime(df['Date'])
        df['Value'] = pd.to_numeric(df['Value'], errors='coerce')
        self._electricity_dataframe = df
        return df
    
    def getElectricityData(self):
        return self._electricity_dataframe
    
    def loadPollutionData(self):
        df = pd.read_csv(os.path.join(DATA_CLEANED_DIR, "air_pollution.csv"))

        aqi_num_cols = [col for col in df.columns if 'AQI Value' in col ]
        for col in aqi_num_cols:
            df[col] = pd.to_numeric(df[col], errors='coerce')
        

        self._pollution_dataframe = df
        return df
    
    def getPollutionData(self):
        return self._pollution_dataframe
    
data_loader = DataLoader()
