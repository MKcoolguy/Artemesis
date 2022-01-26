from dash import html
from dash import dcc
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd

from dashboard import app
from layouts import home, graph

#This file is the main dash server, always run index.py, do not run dashboard.py.

#We will see this layout on every page.
#The way dash works is that its a "single-page layout", so when you have multiple pages, it just reloads the layout but maintains the index layout
#when set up to support multiple pages. So when we click another page, the "main" index layout will stay the same and it will just change the contents of the page.
#What is in this layout below will be present on every single page on our dashboard.
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    dbc.NavbarSimple(
       children=[
          dbc.NavLink("Home", href="/", active="exact"), #These navlinks are part one of the multi page functionality. Obviously, button to another page.
          dbc.NavLink("Graph", href="/graph", active="exact"),
       ],
       brand="S.A.U.C.E. 2.0",
       color="primary",
       dark=True,
    ),
    dbc.Container(id="page-content", className="pt-4"), #Part two of the multi-page functionality. The layout called on button click in the below callback will be placed inside the page-content container.
])

#Should we decide to segregate all of our callbacks into a seperate .py file, this is the one that must remain here as it allows us to use multiple pages.
#This is part three of the multi-page functionality.
#When the user clicks on one of the navbar buttons, it references a pathname. This callback takes that pathname, converts it to a layout, and then reloads
#the page-content container with the appropriate layout located in layouts.py.
@app.callback(Output('page-content', 'children'),
              Input('url', 'pathname'))
def display_page(pathname): 
    if pathname == '/':
        return home
    elif pathname == '/graph':
        return graph
    else:
        return '404'

if __name__ == '__main__':
    app.run_server(debug=True)