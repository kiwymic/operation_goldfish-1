## Plotly and Dash Loading
import plotly.express as px
from jupyter_dash import JupyterDash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash_leaflet as dl
import dash_leaflet.express as dlx
from dash_extensions.javascript import assign
import dash
from dash_extensions.javascript import arrow_function
import dash_bootstrap_components as dbc

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

########## Loads geojson files as geobuf to speed up system
poi_public = dlx.geojson_to_geobuf(json.load(open('./data/poi_public.geojson')))
poi_health = dlx.geojson_to_geobuf(json.load(open('./data/poi_health.geojson')))
poi_parks = dlx.geojson_to_geobuf(json.load(open('./data/poi_parks.geojson')))
poi_food = dlx.geojson_to_geobuf(json.load(open('./data/poi_food.geojson')))
poi_hotel = dlx.geojson_to_geobuf(json.load(open('./data/poi_hotel.geojson')))
poi_shop = dlx.geojson_to_geobuf(json.load(open('./data/poi_shop.geojson')))
poi_finance = dlx.geojson_to_geobuf(json.load(open('./data/poi_finance.geojson')))
poi_tourism = dlx.geojson_to_geobuf(json.load(open('./data/poi_tourism.geojson')))
poi_fountain = dlx.geojson_to_geobuf(json.load(open('./data/poi_fountain.geojson')))
poi_misc = dlx.geojson_to_geobuf(json.load(open('./data/poi_misc.geojson')))
poi_church = dlx.geojson_to_geobuf(json.load(open('./data/poi_churches.geojson')))

housing = pd.read_csv('./data/house_surrounding_avg_prices.csv')

housing_geo = gpd.GeoDataFrame(
    housing, geometry=gpd.points_from_xy(housing.longitude, housing.latitude))

housing = json.loads(housing_geo.to_json())


# ########### Creates Icons for Map
draw_church = assign("""function(feature, latlng){
const icon_church = L.icon({iconUrl: './assets/icon_church.png', iconSize: [15, 25]});
return L.marker(latlng, {icon: icon_church});
}""")

draw_public = assign("""function(feature, latlng){
const icon_public = L.icon({iconUrl: './assets/icon_public.png', iconSize: [15, 25]});
return L.marker(latlng, {icon: icon_public});
}""")

draw_health = assign("""function(feature, latlng){
const icon_health = L.icon({iconUrl: './assets/icon_health.png', 
iconSize: [15, 25]});
return L.marker(latlng, {icon: icon_health});
}""")

draw_parks = assign("""function(feature, latlng){
const icon_parks = L.icon({iconUrl: './assets/icon_parks.png', 
iconSize: [15, 25]});
return L.marker(latlng, {icon: icon_parks});
}""")

draw_food = assign("""function(feature, latlng){
const icon_food = L.icon({iconUrl: './assets/icon_food.png', 
iconSize: [15, 25]});
return L.marker(latlng, {icon: icon_food});
}""")

draw_hotel = assign("""function(feature, latlng){
const icon_hotel = L.icon({iconUrl: './assets/icon_hotel.png', 
iconSize: [15, 25]});
return L.marker(latlng, {icon: icon_hotel});
}""")

draw_shop = assign("""function(feature, latlng){
const icon_shop = L.icon({iconUrl: './assets/icon_shop.png', 
iconSize: [15, 25]});
return L.marker(latlng, {icon: icon_shop});
}""")

draw_finance = assign("""function(feature, latlng){
const icon_finance = L.icon({iconUrl: './assets/icon_finance.png', 
iconSize: [15, 25]});
return L.marker(latlng, {icon: icon_finance});
}""")

draw_tourism = assign("""function(feature, latlng){
const icon_tourism = L.icon({iconUrl: './assets/icon_tourism.png', 
iconSize: [15, 25]});
return L.marker(latlng, {icon: icon_tourism});
}""")

draw_fountain = assign("""function(feature, latlng){
const icon_fountain = L.icon({iconUrl: './assets/icon_fountain.png', 
iconSize: [15, 25]});
return L.marker(latlng, {icon: icon_fountain});
}""")

draw_misc = assign("""function(feature, latlng){
const icon_misc = L.icon({iconUrl: './assets/icon_misc.png', 
iconSize: [15, 25]});
return L.marker(latlng, {icon: icon_misc});
}""")

dd_options = [dict(value=c['properties']['PID'], label=c['properties']['PID']) for c in housing['features']]
dd_defaults = [o["value"] for o in dd_options]

geojson_filter = assign(
    "function(feature, context){{return context.props.hideout.includes(feature.properties.PID);}}")


##### LAYOUT SECTION: BOOTSTRAP


app.layout = dbc.Container([
    dbc.Row([
        dbc.Col(html.H1("Machine Learning for Ames Iowa",
                        className='text-center text-primary, mb-4'),
                width=12)
    ]),

    dbc.Row([
        dbc.Col([
            html.H5("Price Slider",
                    className='text-center text-primary'),
            html.P(id='output-container-range-slider',
                    className='text-center text-primary, mb-1, small'),
            dcc.RangeSlider(
                id='price',
                min=0,
                max=500000,
                step=100,
                marks={
                    0: '$0',
                    # 100000: '$100,000',
                    # 200000: '$200,000',
                    250000: '$250,000',
                    # 300000: '$300,000',
                    # 400000: '$400,000',
                    500000: '$500,000',
                },
                value=[100000, 200000]
            ),
            html.H5("Bedrooms",
                    className='text-center text-primary'),
            # html.P(id="out_bedrooms",
            #        className='text-center text-primary, mb-1, small'),
        dcc.Input(
            id="input_bedrooms",
            type="number",
            placeholder="Input Number",
            min=0,
            max=5
        ),
            html.H5("Bathrooms",
                    className='text-center text-primary'),
            # html.P(id="out_bedrooms",
            #        className='text-center text-primary, mb-1, small'),
        dcc.Input(
            id="input_bathrooms",
            type="number",
            placeholder="Input Number",
            min=0,
            max=5
        ),

            html.H5("Sq Footage Slider",
                    className='text-center text-primary'),
            html.P(id='output-container-sq-foot-slider',
                   className='text-center text-primary, mb-1, small'),
            dcc.RangeSlider(
                id='sqft',
                min=0,
                max=5000,
                step=10,
                marks={
                    0: '0',
                    # 100000: '$100,000',
                    # 200000: '$200,000',
                    2500: '2,500',
                    # 300000: '$300,000',
                    # 400000: '$400,000',
                    5000: '5,000',
                },
                value=[1000, 2000]
            )




        ], width={'size':3, 'order': 1}),
        dbc.Col([
            dl.Map([
                dl.TileLayer(),
                dl.LayersControl(
                    [dl.Overlay(
                        dl.LayerGroup(
                            dl.GeoJSON(
                                data=housing,
                                options=dict(filter=geojson_filter),
                                id="housing_id", zoomToBoundsOnClick=True)
                        ), name="Housing", checked=False
                    )
                    ] +
                    [dl.Overlay(
                        dl.LayerGroup(
                            dl.GeoJSON(
                                data=poi_church,
                                format="geobuf",
                                id="church",
                                cluster=True,
                                options=dict(pointToLayer=draw_church),
                                zoomToBoundsOnClick=True)
                        ), name="Churchs", checked=False
                    ),

                        dl.Overlay(
                            dl.LayerGroup(
                                dl.GeoJSON(
                                    data=poi_public,
                                    format="geobuf",
                                    id="public",
                                    cluster=True,
                                    options=dict(pointToLayer=draw_public),
                                    zoomToBoundsOnClick=True)
                            ), name="Public/Community", checked=False
                        ),

                        dl.Overlay(
                            dl.LayerGroup(
                                dl.GeoJSON(
                                    data=poi_health,
                                    format="geobuf",
                                    id="health",
                                    cluster=True,
                                    options=dict(pointToLayer=draw_health),
                                    zoomToBoundsOnClick=True)
                            ), name="Medical/Health", checked=False
                        ),

                        dl.Overlay(
                            dl.LayerGroup(
                                dl.GeoJSON(
                                    data=poi_parks,
                                    format="geobuf",
                                    id="parks",
                                    cluster=True,
                                    options=dict(pointToLayer=draw_parks),
                                    zoomToBoundsOnClick=True)
                            ), name="Parks/Leisure", checked=False
                        ),

                        dl.Overlay(
                            dl.LayerGroup(
                                dl.GeoJSON(
                                    data=poi_food,
                                    format="geobuf",
                                    id="food",
                                    cluster=True,
                                    options=dict(pointToLayer=draw_food),
                                    zoomToBoundsOnClick=True)
                            ), name="Food/Dining", checked=False
                        ),

                        dl.Overlay(
                            dl.LayerGroup(
                                dl.GeoJSON(
                                    data=poi_hotel,
                                    format="geobuf",
                                    id="hotel",
                                    cluster=True,
                                    options=dict(pointToLayer=draw_hotel),
                                    zoomToBoundsOnClick=True)
                            ), name="Hotels/Accomodations", checked=False
                        ),

                        dl.Overlay(
                            dl.LayerGroup(
                                dl.GeoJSON(
                                    data=poi_shop,
                                    format="geobuf",
                                    id="shop",
                                    cluster=True,
                                    options=dict(pointToLayer=draw_shop),
                                    zoomToBoundsOnClick=True)
                            ), name="Markets/Shopping", checked=False
                        ),

                        dl.Overlay(
                            dl.LayerGroup(
                                dl.GeoJSON(
                                    data=poi_finance,
                                    format="geobuf",
                                    id="finance",
                                    cluster=True,
                                    options=dict(pointToLayer=draw_finance),
                                    zoomToBoundsOnClick=True)
                            ), name="Bankls/ATM", checked=False
                        ),

                        dl.Overlay(
                            dl.LayerGroup(
                                dl.GeoJSON(
                                    data=poi_tourism,
                                    format="geobuf",
                                    id="tourism",
                                    cluster=True,
                                    options=dict(pointToLayer=draw_tourism),
                                    zoomToBoundsOnClick=True)
                            ), name="Tourism/Cultural", checked=False
                        ),

                        dl.Overlay(
                            dl.LayerGroup(
                                dl.GeoJSON(
                                    data=poi_fountain,
                                    format="geobuf",
                                    id="fountain",
                                    cluster=True,
                                    options=dict(pointToLayer=draw_fountain),
                                    zoomToBoundsOnClick=True)
                            ), name="Fountain", checked=False
                        ),

                        dl.Overlay(
                            dl.LayerGroup(
                                dl.GeoJSON(
                                    data=poi_misc,
                                    format="geobuf",
                                    id="misc",
                                    cluster=True,
                                    options=dict(pointToLayer=draw_misc),
                                    zoomToBoundsOnClick=True)
                            ), name="Misc", checked=False
                        )]

                )
            ],
                center=[42.03, -93.64], zoom=12,
                style={'width': '100%',
                       'height': '80vh',
                       'margin': "auto",
                       "display": "block"}
            )



        ], width={'size':9, 'order': 2})
    ]),

    dbc.Row([

    ])
], fluid=True)

#
# app.layout = html.Div(children=[
# ,
#
#     # This just ensures we are getting the PID when clicked
#
#     dcc.Dropdown(id="dd", value=dd_defaults, options=dd_options, clearable=False, multi=True),
#
#     html.Div(id="PIDs"),
#
#     # This is adding a slider
#     html.Label([
#         "Price Range",
#         dcc.RangeSlider(
#             id='price',
#             min=1000,
#             max=500000,
#             step=100,
#             value=[100000, 200000]
#         ),
#         html.Div(id='output-container-range-slider')
#     ])
# ])


@app.callback(Output("PIDs", "children"), [Input("housing_id", "click_feature")])
def house_click(feature):
    if feature is not None:
        return f"You clicked {feature['properties']['PID']}"


@app.callback(
    dash.dependencies.Output('output-container-range-slider', 'children'),
    [dash.dependencies.Input('price', 'value')])
def update_output(value):
    return ('${:,} - ${:,}'.format(value[0], value[1]))


@app.callback(
    dash.dependencies.Output('output-container-sq-foot-slider', 'children'),
    [dash.dependencies.Input('sqft', 'value')])
def update_output(value):
    return ('{:,} - {:,} sq. ft.'.format(value[0], value[1]))


@app.callback(
    Output("out_bedrooms", "children"),
    [Input("input_bedrooms", "value")],
)
def cb_render(*vals):
    return " | ".join((str(val) for val in vals if val))

@app.callback(
    Output("out_bathrooms", "children"),
    [Input("input_bathrooms", "value")],
)
def cb_render(*vals):
    return " | ".join((str(val) for val in vals if val))


app.clientside_callback("function(x){return x;}", Output("housing_id", "hideout"), Input("dd", "value"))

if __name__ == '__main__':
    app.run_server(debug=True)
