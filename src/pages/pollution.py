import dash
from dash import html, dcc, callback, Input, Output
import plotly.express as px
import dash_bootstrap_components as dbc
import pandas as pd
import random
from src.utils import *


dash.register_page(__name__, path='/pollution')


df = data_loader.getPollutionData()

countries = sorted(df["Country"].dropna().unique().tolist())
random_country = random.choice(countries)

POLLUTANTS_MAP = {
    "CO AQI Value": "Monoxyde de Carbone (CO)",
    "Ozone AQI Value": "Ozone (O3)",
    "NO2 AQI Value": "Dioxyde d'Azote (NO2)",
    "PM2.5 AQI Value": "Particules Fines (PM2.5)"
}

layout = dbc.Container(fluid=True, children=[
    
    dbc.Row(dbc.Col(
        html.H1("Air Quality Analytics Page", className='text-center my-4'), 
        width=12
    )),

    dbc.Card(className="mb-4 p-3", children=[
        dbc.Row([
            dbc.Col([
                html.Label("Sélectionnez un Pays :", className='fw-bold'),
                dcc.Dropdown(
                    options=[{"label": c, "value": c} for c in countries],
                    value=random_country,
                    id='pollution_dropdown_country'
                )
            ], md=6),

            dbc.Col([
                html.Label("Sélectionnez une Ville :", className='fw-bold'),
                dcc.Dropdown(
                    id='pollution_dropdown_city'
                )
            ], md=6)
        ]),
    ]),

    dbc.Row(className="mb-4", children=[
        dbc.Col(
            dbc.Card(children=[
                dbc.CardHeader(html.H4("Répartition des Polluants par Ville", className="mb-0")),
                dbc.CardBody(dcc.Graph(id='pollution_histogram'))
            ]),
            width=12
        )
    ]),

    dbc.Row(children=[
        dbc.Col(
            dbc.Card(children=[
                dbc.CardHeader(html.H4("Qualité de l'Air Moyenne par Pays (AQI)")),
                dbc.CardBody(dcc.Graph(id='pollution_map'))
            ]),
            width=12,
        )
    ])
])

# callback pour mettre à jour la liste des villes selon le pays
@callback(
    Output('pollution_dropdown_city', 'options'),
    Output('pollution_dropdown_city', 'value'),
    Input('pollution_dropdown_country', 'value')
)
def update_city_dropdown(selected_country):
    if not selected_country:
        return [], None
    cities = sorted(df[df["Country"] == selected_country]["City"].unique())
    options = [{"label": c, "value": c} for c in cities]
    value = cities[0] if cities else None
    return options, value

# callback pour l'histogramme des polluants
@callback(
    Output('pollution_histogram', 'figure'),
    Input('pollution_dropdown_country', 'value'),
    Input('pollution_dropdown_city', 'value')
)
def update_pollution_histogram(selected_country, selected_city):
    if not selected_city:
        return {}

    # Extraction des données de la ville sélectionnée
    city_row = df[(df["Country"] == selected_country) & (df["City"] == selected_city)].iloc[0]
    
    overall_aqi = city_row["AQI Value"]
    aqi_category = city_row["AQI Category"]

    # Transformation des colonnes en lignes pour le bar chart
    plot_data = []
    for col, label in POLLUTANTS_MAP.items():
        plot_data.append({"Polluant": label, "Valeur AQI": city_row[col]})
    
    df_plot = pd.DataFrame(plot_data)

    # Création du graphique
    fig = px.bar(
        df_plot,
        x="Polluant",
        y="Valeur AQI",
        color="Polluant",
        text="Valeur AQI",
        title=f"Statut à {selected_city} : {aqi_category} (Indice Global : {overall_aqi})",
        labels={"Valeur AQI": "Indice AQI spécifique", "Polluant": "Type de Polluant"},
        color_discrete_sequence=px.colors.qualitative.Vivid
    )
    
    # Ajout de lignes de seuil pour la santé
    fig.add_hline(y=50, line_dash="dot", line_color="green", annotation_text="Sain (0-50)")
    fig.add_hline(y=100, line_dash="dot", line_color="orange", annotation_text="Modéré (51-100)")
    
    fig.update_layout(showlegend=False)
    return fig

# callback pour la carte mondiale
@callback(
    Output('pollution_map', 'figure'),
    Input('pollution_dropdown_country', 'value')
)
def update_pollution_map(_):
    country_aqi = df.groupby("Country")["AQI Value"].mean().reset_index()

    fig = px.choropleth(
    country_aqi,
    locations="Country",
    locationmode="country names",
    color="AQI Value",
    color_continuous_scale="YlOrRd",
    projection="orthographic",  # 🌍 globe effect
    title="Average Air Pollution by Country (Globe View)",
    labels={"AQI Value": "Average AQI"}
    )

    fig.update_geos(
        showcountries=True,
        showcoastlines=True,
        showocean=True,
        oceancolor="LightBlue",
        showland=True,
        landcolor="rgb(0, 60, 10)",
    )
    
    fig.update_layout(margin=dict(l=0, r=0, t=40, b=0))
    return fig