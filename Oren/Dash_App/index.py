## Plotly and Dash Loading
import plotly.express as px
# from jupyter_dash import JupyterDash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import dash_leaflet as dl
import dash_leaflet.express as dlx
from dash_extensions.javascript import assign, arrow_function
import dash
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
import numpy as np

from app import app
from app import server
from apps import maps, data_frame, filters, table_test, ml_test
# from data import loading_stuff
import pickle
from sklearn.preprocessing import LabelEncoder, StandardScaler;
from sklearn.svm import SVR;

from dictionaries import *;

housing = pd.read_csv('./data/ames_housing_price_data_final.csv', index_col = 0);
front_end = housing.drop(["Address", "price_score"], axis = 1);
y = front_end["SalePrice"];
svrg_backend_scaler = StandardScaler();
svr_price_scaler = StandardScaler();
standardized_g = False; # Whether the standard scalar of Gaussian svr is fitted

# Standardize at the beginning.
# Standardizing y
svr_price_scaler.fit(np.array(np.log10(y)).reshape(-1,1));
y_std = svr_price_scaler.transform(np.array(np.log10(y)).reshape(-1,1));



def ftb_flip(fe):
    '''
    Description:
    This is the function which construct the backend data (which directly feeds to CatBoostRegressor)
    given the frontend data. For the svg
    Input:
    fe: The frontend dataframe. Columns must be the same as those in version 6 of the housing data.
    Output: The backend dataframe. Should be ready to "regressor.fit()".
    '''
    global standardized_g;
    #elif method == "svrg":
    be = fe.copy();
    be.drop(columns = ['SalePrice'], axis =1, inplace = True);
    be['ExterQualDisc']=be['ExterQual']-be['OverallQual'];
    be['OverallCondDisc']=be['OverallCond']-be['OverallQual'];
    be['KitchenQualDisc']=be['KitchenQual']-be['OverallQual'];
    be=be.drop(['ExterQual','OverallCond','KitchenQual'],axis=1);
    be = dummify(be, non_dummies, dummies);
    be['GrLivArea_log'] = np.log10(be['GrLivArea']);
    be['LotArea_log'] = np.log10(be['LotArea']);
    be.drop(['GrLivArea', 'LotArea'], axis = 1, inplace = True);
    if not standardized_g:
        be = pd.DataFrame(svrg_backend_scaler.fit_transform(be), columns = be.columns);
        standardized_g = True;
    else:
        be = pd.DataFrame(svrg_backend_scaler.transform(be), columns = be.columns);
    return be;
with open('./data/SVR_model_g.pickle', mode = 'rb') as file:
    svrg = pickle.load(file);
back_end = ftb_flip(front_end);

def pff_flip(fe):
    '''
    Description:
    Given a frontend data frame, and a string describing a regressor, predicts.
    Input:
    fe: The frontend dataframe. Columns must be the same as those in version 6 of the housing data.
    Output: A pd.Series predicting the output.
    '''
    return 10 ** (svr_price_scaler.inverse_transform\
    (svrg.predict(ftb_flip(fe))));
back_end = ftb_flip(front_end);
print(svrg.score(back_end, y_std));


#-----------------------------

# 909176150
# 903227070
df = pd.read_csv('./data/ames_housing_price_data_final.csv')
params = df.columns
df = df[df['PID'] == 909176150]
df_pred = df.copy().drop(['PID', 'Address', 'price_score'], axis =1)
df = df.apply(lambda x: np.round(x, 1) if type(x[0]) == np.float64 else x)
df_current = df.T.reset_index()
df_current.columns = ['Features', 'Current']
sale_price = df_current.loc[1, "Current"]#.values[0]
address = df_current.loc[2, "Current"]
droprows = [0, 1, 2, 12, 13, 14, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40]
df_current = df_current.drop(droprows, axis =0)
df_future = df_current.copy()
df_future.columns = ['Features', 'CompEdit']
basement_footage = df_future.at[17, 'CompEdit'] + df_future.at[6, 'CompEdit']



housing_basic = pd.read_csv('./data/ames_housing_price_data_final.csv')

dropdown = dbc.DropdownMenu(
    children=[
        dbc.DropdownMenuItem("Home", href="/index"),
        dbc.DropdownMenuItem("Maps", href="/maps"),
        dbc.DropdownMenuItem("Planning", href="/table_test"),
        dbc.DropdownMenuItem("Machine Learning", href="/ml_test"),

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

    dcc.Store(id = 'data_pid', storage_type = 'session'),
    dcc.Store(id='selected_house', storage_type='session')
])

# @app.callback(Output('table', 'style_data_conditional'),
#              [Input('table', 'selected_rows')])
# def update_styles(selected_rows):
#     return [{'if': {'derived_virtual_selected_row_ids': i}, 'background_color': '#D2F3FF'} for i in selected_rows]

@app.callback(
    Output("table", "style_data_conditional"),
    Output("selected_house", "data"),
    #Input('table', 'rows'),
    Input("table", "data"),
    Input("table", "selected_rows"),
)
def style_selected_rows(tb_data, sel_rows):
    # if sel_rows is None:
    if sel_rows == []:
        return dash.no_update

    # value_PID = tb_data[sel_rows]["PID"];
    val_PID = {"PID": tb_data[sel_rows[0]]["PID"]};
    val = [
        {"if": {"filter_query": "{{id}} ={}".format(i)}, "backgroundColor": "#404040",}
        for i in sel_rows
    ]
    # print(val)
    return val, val_PID;




# @app.callback(Output("PIDs", "children"), [Input("housing_id", "click_feature")])
# def house_click(feature):
#     if feature is not None:
#         return f"You clicked {feature['properties']['PID']}"

@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/maps':
        return maps.layout
    elif pathname == '/ml_test':
        return ml_test.layout
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


# @app.callback(
#     Output('computed-table', 'data'),
#     Input('daq_bath_full', 'value'),
#     Input('daq_bedroom', 'value')
# )
# def display_output(value1, value2):
#     df_future.at[5, 'CompEdit'] = value1
#     df_future.at[6, 'CompEdit'] = value2
#     return df_future.to_dict('records')


##### Pass a list of PID to the second page. I really think this chunk of code should in the map page.
@app.callback(
    Output("data_pid", "data"),
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
                ['PID']);
    return {"PID": foo};



@app.callback(
    Output('computed-table', 'data'),
    Output('future_price','children'),
    Output("flip_pid",'children'),
    Input('future_sqft', 'value'),
    Input('future_basement', 'value'),
    Input('future_basement', 'max'),
    Input('future_porch', 'value'),
    Input('future_bedroom', 'value'),
    Input('future_bath_full', 'value'),
    Input('future_bath_half', 'value'),
    Input('future_fireplaces', 'value'),
    Input('future_garage', 'value'),
    Input('pool_switch', 'on'),
    Input('future-veneer', 'value'),
    Input('future_overall_q', 'value'),
    Input('future_overall_cond', 'value'),
    Input('future_kitchen_q', 'value'),
    Input('future_exterior_q', 'value'),
    Input('selected_house', 'data')
)
def update_output(sqft_value, basement_value, basement_max, porch_value, bed_value,
                   bath_full_value, bath_half_value, fire_value, garage_value,
                   pool_value, veneer_value, overall_value, cond_value,
                  kitchen_value, exterior_value,
                  house_PID):
    if not house_PID: PID = 909176150;
    else: PID = house_PID["PID"];

    df_future.at[3, 'CompEdit'] = sqft_value
    df_future.at[17, 'CompEdit'] = basement_value
    df_future.at[6, 'CompEdit'] = basement_max - basement_value
    df_future.at[16, 'CompEdit'] = porch_value
    df_future.at[20, 'CompEdit'] = bed_value
    df_future.at[10, 'CompEdit'] = bath_full_value
    df_future.at[11, 'CompEdit'] = bath_half_value
    df_future.at[18, 'CompEdit'] = fire_value
    df_future.at[8, 'CompEdit'] = garage_value
    if pool_value == True:
        df_future.at[19, 'CompEdit'] = 1
    if pool_value == False:
        df_future.at[19, 'CompEdit'] = 0
    df_future.at[9, 'CompEdit'] = veneer_value
    df_future.at[5, 'CompEdit'] = overall_value
    df_future.at[22, 'CompEdit'] = cond_value
    df_future.at[23, 'CompEdit'] = kitchen_value
    df_future.at[21, 'CompEdit'] = exterior_value

    # Numbers: 3-11, 15-23, missing; 4(LotArea), 7(house_age_years,),    15(BldgType),
    needed_row = housing[housing["PID"]==house_PID["PID"]].drop(['PID','Address', 'price_score'], axis =1)
    df_future.at[4, 'CompEdit'] = needed_row.iloc[0]["LotArea"];
    df_future.at[7, 'CompEdit'] = round(needed_row.iloc[0]["house_age_years"], 2);
    df_future.at[15, 'CompEdit'] = needed_row.iloc[0]["BldgType"];

    #### For prediction dataframe
    for col in df_pred.columns:
        df_pred.loc[0, col] = needed_row.iloc[0][col]

    # print(df_pred)
    df_pred.loc[0, 'GrLivArea'] = sqft_value
    df_pred.loc[0, 'BSMT_HighQual'] = basement_value
    df_pred.loc[0, 'BSMT_LowQual'] = basement_max - basement_value
    df_pred.loc[0, 'PorchSF'] = porch_value
    df_pred.loc[0, 'BedroomAbvGr'] = bed_value
    df_pred.loc[0, 'FullBath'] = bath_full_value
    df_pred.loc[0, 'HalfBath'] = bath_half_value
    df_pred.loc[0, 'Fireplaces'] = fire_value
    df_pred.loc[0, 'GarageCars'] = garage_value
    if pool_value == True:
        df_pred.loc[0, 'Pool'] = 1
    if pool_value == False:
        df_pred.loc[0, 'Pool'] = 0
    df_pred.loc[0, 'MasVnrType'] = veneer_value
    df_pred.loc[0, 'OverallQual'] = overall_value
    df_pred.loc[0, 'OverallCond'] = cond_value
    df_pred.loc[0, 'KitchenQual'] = kitchen_value
    df_pred.loc[0, "ExterQual"] = exterior_value

    pred=pff_flip(df_pred)

    # Getting the Address

    temp = housing;
    if 'PID' not in temp.columns:
        temp = temp.reset_index();
    address = temp[temp["PID"] == PID]["Address"];
    # temp["Address"] = temp["Address"].apply(lambda x: x[:-17]); # ", Ames, Iowa, USA"
    return df_future.to_dict('records'),"${:,}".format(np.round(int(pred),0)), address;


@app.callback(
    Output('current-table', 'data'),
    Output('current_price', 'children'),
    Output('future_sqft', 'value'),
    Output('future_basement', 'value'),
    Output('future_basement', 'max'),
    Output('future_porch', 'value'),
    Output('future_overall_q', 'value'),
    Output('future_overall_cond', 'value'),
    Output('future_kitchen_q', 'value'),
    Output('future_exterior_q', 'value'),
    Output('future_bedroom', 'value'),
    Output('future_bath_full', 'value'),
    Output('future_bath_half', 'value'),
    Output('future_fireplaces', 'value'),
    Output('future_garage', 'value'),
    Output('pool_switch', 'value'),
    Output('future-veneer', 'value'),
    Input('selected_house', 'data'))
def update_current_frame(house_PID):
    PID = 909176150;
    if house_PID: PID = house_PID["PID"];

    df = housing;
    if 'PID' not in df:
        df.reset_index(inplace = True);
    params = housing.columns
    df = df[df['PID'] == PID]
    df_pred = df.copy().drop(['PID', 'Address', 'price_score'], axis =1)

    sale_price = int(df["SalePrice"]);
    future_sqft = int(df["GrLivArea"]);
    bsmt_low = int(df["BSMT_LowQual"]);
    bsmt_high = int(df["BSMT_HighQual"]);
    future_porch = int(df["PorchSF"]);
    future_oq = round(float(df["OverallQual"]),2);
    future_oc = round(float(df["OverallCond"]),2);
    future_kitchen_q = round(float(df["KitchenQual"]),2);
    future_exterior_q = round(float(df["ExterQual"]),2);
    future_bedroom = int(df["BedroomAbvGr"]);
    future_bath_full = int(df["FullBath"]);
    future_bath_half = int(df["HalfBath"]);
    future_fireplaces = int(df["Fireplaces"]);
    future_garage = int(df["GarageCars"]);
    future_pool = True if int(df["GarageCars"])==1 else False;
    future_veneer = str(df["MasVnrType"].iloc[0]);

    # df.set_index("PID", inplace = True);
    # print(df)
    # df = df.apply(lambda x: np.round(x[PID], 1) if type(x[PID]) == np.float64 else x[PID])

    df_current = df.T.reset_index()
    df.set_index("PID", inplace = True);
    df_current.columns = ['Features', 'Current']
    df_current["Current"] = df_current.apply(lambda x: np.round(x["Current"], 2) if type(x["Current"]) == float else x["Current"], axis = 1);
    sale_price = df_current.loc[1, "Current"]#.values[0]
    address = df_current.loc[2, "Current"]
    droprows = [0, 1, 2, 12, 13, 14, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40]
    df_current = df_current.drop(droprows, axis =0)
    df_future = df_current.copy()
    df_future.columns = ['Features', 'CompEdit']

    # print(df_future.apply(lambda x: type(x["CompEdit"]), axis = 1))
    print(df_future["CompEdit"])
    #basement_footage = df_future.at[17, 'CompEdit'] + df_future.at[6, 'CompEdit']

    return df_current.to_dict('records'), "${:,}".format(sale_price), future_sqft, bsmt_high, bsmt_high+bsmt_low,\
    future_porch, future_oq, future_oc, future_kitchen_q, future_exterior_q, future_bedroom,\
    future_bath_full, future_bath_half, future_fireplaces, future_garage, future_pool, future_veneer;




#
# @app.callback(
#     Output('selected_house', 'data'),
#     Input('table', "selected_rows"),
#     Input('price', 'value'),
#     Input('sqft', 'value'),
#     Input("input_bathrooms", "value"),
#     Input("input_bedrooms", "value")
# )
# def update_table(selected_rows):
#     food = list(housing_basic[(housing_basic['SalePrice'] > prices[0]) &
#                              (housing_basic['SalePrice'] < prices[1]) &
#                              (housing_basic['GrLivArea'] > sqfts[0]) &
#                              (housing_basic['GrLivArea'] < sqfts[1]) &
#                              (housing_basic['FullBath'] >= bathrms[0]) &
#                              (housing_basic['FullBath'] <= bathrms[1]) &
#                              (housing_basic['BedroomAbvGr'] >= bedrms[0]) &
#                              (housing_basic['BedroomAbvGr'] <= bedrms[1])]
#                ['PID']);
#     print(food[selected_rows])
#     return(selected_rows)

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
