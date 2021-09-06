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
import dash_table

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


# app = Dash(__name__)
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.YETI],
                meta_tags=[{'name': 'viewport',
                            'content': 'width=device-width, initial-scale=1.0'}]
                )

layout = html.Div([
    dbc.Container([
dbc.Col([
            html.H5("Price Slider",
                    className='text-center text-primary'),
            html.P(id='output-container-range-slider',
                    className='text-center text-primary, mb-1, small'),
            dcc.RangeSlider(
                id='price',
                min=0,
                max=800000,
                step=100,
                marks={
                    0: '$0',
                    # 100000: '$100,000',
                    # 200000: '$200,000',
                    # 250000: '$250,000',
                    # 300000: '$300,000',
                    400000: '$400,000',
                    # 600000: '$600,000',
                    800000: '$800,000',
                },
                value=[100000, 200000]
            ),
            html.Hr(),
            html.H5("Bedrooms",
                    className='text-center text-primary'),
            # html.P(id="out_bedrooms",
            #        className='text-center text-primary, mb-1, small'),
            dcc.RangeSlider(
                id='input_bedrooms',
                min=1,
                max=5,
                step=1,
                marks={
                    1: '1',
                    2: '2',
                    3: '3',
                    4: '4',
                    5: '5'
                },
                value=[1, 2]
            ),
            html.Hr(),

            html.H5("Bathrooms",
                    className='text-center text-primary'),
            # html.P(id="out_bedrooms",
            #        className='text-center text-primary, mb-1, small'),

            dcc.RangeSlider(
                    id='input_bathrooms',
                    min=1,
                    max=5,
                    step=1,
                    marks={
                        1: '1',
                        2: '2',
                        3: '3',
                        4: '4',
                        5: '5'
                    },
                    value=[1, 2]
                ),

            html.Hr(),

            html.H5("Sq Footage Slider",
                    className='text-center text-primary'),
            html.P(id='output-container-sq-foot-slider',
                   className='text-center text-primary, mb-1, small'),
            dcc.RangeSlider(
                id='sqft',
                min=0,
                max=2500,
                step=10,
                marks={
                    0: '0',
                    1250: '1250',
                    # 200000: '$200,000',
                    2500: '2,500',
                    # 300000: '$300,000',
                    # 400000: '$400,000',
                    5000: '5,000',
                },
                value=[100, 1000]
            )
        ], width={'size':4, 'order': 1})
    ])
    ])



if __name__ == '__main__':
    app.run_server(debug=True)
