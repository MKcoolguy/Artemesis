import dash
from dash.dependencies import Input, Output, State
from dash import html
from dash import dcc
import dash_bootstrap_components as dbc
import plotly.express as px

from dashboard import app

# The actual site structure is located in index.py and the dash app itself is located in dashboard.py
# The content loaded in the page-content container in index.py are located here.
# If you want to add more, follow the below examples. Put the layout first and the associated callbacks below it.

# Index/Home Page
# Layout
home = html.Div([
    dbc.Row(
        [
            dbc.Col(html.Div( #no callbacks for any of these set up yet, just proof of concept
                [
                dbc.ButtonGroup([dbc.Button("THIS"), dbc.Button("DOES"), dbc.Button("STUFF")]),
                dbc.Button("STUFF 1", color="secondary", className="me-1"),
                dbc.Button("STUFF 2", color="secondary", className="me-1"),
                dbc.Button("STUFF 3", color="secondary", className="me-1"),
                dbc.Button("STUFF 4", color="secondary", className="me-1"),
                dbc.Button("STUFF 5", color="secondary", className="me-1"),
                dbc.ButtonGroup([dbc.Button("THIS"), dbc.Button("IS"), dbc.Button("STUFF")]),
                ],
                className="d-grid gap-2 d-md-flex justify-content-md-center",
            )),
        ]
    ),
    dbc.Row(  # TOP ROW OF QUADRANT
        [
            dbc.Col(html.Div(  # QUADRANT ONE
            )),
            dbc.Col(html.Div(  # QUADRANT TWO
                    dcc.Graph(
                        figure=px.scatter(px.data.gapminder().query("year == 2007"), x="gdpPercap", y="lifeExp",
                                          title="QUADRANT 2 SAMPLE GRAPH")
                    )
                    )),
        ]
    ),
    dbc.Row(  # BOTTOM ROW OF QUADRANT
        [
            dbc.Col(html.Div(  # QUADRANT THREE

            )),
            dbc.Col(html.Div(  # QUADRANT FOUR
                dcc.Graph(
                    figure=px.scatter(px.data.iris(), x="sepal_length", y="sepal_width", color="species",
                                      title="QUADRANT 4 SAMPLE GRAPH"))
            )
            )
        ]
    ),
])

# Index/home page callbacks


# Graphs Page
# Layout
graph = html.Div(
    [
        dbc.Button(
            "Toggle Graph", id="fade-button", className="mb-3", n_clicks=0
        ),
        dbc.Fade(
            dbc.Card(
                dbc.CardBody(
                    dcc.Graph(
                        figure={
                            'data': [
                                {'x': [1, 2, 3], 'y': [4, 1, 2],
                                 'type': 'bar', 'name': 'SF'},
                                {'x': [1, 2, 3], 'y': [2, 4, 5],
                                 'type': 'bar', 'name': u'Montréal'},
                            ],
                            'layout': {
                                'title': 'Dash Data Visualization'
                            }
                        }
                    )
                )
            ),
            id="fade",
            is_in=False,
            appear=False,
        ),
    ]
)

# Graph Page Callbacks
# fade button


@ app.callback(
    Output("fade", "is_in"),
    [Input("fade-button", "n_clicks")],
    [State("fade", "is_in")],
)
def toggle_fade(n, is_in):
    if not n:
        # Button has never been clicked
        return False
    return not is_in
