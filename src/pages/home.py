import dash
from dash import html, dcc
import dash_bootstrap_components as dbc

dash.register_page(__name__, path='/', name='Home')

layout = dbc.Container([
    # hero
    dbc.Row([
        dbc.Col([
            html.Div([
                html.H1("L'Équilibre Planétaire", className="display-4 fw-bold mb-3"),
                html.P(
                    "Explorez la relation complexe entre notre production d'électricité et la pureté de l'air que nous respirons.",
                    className="lead text-muted mb-4"
                ),
                html.Div([
                    dbc.Button("Analyser l'Énergie", href="/electricity", color="warning", className="me-3 px-4 shadow"),
                    dbc.Button("Surveiller la Pollution", href="/pollution", color="success", className="px-4 shadow"),
                ])
            ], className="py-5 text-center bg-light rounded-3 shadow-sm border")
        ])
    ], className="my-5"),

    # elec prod carte
    dbc.Row([
        dbc.Col(dbc.Card([
            dbc.CardBody([
                html.Div(html.I(className="fas fa-bolt fa-3x text-warning mb-3")),
                html.H4("Production d'Énergie", className="fw-bold"),
                html.P("Le moteur de notre économie. Découvrez quels pays mènent la transition vers le renouvelable."),
                dbc.Button("Voir le Mix Énergétique", href="/electricity", color="link", className="p-0")
            ])
        ], className="h-100 text-center border-0 shadow-sm"), md=6),
        
        # poll carte
        dbc.Col(dbc.Card([
            dbc.CardBody([
                html.Div(html.I(className="fas fa-smog fa-3x text-secondary mb-3")),
                html.H4("Qualité de l'Air", className="fw-bold"),
                html.P("Le miroir de nos choix énergétiques. Visualisez l'impact direct des polluants sur la santé publique."),
                dbc.Button("Analyser l'AQI", href="/pollution", color="link", className="p-0")
            ])
        ], className="h-100 text-center border-0 shadow-sm"), md=6),
    ], className="mb-5"),

    dbc.Row([
        dbc.Col([
            html.Div([
                html.H3("💡 Le saviez-vous ?", className="fw-bold"),
                html.P([
                    "Plus de ", html.B("60% de la production mondiale d'électricité"), 
                    " provient encore de combustibles fossiles, ce qui représente la source principale de NO2 et de CO mesurés dans notre section Pollution."
                ], className="mb-0")
            ], className="p-4 border-start border-4 border-primary bg-white shadow-sm")
        ])
    ], className="mb-5")
], fluid=True, className="px-5")