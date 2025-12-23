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

application = Dash(__name__, use_pages=True, pages_folder="./src/pages/", external_stylesheets=[bsp.themes.CYBORG])

# Mes dataframes
elect_prod = pd.read_csv(os.path.join(DATA_CLEANED_DIR, "elec_production.csv"))
print(len(elect_prod['Country'].unique()))

# Layout de la page web
application.layout = html.Div(children=[
    create_header(),
    # Navigation
    # html.Div([
    #     html.Div([
    #         dcc.Link(page["name"], href=page["relative_path"])
    #         for page in dash.page_registry.values()
    #     ])
    # ]),

    dash.page_container,

    # dag.AgGrid(
    #     rowData=elect_prod.to_dict("records"),
    #     columnDefs=[{"field": col} for col in elect_prod.columns],
    #     defaultColDef={"sortable": True, "filter": True, "resizable": True},
    #     style={"height": "500px", "width": "100%"}
    # ),

    # dcc.Graph(
    #     figure=px.histogram(
    #         elect_prod,
    #         x="Country",
    #         y="Value",
    #         histfunc="avg",
    #         title="Average Electricity Production per Country"
    #     )
    # ),
])
    
if __name__ == "__main__":
    application.run(debug=True)
