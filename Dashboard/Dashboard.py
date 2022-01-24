import dash
from dash import html
from dash import dcc
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import plotly.express as px

app = dash.Dash(__name__,external_stylesheets=[dbc.themes.CYBORG])

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    dbc.NavbarSimple(
       children=[
          dbc.NavLink("test page 1", href="/", active="exact"),
          dbc.NavLink("test page 2", href="/", active="exact"),
          dbc.NavLink("test page 3", href="/", active="exact")
       ],
       brand="S.A.U.C.E. 2.0",
       color="primary",
       dark=True,
    ),
    dbc.Container(id="page-content", className="pt-4"),
])
if __name__ == '__main__':
    app.run_server(debug=True)