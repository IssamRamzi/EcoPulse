import dash_bootstrap_components as dbc
import plotly.express as px
from dash import html, dcc, callback, Input, Output
from src.components.cards import create_chart_card, create_metric_card
from src.components.filters import create_country_filter, create_year_filter


def create_page_header():
    return dbc.Row([
    dbc.Col([
        html.Div([
            html.H1([
                "Electricity Production Analytics"
            ], className='fw-bold mb-2'),
            html.P(
                "Explore global electricity generation patterns, renewable energy adoption, and energy mix trends",
                className="lead text-muted mb-0"
            )
        ])
    ], width=12)
], className="mb-4")

def create_filter_section(countries, random_country):
    return dbc.Card([
    dbc.CardBody([
        html.H5([
            html.I(className="fas fa-filter me-2"),
            "Filters"
        ], className="mb-3 fw-bold"),
        dbc.Row([
            create_country_filter(
                'analytics_dropdown_country',
                countries,
                random_country,
                "Country"
            ),
            create_year_filter(
                'analytics_dropdown_year',
                "Select Year"
            )
        ])
    ])
], className="shadow-sm border-0 mb-4")


def elec_callbacks(df):
    @callback(
    Output('analytics_dropdown_year', 'options'),
    Output('analytics_dropdown_year', 'value'),
    Input('analytics_dropdown_country', 'value')
    )
    def update_year_dropdown(selected_country):
        filtered_df = df[df["Country"] == selected_country]
        years_available = sorted(filtered_df["Year"].unique())
        options = [{"label": y, "value": y} for y in years_available]
        value = years_available[-1] if years_available else None
        return options, value


    @callback(
        Output('electricity_metrics', 'children'),
        Input('analytics_dropdown_country', 'value'),
        Input('analytics_dropdown_year', 'value')
    )
    def update_metrics(selected_country, selected_year):
        if not selected_country or not selected_year:
            return []
        
        RENEWABLES = ["Hydro", "Wind", "Solar", "Geothermal", "Combustible Renewables", "Other Renewables"]
        
        filtered_df = df[
            (df["Country"] == selected_country) &
            (df["Year"] == selected_year) &
            (df["Parameter"] == "Net Electricity Production")
        ]
        
        total_prod = filtered_df[filtered_df["Type"] == "Electricity"]["Value"].sum()
        
        renewable_prod = filtered_df[filtered_df["Type"].isin(RENEWABLES)]["Value"].sum()
        
        re_percentage = (renewable_prod / total_prod * 100) if total_prod > 0 else 0
        
        return [
            dbc.Col([
                create_metric_card(
                    "Total Production",
                    f"{total_prod:,.0f} GWh",
                    f"Year {selected_year}",
                    color="primary"
                )
            ], md=4, className="mb-3"),
            
            dbc.Col([
                create_metric_card(
                    "Renewable Energy",
                    f"{re_percentage:.1f}%",
                    f"{renewable_prod:,.0f} GWh from renewables",
                    color="success"
                )
            ], md=4, className="mb-3"),
            
            dbc.Col([
                create_metric_card(
                    "Non-Renewable",
                    f"{100-re_percentage:.1f}%",
                    f"{total_prod - renewable_prod:,.0f} GWh",
                    color="warning"
                )
            ], md=4, className="mb-3")
        ]


    @callback(
        Output('electricity_histogram', 'figure'),
        Input('analytics_dropdown_country', 'value'),
        Input('analytics_dropdown_year', 'value')
    )
    def update_histogram(selected_country, selected_year):
        if not selected_country or not selected_year:
            return {}
        
        RENEWABLES = ["Hydro", "Wind", "Solar", "Geothermal", "Combustible Renewables", "Other Renewables"]
        
        filtered_df = df[
            (df["Country"] == selected_country) &
            (df["Year"] == selected_year) &
            (df["Parameter"] == "Net Electricity Production")
        ]
        
        types_to_exclude = ["Electricity", "Total Renewables (Hydro, Geo, Solar, Wind, Other)"]
        filtered_df_hist = filtered_df[~filtered_df["Type"].isin(types_to_exclude)].copy()
        
        if filtered_df_hist.empty:
            fig = px.bar(title="No Data Available")
            fig.update_layout(template="plotly_dark")
            return fig

        filtered_df_hist['Category'] = filtered_df_hist['Type'].apply(
            lambda x: 'Renewable' if x in RENEWABLES else 'Non-Renewable'
        )
        
        fig = px.bar(
            filtered_df_hist, 
            x="Type",
            y="Value",
            color="Category",
            color_discrete_map={"Renewable": "#10b981", "Non-Renewable": "#f59e0b"},
            title=f"Energy Mix in {selected_country} ({selected_year})",
            labels={"Value": "Production (GWh)", "Type": "Energy Source"}
        )
        
        fig.update_layout(
            template="plotly_dark", 
            font=dict(color="black"), 
            xaxis_tickangle=-45,
            showlegend=True,
            hovermode='x unified',
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)'
        )
        
        return fig

    @callback(
        Output('electricity_map', 'figure'),
        Input('analytics_dropdown_year', 'value')
    )
    def update_map(selected_year):
        if not selected_year:
            return {}
        
        filtered_df = df[
            (df["Year"] == selected_year) &
            (df["Parameter"] == "Net Electricity Production") &
            (df["Type"] == "Electricity")
        ].groupby("Country")["Value"].sum().reset_index()
        
        print(f'{filtered_df["Value"].min()} , {filtered_df["Value"].max()}')
        
        fig = px.choropleth(
            filtered_df,
            range_color=(filtered_df['Value'].min(), filtered_df['Value'].max()),
            locations="Country",
            locationmode="country names",
            color="Value",
            color_continuous_scale="Temps",
            projection="orthographic",  
            title=f"Global Electricity Production ({selected_year})",
            labels={"Value": "Production (GWh)"}
        )
        
        fig.update_geos(
            showcountries=True,
            countrycolor="rgba(255,255,255,0.15)",
            showcoastlines=False,
            showocean=True,
            oceancolor="rgb(220,220,220)",
            showland=True,
            landcolor="rgb(15,18,26)",
            bgcolor="rgba(0,0,0,0)"
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
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            coloraxis_colorbar=dict(
                tickcolor="#000",
                title_font_color="#000",
                tickfont_color="#000"
            )
        )
        
        return fig
    

    @callback(
        Output('renewable_share_histogram', 'figure'),
        Input('analytics_dropdown_country', 'value')
    )
    def update_renewable_share_histogram(selected_country):
        if not selected_country:
            return {}

        RENEWABLES = [
            "Hydro", "Wind", "Solar",
            "Geothermal", "Combustible Renewables", "Other Renewables"
        ]

        country_df = df[
            (df["Country"] == selected_country) &
            (df["Parameter"] == "Net Electricity Production")
        ]

        total_df = (
            country_df[country_df["Type"] == "Electricity"]
            .groupby("Year")["Value"]
            .sum()
            .reset_index(name="Total")
        )

        renewable_df = (
            country_df[country_df["Type"].isin(RENEWABLES)]
            .groupby("Year")["Value"]
            .sum()
            .reset_index(name="Renewable")
        )

        merged_df = total_df.merge(renewable_df, on="Year", how="left")
        merged_df["Renewable"] = merged_df["Renewable"].fillna(0)
        merged_df["Non-Renewable"] = merged_df["Total"] - merged_df["Renewable"]
        
        merged_df["RenewableShare"] = (merged_df["Renewable"] / merged_df["Total"] * 100)
        merged_df["NonRenewableShare"] = (merged_df["Non-Renewable"] / merged_df["Total"] * 100)

        fig = px.bar(
            merged_df,
            x="Year",
            y=["RenewableShare", "NonRenewableShare"],
            labels={
                "Year": "Year",
                "value": "Percentage (%)",
                "variable": "Energy Type"
            },
            title=f"Renewable vs Non-Renewable Electricity Share – {selected_country}",
            template="plotly_dark",
            color_discrete_map={
                "RenewableShare": "#10b981",
                "NonRenewableShare": "#f59e0b"
            }
        )

        # Update legend labels
        fig.for_each_trace(lambda t: t.update(
            name="Renewable" if t.name == "RenewableShare" else "Non-Renewable"
        ))

        fig.update_layout(
            bargap = 0.02,
            yaxis=dict(range=[0, 100], title="Share (%)"),
            xaxis=dict(title="Year"),
            barmode='stack',
            font=dict(color="black"),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            showlegend=True,
            legend=dict(
                title="Energy Type",
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1
            )
        )

        return fig