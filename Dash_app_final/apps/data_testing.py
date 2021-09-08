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

# external_stylesheets = ["./assets/my_custom_table_styling.css"]

# app = Dash(__name__)
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.YETI],

                meta_tags=[{'name': 'viewport',
                            'content': 'width=device-width, initial-scale=1.0'}]
                )


housing_basic = pd.read_csv('./data/basic_housing.csv')
money = FormatTemplate.money(0)

housing_basic = housing_basic[(housing_basic['SalePrice'] > 400000) &
                        (housing_basic['SalePrice'] < 500000)]

              # &
              #           (housing_basic['GrLivArea'] > sqfts[0]) &
              #           (housing_basic['GrLivArea'] < sqfts[1]) &
              #           (housing_basic['FullBath'] >= bathrms[0]) &
              #           (housing_basic['FullBath'] <= bathrms[1]) &
              #           (housing_basic['BedroomAbvGr'] >= bedrms[0]) &
              #           (housing_basic['BedroomAbvGr'] <= bedrms[1])].to_dict('records')


# housing_basic = housing_basic


# def db_table3():
#     housing_basic = pd.read_csv('./data/basic_housing.csv')
#     df = pd.DataFrame.from_dict(housing_basic)
#     conv_array = df.values.tolist()
#     key_array = list(df.keys())
#     DF_SIMPLE = pd.DataFrame({
#         'labels': key_array,
#         'values': conv_array[0]
#     })
#     return make_dash_table(DF_SIMPLE)


#
#
# app.layout = html.Div([
#     html.H1('Page 1'),
#     html.Br(),
#
#     html.H4('Database DataTable 3'),
#     html.Table(db_table3())
# ])


app.layout = html.Div([
    # dbc.Container([
            DataTable(
                id='table',
                # columns=[
                #     dict(id='SalePrice', name='Sale Price', type='numeric', format=money),
                #     {"name": ["Neighborhood"], "id": "Neighborhood"},
                #     dict(id='LotArea', name='Lot Area', type='numeric', format=Format().group(True)),
                #     dict(id='GrLivArea', name='Living Area', type='numeric', format=Format().group(True)),
                #     # {"name": ["Lot Area"], "id": "LotArea"},
                #     # {"name": ["Living Area"], "id": "GrLivArea"},
                #     {"name": [ "Bedrooms"], "id": "BedroomAbvGr"},
                #     {"name": ["Full Bathrooms"], "id": "FullBath"},
                #     {"name": ["Overall Quality"], "id": "OverallQual"},
                # ],
                data=housing_basic.to_dict('records'),
                style_as_list_view=True,
                # page_size=10,
                # fixed_rows={'headers': True},
                # style_cell_conditional = [
                #     {'if': {'column_id': 'SalePrice'},
                #      'width': '15%'},
                #     {'if': {'column_id': 'Neighborhood'},
                #      'width': '15%'},
                #     {'if': {'column_id': 'LotArea'},
                #      'width': '15%'},
                #     {'if': {'column_id': 'GrLivArea'},
                #      'width': '15%'},
                #     {'if': {'column_id': 'BedroomAbvGr'},
                #      'width': '15%'},
                #     {'if': {'column_id': 'FullBath'},
                #      'width': '15%'},
                #     {'if': {'column_id': 'OverallQual'},
                #      'width': '15%'}
                # ],
                # style_cell={
                #     'width': 95, #'{}%'.format(len(housing_basic.columns)),
                #     'textOverflow': 'ellipsis',
                #     'overflow': 'hidden',
                #     'maxWidth': 95
                # },
                # row_selectable='multi',
                cell_selectable= False
                # style_data_conditional=[],
                # sort_action= 'native',
                # filter_action = 'native'
            )
# ])
])



# def db_table3():
#     housing_basic = pd.read_csv('./data/basic_housing.csv')
#     df = pd.DataFrame.from_dict(housing_basic)
#     conv_array = df.values.tolist()
#     key_array = list(df.keys())
#     DF_SIMPLE = pd.DataFrame({
#         'labels': key_array,
#         'values': conv_array[0]
#     })
#     return make_dash_table(DF_SIMPLE)


#
# app = dash.Dash(__name__)
#
# app.layout = html.Div([
#     html.H1('Page 1'),
#     html.Br(),
#
#     html.H4('Database DataTable 3'),
#     html.Table(db_table3())
# ])


if __name__ == '__main__':
    app.run_server(debug=True)