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
path = 'https://raw.githubusercontent.com/angry-Johanna/DVIZ-Project/main/data_csv/'


# Import Kriterien Gemuesekauf Data
# bio
KG_bio_imm = pd.read_csv(path + "Kriterien_Gemuesekauf/bio/bio_immer.CSV")
KG_bio_mei = pd.read_csv(path + "Kriterien_Gemuesekauf/bio/bio_meistens.CSV")
KG_bio_gel = pd.read_csv(path + "Kriterien_Gemuesekauf/bio/bio_gelegentlich.CSV")
KG_bio_sel = pd.read_csv(path + "Kriterien_Gemuesekauf/bio/bio_selten.CSV")
KG_bio_nie = pd.read_csv(path + "Kriterien_Gemuesekauf/bio/bio_nie.CSV")

# regional
KG_reg_imm = pd.read_csv(path + "Kriterien_Gemuesekauf/regional/reg_immer.CSV")
KG_reg_mei = pd.read_csv(path + "Kriterien_Gemuesekauf/regional/reg_meistens.CSV")
KG_reg_gel = pd.read_csv(path + "Kriterien_Gemuesekauf/regional/reg_gelegentlich.CSV")
KG_reg_sel = pd.read_csv(path + "Kriterien_Gemuesekauf/regional/reg_selten.CSV")
KG_reg_nie = pd.read_csv(path + "Kriterien_Gemuesekauf/regional/reg_nie.CSV")

# seasonal
KG_sai_imm = pd.read_csv(path + "Kriterien_Gemuesekauf/saisonal/sais_immer.CSV")
KG_sai_mei = pd.read_csv(path + "Kriterien_Gemuesekauf/saisonal/sais_meistens.CSV")
KG_sai_gel = pd.read_csv(path + "Kriterien_Gemuesekauf/saisonal/sais_gelegentlich.CSV")
KG_sai_sel = pd.read_csv(path + "Kriterien_Gemuesekauf/saisonal/sais_selten.CSV")
KG_sai_nie = pd.read_csv(path + "Kriterien_Gemuesekauf/saisonal/sais_nie.CSV")



# ---- #
# DATA #
# ---- #



# Test-dataset
data = dict(
    character=["Eve", "Cain", "Seth", "Enos", "Noam", "Abel", "Awan", "Enoch", "Azula"],
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