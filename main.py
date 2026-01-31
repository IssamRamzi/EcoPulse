from src.utils import *
import os
import dash
from dash import Dash, html, dcc
import dash_ag_grid as dag
import pandas as pd
import plotly.express as px

import dash_bootstrap_components as bsp

from src.components.header import create_header


data_loader.loadElectricityData()
data_loader.loadPollutionData()

application = Dash(__name__, use_pages=True, pages_folder="./src/pages/", external_stylesheets=[bsp.themes.MATERIA])

# Mes dataframes
elect_prod = pd.read_csv(os.path.join(DATA_CLEANED_DIR, "elec_production.csv"))

# Layout de la page web
application.layout = html.Div(children=[
    create_header(),
    dash.page_container,

])
    
if __name__ == "__main__":
    application.run(debug=True)
