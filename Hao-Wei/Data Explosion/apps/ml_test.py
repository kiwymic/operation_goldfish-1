import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
import dash_table as dt;
import pandas as pd;
import numpy as np;
import plotly.express as px;
import plotly.graph_objs as go;

from app import app
from app import server

## Machine learning toolkits
from catboost import CatBoostRegressor;
from sklearn.preprocessing import LabelEncoder;


##### Load the housing data (and probably the pickle cat)
housing = pd.read_csv('./data/ames_housing_price_data_v4.csv', index_col = 0);
housing_coords = pd.read_csv('./data/house_coordinates_0.25.csv', index_col = 0);
# test = housing.merge(housing_coords, how = "inner", left_index = True, right_index = True);
# test = housing_coords.drop(["Address", "Coords4", "latitude", "longitude"], axis = 1);
# test.sort_values("PID", ascending = True, inplace = True);
# test2 = test.merge(housing["SalePrice"], left_index = True, right_index = True);
x = housing;

##### Preparation for gradient boosting, replace with Mo's code
typedict = {#'PID' : 'nominal',
            'SalePrice' : 'Continuous',
            #Matt
            'LotFrontage' : 'Continuous', 
            'LotArea' : 'Continuous',
            #'maybe_LotShape' : 'Nominal',
            'LandSlope' : 'Nominal', 
            'LandContour' : 'Nominal', 
            #'maybe_MSZoning' : 'Nominal', 
            'Street_paved' : 'Nominal', 
            'Alley' : 'Nominal',
            'Neighborhood' : 'Nominal', 
            #'drop_LotConfig' : 'nominal', 
            #'drop_Condition1' : 'nominal', 
            #'drop_Condition2' : 'nominal',
            'Foundation' : 'Nominal',
            'Utilities' : 'Nominal',
            #'Heating' : 'Nominal',
            #'drop_HeatingQC_nom' : 'Ordinal',
            'CentralAir' : 'Nominal',
            #'drop_Electrical' : 'Nominal',
            'HeatingQC_ord' : 'Ordinal',
            'LotShape_com' : 'Nominal',
            'MSZoning_com' : 'Nominal',
            #'LF_Normal' : 'nominal',
            'LF_Near_NS_RR' : 'Nominal',
            'LF_Near_Positive_Feature' : 'Nominal',
            'LF_Adjacent_Arterial_St' : 'Nominal',
            'LF_Near_EW_RR' : 'Nominal',
            'LF_Adjacent_Feeder_St' : 'Nominal',
            #'LF_Near_Postive_Feature' : 'Nominal',
            'Heating_com' : 'Nominal',
            'Electrical_com' : 'Nominal',
            'LotConfig_com' : 'Nominal', 
            'LotFrontage_log' : 'Continuous',
            'LotArea_log' : 'Continuous',
            #Oren 
            'MiscFeature': 'Nominal',
            'Fireplaces': 'Discrete',
            'FireplaceQu': 'Ordinal',
            'PoolQC': 'Ordinal',
            'PoolArea': 'Continuous',
            'PavedDrive': 'Nominal',
            'ExterQual': 'Ordinal',
            'OverallQual': 'Ordinal',
            'OverallCond': 'Ordinal',
            'MiscVal': 'Continuous',
            #'YearBuilt': 'Discrete',
            #'YearRemodAdd': 'Discrete',
            'KitchenQual': 'Ordinal',
            'Fence': 'Ordinal',
            'RoofStyle': 'Nominal',
            'RoofMatl': 'Nominal',
            #'maybe_Exterior1st': 'Nominal',
            #'drop_Exterior2nd': 'Nominal',
            'ExterCond': 'Ordinal',
            'MasVnrType': 'Nominal',
            'MasVnrArea': 'Continuous',
            #Mo
            #Basement
            'BsmtQual_ord': 'Ordinal',
            'BsmtCond_ord': 'Ordinal',
            'BsmtExposure_ord': 'Ordinal',
            #'BsmtQual_ord_lin': 'Ordinal',
            #'BsmtCond_ord_lin': 'Ordinal',
            #'BsmtExposure_ord_lin': 'Ordinal',
            'TotalBsmtSF': 'Continuous',
            'BSMT_GLQ':'Continuous', 
            'BSMT_Rec':'Continuous',
            'BsmtUnfSF': 'Continuous',
            'BSMT_ALQ':'Continuous',
            'BSMT_BLQ':'Continuous', 
            'BSMT_LwQ':'Continuous', 
            #'drop_BsmtQual': 'Nominal',
            #'drop_BsmtCond': 'Nominal',
            #'drop_BsmtExposure': 'Nominal',
            #'drop_BsmtFinType1': 'Nominal',
            #'drop_BsmtFinSF1': 'Continuous',
            #'drop_BsmtFinType2': 'Nominal',
            #'drop_BsmtFinSF2': 'Continuous',
            #Deck
            'WoodDeckSF':'Continuous', 
            'OpenPorchSF':'Continuous', 
            'ScreenPorch':'Continuous',
            'EnclosedPorch':'Continuous',
            '3SsnPorch':'Continuous',
            #Garage
            'GarageFinish':'Nominal', 
            #'GarageYrBlt':'Continuous',
            'GarageCars':'Ordinal',
            'GarageArea':'Continuous',
            'GarageType_com':'Nominal',
            'GarageQual':'Nominal', 
            'GarageCond':'Nominal',
            #'drop_GarageType':'Nominal',

            # Hao-Wei
            "SaleType": "Nominal",
            "BldgType": "Nominal",
            "Functional_ord": "Ordinal", # Changed from "Functional"
            "1stFlrSF": "Continuous",
            "2ndFlrSF": "Continuous",
            "LowQualFinSF": "Continuous", # Rejectable p-value
            "GrLivArea": "Continuous",
            "BsmtFullBath": "Discrete",
            "BsmtHalfBath": "Discrete", # Rejectable p-value
            "FullBath": "Discrete",
            "HalfBath": "Discrete",
            "BedroomAbvGr": "Discrete",
            "KitchenAbvGr": "Discrete",
            "TotRmsAbvGrd": "Discrete",
            "MoSold": "Discrete", # Rejectable p-value
            "YrSold": "Discrete", # Rejectable p-value
            ####### Below are columns created by myself #######
            #"Functional_dis": "Discrete", # Functional in a (Salvage) 0-7 (Full) scale.
            "1stFlrSF_log": "Continuous",
            "2ndFlrSF_log": "Continuous",
            "GrLivArea_log": "Continuous",
            "number_floors": "Discrete",
            "attic": "Ordinal",
            "PUD": "Nominal",
            #### Whose?
            "SaleCondition": "Nominal",
            "SalePrice_log": "Continuous",
            #"drop_MS_Coded": "Nominal",
            "sold_datetime": "Discrete",
    
            #### New in version 3:
            'ext_Wood_Siding': "Discrete",
            'ext_Hard_Board': "Discrete",
            'ext_Metal_Siding': "Discrete",
            'ext_Vinyl_Siding': "Discrete",
            'ext_Wood_Shingles': "Discrete",
            'ext_Plywood': "Discrete",
            'ext_Stucco': "Discrete",
            'ext_Cement_Board': "Discrete",
            'ext_Face_Brick': "Discrete",
            'ext_Asbestos_Shingles': "Discrete",
            'ext_Common_Brick': "Discrete",
            'ext_Imitation_Stucco': "Discrete",
            'ext_Other': "Discrete",
            #'sold_age_years': "Continuous"
    
            #### New in version 4
            'Garage_age_years': "Continuous",
            'Garage_age_bin': "Ordinal",
            'house_age_years': "Continuous",
            'Remod_age_years': "Continuous",
            'Remod_age_bin': "Ordinal"
}

attic_dict = {"No attic": 0, "Finished": 2, "Unfinished": 1};
fence_dict = {"No Fence": 0, "Minimum Privacy": 3, "Good Privacy": 4, "Good Wood": 2 , "Minimum Wood/Wire": 1};
Garage_age_bin_dict = {"No garage":0, "60+": 1, "40-60": 2, "20-40": 3, "0-20":4};
Remod_age_bin_dict = {"No remodel": 0, "45+": 1, "30-45": 2, "15-30": 3, "0-15":4};

x.drop("sold_datetime", axis = 1, inplace = True);
x["Months_Elapsed"] = 12*(x["YrSold"]-2006) + x["MoSold"];
x["attic"] = x.apply(lambda t: attic_dict[t["attic"]], axis = 1);
x["Fence"] = x.apply(lambda t: fence_dict[t["Fence"]], axis = 1);

x["Garage_age_bin"] = x.apply(lambda t: Garage_age_bin_dict[t["Garage_age_bin"]], axis = 1);
x["Remod_age_bin"] = x.apply(lambda t: Remod_age_bin_dict[t["Remod_age_bin"]], axis = 1);

typedict["Months_Elapsed"] = "Discrete";

col_num = [w for w in x.columns if typedict[w] in ["Continuous", "Discrete", "Ordinal"]];
col_nom = [w for w in x.columns if typedict[w] == "Nominal"];
# TODO: Not avery ordinal variables are in the machine understandable way.
# Fix: HeatingQC_nom, Fence, attic

x_num = x[col_num];
x_nom = x[col_nom];

# Encode all nominal and ordinal variables.

lencoder = LabelEncoder();

temp = pd.DataFrame({"SalePrice": x["SalePrice"]});
for col_name in col_nom:
    # temp = lencoder.fit_transform(np.array(str(x[[col_name]])).reshape(-1,1));
    temp[col_name] = np.array(lencoder.fit_transform(x[col_name].astype(str))).reshape(-1,1);
    
temp.drop("SalePrice", axis = 1, inplace = True);

# Add the positional data here later.
x = pd.concat([x_num, temp], axis = 1);

# Implementing Matt's idea on 8/27. Drop some month/year data, logged data,...
# x = x[(x["SaleCondition"] == 4) | (x["SaleCondition"] == 5)]; # 4=Normal, 5=Partial. shape=(2495, 105)
x.drop(["YrSold", "MoSold", "Months_Elapsed", "SaleType"], axis = 1, inplace = True); # (2495, 99)

y = x["SalePrice"];
ylog = x["SalePrice_log"];

x.drop(["SalePrice", "SalePrice_log"], axis = 1, inplace = True); # (2495, 99)

log_col = [lg for lg in x.columns if lg.find("log") != -1];
x.drop(log_col, axis = 1, inplace = True); #(2495, 94)

# Load and fit models
cat = CatBoostRegressor();
cat.load_model("./data/woof.meow", "cbm");

# These are the columns to be displayed in a standard DataTable.
display_columns = {"Price":"SalePrice", "Ground Living Area":"GrLivArea", "Quality": "OverallQual",\
                  "Bedrooms": "BedroomAbvGr", "Bathrooms": "FullBath", "Neighborhood": "Neighborhood"};
PAGE_SIZE = 10;

layout = html.Div([

    dbc.Container([
    dbc.Row([
        dbc.Col(html.H3("House price prediction in Ames, Iowa",
                        className='text-center text-primary, mb-4'),
                width=12)
    ])
    ]),
    
    dbc.Row([
        ### INPUTS
        dbc.Col([
            html.H5("Please click on graph a house you're interested in:",
                    className='text-center text-primary'),
            dcc.Checklist(id = "show_all_pids",
            options=[
            {'label': 'Show all properties', 'value': 'show_all_pid'}],
            value=[],
            labelStyle={'display': 'inline-block'}
            ),
            dcc.Graph(id="pid_scatter", clickData=None),
            dt.DataTable(id='pid_table',
                         columns=[{"name": k, "id": display_columns[k]} for k in display_columns],
                         page_current=0, page_size=PAGE_SIZE, page_action='custom')
        ], width = {'size':7, 'order':1}),
    
        ### INPUTS
        dbc.Col([
            html.H5("The price of the house:", id = "selected_pid",
                    className='text-center text-primary'),
            dcc.Graph(id="pid_quality_change", figure = px.scatter()),
            dcc.Graph(id="pid_area_change", figure = px.scatter())
        ], width = {'size':5, 'order':2})
    ])
])
        

##### ml_test

@app.callback(
    Output('pid_scatter', 'figure'),
    [Input('data_pid', 'data'),
    Input('show_all_pids', "value"),
    Input('pid_table', "page_current"),
    Input('pid_table', "page_size")])
def test_graph_data_pid(value, show_all, page_current, page_size):
    if not value: return;
    
    temp_house = housing.reset_index();
    temp_house = temp_house[temp_house["PID"].isin(value["PID"])];
    if show_all == []:
        temp_house = temp_house.iloc[\
        page_current*page_size:(page_current+ 1)*page_size];
    
    fig = px.scatter(temp_house, x="GrLivArea", y="SalePrice",
                 size="OverallQual", color="Neighborhood", hover_name= "PID",
                 size_max=10);
    return fig;

@app.callback(
    Output('pid_table', 'data'),
    Input('data_pid', 'data'),
    Input('pid_table', "page_current"),
    Input('pid_table', "page_size"))
def update_table(pid_data, page_current,page_size):
    if not pid_data: return;
    #if len(pid_data["PID"]) <= (page_current)*page_size: return;
    
    temp_house = housing.reset_index();
    temp_house = temp_house[temp_house["PID"].isin(pid_data["PID"])];
    
    return temp_house.iloc[
        page_current*page_size:(page_current+ 1)*page_size
    ][list(display_columns.values())].to_dict('records');

@app.callback(
    Output('selected_pid', 'children'),
    Input('pid_scatter', 'clickData'))
def update_selected_on_click(clickData):
    if not clickData: return;
#     temp = house_coords.reset_index();
#     print(3, clickData['points'][0]['hovertext'])
#     print(temp[temp["PID"] == clickData['points'][0]['hovertext']][["Address"]]);
    return clickData['points'][0]['hovertext'];

@app.callback(
    Output('pid_quality_change', 'figure'),
    Input('pid_scatter', 'clickData'))
def update_quality_chart(clickData):
    if not clickData: return px.scatter();
    
    temp_house = x.reset_index();
    PID = clickData['points'][0]['hovertext'];
    temp_house = temp_house[temp_house["PID"] == PID];
    temp_house.drop("OverallQual", axis = 1, inplace = True);
    temp = pd.DataFrame({"PID": [PID for i in range(10)], "OverallQual": range(1,11,1)})
    temp_house = temp_house.merge(temp, on="PID");
    temp_house.set_index("PID", inplace=True)
    
    temp_house["Sale Price Predicted"] = 10**cat.predict(temp_house)
    
    fig = px.scatter(temp_house, x="OverallQual", y="Sale Price Predicted");
    fig.update_traces(mode='lines+markers');
    return fig;

@app.callback(
    Output('pid_area_change', 'figure'),
    Input('pid_scatter', 'clickData'))
def update_gndarea_chart(clickData):
    if not clickData: return px.scatter();
    
    temp_house = x.reset_index();
    PID = clickData['points'][0]['hovertext'];
    temp_house = temp_house[temp_house["PID"] == PID];
    gr_area = int(temp_house["GrLivArea"]);
    temp_frame = temp_house.set_index("PID");
    pred_price = 10**cat.predict(temp_frame)[0];
    temp_house.drop("GrLivArea", axis = 1, inplace = True);
    temp = pd.DataFrame({"PID": [PID for i in range(300,4800, 10)], "GrLivArea": range(300,4800, 10)})
    temp_house = temp_house.merge(temp, on="PID");
    temp_house.set_index("PID", inplace=True)
    
    temp_house["Sale Price Predicted"] = 10**cat.predict(temp_house)
    
#     fig = go.Figure();
#     fig1 = go.Scatter(temp_house, x="GrLivArea", y="Sale Price Predicted");
#     fig1.update_traces(mode='lines');
#     fig2 = go.Scatter(x=[gr_area], y=[pred_price]);
#     fig2.update_traces(marker=dict(size=12, color = '#FF8833'));
#     fig2.add_trace(go.Scatter(temp_house, x="GrLivArea", y="Sale Price Predicted"));
    
#     fig.add_trace(fig1);
#     fig.add_trace(fig2);
    fig = px.scatter(temp_house, x="GrLivArea", y="Sale Price Predicted");
    fig.update_traces(mode='lines');
    fig.add_trace(go.Scatter(x=[gr_area], y=[pred_price]));
    fig.update_traces(marker=dict(size=12, color = '#FF8833'));
    return fig;


# layout = html.Div([
#     html.H3('App 1'),
#     dcc.Dropdown(
#         id='app-1-dropdown',
#         options=[
#             {'label': 'App 1 - {}'.format(i), 'value': i} for i in [
#                 'NYC', 'MTL', 'LA'
#             ]
#         ]
#     ),
#     html.Div(id='app-1-display-value'),
#     dcc.Link('Go to App 2', href='/apps/app2')
# ])


# @app.callback(
#     Output('app-1-display-value', 'children'),
#     Input('app-1-dropdown', 'value'))
# def display_value(value):
#     return 'You have selected "{}"'.format(value)