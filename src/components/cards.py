import dash_bootstrap_components as dbc
from dash import html, dcc


def create_metric_card(title, value, subtitle=None, icon=None, color="primary"):
    
    card_content = [
        dbc.CardBody([
            html.Div([
                html.I(className=f"{icon} fa-2x mb-2", style={"color": f"var(--bs-{color})"}) if icon else None,
                html.H6(title, className="text-muted text-uppercase mb-2"),
                html.H2(value, className="mb-0 fw-bold"),
                html.P(subtitle, className="text-muted small mb-0") if subtitle else None
            ])
        ])
    ]
    
    return dbc.Card(
        card_content,
        className="shadow-sm border-0 h-100",
        style={"borderLeft": f"4px solid var(--bs-{color})"}
    )


def create_chart_card(title, chart_id, subtitle=None, tools=None):
    
    header_content = [
        html.H4(title, className="mb-0 fw-bold fg-red"),
    ]
    
    if subtitle:
        header_content.append(
            html.P(subtitle, className="text-muted small mb-0 mt-1")
        )
    
    card_components = [
        dbc.CardHeader(
            html.Div(header_content),
            className="bg-white border-bottom"
        )
    ]
    
    if tools:
        card_components.append(
            dbc.CardBody(
                html.Div(tools, className="mb-3"),
                className="bg-light border-bottom py-3"
            )
        )
    
    card_components.append(
        dbc.CardBody([
            dcc.Graph(id=chart_id, config={'displayModeBar': False})
        ])
    )
    
    return dbc.Card(
        card_components,
        className="shadow-sm border-0 mb-4"
    )


def create_filter_card(filters):
   
    return dbc.Card([
        dbc.CardBody([
            html.H5("Filters", className="mb-3 fw-bold"),
            html.Div(filters)
        ])
    ], className="shadow-sm border-0 mb-4")