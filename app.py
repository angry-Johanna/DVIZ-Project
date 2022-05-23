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
KG_bio_imm = pd.read_csv(path + "Kriterien_Gemuesekauf/bio/bio_immer.CSV",sep=";")
KG_bio_mei = pd.read_csv(path + "Kriterien_Gemuesekauf/bio/bio_meistens.CSV",sep=";")
KG_bio_gel = pd.read_csv(path + "Kriterien_Gemuesekauf/bio/bio_gelegentlich.CSV",sep=";")
KG_bio_sel = pd.read_csv(path + "Kriterien_Gemuesekauf/bio/bio_selten.CSV",sep=";")
KG_bio_nie = pd.read_csv(path + "Kriterien_Gemuesekauf/bio/bio_nie.CSV",sep=";")
KG_bio_comp = pd.read_csv(path + "Kriterien_Gemuesekauf/bio/bio_complete.CSV",sep=";")

# regional
KG_reg_imm = pd.read_csv(path + "Kriterien_Gemuesekauf/regional/reg_immer.CSV",sep=";")
KG_reg_mei = pd.read_csv(path + "Kriterien_Gemuesekauf/regional/reg_meistens.CSV",sep=";")
KG_reg_gel = pd.read_csv(path + "Kriterien_Gemuesekauf/regional/reg_gelegentlich.CSV",sep=";")
KG_reg_sel = pd.read_csv(path + "Kriterien_Gemuesekauf/regional/reg_selten.CSV",sep=";")
KG_reg_nie = pd.read_csv(path + "Kriterien_Gemuesekauf/regional/reg_nie.CSV",sep=";")
KG_reg_comp = pd.read_csv(path + "Kriterien_Gemuesekauf/regional/reg_complete.CSV",sep=";")

# seasonal
KG_sai_imm = pd.read_csv(path + "Kriterien_Gemuesekauf/saisonal/sais_immer.CSV",sep=";")
KG_sai_mei = pd.read_csv(path + "Kriterien_Gemuesekauf/saisonal/sais_meistens.CSV",sep=";")
KG_sai_gel = pd.read_csv(path + "Kriterien_Gemuesekauf/saisonal/sais_gelegentlich.CSV",sep=";")
KG_sai_sel = pd.read_csv(path + "Kriterien_Gemuesekauf/saisonal/sais_selten.CSV",sep=";")
KG_sai_nie = pd.read_csv(path + "Kriterien_Gemuesekauf/saisonal/sais_nie.CSV",sep=";")
KG_sai_comp = pd.read_csv(path + "Kriterien_Gemuesekauf/saisonal/sais_complete.CSV",sep=";")


# ---- #
# DATA #
# ---- #



# Test-dataset



# ------- #
# BUTTONS #
# ------- #



# ------- #
# FIGURES #
# ------- #


# ---------- #
# APP & HTML #
# ---------- #
app = dash.Dash(__name__)

server = app.server

app.layout = html.Div([
    html.H4('Shopping Organic'),
    dcc.Graph(id="graph-organic"),
    dcc.Checklist(
        id="checklist",
        options=["Always", "Often", "Sometimes","Rarely","Never"],
        value=["Always", "Never"],
        inline=True
    )
    
])



# --------- #
# CALLBACKS #
# --------- #

@app.callback(
    Output("graph-organic", "figure"), 
    Input("checklist", "value"))

def update_line_chart(cat):
    df = KG_bio_comp
    mask = df.Category.isin(cat)
    fig = px.line(df[mask], 
        x="Year", y=["Frau","Mann"])
    fig.update_xaxes(type='category')
    fig.update_yaxes(range=[0,100])
    return fig




if __name__ == '__main__':
    app.run_server(debug=True)