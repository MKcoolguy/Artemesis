import unittest
from unittest import TestCase
from index import whatismyip, VALID_USERNAME_PASSWORD_PAIRS
from index import dash
import dash_auth
import dash_bootstrap_components as dbc


class Test(unittest.TestCase):
    def test_address_generation(self):
        addressraw = whatismyip.whatismylocalip()
        address = ''
        for item in addressraw:
            address = address + item
        assert isinstance(address, str)
        assert len(address) > 0
        assert '.' in address

    def test_dropdown_menu(self):
        # Initialize the app
        app = dash.Dash(__name__)
        app.layout = dbc.Row(dbc.DropdownMenu(
            children=[
                dbc.DropdownMenuItem(dbc.NavLink("Github", href="https://github.com/soft-eng-practicum/Artemis")),
                dbc.DropdownMenuItem(dbc.NavLink("Summary Poster", href="https://ggcedu.sharepoint.com/:p:/r/sites/APL/_layouts/15/Doc.aspx?sourcedoc=%7BA6BFB3D3-0AA6-4612-99E0-5825D0227F5D%7D&file=NASA-MINDS-Poster.pptx&action=edit&mobileredirect=true")),
                dbc.DropdownMenuItem(dbc.NavLink("Semester Plan", href="https://sway.office.com/vzl8CVGTqe7gqqzH?ref=Link")),
            ],
            label="Artemis Mission'",
            color="primary",
            className="m-1",
        )
        )

        # Set up the test client
        client = app.layout()

        # Simulate a click on the dropdown toggle
        response = client.post('/', data={'_dash-update-component': 'dropdown-menu.dropdown.toggle.n_clicks'})

        # Check that the dropdown menu was toggled
        assert b'aria-expanded="true"' in response.data

        # Simulate a click on the first dropdown item
        response = client.post('/', data={'_dash-update-component': 'dropdown-menu.dropdown.items.0.n_clicks'})

        # Check that the first dropdown item was clicked
        assert b'Item 1' in response.data


