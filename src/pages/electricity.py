import dash
from dash import html, dcc
import plotly.graph_objects as go
from src.utils import *
import dash_bootstrap_components as dbc
from src.components.cards import create_chart_card, create_metric_card
from src.components.filters import create_country_filter, create_year_filter
from src.components.electricity_ui import create_page_header, create_filter_section, elec_callbacks
import random

dash.register_page(__name__, path='/electricity', name='Electricity Analytics Page')

df = data_loader.getElectricityData()
df['Year'] = pd.to_datetime(df['Date']).dt.year

countries = df["Country"].unique().tolist()
years = sorted(df["Year"].unique())
random_country = random.choice(countries)

# header
page_header = create_page_header()

# filters
filters_section = create_filter_section(countries, random_country)

metrics_row = dbc.Row(id='electricity_metrics', className="mb-4")


charts_section = html.Div([

    dbc.Row([
        dbc.Col(
            create_chart_card(
                "Energy Mix Analysis",
                "electricity_histogram",
                "Breakdown of electricity production by energy source"
            ),
            width=12
        )
    ], className="mb-4"),

    dbc.Row([
        dbc.Col(
            create_chart_card(
                "Renewable Electricity Share (%)",
                "renewable_share_histogram",
                "Share of renewable electricity production over time"
            ),
            width=12
        )
    ], className="mb-4"),

    dbc.Row([
        dbc.Col(
            create_chart_card(
                "Global Electricity Production",
                "electricity_map",
                "Total electricity production by country"
            ),
            width=12
        )
    ])

])

# Main layout
layout = dbc.Container(fluid=True, children=[
    page_header,
    filters_section,
    metrics_row,
    charts_section
])


elec_callbacks(df)