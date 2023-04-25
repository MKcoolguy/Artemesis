import base64
import os
import socket
import dash
import whatismyip
import cv2
import dash_auth
import dash_bootstrap_components as dbc
import datetime
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
logo = html.Img(src='https://colleges-static.raise.me/georgia-gwinnett-college/logo-120x120.png')
brand_text = html.Div([
    html.Span('S.A.U.C.E.'),
    html.Span('2.0', style={'font-weight': 'bold'})
])

#Base layout for all webpages
app.layout = html.Div([
    html.H1('The time is: ' + str(datetime.datetime.now())),
    dbc.Row(
        dbc.Col(
            html.Img(src='https://colleges-static.raise.me/georgia-gwinnett-college/logo-120x120.png'),
            width=10,
            align="center"
        ),
        justify="center",
        style={"background-color": "seagreen", "padding": "10px","border-bottom":"0px"}

    ),
    ## Drop-Down menu
    dbc.Row(
        dbc.DropdownMenu(
        children=[
            dbc.DropdownMenuItem(dbc.NavLink("Github", href="https://github.com/soft-eng-practicum/Artemis")),
            dbc.DropdownMenuItem(dbc.NavLink("Summary Poster", href="https://ggcedu.sharepoint.com/:p:/r/sites/APL/_layouts/15/Doc.aspx?sourcedoc=%7BA6BFB3D3-0AA6-4612-99E0-5825D0227F5D%7D&file=NASA-MINDS-Poster.pptx&action=edit&mobileredirect=true")),
            dbc.DropdownMenuItem(dbc.NavLink("Semester Plan", href="https://sway.office.com/vzl8CVGTqe7gqqzH?ref=Link")),
        ],
        direction = "up",
        toggle_style={
            "font-color" : "seagreen",
            "textTransform": "uppercase",
            "background": "#4f2400",
        },
        toggleClassName="fst-italic border border-dark",
        label='Artemis Mission',
        color="seagreen",
    ),
        style={"background-color": "seagreen", "padding": "10px", "border-bottom": "0px"}
    ),
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content'),
])

#Live Camera Stream component
my_stream = html.Div([
    dbc.Card(
            dbc.CardBody([
                html.Div([
                    html.Img(src="/video_feed", style ={'align': 'center', 'height': '50%','width': '50%' })
                ], style={'textAlign': 'center'}),
            ])
        ),
])

#Crack Detection Stream component
my_stream_crack_detect = html.Div([
    dbc.Card(
            dbc.CardBody([
                html.Div([
                    html.H4("Crack Detector"),
                                    dcc.Interval(
                                    id = 'graph-update',
                                    interval = 1000,
                                    n_intervals = 0
                    ),
                    html.Img(id="image", src=app.get_asset_url('test_0.png'), style ={'align': 'center', 'height': '50%','width': '50%'})
                            ])
                ], style={'textAlign': 'center'}),
    ),
            ])

#Styling function for text blocks
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

#Home page
home = html.Div([
    dcc.Tabs(id="tabs-styled-with-props", value='tab-1', children=[
        dcc.Tab(label='Temperature Sensor On/Off', value='temp-sensor'),
        dcc.Tab(label='Distance Sensor On/Off', value='distance-sensor'),
        dcc.Tab(label='Camera On/Off', value='camera-feed'),
        dcc.Tab(label='All On/Off', value='all-plugins'),
    ], colors={
        "border": "black",
        "primary": "seagreen",
        "background": "seagreen"
    }), html.Div(id='tabs-content-props'),

    dbc.Card(
        dbc.CardBody([
                dcc.Slider(
                    id='data-collection-slider',
                    min=1,
                    max=5,
                    step=1,
                    value=10,
                    marks={i: str(i) for i in range(1, 5)}
                ),
            dbc.Row([
                dbc.Col([
                    #Temperature
                    html.Div(id="live-update-text"),
                    dcc.Interval(
                        id='interval-component-2',
                        interval=1*1000, # in milliseconds
                        n_intervals=0
                        )
                ], width=6),
                dbc.Col([
                    #Distance
                    html.Div(id="live-update-text-2"),
                    dcc.Interval(
                        id='interval-component-4',
                        interval=1*1000, # in milliseconds
                        n_intervals=0
                        )
                ], width=6),
            ], align='center'),
            html.Br(),
            dbc.Row([
                #Camera feed
                dbc.Col([
                  my_stream
                ], width=6),
                dbc.Col([
                    #Distance/Time Graph
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
                ], width=6),
                dbc.Col([
                        #Crack detection Stream
                        my_stream_crack_detect
                ], width=6),
            ], ),
        ]), color = 'seagreen'
    )
])

# TODO add filepath for local archived data and create function to rename files with timestamp at the end of file name
filepath = os.path.join(cwd, 'assets/data/temperature.csv')
archived_data_page = html.Div([
    # dcc.Link('temperature.csv', href = filepath),
    ArchivedData.get_all_data('assets/data/')

])

##Updates the current time every time the page is refreshed // Bradley
def serve_layout():
    return html.H1('The time is: ' + str(datetime.datetime.now()))


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
        else :
            passWord.append(line.rstrip("\n"))


VALID_USERNAME_PASSWORD_PAIRS = {
    }
for x in userName:
    VALID_USERNAME_PASSWORD_PAIRS.update({userName[userName.index(x)]: passWord[userName.index(x)]})


auth = dash_auth.BasicAuth(
    app,
    VALID_USERNAME_PASSWORD_PAIRS
)

##Grabbing local ip
addressraw = whatismyip.whatismylocalip()
address = ''
for item in addressraw:
    address = address + item

# Run application
if __name__ == '__main__':
    print(address)
    app.run_server(debug=True, host=addressraw[0], port=8080)
