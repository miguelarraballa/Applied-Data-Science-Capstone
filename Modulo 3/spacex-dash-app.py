# spacex_dash_app.py

import pandas as pd
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px

# Load dataset
spacex_df = pd.read_csv("spacex_launch_dash.csv")

# Get minimum and maximum payload mass
min_payload = spacex_df["Payload Mass (kg)"].min()
max_payload = spacex_df["Payload Mass (kg)"].max()

# Get list of launch sites
launch_sites = spacex_df["Launch Site"].unique()

# Create Dash app
app = dash.Dash(__name__)

app.layout = html.Div(children=[
    html.H1(
        "SpaceX Launch Records Dashboard",
        style={"textAlign": "center", "color": "#503D36", "font-size": 40}
    ),

    # TASK 1: Launch Site dropdown
    dcc.Dropdown(
        id="site-dropdown",
        options=(
            [{"label": "All Sites", "value": "ALL"}] +
            [{"label": site, "value": site} for site in launch_sites]
        ),
        value="ALL",  # default value
        placeholder="Select a Launch Site here",
        searchable=True
    ),

    html.Br(),

    # Pie chart
    html.Div(dcc.Graph(id="success-pie-chart")),

    html.Br(),

    # Payload slider label
    html.P("Payload range (Kg):"),

    # TASK 3: Payload RangeSlider
    dcc.RangeSlider(
        id="payload-slider",
        min=0,
        max=10000,
        step=1000,
        marks={
            0: "0",
            2500: "2500",
            5000: "5000",
            7500: "7500",
            10000: "10000"
        },
        value=[min_payload, max_payload]
    ),

    html.Br(),

    # Scatter chart
    html.Div(dcc.Graph(id="success-payload-scatter-chart"))
])


# TASK 2: Callback for pie chart
@app.callback(
    Output("success-pie-chart", "figure"),
    Input("site-dropdown", "value")
)
def update_pie_chart(selected_site):
    if selected_site == "ALL":
        # All sites: show total successful launches by site (sum of "class")
        df_all = spacex_df.copy()
        fig = px.pie(
            df_all,
            values="class",             # 0/1 values, sum = number of successes
            names="Launch Site",
            title="Total Successful Launches by Site"
        )
    else:
        # Single site: show success vs failure
        df_site = spacex_df[spacex_df["Launch Site"] == selected_site]
        fig = px.pie(
            df_site,
            names="class",
            title=f"Total Launches for site {selected_site}",
            labels={"class": "Launch Outcome"}
        )

    return fig


# TASK 4: Callback for scatter chart
@app.callback(
    Output("success-payload-scatter-chart", "figure"),
    [
        Input("site-dropdown", "value"),
        Input("payload-slider", "value")
    ]
)
def update_scatter_chart(selected_site, payload_range):
    low, high = payload_range

    # Filter by payload range
    mask = (
        (spacex_df["Payload Mass (kg)"] >= low) &
        (spacex_df["Payload Mass (kg)"] <= high)
    )
    filtered_df = spacex_df[mask]

    # Filter by launch site if not ALL
    if selected_site != "ALL":
        filtered_df = filtered_df[filtered_df["Launch Site"] == selected_site]
        title = f"Payload vs. Outcome for site {selected_site}"
    else:
        title = "Payload vs. Outcome for all sites"

    fig = px.scatter(
        filtered_df,
        x="Payload Mass (kg)",
        y="class",
        color="Booster Version Category",
        title=title,
        labels={
            "class": "Launch Outcome"
        }
    )

    return fig


if __name__ == "__main__":
    # Works both in the course environment and locally
    app.run(host="0.0.0.0", port=8050, debug=False)