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

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    dbc.NavbarSimple( #Bootstrap Navbar
       children=[
          dbc.NavLink("Home", href="/", active="exact"),
          dbc.NavLink("Graph", href="/graph", active="exact"),
       ],
       brand="S.A.U.C.E. 2.0",
       color="primary",
       dark=True,
    ),
    dbc.Container(id="page-content", className="pt-4"),
])

#This is the callback function that updates the page after selection with the appropriate layout.
#Because of how this works, this is the one callback function that we cannot segregate into either layouts.py or callbacks.py
#depending on how we want to do it going forward.
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