from dash import html
from dash import dcc
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import os
cwd = os.path.dirname(__file__)  # Used for consistent file detection.


class Graphs:
    #Creates the temperature graph
 
    def createTempGraph():
        df = pd.read_csv(os.path.join(cwd, 'assets/data/temperature.csv'))
        df.columns = ['Time', 'Temperature']
        return go.Figure(
            data=px.line(
                x=df['Time'],
                y=df['Temperature']
            ).update_layout(
                xaxis_title='Time',
                yaxis_title='Temperature',
                template='plotly_dark',
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
            )
        )

    def createDistanceGraph():
        df = pd.read_csv(os.path.join(cwd, 'assets/data/distance.csv'))
        df.columns = ['Time', 'Distance']
        return go.Figure(
            data=px.line(
                x=df['Time'],
                y=df['Distance']
            ).update_layout(
                xaxis_title='Time',
                yaxis_title='Distance',
                template='plotly_dark',
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
            )
        )

    #returns the most recent temperature value read from the sensor.
    def get_most_recent_temp():
        df = pd.read_csv(os.path.join(cwd, 'assets/data/temperature.csv'))
        y = df['Temperature']
        return y.iat[-1]

    
    def get_most_recent_distance():
        df = pd.read_csv(os.path.join(cwd, 'assets/data/distance.csv'))
        y = df['Distance']
        return y.iat[-1]
    
    # Iris bar figure
    def drawFigure():
        df = px.data.iris()
        return html.Div([
            dbc.Card(
                dbc.CardBody([
                    dcc.Graph(
                        figure=px.bar(
                             df, x="sepal_width", y="sepal_length", color="species"
                             ).update_layout(
                            template='plotly_dark',
                            plot_bgcolor='rgba(0, 0, 0, 0)',
                            paper_bgcolor='rgba(0, 0, 0, 0)',
                        ),
                        config={
                            'displayModeBar': False
                        }
                    )
                ])
            ),
        ])

class ArchivedData:
    
    #Lists and returns all files in data directory
    def get_all_data(path):
        file_names=os.listdir(os.path.join(cwd, path))
        file_list = html.Ul([html.Li(file) for file in file_names])
        return file_list