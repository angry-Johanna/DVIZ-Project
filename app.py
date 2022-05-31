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
import lorem

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

# import organic farms
org_farm = pd.read_csv(path + "csv_Biologischer_Landbau_bubble.csv",sep=";")

# ---- #
# DATA #
# ---- #

# format meat consumption for barchart
comp_meat = pd.DataFrame({
    "Year": meat_cons.Year,     
    "Cow": meat_cons.Cow, 
    "Veal":meat_cons.Veal, 
    "Pig":meat_cons.Pig, 
    "Chicken":meat_cons.Chicken,
    "Others" : meat_cons.Total - (meat_cons.Cow + meat_cons.Veal + meat_cons.Pig + meat_cons.Chicken)
})
# Also remove a few entries
comp_meat_5 = comp_meat.query("Year%5==0")


# filter organic farm to take only every 5th year
org_farm_5 = org_farm.query("Year%5==0")


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

# ------- SUNBURST FOODTYPE CONSUMPTION ------
mask = ft_per_pers.year.isin([2020])
fig_sunburst = px.sunburst(
    ft_per_pers[mask], 
    path=["Type","Sub_Type","Food"], 
    values="Amount", 
    color="Type",
    color_discrete_map={'(?)':'black', "plantbased":"green","animalbased":"red"}
)
fig_sunburst.update_traces(insidetextorientation='radial')

# ------- BAR CHART MEAT CONSUMPTION ---------
color_map_bar = {
    "Cow":"#199c61",
    "Veal":"#5ae34d",
    "Pig":"#c5e34d",
    "Chicken":"#e3c04d",
    "Others":"#e3734d"
}

fig_barchart = px.bar(
    comp_meat_5, 
    x = "Year", 
    y = [
        "Cow", 
        "Veal", 
        "Pig",
        "Chicken", 
        "Others"
    ],
    color_discrete_map = color_map_bar
)


# ------ BUBBLE CHART ORGANIC FARMS
color_map_bubble = {
    "< 1 ha":"#199c61",
    "1  - <   3 ha":"#5ae34d",
    "3  - <   5 ha":"#c5e34d",
    "5  - < 10 ha":"#e3c04d",
    "10  - <  20 ha":"#e3734d",
    "20  - <  30 ha":"#199c61",
    "30  - < 50 ha":"#5ae34d",
    "50  +  ha":"#c5e34d"
}

fig_bubble = px.scatter(
    org_farm_5, 
    x="Year", 
    y="Size",
	size="Number",
    color="Size",
    size_max = 60,
    color_discrete_map = color_map_bubble
)



# ---------- #
# Text       #
# ---------- #

text_1 = lorem.text()
text_2 = lorem.paragraph()

# ---------- #
# APP & HTML #
# ---------- #
app = dash.Dash(__name__)

server = app.server

# sidebar
SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "16rem",
    "padding": "2rem 1rem",
    "background-color": "#FFFAF0",
    "font-family": "Helvetica",
    "outline": "none",
    "text-decoration": "none",
    "font-size": 13,
}

sidebar = html.Div(
    [
        html.H2("Table of contents", className="display-4"),
        html.Hr(),
        dbc.Nav(
            [
                dbc.NavLink("Intro", href="http://127.0.0.1:8050/buying_organic#intro", active="exact"),
                html.Br(),
                dbc.NavLink("Shopping organic groceries", href="http://127.0.0.1:8050/buying_organic#buying_organic", active="exact"),
                html.Br(),
                dbc.NavLink("Type of food consumed per person", href="http://127.0.0.1:8050/buying_organic#sunburst", active="exact"),
                html.Br(),
                dbc.NavLink("Meat Consumption per person and year", href="http://127.0.0.1:8050/buying_organic#meat_consumption", active="exact"),
                html.Br(),
                dbc.NavLink("Organic Farms Land usage", href="http://127.0.0.1:8050/buying_organic#organic_farms", active="exact"),
            ],
            vertical=True,
            pills=True,
        ),
    ],
    style=SIDEBAR_STYLE,
)

# Table styling
app.layout = html.Div([
    
    html.Div([
        sidebar
    ]),    
    
    html.Div([
        html.P("", id="intro"),
        html.H1("How do the Swiss behave regarding grocerie shopping?"),
        html.P(text_2),
        html.P(text_2)
    ]),
    
    # Buying organic
    html.Div([
        html.P("", id="buying_organic"),
        html.H2("Shopping organic groceries"),
        html.P(text_2),
        html.Br(), 
        dcc.Graph(figure=fig_line_org),
        html.Br(),
        html.P(text_2),
        html.Br()
    ]),
    
    
    # sunburst
    html.Div([
        html.P("", id="sunburst"),
        html.H2("Type of food consumed per person"),
        html.P(text_2),
        html.Br(), 
        dcc.Graph(figure=fig_sunburst),
        html.P(text_2),
        html.Br(),
    ]),
    
    # Meat Consumption
    html.Div([
        html.P("", id="meat_consumption"),
        html.H2("Meat Consumption per person and year"),
        html.P(text_2),
        html.Br(), 
        dcc.Graph(figure=fig_barchart),
        html.Br(),
        html.P(text_2),
        html.Br()
    ]),
    
    # Organic Farms
    html.Div([
        html.P("", id="organic_farms"),
        html.H2("Organic Farms Land usage"),
        html.P(text_2),
        html.Br(), 
        dcc.Graph(figure=fig_bubble),
        html.Br(),
        html.P(text_2),
        html.Br()
    ]),
    
    # Source
    html.Div([
        html.H4("Sources:"),
        html.P("https://www.bfs.admin.ch/bfs/de/home/statistiken/kataloge-datenbanken/tabellen.html"),
        html.H4("Masterminds behind this project:"),
        html.P("Johanna Koch and Nadja Kaufmann, HSLU-I")
    ])
])



# --------- #
# CALLBACKS #
# --------- #



if __name__ == '__main__':
    app.run_server(debug=True)