import dash
from dash.dependencies import Input, Output, State
from dash import html
from dash import dcc
import dash_bootstrap_components as dbc

from dashboard import app

# Each one of these will contain the general design of a page based on the name of the layout. Bootstrap is used for most of our CSS needs.
# The actual site structure is located in index.py and the dash app itself is located in dashboard.py

#index/home page.
home = html.Div([
    dbc.Button("cool button", id="cool-button", n_clicks=0),
    dbc.Offcanvas(
        html.P(
            "This is a really cool button to test a really cool page"
        ),
        id="offcanvas-cool-button",
        title="we like to test",
        is_open=False,
    ),
]
)
# Index/home page callbacks
# home cool-button.
@app.callback(
    Output("offcanvas-cool-button", "is_open"),
    Input("cool-button", "n_clicks"),
    [State("offcanvas-cool-button", "is_open")],
)
def toggle_offcanvas(n1, is_open):
    if n1:
        return not is_open
    return is_open


# Graph page
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
@app.callback(
    Output("fade", "is_in"),
    [Input("fade-button", "n_clicks")],
    [State("fade", "is_in")],
)
def toggle_fade(n, is_in):
    if not n:
        # Button has never been clicked
        return False
    return not is_in
