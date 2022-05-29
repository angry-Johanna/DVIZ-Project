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


# Import Kriterien Gemuesekauf organic Data 
KG_bio_comp = pd.read_csv(path + "Kriterien_Gemuesekauf/bio/bio_complete.CSV",sep=";")

# import type of food eaten per person/year
ft_per_pers = pd.read_csv(path + "csv_Nahrungsmittelverbrauch_Bilanz_pro_Pers_new_sunburst.csv",sep=";")

# import meat consumption per person/year
meat_cons = pd.read_csv(path + "csv_Fleischbilanz_Verbr_pro_Pers_barchart.csv",sep=";")

# ---- #
# DATA #
# ---- #

# format meat consumption for barchart
comp_meat = {
    "Year": meat_cons.Year,     
    "Cow": meat_cons.Cow, 
    "Veal":meat_cons.Veal, 
    "Pig":meat_cons.Pig, 
    "Chicken":meat_cons.Chicken,
    "Others" : meat_cons.Total - (meat_cons.Cow + meat_cons.Veal + meat_cons.Pig + meat_cons.Chicken)
}



# ------- #
# BUTTONS #
# ------- #



# ------- #
# FIGURES #
# ------- #

# ------- LINE CHART ORGANIC ---------
# initial chart
fig_line_org = go.Figure()

# drop duplicates from category
KG_bio_comp_cat = KG_bio_comp.Category.drop_duplicates()

# color_map to color lines
color_map = {"Always":"#199c61","Often":"#5ae34d","Sometimes":"#c5e34d","Rarely":"#e3c04d","Never":"#e3734d"}

# add lines for each category
for index, value in KG_bio_comp_cat.items():
    # mask to draw a line for each category individually
    mask = KG_bio_comp.Category.isin([value])
    # create names for lines
    name_men = "Men buying "+value.lower()+" organic"
    name_women = "Women buying "+value.lower()+" organic"
    # add line for men
    fig_line_org.add_trace(go.Scatter(
    x=KG_bio_comp[mask].Year, 
    y=KG_bio_comp[mask].Mann,
    name = name_men,
    mode = 'lines',
    text = value,
    marker = {'color' : color_map[value]},
    line = {'dash': 'dot'}
    ))
    # add line for women
    fig_line_org.add_trace(go.Scatter(
    x=KG_bio_comp[mask].Year, 
    y=KG_bio_comp[mask].Frau,
    name = name_women,
    mode = 'lines',
    text = value,
    marker = {'color' : color_map[value]}
    ))

# make it pretty
fig_line_org.update_layout(
    title="Shopping organic",
    xaxis_title="Year",
    yaxis_title="Percentage",
    legend_title="Legend Title",
    font=dict(
        family="Courier New, monospace",
        size=15,
        color="RebeccaPurple"
    )
)
fig_line_org.update_yaxes(range=[0,50])


# ------- BAR CHART MEAT CONSUMPTION ---------

fig_barchart = px.bar(comp_meat, x = "Year", y=["Cow", "Veal", "Pig","Chicken", "Others"])




# ---------- #
# APP & HTML #
# ---------- #
app = dash.Dash(__name__)

server = app.server

app.layout = html.Div([
    
    # Buying organic
    html.Div([
        html.H1("Shopping organic groceries"),
        html.Br(), 
        html.Br(), 
        dcc.Graph(figure=fig_line_org)
    ]),
    
    # sunburst
    html.H1('Type of Food consumed per person'),
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
    ),
    
    # Meat Consumption
    html.Div([
        html.H1("Meat Consumption per person and year"),
        html.Br(), 
        html.Br(), 
        dcc.Graph(figure=fig_barchart)
    ])
    
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