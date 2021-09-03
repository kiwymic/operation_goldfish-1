## Plotly and Dash Loading
import plotly.express as px
# from jupyter_dash import JupyterDash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import dash_leaflet as dl
import dash_leaflet.express as dlx
from dash_extensions.javascript import assign
import dash
from dash_extensions.javascript import arrow_function
import dash_bootstrap_components as dbc
from dash_table import DataTable, FormatTemplate
from dash_table.Format import Format, Group

import json

# Pandas and geopandas stuff
import pandas as pd
import geopandas as gpd
import pandas_datareader.data as web
# from geopy.geocoders import Nominatim
# import geopandas as gpd
# import fiona
# from arcgis.gis import GIS
# from geopy.distance import geodesic
# import shapely.geometry
import geobuf

external_stylesheets = ["./assets/my_custom_table_styling.css"]

# app = Dash(__name__)
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.YETI],
                meta_tags=[{'name': 'viewport',
                            'content': 'width=device-width, initial-scale=1.0'}]
                )


housing_basic = pd.read_csv('./data/basic_housing.csv')
money = FormatTemplate.money(0)

layout = html.Div([
    dbc.Container([
            DataTable(
                id='table',
                columns=[
                    dict(id='SalePrice', name='Sale Price', type='numeric', format=money),
                    {"name": ["Neighborhood"], "id": "Neighborhood"},
                    dict(id='LotArea', name='Lot Area', type='numeric', format=Format().group(True)),
                    dict(id='GrLivArea', name='Living Area', type='numeric', format=Format().group(True)),
                    # {"name": ["Lot Area"], "id": "LotArea"},
                    # {"name": ["Living Area"], "id": "GrLivArea"},
                    {"name": [ "Bedrooms"], "id": "BedroomAbvGr"},
                    {"name": ["Full Bathrooms"], "id": "FullBath"},
                    {"name": ["Overall Quality"], "id": "OverallQual"},
                ],
                data=housing_basic.to_dict('records'),
                style_as_list_view=True,
                page_size=10,
                fixed_rows={'headers': True},
                style_cell_conditional = [
                    {'if': {'column_id': 'SalePrice'},
                     'width': '15%'},
                    {'if': {'column_id': 'Neighborhood'},
                     'width': '15%'},
                    {'if': {'column_id': 'LotArea'},
                     'width': '15%'},
                    {'if': {'column_id': 'GrLivArea'},
                     'width': '15%'},
                    {'if': {'column_id': 'BedroomAbvGr'},
                     'width': '15%'},
                    {'if': {'column_id': 'FullBath'},
                     'width': '15%'},
                    {'if': {'column_id': 'OverallQual'},
                     'width': '15%'}
                ],
                # style_cell={
                #     'width': 95, #'{}%'.format(len(housing_basic.columns)),
                #     'textOverflow': 'ellipsis',
                #     'overflow': 'hidden',
                #     'maxWidth': 95
                # },
                row_selectable='multi',
                cell_selectable= False,
                style_data_conditional=[],
                sort_action= 'native',
                filter_action = 'native'
            )
])
])



if __name__ == '__main__':
    app.run_server(debug=True)