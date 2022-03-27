from tkinter.ttk import Style
from urllib import request
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
from sympy import im
from figures import Graphs
from figures import ArchivedData
import os
from subprocess import call
from dash.exceptions import PreventUpdate
import cv2
from flask import Flask, Response
cwd = os.path.dirname(__file__)  # Used for consistent file detection.

class VideoCamera(object):
    def __init__(self):
        self.video = cv2.VideoCapture(0)

    def __del__(self):
        self.video.release()

    def get_frame(self):
        success, image = self.video.read()
        ret, jpeg = cv2.imencode('.jpg', image)
        return jpeg.tobytes()


server = Flask(__name__)
#app = dash.Dash(__name__, server=server)
app = JupyterDash(external_stylesheets=[dbc.themes.SLATE], server=server, suppress_callback_exceptions=True)
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

def gen(camera):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')


@server.route('/video_feed')
def video_feed():
    return Response(gen(VideoCamera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


my_stream = html.Div([
    #html.H1("Webcam Test"),
    #html.Img(src="/video_feed")

    dbc.Card(
            dbc.CardBody([
                html.Div([
                    html.Img(src="/video_feed", style ={'align': 'center', 'height': '100%','width': '100%'})
                ], style={'textAlign': 'center'}),
            ])
        ),
])

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
                #Camera feed
                dbc.Col([
                  my_stream
                ], width=6),
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
        temp_filepath = os.path.join(cwd, 'assets/temperature.py')
        exec(open(temp_filepath).read())
        '''
        return html.Div([
            html.H3('Temp Sensor On')
        ])'''
    elif tab == 'distance-sensor':
        from assets import app_utils
        app_utils.Temperature.get_data()
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

if __name__ == '__main__':
    app.run_server(debug=True)