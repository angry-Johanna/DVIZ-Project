import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output, State
import dash_daq as daq
import dash_bootstrap_components as dbc
import numpy as np
import pandas as pd
import plotly.graph_objs as go
import plotly.express as px

# ----------- #
# IMPORT DATA #
# ----------- #



# ---- #
# DATA #
# ---- #

# Test-dataset
data = dict(
    character=["Eve", "Cain", "Seth", "Enos", "Noam", "Abel", "Awan", "Enoch", "Azura"],
    parent=["", "Eve", "Eve", "Seth", "Seth", "Eve", "Eve", "Awan", "Eve" ],
    value=[10, 14, 12, 10, 2, 6, 6, 4, 4])



# ------- #
# BUTTONS #
# ------- #



# ------- #
# FIGURES #
# ------- #
# Testfigure
fig_test = px.sunburst(
    data,
    names='character',
    parents='parent',
    values='value',
)


# ---------- #
# APP & HTML #
# ---------- #
app = dash.Dash(__name__)

server = app.server

app.layout = html.Div([
    
    # Test-Figure
    html.Div([
        html.Label("Test-Figure", style={'font-size': 'medium'}),
        html.Br(),
        html.Label('Click on it to know more!', style={'font-size':'9px'}),
        html.Br(), 
        html.Br(), 
        dcc.Graph(figure=fig_test)
    ])
    
])



# --------- #
# CALLBACKS #
# --------- #



if __name__ == '__main__':
    app.run_server(debug=True)