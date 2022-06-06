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


# ------- #
# COLORS  #
# ------- #

# Colors for Chart Backgrounds
paper_bgcolor = "#f2f2f2"
plot_bgcolor = '#DCDCDC'

# ------- #
# FIGURES #
# ------- #

#-------------------------------------#
# ------- LINE CHART ORGANIC ---------#
#-------------------------------------#

# Group some Categories together for better readability
grouped_line = pd.DataFrame({'Year':[],'Category':[],'Frau':[],'Mann':[]})

# filter years for unique values
year = KG_bio_comp['Year'].drop_duplicates()

# Create new dataframe with the new grouped categories
for y in year:
    # Category for "Always or often" buying organic
    query_1 = "Year=="+ str(y) + "and (Category=='Always' or Category=='Often')"
    frau_1 = KG_bio_comp.query(query_1).sum().Frau
    mann_1 = KG_bio_comp.query(query_1).sum().Mann
    tmp_1 = pd.DataFrame({'Year':[y],'Category':["Always or often"],'Frau':[frau_1],'Mann':[mann_1]})
    grouped_line = pd.concat([grouped_line,  tmp_1], ignore_index=True)
    
    # Category for "Sometimes" buying organic
    query_2 = "Year=="+ str(y) + "and Category=='Sometimes'"
    frau_2 = KG_bio_comp.query(query_2).sum().Frau
    mann_2 = KG_bio_comp.query(query_2).sum().Mann
    tmp_2 = pd.DataFrame({'Year':[y],'Category':["Sometimes"],'Frau':[frau_2],'Mann':[mann_2]})
    grouped_line = pd.concat([grouped_line,  tmp_2], ignore_index=True)

    # Category for "Rarely or never" buying organic
    query_3 = "Year=="+ str(y) + "and (Category=='Rarely' or Category=='Never')"
    frau_3 = KG_bio_comp.query(query_3).sum().Frau
    mann_3 = KG_bio_comp.query(query_3).sum().Mann
    tmp_3 = pd.DataFrame({'Year':[y],'Category':["Rarely or never"],'Frau':[frau_3],'Mann':[mann_3]})
    grouped_line = pd.concat([grouped_line,  tmp_3], ignore_index=True)


# initial chart
fig_line_org = go.Figure()

# drop duplicates from category
KG_bio_comp_cat = grouped_line.Category.drop_duplicates()

# color_map to color lines
color_map_line = {
    "Always or often":"#238443",
    "Sometimes":"#78c679",
    "Rarely or never":"#045a8d"
}

# add lines for each category
for index, value in KG_bio_comp_cat.items():
    # mask to draw a line for each category individually
    mask = grouped_line.Category.isin([value])
    # create names for lines
    name_men = "Men buying "+value.lower()+" organic"
    name_women = "Women buying "+value.lower()+" organic"
    # add line for men
    fig_line_org.add_trace(go.Scatter(
    x=grouped_line[mask].Year, 
    y=grouped_line[mask].Mann,
    name = name_men,
    mode = 'lines',
    text = value,
    marker = {'color' : color_map_line[value]},
    line = {'dash': 'dot'}
    ))
    # add line for women
    fig_line_org.add_trace(go.Scatter(
    x=grouped_line[mask].Year, 
    y=grouped_line[mask].Frau,
    name = name_women,
    mode = 'lines',
    text = value,
    marker = {'color' : color_map_line[value]}
    ))

# make it pretty
fig_line_org.update_layout(
    title="Shopping organic",
    xaxis_title="Year",
    yaxis_title="Percentage [%]",
    # legend_title="Legend Title",
    font=dict(
        family="Helvetica, sans-serif",
        size=15,
        color="black"
    )
)

fig_line_org.layout.paper_bgcolor = paper_bgcolor
fig_line_org.layout.plot_bgcolor = plot_bgcolor
#fig_line_org.update_yaxes(range=[0,70])


#---------------------------------------------#
# ------- SUNBURST FOODTYPE CONSUMPTION ------#
#---------------------------------------------#

mask = ft_per_pers.year.isin([2020])
fig_sunburst = px.sunburst(
    ft_per_pers[mask], 
    path=["Type","Sub_Type","Food"], 
    values="Amount", 
    color="Type",
    color_discrete_map={'(?)':'black', "plantbased":"#41ab5d", "animalbased":"#3690c0"}
)
fig_sunburst.update_traces(insidetextorientation='radial')
fig_sunburst.layout.paper_bgcolor = paper_bgcolor
fig_sunburst.layout.plot_bgcolor = plot_bgcolor


#---------------------------------------------#
# ------- BAR CHART MEAT CONSUMPTION ---------#
#---------------------------------------------#

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
fig_barchart.layout.paper_bgcolor = paper_bgcolor
fig_barchart.layout.plot_bgcolor = plot_bgcolor




#-----------------------------------------#
# ------ BUBBLE CHART ORGANIC FARMS ------#
#-----------------------------------------#

# filter organic farm to take only every 5th year
org_farm_5 = org_farm.query("Year%5==0")

# filter those years to unique values
year = org_farm_5['Year'].drop_duplicates()

# Group some farm-sizes together for better readability
grouped_bub = pd.DataFrame({'Year':[],'Size':[],'Count':[]})
for y in year:
    # Create new size "Up to 10 hectare"
    query_1 = "Year==" + str(y) + " and (Size=='< 1 ha' or Size=='1  - <   3 ha' or Size=='3  - <   5 ha' or Size=='5  - < 10 ha')"
    count_size_1 = org_farm_5.query(query_1).sum().Number
    tmp_1 = pd.DataFrame({'Year':[y],'Size':["Up to 10 hectare"],'Count':[count_size_1]})
    grouped_bub = pd.concat([grouped_bub,  tmp_1], ignore_index=True)
    
    # Create new size "Up to 50 hectare"
    query_2 = "Year==" + str(y) + " and (Size=='10  - <  20 ha' or Size=='20  - <  30 ha' or Size=='30  - < 50 ha')"
    count_size_2 = org_farm_5.query(query_2).sum().Number
    tmp_2 = pd.DataFrame({'Year':[y],'Size':["Up to 50 hectare"],'Count':[count_size_2]})
    grouped_bub = pd.concat([grouped_bub,  tmp_2], ignore_index=True)
    
    # Create new size "50+ hectare"
    query_3 = "Year==" + str(y) + " and (Size=='50  +  ha')"
    count_size_3 = org_farm_5.query(query_3).sum().Number
    tmp_3 = pd.DataFrame({'Year':[y],'Size':["Over 50 hectare"],'Count':[count_size_3]})
    grouped_bub = pd.concat([grouped_bub,  tmp_3], ignore_index=True)

# keep nice colormap for maybe later reference
color_map_bubble = {
    "Up to 10 hectare":"#addd8e",
    "Up to 50 hectare":"#f7fcb9",
    "Over 50 hectare":"#74a9cf"
}

fig_bubble = px.scatter(
    grouped_bub, 
    x="Year", 
    y="Size",
	size="Count",
    color="Size",
    size_max = 100,
    color_discrete_map = color_map_bubble
)

fig_bubble.layout.paper_bgcolor = paper_bgcolor
fig_bubble.layout.plot_bgcolor = plot_bgcolor

# ---------- #
#    Text    #
# ---------- #

text_1 = lorem.text()
text_2 = lorem.paragraph()

text_intro = "With this data storytelling we want to figure out how the Swiss people eat and how their diet has changed over the last years. We are particularly interested in whether there is a correlation between the change in our eating habits and the increased awareness of climate change. In our close environment there are more and more vegetarians / vegans, and more and more people buy organic food. Can this development also be observed in the Swiss population, or are our feelings deceiving us? We want to get to the bottom of these questions and find possible answers through our visualisations."

text_foodtype1 = "To get a good overview of the eating habits of the Swiss, let's look at the distribution of the different food-types in our daily diet. The graph below shows the annual amount of food consumed per person in kilograms."
text_foodtype2 = "At first glance, our diet consists largely of plant-based foods. We mostly eat vegetables and fruits (222 kg/year), in addition to a large proportion of carbohydrates such as wheat and potatoes (177 kg/year). The main part of our animal diet consists of dairy products and less than a quarter is our meat consumption. Nevertheless, the consumption of meat (excluding fish) per person amounts to 47 kg per year. This corresponds to the weight of 31 chickens, eaten per person each year."

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
    "background-color": "#f2f2f2",
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
        html.H1("Changes in the eating habits of the Swiss"),
        html.P(text_intro),
    ]),
    
    # sunburst
    html.Div([
        html.P("", id="sunburst"),
        html.H2("Type of food consumed per person / per year"),
        html.P(text_foodtype1),
        html.Br(), 
        dcc.Graph(figure=fig_sunburst),
        html.P(text_foodtype2),
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

# Delete later
# keep nice colormap for maybe later reference
color_map_bubble_old = {
    "< 1 ha":"#006837",
    "1  - <   3 ha":"#41ab5d",
    "3  - <   5 ha":"#addd8e",
    "5  - < 10 ha":"#f7fcb9",
    "10  - <  20 ha":"#d0d1e6",
    "20  - <  30 ha":"#74a9cf",
    "30  - < 50 ha":"#3690c0",
    "50  +  ha":"#045a8d"
}

# colormap for line chart
color_map_line_old = {"Always":"#238443","Often":"#78c679","Sometimes":"#a6bddb","Rarely":"#3690c0","Never":"#045a8d"}


if __name__ == '__main__':
    app.run_server(debug=True)