from globals import *
import pandas as pd
import os
import time 


def clean_electricity_dataset():
    df = pd.read_csv(os.path.join(DATA_RAW_DIR,"global_electricity_production_data.csv"))
    df = df.rename(columns={"country_name": 'Country', 'date': "Date", "parameter": "Parameter", 'product' : "Type", 'value': 'Value', 'unit' : 'Unit'})
    df = replace_countries_names(df)

    df['Value'] = pd.to_numeric(df['Value'], errors='coerce')
    df = df.dropna(subset=['Value'])

    df['Date'] = pd.to_datetime(df['Date'], errors='coerce')

    df = df.sort_values(['Country', 'Date'], ascending=True)

    df.to_csv(os.path.join(DATA_CLEANED_DIR, "elec_production.csv"), index=False)

def clean_pollution_dataset():
    df = pd.read_csv(os.path.join(DATA_RAW_DIR, "global_air_pollution_dataset.csv"))
    replace_countries_names(df)

    aqi_num_cols = [col for col in df.columns if 'AQI Value' in col ]
    for col in aqi_num_cols:
        df[col] = pd.to_numeric(df[col], errors='coerce')

    df = df.dropna(subset=['AQI Value'])
    df = df.sort_values(['Country', 'City'], ascending=True)
    df.to_csv(os.path.join(DATA_CLEANED_DIR, "air_pollution.csv"), index=False)




def replace_countries_names(df : pd.DataFrame):
    country_mapping = {
        "United Kingdom": 'UK',
        "United Kingdom of Great Britain and Northern Ireland": 'UK',

        "United States of America": 'USA',
        "United States": 'USA',


        # https://community.plotly.com/t/choropleth-maps-crimea-annexation-by-russia/85281
        'Czech Republic': 'Czechia',
        'Russia': 'Russian Federation'
    }
    df['Country'] = df['Country'].replace(country_mapping)
    return df

if __name__ == "__main__":
    start = time.time()
    clean_electricity_dataset()
    clean_pollution_dataset()
    print(f"Data Cleaned in {time.time() - start}s")
