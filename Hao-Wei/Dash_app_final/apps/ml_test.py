import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
import dash_table as dt;
import pandas as pd;
import numpy as np;
import plotly.express as px;
import plotly.graph_objs as go;
import pickle;

from dictionaries import *;
# from RegressorEncapsulation import EncapsulatedModel;

from app import app
from app import server

## Machine learning toolkits
from catboost import CatBoostRegressor;
from sklearn.preprocessing import LabelEncoder, StandardScaler;
from sklearn.linear_model import LinearRegression, Lasso, RidgeCV;
from sklearn.svm import SVR;

from RegressorEncapsulation import EncapsulatedModel # Import Foo into main_module's namespace explicitly
from sklearn.ensemble import StackingRegressor;
from sklearn.kernel_ridge import KernelRidge;

# The housing data
# housing_address = pd.read_csv('./data/house_coordinates_address.csv', index_col = 0);
# housing = pd.read_csv('./data/ames_housing_price_data_v6.csv', index_col = 0);
housing = pd.read_csv('./data/ames_housing_price_data_final.csv', index_col = 0);
front_end = housing.drop(["Address", "price_score"], axis = 1);
y = front_end["SalePrice"];

# Some first step preprocessing.
svr_backend_scaler = StandardScaler();
svrg_backend_scaler = StandardScaler();
svr_price_scaler = StandardScaler();
standardized_l = False; # Whether the standard scalar of linear svr is fitted
standardized_g = False; # Whether the standard scalar of Gaussian svr is fitted

svr_price_scaler.fit(np.array(np.log10(y)).reshape(-1,1));
y_std = svr_price_scaler.transform(np.array(np.log10(y)).reshape(-1,1));

############ Generate the pickle...
# cbl = CatBoostRegressor(subsample= 0.85, depth= 2, random_seed= 0, learning_rate= 0.04, iterations= 4000, verbose=False);
# lm = Lasso(alpha=1e-06, copy_X=True, fit_intercept= True, max_iter= 1000, normalize= True, positive= False, precompute= False, selection= 'cyclic', tol= 0.001);
# svrg = SVR(C= 6000, epsilon = 0.1, gamma = 6e-5, max_iter=-1, shrinking=True);
# svrl = KernelRidge(alpha=0.005, coef0 = 0.0, kernel = "linear");
#
# models = [("cat", EncapsulatedModel("cat", cbl)), ("lm", EncapsulatedModel("lm", lm)),\
#           ("svrl", EncapsulatedModel("svrl", svrl)), ("svrg", EncapsulatedModel("svrg", svrg))];
# stack_ridge = StackingRegressor(estimators=models,
#     final_estimator = RidgeCV(alphas = np.logspace(-2,2,9), cv = 5));
#
# stack_ridge.fit(front_end, y);
# print("Stacked", stack_ridge.score(front_end, y));
# with open('./ensemble_ridge.pickle', mode = 'wb') as file:
#      pickle.dump(stack_ridge, file)

# Utility functions which sends from front end to back end
def front_to_back(fe, method = "cat"):
    '''
    Description:
    This is the function which construct the backend data (which directly feeds to CatBoostRegressor)
    given the frontend data.
    Input:
    fe: The frontend dataframe. Columns must be the same as those in version 6 of the housing data.
    method: The string which describes the regressor. Default = cat.
    Compatible values: "cat": CatBoostRegressor; "lm": Multilinear method (with lasso penalization)
    "svrl": Support vector regressor with linear kernel
    Output: The backend dataframe. Should be ready to "regressor.fit()".
    '''
    global standardized_l;
    global standardized_g;

    be = fe.copy();

    if method == "x": return be;
    elif method == "cat":
        be['ExterQualDisc']=be['ExterQual']-be['OverallQual'];
        be['OverallCondDisc']=be['OverallCond']-be['OverallQual'];
        be['KitchenQualDisc']=be['KitchenQual']-be['OverallQual'];
        be=be.drop(["SalePrice", 'ExterQual','OverallCond','KitchenQual'],axis=1);

        be = dummify(be, non_dummies, dummies);
    elif method in ["lm", "svrl"]:
        be.drop(columns = ['SalePrice'], axis =1, inplace = True);
        be['GrLivArea_log'] = np.log10(be['GrLivArea']);
        be['LotArea_log'] = np.log10(be['LotArea']);
        be['ExterQualDisc'] = be['ExterQual'] - be['OverallQual'];
        be['OverallCondDisc'] = be['OverallCond'] - be['OverallQual'];
        be['KitchenQualDisc'] = be['KitchenQual'] - be['OverallQual'];
        be = be.drop(['ExterQual','OverallCond','KitchenQual'], axis=1);

        be['BSMT_LowQual_bin'] = pd.cut(be['BSMT_LowQual'], [-1, 1, 500, 1000, 1500, 2500], labels = ['No basement', '0-500', '500-1000', '1000-1500', '1500+']);
        be['BSMT_HighQual_bin'] = pd.cut(be['BSMT_HighQual'], [-1, 1, 500, 1000, 1500, 2500], labels = ['No basement', '0-500', '500-1000', '1000-1500', '1500+']);
        be.drop(['BSMT_HighQual', 'BSMT_LowQual', 'GrLivArea', 'LotArea'], axis = 1, inplace = True);

        be = dummify(be, non_dummies_linear, dummies_linear);

        if method == "svrl":
            if not standardized_l:
                be = pd.DataFrame(svr_backend_scaler.fit_transform(be), columns = be.columns);
                standardized_l = True;
            else:
                be = pd.DataFrame(svr_backend_scaler.transform(be), columns = be.columns);
    elif method == "svrg":
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

def predict_from_front(fe, method = "cat"):
    '''
    Description:
    Given a frontend data frame, and a string describing a regressor, predicts.
    Input:
    fe: The frontend dataframe. Columns must be the same as those in version 6 of the housing data.
    method: The string which describes the regressor. Default = "cat". Compatible values: See above.
    Output: A pd.Series predicting the output.
    '''
    if method_dict[method]["Scale"] == "lin":
        return method_dict[method]["Regressor"].predict(front_to_back(fe, method));
    elif method_dict[method]["Scale"] == "log": # The method is log scaled. Needs an exponentiation
        return 10 ** method_dict[method]["Regressor"].predict(front_to_back(fe, method));
    else: # The method is log scaled then standardized.
        return 10 ** (svr_price_scaler.inverse_transform\
        (method_dict[method]["Regressor"].predict(front_to_back(fe, method))));
    return;

##########################
# The zoo of regressors...
cat = CatBoostRegressor();
cat.load_model("./data/HousePriceCatBoost", "cbm");

with open('./data/linearmodel.pickle', mode = 'rb') as file:
    lm = pickle.load(file);

with open('./data/SVR_model.pickle', mode = 'rb') as file:
    svrl = pickle.load(file);

with open('./data/SVR_model_g.pickle', mode = 'rb') as file:
    svrg = pickle.load(file);

with open('./data/ensemble_ridge.pickle', mode = 'rb') as file:
    ensr = pickle.load(file);

back_end = front_to_back(front_end, "svrl");
back_end = front_to_back(front_end, "svrg");

method_dict = {
    "cat": {"Scale": "lin", "Order": False, "Regressor": cat,
            "Altered": ['Neighborhood', 'BldgType', 'MasVnrType', 'ExterQual','OverallCond','KitchenQual']},
    "lm": {"Scale": "log", "Order": True, "Regressor": lm,
            "Altered": ['Neighborhood', 'BldgType', 'MasVnrType', 'BSMT_HighQual', 'BSMT_LowQual',
            'ExterQual','OverallCond','KitchenQual', 'GrLivArea', 'LotArea']},
    "svrl":{"Scale": "fitlog", "Order": True, "Regressor": svrl,
            "Altered": ['Neighborhood', 'BldgType', 'MasVnrType', 'BSMT_HighQual', 'BSMT_LowQual',
            'ExterQual','OverallCond','KitchenQual', 'GrLivArea', 'LotArea']},
    "svrg":{"Scale": "fitlog", "Order": True, "Regressor": svrg,
            "Altered": ['Neighborhood', 'BldgType', 'MasVnrType',
            'ExterQual','OverallCond','KitchenQual', 'GrLivArea', 'LotArea']},
    "x":{"Scale": "lin", "Order": True, "Regressor": ensr,
            "Altered": ['Neighborhood', 'BldgType', 'MasVnrType', 'BSMT_HighQual', 'BSMT_LowQual',
            'ExterQual','OverallCond','KitchenQual', 'GrLivArea', 'LotArea']}
};

# Testing area for the latest machine learning model.
#transformation of front-end to back-end.
#back_end = front_to_back(front_end, "svrl");

# back_end = front_to_back(front_end, "svrg");
# print(svrg.score(back_end, y_std));
print(ensr.score(front_end, y));

##########################
# Constants, though much more should be defined...

# These are the columns to be displayed in a standard DataTable.
display_columns = {"Address": "Address", "Sale Price Price":"SalePrice", "Ground Living Area":"GrLivArea", "Quality (1-8)": "Quality",\
                  "# of Bedrooms": "BedroomAbvGr", "# of Bathrooms": "FullBath", "Neighborhood": "Neighborhood"};
PAGE_SIZE = 10;

#########################
# The interface

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
            html.Hr(),
            dcc.Checklist(id = "show_all_pids",
            options=[
            {'label': 'Show all properties', 'value': 'show_all_pid'}],
            value=[],
            labelStyle={'display': 'inline-block'},
            className='text-center'
            ),
            dcc.Graph(id="pid_scatter", clickData=None, style={"height": "60%"}),
            dt.DataTable(id='pid_table',
                         columns=[{"name": k, "id": display_columns[k]} for k in display_columns],
                         page_current=0, page_size=PAGE_SIZE, page_action='custom')
        ], width = {'size':7, 'order':1}),

        ### INPUTS
        dbc.Col([
            html.H5("Here is your dream home...", id = "selected_pid",
                    className='text-center text-primary'),
            html.Hr(),
            html.P("The nitty gritty:"),
            dcc.Checklist(id = "check_methods",
            options=[
                {'label': 'CatBoost', 'value': 'check_cat'},
                {'label': 'Linear', 'value': 'check_lm'},
                {'label': 'Linear SVR', 'value': 'check_svrl'},
                {'label': 'Gaussian SVR', 'value': 'check_svrg'},
                {'label': 'X', 'value': 'check_x'}],
            value=['check_cat', 'check_lm', 'check_svrg'],
            labelStyle={'display': 'inline-block'},
            className='text-center'),
            html.Hr(),

            html.P("Let's get ready to flip the house and get filthy rich!"),

            html.Div([
            dcc.Dropdown(
                id='flip_major',
                options=[{'label': column_title_dict[i]["Description"], 'value': i}\
                for i in [i for i in column_title_dict if (column_title_dict[i]["Actionable"]==True) &\
                (column_title_dict[i]["Select"]=="Major")]],
                value='GrLivArea'
            )], style={'width': '48%', 'display': 'inline-block'}),

            html.Div([
                dcc.Dropdown(
                    id='flip_minor',
                    options=[{'label': column_title_dict[i]["Description"], 'value': i}\
                    for i in column_title_dict if (column_title_dict[i]["Actionable"]==True) &\
                    (column_title_dict[i]["Select"]=="Minor")],
                    value=''
                )
            ], style={'width': '48%', 'float': 'right', 'display': 'inline-block'}),
            dcc.Graph(id="pid_quality_change", figure = px.scatter()),
            html.Hr(),
            html.P("Just looking around?"),
            html.Div([
            dcc.Dropdown(
                id='explore_major',
                options=[{'label': column_title_dict[i]["Description"], 'value': i}\
                for i in [i for i in column_title_dict if (column_title_dict[i]["Select"]=="Major")]],
                value='LotArea'
            )], style={'width': '48%', 'display': 'inline-block'}),

            html.Div([
                dcc.Dropdown(
                    id='explore_minor',
                    options=[{'label': column_title_dict[i]["Description"], 'value': i}\
                    for i in column_title_dict if (column_title_dict[i]["Select"]=="Minor")],
                    value=''
                )
            ], style={'width': '48%', 'float': 'right', 'display': 'inline-block'}),

            dcc.Graph(id="pid_area_change", figure = px.scatter())
        ], width = {'size':5, 'order':2})
    ])
])


##### ml_test

# Update the scatter plot. Especially important when coming from the map page.
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
    temp_house["Quality"] = temp_house["OverallQual"].apply(lambda x: int(7*x+1));
    if show_all == []:
        temp_house = temp_house.iloc[\
        page_current*page_size:(page_current+ 1)*page_size];

    fig = px.scatter(temp_house, x="GrLivArea", y="SalePrice",
                 size="Quality", color="Neighborhood", hover_name= "Address",
                 size_max=10);
    return fig;

# Update the data table in the below.
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
    temp_house["Quality"] = temp_house["OverallQual"].apply(lambda x: int(7*x+1));

    return temp_house.iloc[
        page_current*page_size:(page_current+ 1)*page_size
    ][list(display_columns.values())].to_dict('records');

# When a point on the plot is selected, fetch and display the address.
@app.callback(
    Output('selected_pid', 'children'),
    Input('pid_scatter', 'clickData'))
def update_selected_on_click(clickData):
    if not clickData: return "Looking for your dream home?";
    address = clickData['points'][0]['hovertext'];
    # temp = housing;
    # temp = temp.reset_index();
    # temp = temp[temp["A"] == clickData['points'][0]['hovertext']]
    # # temp["Address"] = temp["Address"].apply(lambda x: x[:-17]); # ", Ames, Iowa, USA"
    # address = temp[temp["PID"] == clickData['points'][0]['hovertext']]["Address"];
    return "Your selection: " + address;
#     return clickData['points'][0]['hovertext'];

def flipping_chart(PID, major, minor=None, estimator = ["cat"]):
    '''
    Description:
    The guy who draws. The core of this file. If you dare deleting this...
    I will cry.
    Input:
    PID: A nine-digit-ish thing for each property used by USPS or so...
    major: The major variable. Will be the x-axis of a flipping chart.
    minor: The minor variable. If assigned, will summon spaghettis for each unique value.
    estimator: A list of strings, each represents a regressor.
    Output:
    A flipping chart. Yeah.
    '''
    fig = px.scatter();

    for method in estimator:
        temp_house = front_end.reset_index();
        temp_house = temp_house[temp_house["PID"] == PID];

        # Compute the predicted value of the selected house.
        maj_val = float(temp_house[major]);
        temp_frame = temp_house.set_index("PID");
        pred_price = predict_from_front(temp_frame, method)[0];
        # pred_price = cat.predict(front_to_back(temp_frame, "cat"))[0];

        temp_house.drop(major, axis = 1, inplace = True);
        if minor: temp_house.drop(minor, axis = 1, inplace = True);

        if "Range" in column_title_dict[major]:
            major_range = np.linspace(column_title_dict[major]["Range"][0],\
            column_title_dict[major]["Range"][1],\
            int((column_title_dict[major]["Range"][1]-column_title_dict[major]["Range"][0])/\
            column_title_dict[major]["Range"][2])+1);
        else:
            r_max = front_end[major].max();
            r_min = front_end[major].min();
            major_range = np.linspace(r_min, r_max, 300);
        if minor:
            minor_range = sorted(list(front_end[minor].unique()));

        temp = pd.DataFrame({"PID": [PID for i in major_range], major: major_range});
        temp_house = temp_house.merge(temp, on="PID");
        temp_major = temp_house[major];

        if minor:
            temp = pd.DataFrame({"PID": [PID for i in minor_range], minor: minor_range});
            temp_house = temp_house.merge(temp, on="PID");
            temp_minor = temp_house[minor];

        temp_house.set_index("PID", inplace=True);
        # temp_house = front_to_back(temp_house, "cat");

        # If the order of variables matter for the regressor, rearrange it.
        if method_dict[method]["Order"]:
            temp_house = temp_house[front_end.columns];

        temp_house["Sale Price Predicted"] = predict_from_front(temp_house, method);

        if not minor:
            fig.add_trace(go.Scatter(x=temp_house[major], y=temp_house["Sale Price Predicted"],\
            name = major+'_'+method));
            # fig = px.line(temp_house, x=major, y="Sale Price Predicted",\
            # labels={major: column_title_dict[major]["Description"]});
        else:
            #fig = px.scatter();
            for i in minor_range:
                temp = temp_house[temp_house[minor]==i];

                if type(i) in [np.float64, np.int64]: name = "{:.2f}_{}".format(i, method);
                else: name = i + '_' + method;
                fig.add_trace(go.Scatter(x=temp[major], y=temp["Sale Price Predicted"], name = name));

        fig.add_trace(go.Scatter(x=[maj_val], y=[pred_price], name="Current_"+method,\
        marker=dict(size=12)));

        if not minor:
            fig.update_layout(showlegend=False);

    fig.update_layout(legend=dict(yanchor="bottom", y=0.01, xanchor="right", x=0.99,\
    font=dict(size=8), bgcolor='rgba(0,0,0,0)'));
    fig.update_xaxes(title_text=column_title_dict[major]["Description"]);
    fig.update_yaxes(title_text="Sales Price Predicted");
    return fig;


@app.callback(
    Output('pid_quality_change', 'figure'),
    Input('pid_scatter', 'clickData'),
    Input('flip_major', 'value'),
    Input('flip_minor', 'value'),
    Input('check_methods', 'value'))
def update_flip_chart(clickData, major, minor, methods):
    if not clickData or not major: return px.scatter();

    temp = housing;
    methods = [x[6:] for x in methods];
    address = clickData['points'][0]['hovertext'];
    if "PID" not in temp.columns: temp.reset_index(inplace = True);
    PID = int(temp[temp["Address"]==address]["PID"]);
    return flipping_chart(PID, major, minor, methods);

@app.callback(
    Output('pid_area_change', 'figure'),
    Input('pid_scatter', 'clickData'),
    Input('explore_major', 'value'),
    Input('explore_minor', 'value'),
    Input('check_methods', 'value'))
def update_explore_chart(clickData, major, minor, methods):
    if not clickData or not major: return px.scatter();

    temp = housing;
    methods = [x[6:] for x in methods];
    address = clickData['points'][0]['hovertext'];
    if "PID" not in temp.columns: temp.reset_index(inplace = True);
    PID = int(temp[temp["Address"]==address]["PID"]);
    return flipping_chart(PID, major, minor, methods);


# @app.callback(
#     Output('app-1-display-value', 'children'),
#     Input('app-1-dropdown', 'value'))
# def display_value(value):
#     return 'You have selected "{}"'.format(value)
