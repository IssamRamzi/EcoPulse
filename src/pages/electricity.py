import dash
from dash import html, dcc, callback, Input, Output
import plotly.express as px
from src.utils import *
import dash_bootstrap_components as dbc

import random

dash.register_page(__name__, path='/electricity')

df = data_loader.getElectricityData()

# Ajout d'une colonne Year
df['Year'] = pd.to_datetime(df['Date']).dt.year

countries = df["Country"].unique().tolist()
years = sorted(df["Year"].unique())

random_country = random.choice(countries)

layout = dbc.Container(fluid=True, children=[
    
    dbc.Row(dbc.Col(
        html.H1("Electricity Analytics Page", className='text-center my-4'), 
        width=12
    )),

    dbc.Card(className="mb-4 p-3", children=[
        dbc.Row([
            dbc.Col([
                html.Label("Select a Country:", className='fw-bold'),
                dcc.Dropdown(
                    options=[{"label": c, "value": c} for c in countries],
                    value=random_country,
                    id='analytics_dropdown_country'
                )
            ], md=6),

            dbc.Col([
                html.Label("Select a Year:", className='fw-bold'),
                dcc.Dropdown(
                    options=[],
                    id='analytics_dropdown_year'
                )
            ], md=6)
        ]),
    ]),

    dbc.Row(className="mb-4", children=[
        dbc.Col(
            dbc.Card(children=[
                dbc.CardHeader(html.H4("Mix Énergétique par Année et Pays", className="mb-0")),
                dbc.CardBody(dcc.Graph(id='electricity_histogram'))
            ]),
            width=12
        )
    ]),

    dbc.Row(children=[
        dbc.Col(
            dbc.Card(children=[
                dbc.CardHeader(html.H4("Production Totale Mondiale")),
                dbc.CardBody(dcc.Graph(id='electricity_map'))
            ]),
            width=12
        )
    ])
])


@callback(
    Output('analytics_dropdown_year', 'options'),
    Output('analytics_dropdown_year', 'value'),
    Input('analytics_dropdown_country', 'value')
)
def update_year_dropdown(selected_country):
    filtered_df = df[df["Country"] == selected_country]
    years_available = sorted(filtered_df["Year"].unique())
    options = [{"label": y, "value": y} for y in years_available]
    value = years_available[0] if years_available else None
    return options, value


@callback(
    Output('electricity_histogram', 'figure'),
    Input('analytics_dropdown_country', 'value'),
    Input('analytics_dropdown_year', 'value')
)
def update_histogram(selected_country, selected_year):
    if not selected_country or not selected_year:
        return {}
        
    RENEWABLES = ["Hydro", "Wind", "Solar", "Geothermal", "Combustible Renewables", "Other Renewables", "Total Renewables (Hydro, Geo, Solar, Wind, Other)"]
    TOTAL_NET_PRODUCT = 'Electricity' 
    TOTAL_RENEWABLES_LINE = "Total Renewables (Hydro, Geo, Solar, Wind, Other)"

    filtered_df = df[
        (df["Country"] == selected_country) &
        (df["Year"] == selected_year) &
        (df["Parameter"] == "Net Electricity Production")
    ]
    
    # 1. Calcul de la Production Totale Nette (Dénominateur)
    total_net_prod_series = filtered_df[filtered_df["Type"] == TOTAL_NET_PRODUCT]["Value"]
    total_net_prod = total_net_prod_series.iloc[0] if not total_net_prod_series.empty else 0

    # 2. Calcul de la Production Renouvelable (Numérateur)
    total_re_prod = filtered_df[filtered_df["Type"].isin(RENEWABLES)]["Value"].sum()
        
    # 3. Calcul du Pourcentage Final
    if total_net_prod > 0:
        re_share_percent = round((total_re_prod / total_net_prod) * 100, 1)
    else:
        re_share_percent = 0
        
    # 4. Ajuster le DF pour l'histogramme (Exclure les lignes totales)
    types_to_exclude = [TOTAL_NET_PRODUCT, TOTAL_RENEWABLES_LINE]
    filtered_df_hist = filtered_df[~filtered_df["Type"].isin(types_to_exclude)]

    # 5. Création du Titre avec le % RE
    new_title = (
        f"Mix Énergétique en {selected_country} ({selected_year}) - "
        f"Part Renouvelable: {re_share_percent:.1f}%"
    )

    # 6. Création de la figure
    fig = px.bar(
        filtered_df_hist, 
        x="Type",
        y="Value",
        title=new_title,
        labels={"Value": "Production (GWh)", "Type": "Energy Type"}
    )
    
    return fig

@callback(
    Output('electricity_map', 'figure'),
    Input('analytics_dropdown_year', 'value')
)
def update_map(selected_year):
    filtered_df = df[
        (df["Year"] == selected_year) &
        (df["Parameter"] == "Net Electricity Production")
    ].groupby("Country")["Value"].sum().reset_index()

    fig = px.choropleth(
        filtered_df,
        locations="Country",
        locationmode="country names",
        color="Value",
        color_continuous_scale="Viridis",
        title=f"Total Electricity Production by Country ({selected_year})",
        labels={"Value": "Production (GWh)"}
    )
    fig.update_geos(showcountries=True)
    return fig