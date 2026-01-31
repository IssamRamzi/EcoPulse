import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
from dash import html, dcc, callback, Input, Output
from src.components.cards import create_chart_card, create_metric_card


POLLUTANTS_MAP = {
    "CO AQI Value": "CO",
    "Ozone AQI Value": "O3",
    "NO2 AQI Value": "NO2",
    "PM2.5 AQI Value": "PM2.5"
}

POLLUTANTS_FULL = {
    "CO AQI Value": "Carbon Monoxide",
    "Ozone AQI Value": "Ozone",
    "NO2 AQI Value": "Nitrogen Dioxide",
    "PM2.5 AQI Value": "Fine Particles"
}

AQI_COLORS = {
    "Good": "#10b981",
    "Moderate": "#fbbf24",
    "Unhealthy for Sensitive Groups": "#fb923c",
    "Unhealthy": "#ef4444",
    "Very Unhealthy": "#dc2626",
    "Hazardous": "#991b1b"
}

def create_page_header():
    dbc.Row([
    dbc.Col([
        html.Div([
            html.H1([
                html.Span("🌫️ ", className="me-2"),
                "Air Quality Analytics"
            ], className='fw-bold mb-2'),
            html.P(
                "Monitor air pollution levels, track AQI trends, and understand health impacts across cities worldwide",
                className="lead text-muted mb-0"
            )
        ])
    ], width=12)
], className="mb-4")



def pollution_callbacks(df):
    @callback(
        Output('pollution_dropdown_city', 'options'),
        Output('pollution_dropdown_city', 'value'),
        Input('pollution_dropdown_country', 'value')
    )
    def update_city_dropdown(selected_country):
        if not selected_country:
            return [], None
            
        cities = sorted(df[df["Country"] == selected_country]["City"].dropna().unique())
        
        options = [{"label": c, "value": c} for c in cities]
        value = cities[0] if cities else None
        return options, value


    @callback(
        Output('pollution_metrics', 'children'),
        Input('pollution_dropdown_country', 'value'),
        Input('pollution_dropdown_city', 'value')
    )
    def update_metrics(selected_country, selected_city):
        if not selected_city:
            return []
        
        city_row = df[(df["Country"] == selected_country) & (df["City"] == selected_city)].iloc[0]
        
        overall_aqi = city_row["AQI Value"]
        aqi_category = city_row["AQI Category"]
        color = "success" if overall_aqi <= 50 else "warning" if overall_aqi <= 100 else "danger"
        
        
        pollutant_values = {POLLUTANTS_MAP[k]: city_row[k] for k in POLLUTANTS_MAP.keys()}
        dominant = max(pollutant_values, key=pollutant_values.get)
        
        return [
            dbc.Col([
                create_metric_card(
                    "Overall AQI",
                    f"{overall_aqi:.0f}",
                    aqi_category,
                    color=color
                )
            ], md=4, className="mb-3"),
            
            dbc.Col([
                create_metric_card(
                    "Dominant Pollutant",
                    dominant,
                    f"Level: {pollutant_values[dominant]:.0f}",
                    color="info"
                )
            ], md=4, className="mb-3"),
            
            dbc.Col([
                create_metric_card(
                    "Health Status",
                    "",
                    get_health_advice(overall_aqi),
                    color=color
                )
            ], md=4, className="mb-3")
        ]


    def get_health_advice(aqi):
        if aqi <= 50:
            return "Air quality is satisfactory"
        elif aqi <= 100:
            return "Acceptable for most people"
        elif aqi <= 150:
            return "Sensitive groups take caution"
        elif aqi <= 200:
            return "Everyone may experince effects"
        elif aqi <= 300:
            return "Health alert - reduce exposure"
        else:
            return "Health emergency - stay indoors"


    @callback(
        Output('pollution_histogram', 'figure'),
        Input('pollution_dropdown_country', 'value'),
        Input('pollution_dropdown_city', 'value')
    )
    def update_pollution_histogram(selected_country, selected_city):
        if not selected_city:
            return {}

        city_row = df[(df["Country"] == selected_country) & (df["City"] == selected_city)].iloc[0]
        
        overall_aqi = city_row["AQI Value"]
        aqi_category = city_row["AQI Category"]

        plot_data = []
        for col, label in POLLUTANTS_MAP.items():
            full_name = POLLUTANTS_FULL[col]
            plot_data.append({
                "Pollutant": label,
                "Full Name": full_name,
                "AQI Value": city_row[col]
            })
        
        df_plot = pd.DataFrame(plot_data)

        fig = px.bar(
            df_plot,
            x="Pollutant",
            y="AQI Value",
            color="Pollutant",
            text="AQI Value",
            title=f"Air Quality in {selected_city} - {aqi_category} (Overall AQI: {overall_aqi:.0f})",
            labels={"AQI Value": "AQI Level", "Pollutant": "Pollutant"},
            color_discrete_sequence=px.colors.qualitative.Bold,
            template="plotly_dark",
            hover_data={"Full Name": True, "Pollutant": False}
        )
        
        fig.add_hline(
            y=50, line_dash="dot", line_color="#10b981", 
            annotation_text="Good (0-50)", annotation_position="right"
        )
        fig.add_hline(
            y=100, line_dash="dot", line_color="#fbbf24",
            annotation_text="Moderate (51-100)", annotation_position="right"
        )
        fig.add_hline(
            y=150, line_dash="dot"  , line_color="#fb923c",
            annotation_text="Unhealthy for Sensitive (101-150)", annotation_position="right"
        )
        
        fig.update_traces(texttemplate='%{text:.0f}', textposition='outside')
        fig.update_layout(
            font = dict(color="black"),
            showlegend=False,
            hovermode='x unified',
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            xaxis_title="Pollutant Type",
            yaxis_title="AQI Value"
        )
        
        return fig


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
            color_continuous_scale="Temps",
            projection="orthographic",
            title="Average Air Quality Index by Country",
            labels={"AQI Value": "Average AQI"},
        )

        fig.update_geos(
            showcountries=True,
            countrycolor="rgba(255,255,255,0.15)",   
            showcoastlines=False,
            showocean=True,
            oceancolor="rgb(220,220,220)",               
            showland=True,
            landcolor="rgb(15,18,26)",                
            bgcolor="rgba(0,0,0,0)",
        )

        fig.update_layout(
            font=dict(
                color="#E5E7EB",                      
                size=14
            ),
            title=dict(
                x=0.5,
                font=dict(size=18, color="#F9FAFB")
            ),
            margin=dict(l=0, r=0, t=50, b=0),
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",

            coloraxis_colorbar=dict(
                tickcolor="#000",
                title_font_color="#000",
                tickfont_color="#000"
            )
        )

        return fig
    @callback(
        Output('top_countries_bar_chart', 'figure'),
        Input('pollution_dropdown_country', 'options') 
    )
    def update_top_countries_chart(_):
        avg_aqi = df.groupby("Country")["AQI Value"].mean().reset_index()
        
        top_10 = avg_aqi.sort_values(by="AQI Value", ascending=False).head(10)
        
        fig = px.bar(
            top_10,
            x="AQI Value",
            y="Country",
            orientation='h', 
            text="AQI Value",
            color="AQI Value",
            color_continuous_scale="Reds", 
            title="Niveau moyen de pollution par pays"
        )
        
        fig.update_layout(yaxis=dict(autorange="reversed"))
        
        fig.update_traces(texttemplate='%{text:.0f}', textposition='outside')
        fig.update_layout(
            template="plotly_dark", 
            font=dict(color="black"),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            xaxis_title="AQI Moyen",
            yaxis_title=None,
            coloraxis_showscale=False, 
            margin=dict(l=0, r=50, t=30, b=0)
        )
        
        return fig
    
    @callback(
        Output('pollution_dropdown_country', 'value'),
        Input('pollution_map', 'clickData'),
        prevent_initial_call=True
    )
    def update_country_from_map(clickData):
        if clickData is None:
            print("No data")
        
        selected_country = clickData['points'][0]['location']
        
        return selected_country
