import dash
from dash import html, dcc, callback, Input, Output
import plotly.express as px
from src.utils import *

dash.register_page(__name__, path='/')

layout = html.Div(
    children=[
        "Home Page"
    ]
)


