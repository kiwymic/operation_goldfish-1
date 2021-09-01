# ## Plotly and Dash Loading
# import plotly.express as px
# # from jupyter_dash import JupyterDash
# import dash_core_components as dcc
# import dash_html_components as html
# from dash.dependencies import Input, Output, State
# import dash_leaflet as dl
# import dash_leaflet.express as dlx
# from dash_extensions.javascript import assign
# import dash
# from dash_extensions.javascript import arrow_function
# import dash_bootstrap_components as dbc
# import dash_table
#
# import json
#
# # Pandas and geopandas stuff
# import pandas as pd
# import geopandas as gpd
# import pandas_datareader.data as web
# # from geopy.geocoders import Nominatim
# # import geopandas as gpd
# # import fiona
# # from arcgis.gis import GIS
# # from geopy.distance import geodesic
# # import shapely.geometry
# import geobuf
#



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

housing_basic = pd.read_csv('./data/basic_housing.csv')

housing_geo = pd.read_csv('./data/house_surrounding_avg_prices.csv')

housing_geo = gpd.GeoDataFrame(
    housing_geo, geometry=gpd.points_from_xy(housing_geo.longitude, housing_geo.latitude))

housing_geo = json.loads(housing_geo.to_json())
geojson = housing_geo