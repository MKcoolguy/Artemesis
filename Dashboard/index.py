import base64
import os
import socket
import whatismyip
import cv2
import dash
import dash_bootstrap_components as dbc
from dash import dcc, html
from dash.dependencies import Input, Output
from flask import Flask, Response
from jupyter_dash import JupyterDash

from scipy.fft import dst

from CrackDetectionDir import CrackDetection
from figures import ArchivedData, Graphs
from pi_camera import VideoCamera

cwd = os.path.dirname(__file__)  # Used for consistent file detection.

server = Flask(__name__)
app = JupyterDash(external_stylesheets=[dbc.themes.SLATE], server=server, suppress_callback_exceptions=True)


# Generate camera frame
def video_gen(camera):
    while True:
        success, image = camera.get_frame()
        ret, jpeg = cv2.imencode('.jpg', image)
        frame = jpeg.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')


# Video feed route
@server.route('/video_feed')
def video_feed():
    return Response(video_gen(VideoCamera),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


# Base layout for all webpages

# added school logos in navigation bar
logo = html.Img(src='https://colleges-static.raise.me/georgia-gwinnett-college/logo-120x120.png', style={'align': "center",'height': '100%', 'width': '100%'})
logo2 = html.Img(src='https://i.ytimg.com/vi/xq0ycmmlvII/maxresdefault.jpg', style={'align': 'center', 'height':'100%','width':'100%'})

app.layout = html.Div([
    logo2,
    dbc.NavbarSimple(
       children=[
          dbc.NavLink(logo),
          dbc.NavLink("Home", href="/", active="exact"),
          dbc.NavLink("Archived Data", href="/archivedData", active="exact"),
       ],
       brand="S.A.U.C.E. 2.0",
       color="Black",
       dark=True,

    ),
    # represents the browser address bar and doesn't render anything
    dcc.Location(id='url', refresh=False),
    # content will be rendered in this element
    html.Div(id='page-content')
])

# Live Camera Stream component
my_stream = html.Div([
    dbc.Card(
        dbc.CardBody([
            html.Div([
                html.Img(src="/video_feed", style={'align': 'center', 'height': '100%', 'width': '100%'})
            ], style={'textAlign': 'center'}),
        ])
    ),
])

# Crack Detection Stream component
my_stream_crack_detect = html.Div([
    dbc.Card(
        dbc.CardBody([
            html.Div([
                html.H4("Crack Detector"),
                dcc.Interval(
                    id='graph-update',
                    interval=1000,
                    n_intervals=0
                ),
                html.Img(id="image", src=app.get_asset_url('test_0.png'),
                         style={'align': 'center', 'height': '100%', 'width': '100%'})
            ])
        ], style={'textAlign': 'center'}),
    ),
])


# Styling function for text blocks
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


# Home page
home = html.Div([
    dcc.Tabs(id="tabs-styled-with-props", value='tab-1', children=[
        dcc.Tab(label='Temperature Sensor On/Off', value='temp-sensor'),
        dcc.Tab(label='Distance Sensor On/Off', value='distance-sensor'),
        dcc.Tab(label='Camera On/Off', value='camera-feed'),
        dcc.Tab(label='All On/Off', value='all-plugins'),
    ], colors={
        "border": "Black",
        "primary": "Sienna",
        "background": "SeaGreen"
    }), html.Div(id='tabs-content-props'),
    dbc.Card(
        dbc.CardBody([
            dbc.Row([
                dbc.Col([
                    # Temperature
                    html.Div(id="live-update-text"),
                    dcc.Interval(
                        id='interval-component-2',
                        interval=1 * 1000,  # in milliseconds
                        n_intervals=0
                    )
                ], width=6),
                dbc.Col([
                    # Distance
                    html.Div(id="live-update-text-2"),
                    dcc.Interval(
                        id='interval-component-4',
                        interval=1 * 1000,  # in milliseconds
                        n_intervals=0
                    )
                ], width=6),
            ], align='center'),
            html.Br(),
            dbc.Row([
                # Camera feed
                dbc.Col([
                    my_stream
                ], width=8),
                dbc.Col([
                    # Distance/Time Graph
                    html.Div([
                        dbc.Card(
                            dbc.CardBody([
                                dcc.Graph(
                                    id='distGraph',
                                    figure=Graphs.createDistanceGraph()),
                                dcc.Interval(
                                    id='interval-component-3',
                                    interval=1 * 1000,
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
                    # Temperature/Time Graph
                    html.Div([
                        dbc.Card(
                            dbc.CardBody([
                                dcc.Graph(
                                    id='tempGraph',
                                    figure=Graphs.createTempGraph()),
                                dcc.Interval(
                                    id='interval-component',
                                    interval=1 * 1000,
                                    n_intervals=0
                                )
                            ])
                        )
                    ]),
                ], width=6),
                dbc.Col([
                    # Crack detection Stream
                    my_stream_crack_detect
                ], width=6),
            ], ),
        ]), color='SeaGreen'
    )
])

# TODO add filepath for local archived data and create function to rename files with timestamp at the end of file name
filepath = os.path.join(cwd, 'assets/data/temperature.csv')
archived_data_page = html.Div([
    # dcc.Link('temperature.csv', href = filepath),
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


##Gets real time distance vlaue
@app.callback(
    Output('live-update-text-2', 'children'),
    Input('interval-component-4', 'n_intervals'))
def refresh_temp_value(n_clicks):
    recent_distance = Graphs.get_most_recent_distance()
    format_float = "{:.2f}".format(recent_distance)
    return drawText('Distance: %s cm' % format_float)


##Crack detection stream
@app.callback(
    Output('image', 'src'),
    Input('graph-update', 'n_intervals'))
def update_snapshot(n):
    frame = VideoCamera.get_photo()
    frame2 = CrackDetection.do_this(frame)
    _, buffer = cv2.imencode('.png', frame2)
    source_image = base64.b64encode(buffer).decode('utf-8')
    return 'data:image/png;base64,{}'.format(source_image)


##Save snapshop feature
##@app.callback(
##def save_snapshots(cap, 'snapshot.jpg')
##)

##Callback for turning the sensors and camera on and off
# TODO plug the script in to toggle sensors and camera
@app.callback(
    Output('tabs-content-props', 'children'),
    Input('tabs-styled-with-props', 'value'))
def render_content(tab):
    if tab == 'temp-sensor':
        temp_filepath = os.path.join(cwd, 'assets/temperature.py')
        exec(open(temp_filepath).read())
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
            html.H3('Temperature Sensor, Distance Sensor, and Camera Live-Feed On')
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
#Authentication
passWord = []
userName = []
it = 0
it2 = 0
with open("Users.txt") as openfileobject:
    for line in openfileobject:
        it+=1
        if (it%2 != 0):
            userName.append(line.rstrip('\n'))
            print(userName)
        else :
            passWord.append(line.rstrip("\n"))
            print(passWord)


for x in userName:
    VALID_USERNAME_PASSWORD_PAIRS = {
        userName[userName.index(x)]: passWord[userName.index(x)]
    }




##auth = dash_auth.BasicAuth(
    app,
    VALID_USERNAME_PASSWORD_PAIRS
##)

##Grabbing local ip

addressraw = whatismyip.whatismylocalip()
address = ''
for item in addressraw:
    address = address + item

# Run application
if __name__ == '__main__':
    print(address)
    app.run_server(debug=True, host=address, port=8050)
