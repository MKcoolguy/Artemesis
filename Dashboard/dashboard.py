import dash
import dash_bootstrap_components as dbc

#This will solely contain the information needed to run the dashboard instance and nothing more for cleanliness and avoiding circular imports.
#Run the dashboard instance from index.py!

app = dash.Dash(__name__,external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server