import dash
from dash import html, dcc
import dash_bootstrap_components as dbc
import pandas as pd
from src.utils import data_loader
from src.components.cards import create_metric_card, create_chart_card

dash.register_page(__name__, path='/', name='Home')

df_poll = data_loader.getPollutionData()
df_elec = data_loader.getElectricityData()


def layout():
    return dbc.Container(fluid=True, children=[
        # Hero Section
        "Home"
    ])