import dash
from dash import html, dcc, callback, Input, Output
import plotly.express as px
import plotly.graph_objects as go
import dash_bootstrap_components as dbc
import pandas as pd
import random
from src.utils import *
from src.components.cards import create_chart_card
from src.components.filters import create_country_filter, create_city_filter
from src.components.pollution_ui import create_page_header, pollution_callbacks


dash.register_page(__name__, path='/pollution', name='Air Quality Analytics Page')

df = data_loader.getPollutionData()

countries = sorted(df["Country"].dropna().unique().tolist())
random_country = random.choice(countries)


print(random_country)


# header
page_header = create_page_header()
# section
filters_section = dbc.Card([
    dbc.CardBody([
        html.H5([
            html.I(className="fas fa-filter me-2"),
            "Location Selection"
        ], className="mb-3 fw-bold"),
        dbc.Row([
            create_country_filter(
                'pollution_dropdown_country',
                countries,
                random_country,
                "Select Country"
            ),
            create_city_filter(
                'pollution_dropdown_city',
                "Select City"
            )
        ])
    ])
], className="shadow-sm border-0 mb-4")

# Metrics row
metrics_row = dbc.Row(id='pollution_metrics', className="mb-4")

# Charts section
charts_section = html.Div([
    dbc.Row([
        dbc.Col([
            create_chart_card(
                "Pollutant Breakdown",
                'pollution_histogram',
                "Individual AQI values for each pollutant"
            )
        ], width=12)
    ]),
    
    dbc.Row([
        dbc.Col([
            create_chart_card(
                "Global Air Quality Map",
                'pollution_map',
                "Average AQI by country - Interactive globe view"
            )
        ], width=12)
    ])
])

# Main layout
layout = dbc.Container(fluid=True, children=[
    page_header,
    filters_section,
    metrics_row,
    charts_section
])





pollution_callbacks(df)
