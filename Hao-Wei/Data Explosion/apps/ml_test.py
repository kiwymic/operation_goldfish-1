import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
import dash_table as dt;
import pandas as pd;
import numpy as np;
import plotly.express as px;
import plotly.graph_objs as go;

from dictionaries import *;

from app import app
from app import server

## Machine learning toolkits
from catboost import CatBoostRegressor;
from sklearn.preprocessing import LabelEncoder;

# Utility functions which sends from front end to back end
def front_to_back_cat(fe):
    be = fe.copy();

    be['ExterQualDisc']=be['ExterQual']-be['OverallQual'];
    be['OverallCondDisc']=be['OverallCond']-be['OverallQual'];
    be['KitchenQualDisc']=be['KitchenQual']-be['OverallQual'];
    be=be.drop(["SalePrice", 'ExterQual','OverallCond','KitchenQual'],axis=1);

    be = dummify(be, non_dummies, dummies);
    return be;

housing_address = pd.read_csv('./data/house_coordinates_address.csv', index_col = 0);
housing = pd.read_csv('./data/ames_housing_price_data_v6.csv', index_col = 0);
front_end = housing;
y = front_end["SalePrice"];

# Loading Mo's frontend to backend code.
#transformation of front-end to back-end, and catboost application

back_end = front_to_back_cat(front_end);

cat = CatBoostRegressor();
cat.load_model("./data/HousePriceCatBoost", "cbm")
print(cat.score(back_end, y))
cat_pred = cat.predict(back_end)

# These are the columns to be displayed in a standard DataTable.
display_columns = {"Sale Price Price":"SalePrice", "Ground Living Area":"GrLivArea", "Quality (1-8)": "Quality",\
                  "# of Bedrooms": "BedroomAbvGr", "# of Bathrooms": "FullBath", "Neighborhood": "Neighborhood"};
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
            html.Hr(),
            dcc.Checklist(id = "show_all_pids",
            options=[
            {'label': 'Show all properties', 'value': 'show_all_pid'}],
            value=[],
            labelStyle={'display': 'inline-block'},
            className='text-center'
            ),
            dcc.Graph(id="pid_scatter", clickData=None),
            dt.DataTable(id='pid_table',
                         columns=[{"name": k, "id": display_columns[k]} for k in display_columns],
                         page_current=0, page_size=PAGE_SIZE, page_action='custom')
        ], width = {'size':7, 'order':1}),

        ### INPUTS
        dbc.Col([
            html.H5("Here is your dream home...", id = "selected_pid",
                    className='text-center text-primary'),
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
                 size="Quality", color="Neighborhood", hover_name= "PID",
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
    temp = housing_address.reset_index();
    temp = temp[temp["PID"] == clickData['points'][0]['hovertext']]
    # temp["Address"] = temp["Address"].apply(lambda x: x[:-17]); # ", Ames, Iowa, USA"
    address = temp[temp["PID"] == clickData['points'][0]['hovertext']]["Address"];
    return "Your selection: " + address;
#     return clickData['points'][0]['hovertext'];

def flipping_chart(PID, major, minor=None):
    '''
    Input:
    PID: A nine-digit-ish thing for each property used by USPS or so...
    major: The major variable. Will be the x-axis of a flipping chart.
    minor: The minor variable. If assigned, will summon spaghettis for each unique value.
    Output:
    A flipping chart. Yeah.
    '''
    temp_house = front_end.reset_index();
    temp_house = temp_house[temp_house["PID"] == PID];

    # Compute the predicted value of the selected house.
    maj_val = float(temp_house[major]);
    temp_frame = temp_house.set_index("PID");
    pred_price = cat.predict(front_to_back_cat(temp_frame))[0];

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
        print(minor_range)

    temp = pd.DataFrame({"PID": [PID for i in major_range], major: major_range});
    temp_house = temp_house.merge(temp, on="PID");
    if minor:
        temp = pd.DataFrame({"PID": [PID for i in minor_range], minor: minor_range});
        temp_house = temp_house.merge(temp, on="PID");
        temp_minor = temp_house[minor];

    temp_house.set_index("PID", inplace=True);
    temp_house = front_to_back_cat(temp_house);

    # If the column is killed when moving to backend, pad it.
    temp_house["Sale Price Predicted"] = cat.predict(temp_house);
    if minor in ['Neighborhood', 'BldgType', 'MasVnrType', 'ExterQual','OverallCond','KitchenQual']:
        temp_house.reset_index(inplace = True);
        temp_house[minor] = temp_minor;
        print(temp_house[["Sale Price Predicted", minor]])

    if not minor:
        fig = px.line(temp_house, x=major, y="Sale Price Predicted",\
        labels={major: column_title_dict[major]["Description"]});
    else:
        fig = px.scatter();
        for i in minor_range:
            temp = temp_house[temp_house[minor]==i];

            fig.add_trace(go.Scatter(x=temp[major], y=temp["Sale Price Predicted"], name = str(i)));

    fig.add_trace(go.Scatter(x=[maj_val], y=[pred_price], name="Current",\
    marker=dict(size=12, color = '#FF8833')));

    if not minor:
        fig.update_layout(showlegend=False);

    fig.update_layout(legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01, bgcolor='rgba(0,0,0,0)'));
    fig.update_xaxes(title_text=column_title_dict[major]["Description"]);
    fig.update_yaxes(title_text="Sales Price Predicted");
    return fig;


@app.callback(
    Output('pid_quality_change', 'figure'),
    Input('pid_scatter', 'clickData'),
    Input('flip_major', 'value'),
    Input('flip_minor', 'value'))
def update_flip_chart(clickData, major, minor):
    if not clickData or not major: return px.scatter();

    PID = clickData['points'][0]['hovertext'];
    return flipping_chart(PID, major, minor);

@app.callback(
    Output('pid_area_change', 'figure'),
    Input('pid_scatter', 'clickData'),
    Input('explore_major', 'value'),
    Input('explore_minor', 'value'))
def update_explore_chart(clickData, major, minor):
    if not clickData or not major: return px.scatter();

    PID = clickData['points'][0]['hovertext'];
    return flipping_chart(PID, major, minor);


# @app.callback(
#     Output('app-1-display-value', 'children'),
#     Input('app-1-dropdown', 'value'))
# def display_value(value):
#     return 'You have selected "{}"'.format(value)
