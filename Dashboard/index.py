import dash
from dash import dcc
from dash import html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from jupyter_dash import JupyterDash
from figures import Graphs

# Text field
def drawText(user_value):
    return html.Div([
        dbc.Card(
            dbc.CardBody([
                html.Div([
                    user_value
                ], style={'textAlign': 'center'}),
                
            ])
        ),
    ])



# Build App
app = JupyterDash(external_stylesheets=[dbc.themes.SLATE])
app.layout = html.Div([
    dbc.Card(
        dbc.CardBody([
            dbc.Row([
                dbc.Col([
                    #Temperature
                    html.Div(id="live-update-text"),
                    dcc.Interval(
                        id='interval-component-2',
                        interval=1*1000, # in milliseconds
                        n_intervals=0
                        )
                    #drawText(recent_temp)
                ], width=3),
                dbc.Col([
                    drawText("Testing...")
                ], width=3),
                dbc.Col([
                    drawText("Testing...")
                ], width=3),
                dbc.Col([
                    drawText("Testing...")
                ], width=3),
            ], align='center'), 
            html.Br(),
            dbc.Row([
                dbc.Col([
                    Graphs.drawFigure() 
                ], width=3),
                dbc.Col([
                    Graphs.drawFigure()
                ], width=3),
                dbc.Col([
                    Graphs.drawFigure() 
                ], width=6),
            ], align='center'), 
            html.Br(),
            dbc.Row([
                dbc.Col([
                    #Temperature/Time Graph
                    html.Div([
                        dbc.Card(
                            dbc.CardBody([
                                dcc.Graph(
                                    id='tempGraph',
                                    figure=Graphs.createTempGraph()),
                                    dcc.Interval(
                                        id='interval-component',
                                        interval=1*1000,
                                        n_intervals=0
                                    )
                            ])
                        )
                    ]),
                ], width=9),
                dbc.Col([
                    Graphs.drawFigure()
                ], width=3),
            ], align='center'),      
        ]), color = 'dark'
    )
])

##Updates the temperature/time graph.
@app.callback(
    dash.dependencies.Output('tempGraph', 'figure'),
    dash.dependencies.Input('interval-component', 'n_intervals'))
def refresh_data(n_clicks):
    return Graphs.createTempGraph()


##Gets real time temp vlaue
@app.callback(
    Output('live-update-text', 'children'),
    Input('interval-component-2', 'n_intervals'))
def refresh_temp_value(n_clicks):
    recent_temp = Graphs.get_most_recent_temp() #Stores
    return drawText(recent_temp)


# Run app and display result inline in the notebook
if __name__ == "__main__":
    app.run_server(host='0.0.0.0', port='8050', mode='external')