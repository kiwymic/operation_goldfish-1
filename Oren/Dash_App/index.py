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
from dash_table import DataTable, FormatTemplate

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


from app import app
from app import server
from apps import maps, data_frame, app1, filters, table_test # ml_test
# from data import loading_stuff


housing_basic = pd.read_csv('./data/basic_housing.csv')

dropdown = dbc.DropdownMenu(
    children=[
        dbc.DropdownMenuItem("Home", href="/index"),
        dbc.DropdownMenuItem("Maps", href="/maps"),
        dbc.DropdownMenuItem("Machine Learning", href="/app1"),
        dbc.DropdownMenuItem("Table", href="/table_test"),
    ],
    nav = True,
    in_navbar = True,
    label = "Explore",
)

navbar = dbc.Navbar(
    dbc.Container(
        [
            html.A(
                # Use row and col to control vertical alignment of logo / brand
                dbc.Row(
                    [
                        dbc.Col(html.Img(src="/assets/goldfish.png", height="50px")),
                        dbc.Col(dbc.NavbarBrand("Project Goldfish - Machine Learning for Ames, Iowa", className="mb-1")),
                    ],
                    align="center",
                    no_gutters=False,
                ),
                href="/index",
            ),
            dbc.NavbarToggler(id="navbar-toggler2"),
            dbc.Collapse(
                dbc.Nav(
                    # right align dropdown menu with ml-auto className
                    [dropdown], className="ml-auto", navbar=True
                ),
                id="navbar-collapse2",
                navbar=True,
            ),
        ]
    ),
    color="dark",
    dark=True,
    className="mb-4",
)

def toggle_navbar_collapse(n, is_open):
    if n:
        return not is_open
    return is_open

for i in [2]:
    app.callback(
        Output(f"navbar-collapse{i}", "is_open"),
        [Input(f"navbar-toggler{i}", "n_clicks")],
        [State(f"navbar-collapse{i}", "is_open")],
    )(toggle_navbar_collapse)

# embedding the navigation bar
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    navbar,
    html.Div(id='page-content'),
    # html.Div(data_frame.layout)
])

# @app.callback(Output('table', 'style_data_conditional'),
#              [Input('table', 'selected_rows')])
# def update_styles(selected_rows):
#     return [{'if': {'derived_virtual_selected_row_ids': i}, 'background_color': '#D2F3FF'} for i in selected_rows]

@app.callback(
    Output("table", "style_data_conditional"),
    Input("table", "selected_rows"),
)
def style_selected_rows(sel_rows):
    if sel_rows is None:
        return dash.no_update
    val = [
        {"if": {"filter_query": "{{id}} ={}".format(i)}, "backgroundColor": "#404040",}
        for i in sel_rows
    ]
    return val




# @app.callback(Output("PIDs", "children"), [Input("housing_id", "click_feature")])
# def house_click(feature):
#     if feature is not None:
#         return f"You clicked {feature['properties']['PID']}"

@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/maps':
        return maps.layout
    elif pathname == '/plans':
        return plans.layout
    elif pathname == '/table_test':
        return table_test.layout
    else:
        return maps.layout

@app.callback(
    Output('output-container-range-slider', 'children'),
    [Input('price', 'value')])
def update_output_price_range(value):
    return ('${:,} - ${:,}'.format(value[0], value[1]))

@app.callback(
    Output('output-container-sq-foot-slider', 'children'),
    [Input('sqft', 'value')])
def update_output(value):
    return ('{:,} - {:,} sq. ft.'.format(value[0], value[1]))

@app.callback(
    # dash.dependencies.Output('PID_list', 'children'),
    Output("housing_id", "hideout"),
    Input('price', 'value'),
    Input('sqft', 'value'),
    Input("input_bathrooms", "value"),
    Input("input_bedrooms", "value")
)
def update_output(prices, sqfts, bathrms, bedrms):
    foo = list(housing_basic[(housing_basic['SalePrice'] > prices[0]) &
                        (housing_basic['SalePrice'] < prices[1]) &
                        (housing_basic['GrLivArea'] > sqfts[0]) &
                        (housing_basic['GrLivArea'] < sqfts[1]) &
                        (housing_basic['FullBath'] >= bathrms[0]) &
                        (housing_basic['FullBath'] <= bathrms[1]) &
                        (housing_basic['BedroomAbvGr'] >= bedrms[0]) &
                        (housing_basic['BedroomAbvGr'] <= bedrms[1])]
                ['PID'])
    return dict(name=foo)




#### Creating filter for data_table

@app.callback(
    # dash.dependencies.Output('PID_list', 'children'),
    Output("table", "data"),
    # Output("pid_scatter", "figure"),
    Input('price', 'value'),
    Input('sqft', 'value'),
    Input("input_bathrooms", "value"),
    Input("input_bedrooms", "value")
)
def update_output(prices, sqfts, bathrms, bedrms):
    return housing_basic[(housing_basic['SalePrice'] > prices[0]) &
                        (housing_basic['SalePrice'] < prices[1]) &
                        (housing_basic['GrLivArea'] > sqfts[0]) &
                        (housing_basic['GrLivArea'] < sqfts[1]) &
                        (housing_basic['FullBath'] >= bathrms[0]) &
                        (housing_basic['FullBath'] <= bathrms[1]) &
                        (housing_basic['BedroomAbvGr'] >= bedrms[0]) &
                        (housing_basic['BedroomAbvGr'] <= bedrms[1])].to_dict('records')


@app.callback(
    Output('computed-table', 'data'),
    Input('daq_bath_full', 'value'),
    Input('daq_bedroom', 'value')
)
def display_output(value1, value2):
    df_future.at[5, 'CompEdit'] = value1
    df_future.at[6, 'CompEdit'] = value2
    return df_future.to_dict('records')


# def update_output(prices, sqfts, bathrms, bedrms):
#     foo = list(maps.housing_basic[(maps.housing_basic['SalePrice'] > prices[0]) &
#                         (maps.housing_basic['SalePrice'] < prices[1]) &
#                         (maps.housing_basic['GrLivArea'] > sqfts[0]) &
#                         (maps.housing_basic['GrLivArea'] < sqfts[1]) &
#                         (maps.housing_basic['FullBath'] >= bathrms[0]) &
#                         (maps.housing_basic['FullBath'] <= bathrms[1]) &
#                         (maps.housing_basic['BedroomAbvGr'] >= bedrms[0]) &
#                         (maps.housing_basic['BedroomAbvGr'] <= bedrms[1])]
#                 ['PID'])
#     return dict(name=foo)
############ TRYING TO MAKE IT CLIENTSIDE - NOT WORKING!!!
# app.clientside_callback("function(x){return x;}",
#     # dash.dependencies.Output('PID_list', 'children'),
#     Output("housing_id", "hideout"),
#     Input('price', 'value'),
#     Input('sqft', 'value'),
#     Input("input_bathrooms", "value"),
#     Input("input_bedrooms", "value")
# )
# def update_output(prices, sqfts, bathrms, bedrms):
#     foo = list(maps.housing_basic[(maps.housing_basic['SalePrice'] > prices[0]) &
#                        (maps.housing_basic['SalePrice'] < prices[1]) &
#                        (maps.housing_basic['GrLivArea'] > sqfts[0]) &
#                        (maps.housing_basic['GrLivArea'] < sqfts[1]) &
#                        (maps.housing_basic['FullBath'] == bathrms) &
#                        (maps.housing_basic['BedroomAbvGr'] == bedrms)]
#                 ['PID'])
#     return dict(name=foo)




if __name__ == '__main__':
    app.run_server(debug=True)