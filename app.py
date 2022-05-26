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



# import type of food eaten per person
ft_per_pers = pd.read_csv(path + "csv_Nahrungsmittelverbrauch_Bilanz_pro_Pers_new_sunburst.csv",sep=";")

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

# ------- LINE CHART ---------
# initial chart
fig_line = go.Figure()

# drop duplicates from category
KG_bio_comp_cat = KG_bio_comp.Category.drop_duplicates()

# add lines for each category
for index, value in KG_bio_comp_cat.items():
    # mask to draw a line for each category individually
    mask = KG_bio_comp.Category.isin([value])
    # create names for lines
    name_men = "Men buying "+value.lower()+" organic"
    name_women = "Women buying "+value.lower()+" organic"
    # add line for men
    fig_line.add_trace(go.Scatter(
    x=KG_bio_comp[mask].Year, 
    y=KG_bio_comp[mask].Mann,
    name = name_men,
    text = "blabla"
    ))
    # add line for women
    fig_line.add_trace(go.Scatter(
    x=KG_bio_comp[mask].Year, 
    y=KG_bio_comp[mask].Frau,
    name = name_women
    ))

# make it pretty
fig_line.update_layout(
    title="Shopping organic",
    xaxis_title="Year",
    yaxis_title="Percentage",
    legend_title="Legend Title",
    font=dict(
        family="Courier New, monospace",
        size=18,
        color="RebeccaPurple"
    )
)
fig_line.update_yaxes(range=[0,100])

# ---------- #
# APP & HTML #
# ---------- #
app = dash.Dash(__name__)

server = app.server

app.layout = html.Div([
    
    # Buying organic
    html.Div([
        html.Label("Buying organic", style={'font-size': 'medium'}),
        html.Br(),
        html.Label('Click on it to know more!', style={'font-size':'9px'}),
        html.Br(), 
        html.Br(), 
        dcc.Graph(figure=fig_line)
    ]),
    
    # sunburst
    html.H4('Type of Food consumed per person'),
    dcc.Graph(id="graph-foodtype"),
    dcc.Slider(
        min=2007, 
        max=2020,
        step=None,
        marks= {
            2007: "2007",
            2008: "2008",
            2009: "2009",
            2010: "2010",
            2011: "2011",
            2012: "2012",
            2013: "2013",
            2014: "2014",
            2015: "2015",
            2016: "2016",
            2017: "2017",
            2018: "2018",
            2019: "2019",
            2020: "2020"
        },
        id="slider_foodtype",
        value=2007
    )
    
])



# --------- #
# CALLBACKS #
# --------- #

# callback for sunburst
@app.callback(
    Output("graph-foodtype", "figure"), 
    Input("slider_foodtype", "value"))

def update_sunburst_chart(year):
    df = ft_per_pers
    mask = df.year.isin([year])
    fig =  px.sunburst(
        ft_per_pers[mask], 
        path=["Type","Food"], 
        values="Amount",
        color="Type",
        color_discrete_map={'(?)':'black', "plantbased":"green","animalbased":"red"},
        )
    fig.update_traces(insidetextorientation='radial')
    return fig



if __name__ == '__main__':
    app.run_server(debug=True)