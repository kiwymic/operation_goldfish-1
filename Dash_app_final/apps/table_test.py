import dash
from dash.dependencies import Input, Output, State
import dash_table
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
from collections import OrderedDict
# import dash_design_kit as ddk
import dash_daq as daq
import dash_bootstrap_components as dbc
import numpy as np

df = pd.read_csv('./data/ames_housing_price_data_final.csv')
params = df.columns
df = df[df['PID'] == 909176150]
df_pred = df.copy()
df = df.apply(lambda x: np.round(x, 1) if type(x[0]) == np.float64 else x)
df_current = df.T.reset_index()
df_current.columns = ['Features', 'Current']
sale_price = df_current.loc[1, "Current"]
address = df_current.loc[2, "Current"]
droprows = [0, 1, 2, 12, 13, 14, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40]
df_current = df_current.drop(droprows, axis =0)


df_future = df_current.copy()
df_future.columns = ['Features', 'CompEdit']

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.YETI],
                meta_tags=[{'name': 'viewport',
                            'content': 'width=device-width, initial-scale=1.0'}]
                )


layout = html.Div([
    dbc.Container([
        dbc.Row([
            dbc.Col(children=[html.H3("Current House",
                                      className='text-center text-primary, mb-4'),
                                html.H3("${:,}".format(sale_price),
                                      className='text-center text-primary, mb-4', id = 'current_price'),
                              dash_table.DataTable(
                                  id='current-table',
                                  columns=[
                                      {'name': 'Feature',  'id': 'Features'},
                                      {'name': 'Current House', 'id': 'Current'}
                                  ],
                                  data=df_current.to_dict('records'),
                                  style_cell_conditional=[
                                        {'if': {'column_id': 'Features'},
                                            'width': '10px'},
                                        {'if': {'column_id': 'Current'},
                                            'width': '10px'},
                                        ],
                                  fill_width=False
                              )],
                width={"size": 3}
            ),

            dbc.Col(children=[
                            html.H3("Home Address",
                                      className='text-center text-primary, mb-4'),
                            html.H3("Here is your dream home...", id = "flip_pid",
                                    className='text-center text-primary'),
                                # html.H3(address,
                                #       className='text-center text-primary, mb-4'),
#### Square Footage slider
                html.P('General Living Area Square Footage',
                       className='text-center text-primary, mb-1, medium'),
                dcc.Slider(
                    id='future_sqft',
                    min=000,
                    max=5000,
                    step=10,
                    marks={
                        00: '0',
                        1250: '1,250',
                        2500: '2,500',
                        3750: '3,750',
                        5000: '5,000',
                    },
                    value= df_current.at[3, 'Current']   ########## NEED TO FIND ROW FOR IT
                ),
#### Basement Slider
                html.P('Finished Basement Square Footage',
                       className='text-center text-primary, mb-1, medium'),
                dcc.Slider(
                    id='future_basement',
                    min=0,
                    # max= 2500,
                    max= df_current.at[17, 'Current'] + df_current.at[6, 'Current'] ,
                    step=1,
                    marks={
                        0: '0',
                        # 100: '100',
                        # 2500: '2,500',
                        (df_current.at[17, 'Current'] + df_current.at[6, 'Current']):
                            f"{df_current.at[17, 'Current'] + df_current.at[6, 'Current']}",
                    },
                    value= df_current.at[17, 'Current']
                ),
#### Porch Slider
                html.P('Porch Square Footage',
                       className='text-center text-primary, mb-1, medium'),
                dcc.Slider(
                    id='future_porch',
                    min=000,
                    max=1250,
                    step=10,
                    marks={
                        0: '0',
                        250: '250',
                        500: '500',
                        750: '750',
                        1000: '1,000',
                        1250: '1,250',
                    },
                    value= df_current.at[16, 'Current']
                ),

########## QUALITY SLIDERS
                html.P('Overall Quality',
                       className='text-center text-primary, mb-1, medium'),
                dcc.Slider(
                    id='future_overall_q',
                    min=0,
                    max=1,
                    step=.1,
                    marks={
                        0: '0',
                        .5: '.5',
                        1: '1'
                    },
                    value= df_current.at[5, 'Current']
                ),
                html.P('Overall Condition',
                       className='text-center text-primary, mb-1, medium'),
                dcc.Slider(
                    id='future_overall_cond',
                    min=0,
                    max=1,
                    step=.1,
                    marks={
                        0: '0',
                        .5: '.5',
                        1: '1'
                    },
                    value=df_current.at[22, 'Current']
                ),
                html.P('Kitchen Quality',
                       className='text-center text-primary, mb-1, medium'),
                dcc.Slider(
                    id='future_kitchen_q',
                    min=0,
                    max=1,
                    step=.1,
                    marks={
                        0: '0',
                        .5: '.5',
                        1: '1'
                    },
                    value=df_current.at[23, 'Current']
                ),
                html.P('Exterior Quality',
                       className='text-center text-primary, mb-1, medium'),
                dcc.Slider(
                    id='future_exterior_q',
                    min=0,
                    max=1,
                    step=.1,
                    marks={
                        0: '0',
                        .5: '.5',
                        1: '1'
                    },
                    value=df_current.at[21, 'Current']
                ),



###### NUMERIC INPUTS

#######Bedroom
                daq.NumericInput(
                    id='future_bedroom',
                    min=0,
                    max=6,
                    value=df_current.at[20, 'Current'],
                    label='Bedrooms',
                    labelPosition='top',
                ),
####### Bathroom - full
                daq.NumericInput(
                    id='future_bath_full',
                    min=1,
                    max=4,
                    value=df_current.at[10, 'Current'],
                    label = 'Bathrooms - Full',
                    labelPosition = 'top',
                ),
####### Bathroom - half
                daq.NumericInput(
                    id='future_bath_half',
                    min=0,
                    max=2,
                    value= df_current.at[11, 'Current'],
                    label = 'Bathrooms - Half',
                    labelPosition = 'top',
                ),
####### Fireplaces
                daq.NumericInput(
                    id='future_fireplaces',
                    min=0,
                    max=4,
                    value= df_current.at[18, 'Current'],
                    label = 'Fireplaces',
                    labelPosition = 'top',
                ),
####### Garage
                daq.NumericInput(
                    id='future_garage',
                    min=0,
                    max=5,
                    value= df_current.at[8, 'Current'],
                    label = 'Garage - Cars',
                    labelPosition = 'top',
                ),

##### Pool - boolean
                daq.BooleanSwitch(
                    id="pool_switch",
                    on=0,
                    color="#9B51E0",
                    label="Pool",
                    labelPosition="top"
                ),
####### Dropdown for masonry veneer
                html.P('Mason Veneer Type',
                       className='text-center text-primary, mb-1, medium'),
                dcc.Dropdown(
                        id='future-veneer',
                        options=[
                            {'label': 'None', 'value': 'None'},
                            {'label': 'Brick Face', 'value': 'Brick Face'},
                            {'label': 'Stone', 'value': 'Stone'}
                        ],
                        value= df_current.at[9, 'Current']
                    )


            ],
                width={"size": 6}
            ),

            dbc.Col(children=[html.H3("Future House",
                                      className='text-center text-primary, mb-4'),
                                html.H3("${:,}".format(sale_price), id='future_price', ########## Change
                                      className='text-center text-primary, mb-4'),
                dash_table.DataTable(
                    id='computed-table',
                    columns=[
                        {'name': 'Feature', 'id': 'Features'},
                        {'name': 'Future House', 'id': 'CompEdit'}
                    ],
                    data=df_future.to_dict('records'),
                                  style_cell_conditional=[
                                        {'if': {'column_id': 'Features'},
                                            'width': '10px'},
                                        {'if': {'column_id': 'CompEdit'},
                                            'width': '10px'},
                                        ],
                                  fill_width=False
                )
                ],
                width={"size": 3}
            )
            ])
        ])
])

#
# @app.callback(
#     Output('computed-table', 'data'),
#     Input('future_sqft', 'value'),
#     Input('future_basement', 'value'),
#     Input('future_porch', 'value'),
#     # Input('future_overall_q', 'value'),
#     Input('future_bedroom', 'value'),
#     Input('future_bath_full', 'value'),
#     Input('future_bath_half', 'value'),
#     Input('future_fireplaces', 'value'),
#     Input('future_garage', 'value'),
#     Input('pool_switch', 'value'),
#     Input('future-veneer', 'value')
# )
# def display_output(sqft_value, basement_value, porch_value, bed_value,
#                    bath_full_value, bath_half_value, fire_value, garage_value,
#                    pool_value, veneer_value):
#     df_future.at[3, 'CompEdit'] = sqft_value
#     df_future.at[17, 'CompEdit'] = basement_value
#     df_future.at[6, 'CompEdit'] = basement_value - (df_current[17, 'CompEdit'] + df_current[6, 'CompEdit'])
#     df_future.at[16, 'CompEdit'] = porch_value
#     df_future.at[20, 'CompEdit'] = bed_value
#     df_future.at[3, 'CompEdit'] = bath_full_value
#     df_future.at[11, 'CompEdit'] = bath_half_value
#     df_future.at[18, 'CompEdit'] = fire_value
#     df_future.at[8, 'CompEdit'] = garage_value
#     df_future.at[19, 'CompEdit'] = pool_value
#     df_future.at[9, 'CompEdit'] = veneer_value
#     return df_future.to_dict('records')


if __name__ == '__main__':
    app.run_server(debug=True)


# @app.callback(
#     Output('numeric-input-output', 'children'),
#     Input('my-daq-numericinput', 'value')
# )
# def update_output(value):
#     return 'The value is {}.'.format(value)




@app.callback(
    Output('computed-table', 'figure'),
    Output('boolean-switch-output', 'children'),
    Input('my-boolean-switch', 'on')
)
def update_output(on):
    return 'The switch is {}.'.format(on)


if __name__ == '__main__':
    app.run_server(debug=True)
