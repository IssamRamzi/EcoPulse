import dash_bootstrap_components as dbc
from dash import html, dcc


def create_country_filter(dropdown_id, countries, default_value=None, label="Select a Country"):
    return dbc.Col([
        html.Label(label, className='fw-bold mb-2'),
        dcc.Dropdown(
            options=[{"label": c, "value": c} for c in countries],
            value=default_value,
            id=dropdown_id,
            className="shadow-sm"
        )
    ], md=6, className="mb-3")


def create_year_filter(dropdown_id, label="Select a Year"):
    
    return dbc.Col([
        html.Label(label, className='fw-bold mb-2'),
        dcc.Dropdown(
            options=[],
            id=dropdown_id,
            className="shadow-sm"
        )
    ], md=6, className="mb-3")


def create_city_filter(dropdown_id, label="Select a City"):
    
    return dbc.Col([
        html.Label(label, className='fw-bold mb-2'),
        dcc.Dropdown(
            id=dropdown_id,
            className="shadow-sm"
        )
    ], md=6, className="mb-3")


def create_date_range_picker(start_id, end_id, label="Date Range"):
    
    return dbc.Col([
        html.Label(label, className='fw-bold mb-2'),
        dbc.Row([
            dbc.Col([
                dcc.DatePickerSingle(
                    id=start_id,
                    className="w-100"
                )
            ], width=6),
            dbc.Col([
                dcc.DatePickerSingle(
                    id=end_id,
                    className="w-100"
                )
            ], width=6)
        ])
    ], md=6, className="mb-3")