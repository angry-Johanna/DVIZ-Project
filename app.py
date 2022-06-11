import dash
from dash import dcc
from dash import html
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.graph_objs as go
import plotly.express as px
from plotly.subplots import make_subplots

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
    "Always or often":"#006837",
    "Sometimes":"#78c679",
    "Rarely or never":"#3690c0"
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
    marker = {'color' : color_map_line[value]},
    hovertemplate = '%{y}%<extra></extra>' ,
    line = {'dash': 'dot'}
    ))
    # add line for women
    fig_line_org.add_trace(go.Scatter(
    x=grouped_line[mask].Year, 
    y=grouped_line[mask].Frau,
    name = name_women,
    marker = {'color' : color_map_line[value]},
    hovertemplate = '%{y}%<extra></extra>' 
    ))

# make it pretty
fig_line_org.update_layout(
    title="Shopping Organic",
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
#fig_line_org.update_layout(hovermode="x")
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
    color_discrete_map={"plantbased":"#41ab5d", "animalbased":"#3690c0"},
    hover_name = "Food",
    hover_data= {"Amount": ":.2f", "Type":False}
)

fig_sunburst.update_traces(insidetextorientation='radial')
fig_sunburst.layout.paper_bgcolor = paper_bgcolor
fig_sunburst.layout.plot_bgcolor = plot_bgcolor

fig_sunburst.update_layout(
    height=600,
    title_text="Different Types of Food Consumed 2020 [in kg]",
    font=dict(
        family="Helvetica, sans-serif",
        size=15,
        color="black"
    )
)

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


fig_barchart = make_subplots(
    rows=2, 
    cols=2, 
    subplot_titles=("Cow Meat Consumption", "Chicken Meat Consumption", "Veal Meat Consumption", "Pig Meat Consumption" )
)

fig_barchart.add_trace(
    go.Bar(
        x=comp_meat_5["Year"], 
        y=comp_meat_5["Cow"],
        name = "Cow",
        marker = {'color' : "#41ab5d"},
        hovertemplate = '%{y} kg<extra></extra>'
    ),
    row=1, col=1
)

fig_barchart.add_trace(
    go.Bar(
        x=comp_meat_5["Year"], 
        y=comp_meat_5["Veal"],
        name = "Veal",
        marker = {'color' : "#f7fcb9"},
        hovertemplate = '%{y} kg<extra></extra>'
    ),
    row=2, col=1
)

fig_barchart.add_trace(
    go.Bar(
        x=comp_meat_5["Year"], 
        y=comp_meat_5["Chicken"],
        name = "Chicken",
        marker = {'color' : "#74a9cf"},
        hovertemplate = '%{y} kg<extra></extra>'
    ),
    row=1, col=2
)

fig_barchart.add_trace(
    go.Bar(
        x=comp_meat_5["Year"], 
        y=comp_meat_5["Pig"],
        name = "Pig",
        marker = {'color' : "#045a8d"},
        hovertemplate = '%{y} kg<extra></extra>'
    ),
    row=2, col=2
)

fig_barchart.update_layout(
    showlegend=False, 
    height=600, 
    title_text="Meat Consumption per Person per Year [in kg]",
    font=dict(
        family="Helvetica, sans-serif",
        size=15,
        color="black"
    )
)

# Pig
fig_barchart.update_yaxes(range=[0, 25], row=2, col=2)
# Cow
fig_barchart.update_yaxes(range=[0, 25], row=1, col=1)
# Veal
fig_barchart.update_yaxes(range=[0, 25], row=2, col=1)
# Chicken
fig_barchart.update_yaxes(range=[0, 25], row=1, col=2)

# Pig
# fig_barchart.update_yaxes(range=[0, 35], row=2, col=2)
# Cow
# fig_barchart.update_yaxes(range=[0, 13], row=1, col=1)
# Veal
# fig_barchart.update_yaxes(range=[0, 4], row=2, col=1)
# Chicken
# fig_barchart.update_yaxes(range=[0, 13], row=1, col=2)

fig_barchart.layout.paper_bgcolor = paper_bgcolor
fig_barchart.layout.plot_bgcolor = plot_bgcolor
#fig_barchart.update_layout(hovermode="x")




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
    tmp_1 = pd.DataFrame({'Year':[y],'Size':["Up to 10 hectares"],'Count':[count_size_1]})
    grouped_bub = pd.concat([grouped_bub,  tmp_1], ignore_index=True)
    
    # Create new size "Up to 50 hectare"
    query_2 = "Year==" + str(y) + " and (Size=='10  - <  20 ha' or Size=='20  - <  30 ha' or Size=='30  - < 50 ha')"
    count_size_2 = org_farm_5.query(query_2).sum().Number
    tmp_2 = pd.DataFrame({'Year':[y],'Size':["Up to 50 hectares"],'Count':[count_size_2]})
    grouped_bub = pd.concat([grouped_bub,  tmp_2], ignore_index=True)
    
    # Create new size "50+ hectare"
    query_3 = "Year==" + str(y) + " and (Size=='50  +  ha')"
    count_size_3 = org_farm_5.query(query_3).sum().Number
    tmp_3 = pd.DataFrame({'Year':[y],'Size':["Over 50 hectares"],'Count':[count_size_3]})
    grouped_bub = pd.concat([grouped_bub,  tmp_3], ignore_index=True)

# keep nice colormap for maybe later reference
color_map_bubble = {
    "Up to 10 hectares":"#addd8e",
    "Up to 50 hectares":"#f7fcb9",
    "Over 50 hectares":"#74a9cf"
}

fig_bubble = px.scatter(
    grouped_bub, 
    x="Year", 
    y="Size",
	size="Count",
    color="Size",
    size_max = 100,
    color_discrete_map = color_map_bubble,
    hover_data={'Year':False}
)

fig_bubble.update_layout(
    showlegend=False, 
    title_text="Land Usage of Organic Farms",
    xaxis_title="Year",
    yaxis_title="Size of farm",
    font=dict(
        family="Helvetica, sans-serif",
        size=15,
        color="black"
    )
)


fig_bubble.layout.paper_bgcolor = paper_bgcolor
fig_bubble.layout.plot_bgcolor = plot_bgcolor

# ---------- #
#    Text    #
# ---------- #
text_intro = "With this data storytelling we want to figure out what the Swiss people eat and how their diet has changed over the last years. We are particularly interested in whether there is a correlation between the change in our eating habits and the increased awareness of climate change. In our close environment there are more and more vegetarians / vegans, and more and more people buy organic food. Can this development also be observed in the Swiss population, or are our feelings deceiving us? We want to get to the essence of these questions and find possible answers through our visualisations."

text_foodtype1 = "To get a good overview of the eating habits of the Swiss, let's look at the distribution of the different food-types in our daily diet. The graph below shows the annual amount of food consumed per person in kilograms."
text_foodtype2 = "At first glance, our diet consists largely of plant-based foods. We mostly eat vegetables and fruits (222 kg/year), in addition to a large proportion of carbohydrates such as wheat and potatoes (177 kg/year). The main part of our animal diet consists of dairy products and less than a quarter is our meat consumption. Nevertheless, the consumption of meat (excluding fish) per person amounts to 47 kg per year. This corresponds to the weight of 31 chickens, eaten per person each year – in our opinion way too much, as meat is mainly responsible for rising CO2 emissions."

text_meat1 = "As we have seen from the previous presentation, the Swiss still eat a lot of meat. But what exactly is the composition of this meat consumption? From which animals do we eat how much? And has there been a change in consumption among the individual animal species? Let’s have a look at it…"
text_meat2 = "There have been different developments over the years for the different animal species. The consumption of veal and pig has decreased considerably. Especially in the case of veal, consumption has shrunk from 3.3 kg per person / per year to 2 kg. A totally different behaviour can be observed with cow and chicken. Here, consumption has steadily increased and is currently at its highest level since 2000. An explanation for this different development is not trivial and cannot be answered based on the data analysis. Nevertheless, the overall decrease in meat consumption is more significant than the increase in the consumption of cow and chicken. This could indeed be related to people's attitudes towards climate change and the importance of animal welfare, which is not given by factory farming. However, it cannot be clearly clarified based on our visualisation but we’re happy to see that at least a little less meat is eaten."

text_organic1 = "Since there is a visible change in meat consumption, we asked ourselves whether the Swiss also attach more importance to organic quality in food or if this has become more important for them. We were particularly interested in the difference between the sexes. Do more women or more men buy organic products? And how has this changed in recent years?"
text_organic2 = "At first glance, it is immediately noticeable that there was a large increase and over 50% of men always or almost always buy organic products. Among women who always buy organic, the value decreased slightly. We cannot explain this change directly as it depends on many different factors. This increase in the purchase of organic products among men is proportionally also directly visible through the decreasing share of those who rarely buy organic products. Here the proportion has decreased accordingly. Among those who buy organic products from time to time, the proportion has increased for both genders and is almost at the same level in 2019."

text_farms1 = "According to the results of the survey above, the Swiss population is increasingly buying organic products. So, there should also be a noticeable change in the number or size of organic farms. Does this correspond to the facts?"
text_farms2 = "It is clearly visible that something has changed on organic farms in the last 20 years. The biggest change is visible on farms larger than 50 hectares. The number of these farms has increased almost ten times from 62 to 517, which is an enormous growth. The number of farms up to 50 hectares also increased considerably from 3,487 to 5,571. The small farms saw the smallest change of slightly more than 100 more farms over the years."

text_conclusion = "The eating habits of the Swiss have changed more than expected over the last 20 years: consumption of certain types of meat, such as pigs and calves, has decreased significantly, while consumption of cows and chickens has surprisingly increased. Despite this increase, the diet of the average Swiss is largely plant-based and if animal products are consumed, it is mainly dairy products. The biggest change has probably been in behaviour towards organic products, and here our visualisations are in line with the general organic boom. In the last few years, this sector has grown strongly as the demand for organic has risen sharply. This change is also clearly visible in the number of organic farms and a rising trend is emerging. In the end, the Swiss will have to continue to change their diet and a declining trend would have to be observed in the future, especially in meat consumption, so that global warming can be stopped or at least slowed down. With this high consumption of meat and animal products, it is not possible to achieve the climate goals - even despite the increasing demand for organic products."

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
    "font-size": 15,
}

sidebar = html.Div(
    [
        html.H2("Table of Contents", className="display-4"),
        html.Hr(),
        dbc.Nav(
            [
                dbc.NavItem(dbc.NavLink("Intro", href="http://127.0.0.1:8050/buying_organic#intro", active="exact", class_name="navlink")),
                html.Br(),
                dbc.NavItem(dbc.NavLink("Type of Food Consumed", href="http://127.0.0.1:8050/buying_organic#sunburst", active="exact", class_name="navlink")),
                html.Br(),
                dbc.NavItem(dbc.NavLink("Meat Consumption", href="http://127.0.0.1:8050/buying_organic#meat_consumption", active="exact", class_name="navlink")),
                html.Br(),
                dbc.NavItem(dbc.NavLink("Shopping Organic Groceries", href="http://127.0.0.1:8050/buying_organic#buying_organic", active="exact", class_name="navlink")),
                html.Br(),
                dbc.NavItem(dbc.NavLink("Land Usage of Organic Farms", href="http://127.0.0.1:8050/buying_organic#organic_farms", active="exact", class_name="navlink")),
                html.Br(),
                dbc.NavItem(dbc.NavLink("Conclusion", href="http://127.0.0.1:8050/buying_organic#conclusion", active="exact", class_name="navlink")),
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
        html.H1("Changes in the Eating Habits of the Swiss"),
        html.P(text_intro),
    ]),
    
    # sunburst
    html.Div([
        html.P("", id="sunburst"),
        html.H2("Type of Food Consumed in 2020"),
        html.P(text_foodtype1),
        html.Br(), 
        dcc.Graph(figure=fig_sunburst),
        html.Label("Datasource: https://www.bfs.admin.ch/bfs/de/home/statistiken/kataloge-datenbanken/tabellen.assetdetail.20904914.html"),
        html.P(text_foodtype2),
        html.Br(),
    ]),
    
    # Meat Consumption
    html.Div([
        html.P("", id="meat_consumption"),
        html.H2("Meat Consumption"),
        html.P(text_meat1),
        html.Br(), 
        dcc.Graph(figure=fig_barchart),
        html.Label("Datasource: https://www.bfs.admin.ch/bfs/de/home/statistiken/kataloge-datenbanken/tabellen.assetdetail.20904916.html"),
        html.Br(),
        html.P(text_meat2),
        html.Br()
    ]),
    
    
    # Buying organic
    html.Div([
        html.P("", id="buying_organic"),
        html.H2("Shopping Organic Groceries"),
        html.P(text_organic1),
        html.Br(), 
        dcc.Graph(figure=fig_line_org),
        html.Label("Datasource: https://www.bfs.admin.ch/bfs/de/home/statistiken/kataloge-datenbanken/tabellen.assetdetail.11708774.html"),
        html.Br(),
        html.P(text_organic2),
        html.Br()
    ]),
    
 
    # Organic Farms
    html.Div([
        html.P("", id="organic_farms"),
        html.H2("Land Usage of Organic Farms"),
        html.P(text_farms1),
        html.Br(), 
        dcc.Graph(figure=fig_bubble),
        html.Label("Datasource: https://www.bfs.admin.ch/bfs/de/home/statistiken/kataloge-datenbanken/tabellen.assetdetail.17064714.html"),
        html.Br(),
        html.P(text_farms2),
        html.Br()
    ]),
    
    html.Div([
        html.P("", id="conclusion"),
        html.H2("Conclusion"),
        html.P(text_conclusion),
    ]),
    
    # Source
    html.Div([
        #html.H4("Sources:"),
        #html.P("https://www.bfs.admin.ch/bfs/de/home/statistiken/kataloge-datenbanken/tabellen.html"),
        html.Footer("Masterminds behind this project: Johanna Koch and Nadja Kaufmann, AI & ML student at HSLU-I 😎")
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