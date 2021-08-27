## Plotly and Dash Loading
import plotly.express as px
from jupyter_dash import JupyterDash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash_leaflet as dl
import dash_leaflet.express as dlx
from dash_extensions.javascript import assign
from dash import Dash
from dash_extensions.javascript import arrow_function

import json

# Pandas and geopandas stuff
import pandas as pd
import geopandas as gpd
from geopy.geocoders import Nominatim
import geopandas as gpd
import fiona
from arcgis.gis import GIS
from geopy.distance import geodesic
import shapely.geometry
import geobuf




lon_min = -93.7638;
lon_max = -93.4449;
lat_min = 41.9503;
lat_max = 42.1089;

def clean_Ames_location(df_place):
    '''
    DOCSTRING
    This cleans up the geopandas file for all the location data.
    It removes places that are more/less than a specific area based on lat and long.
    It then converts the files to JSON and then a GEOBUF, which will allow for faster loading.
    The boundary latitudes and longitudes are given by the global variables "lon, lat"_"min, max".
 
    INPUT:
    Geopandas data frame: Includes a geometry column
    
    OUTPUT:
    Geobuf file, with only locations within the specified area.
    '''
    df_place = df_place[(df_place['geometry'].x >= lon_min) &
                        (df_place['geometry'].x <= lon_max) & 
                        (df_place['geometry'].y >= lat_min) & 
                        (df_place['geometry'].y <= lat_max)]; 
    
### TO STOP CONVERSION TO GEOJSON, COMMENT OUT THIS LINE   
    df_place = json.loads(df_place.to_json())
    
### TO STOP CONVERSION TO GEOBUF, COMMENT OUT THIS LINE
#     df_place = dlx.geojson_to_geobuf(df_place)
    
    return df_place



gis_osm_pofw = gpd.read_file(
    '../../GeoJsonFiles/iowa-latest-free/gis_osm_pofw_free_1.shp')
churches = clean_Ames_location(gis_osm_pofw)


draw_church = assign("""function(feature, latlng){
const icon_church = L.icon(
{iconUrl: `../assets/Church_symbol_gray.svg`, 
iconSize: [64, 48]}
);
return L.marker(latlng, {icon: cross});
}""")







app = Dash(__name__)


housing = pd.read_csv('../../Data/house_surrounding_avg_prices.csv')
housing = housing.head(10)
housing_geo = gpd.GeoDataFrame(
    housing, geometry=gpd.points_from_xy(housing.longitude, housing.latitude))

housing = json.loads(housing_geo.to_json())



dd_options = [dict(value=c['properties']['PID'], label=c['properties']['PID']) for c in housing['features']]
dd_defaults = [o["value"] for o in dd_options]



geojson_filter = assign(
    "function(feature, context){{return context.props.hideout.includes(feature.properties.PID);}}")

app.layout = html.Div(children=[
    dl.Map([
    dl.TileLayer(),
    dl.LayersControl(
        [dl.Overlay(
            dl.LayerGroup(
                dl.GeoJSON(
                    data=housing, 
                    options=dict(filter=geojson_filter), 
                    id="housing_id", cluster=True, zoomToBoundsOnClick=True)
            ), name = "Housing", checked = "True"
        ) ,
         dl.Overlay(
            dl.LayerGroup(
                dl.GeoJSON(
                    data=churches, id="church", cluster=True, options=dict(pointToLayer=draw_church), zoomToBoundsOnClick=True)
            ), name = "Churchs", checked = "False"
        )
        ]
     )
    ],
        center=[42.03, -93.64], zoom=12,
        style={'width': '100%', 'height': '50vh', 'margin': "auto", "display": "block"}
    ),
    
    # This just ensures we are getting the PID when clicked


    dcc.Dropdown(id="dd", value=dd_defaults, options=dd_options, clearable=False, multi=True),
        html.Div(id="PIDs"),
# This is adding a slider
    html.Label([
        "Price Range",
        dcc.RangeSlider(
            id='price',
            min=1000,
            max=500000,
            step=100,
            value=[100000, 200000]
        ),
    html.Div(id='output-container-range-slider')
    ])
])


            
            #             dl.GeoJSON(
#                 data=housing, options=dict(
#                 filter=geojson_filter),
#                        id="housing")),
#                     name="Housing", checked=True)]
#          ])

@app.callback(Output("PIDs", "children"), [Input("housing_id", "click_feature")])
def house_click(feature):
    if feature is not None:
        return f"You clicked {feature['properties']['PID']}"

app.clientside_callback("function(x){return x;}", Output("housing_id", "hideout"), Input("dd", "value"))
    

if __name__ == '__main__':
    app.run_server()