import dash
from dash import dcc
from dash import html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from jupyter_dash import JupyterDash
from scipy.fft import dst
from sklearn import utils
from figures import Graphs
from figures import ArchivedData
from assets import utils
import os
import subprocess
cwd = os.path.dirname(__file__)  # Used for consistent file detection.


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
    dbc.NavbarSimple(
       children=[
          dbc.NavLink("Home", href="/", active="exact"),
          dbc.NavLink("Archived Data", href="/archivedData", active="exact"),
       ],
       brand="S.A.U.C.E. 2.0",
       color="primary",
       dark=True,
    ),
    # represents the browser address bar and doesn't render anything
    dcc.Location(id='url', refresh=False),
    # content will be rendered in this element
    html.Div(id='page-content')
])



home = html.Div([
    dcc.Tabs(id="tabs-styled-with-props", value='tab-1', children=[
        dcc.Tab(label='Temperature Sensor On/Off', value='temp-sensor'),
        dcc.Tab(label='Distance Sensor On/Off', value='distance-sensor'),
        dcc.Tab(label='Camera On/Off', value='camera-feed'),
        dcc.Tab(label='All On/off', value='all-plugins'),
    ], colors={
        "border": "black",
        "primary": "Silver",
        "background": "dark"
    }), html.Div(id='tabs-content-props'),
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
                ], width=3),
                dbc.Col([
                    #Distance
                    html.Div(id="live-update-text-2"),
                    dcc.Interval(
                        id='interval-component-4',
                        interval=1*1000, # in milliseconds
                        n_intervals=0
                        )
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
                    html.Div([
                        dbc.Card(
                            dbc.CardBody([
                                dcc.Graph(
                                    id='distGraph',
                                    figure=Graphs.createDistanceGraph()),
                                    dcc.Interval(
                                        id='interval-component-3',
                                        interval=1*1000,
                                        n_intervals=0
                                    )
                            ])
                        )
                    ]),
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


# TODO add filepath for local archived data and create function to rename files with timestamp at the end of file name
filepath = os.path.join(cwd, 'assets/data/temperature.csv')
archived_data_page = html.Div([
    #dcc.Link('temperature.csv', href = filepath),
    ArchivedData.get_all_data('assets/data/')
    
])


##Updates the temperature/time graph.
@app.callback(
    dash.dependencies.Output('tempGraph', 'figure'),
    dash.dependencies.Input('interval-component', 'n_intervals'))
def refresh_data(n_clicks):
    return Graphs.createTempGraph()


##Updates the distance/time graph.
@app.callback(
    dash.dependencies.Output('distGraph', 'figure'),
    dash.dependencies.Input('interval-component-3', 'n_intervals'))
def refresh_data(n_clicks):
    return Graphs.createDistanceGraph()


##Gets real time temp vlaue
@app.callback(
    Output('live-update-text', 'children'),
    Input('interval-component-2', 'n_intervals'))
def refresh_temp_value(n_clicks):
    recent_temp = Graphs.get_most_recent_temp()
    return drawText('Temperature: %s F' % recent_temp)


##Gets real time ditance vlaue
@app.callback(
    Output('live-update-text-2', 'children'),
    Input('interval-component-4', 'n_intervals'))
def refresh_temp_value(n_clicks):
    recent_distance = Graphs.get_most_recent_distance()
    format_float = "{:.2f}".format(recent_distance)
    return drawText('Distance: %s cm' % format_float)


##Callback for turning the sensors and camera on and off
# TODO plug the script in to toggle sensors and camera
@app.callback(
    Output('tabs-content-props', 'children'),
    Input('tabs-styled-with-props', 'value'))
def render_content(tab):
    if tab == 'temp-sensor':
        #utils.Temperature.run_temp_script()
        temp_filepath = os.path.join(cwd, 'assets/temperature.py')
        subprocess.call(temp_filepath, shell=True)
        #os.system(temp_filepath)
        return html.Div([
            html.H3('Temp Sensor On')
        ])
    elif tab == 'distance-sensor':
        dist_filepath = os.path.join(cwd, 'assets/distance.py')
        os.system(dist_filepath)
        return html.Div([
            html.H3('Distance Sensor On')
        ])
    elif tab == 'camera-feed':
        stream_filepath = os.path.join(cwd, 'assets/stream.py')
        os.system(stream_filepath)
        return html.Div([
            html.H3('Camera On')
        ])
    elif tab == 'all-plugins':
        return html.Div([
            html.H3('Temperature Sensor, Distance Sensor, and Camera Feed On')
        ])

##Callback for webpages
@app.callback(
    Output('page-content', 'children'),
    Input('url', 'pathname'))
def display_page(pathname):
    if pathname == '/':
        return home
    elif pathname == '/archivedData':
        return archived_data_page

    

# Run app and display result inline in the notebook
if __name__ == "__main__":
    app.run_server(host='0.0.0.0', port='8050', mode='external')