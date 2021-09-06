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

df = pd.read_csv('./data/basic_housing.csv', index_col=0)
params = df.columns
df = df[df['PID'] == 916176125]

df_current = df.T.reset_index()
df_current.columns = ['Features', 'Current']
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
                        1250: '1250',
                        2500: '2,500',
                        5000: '5,000',
                    },
                    value= 1000  ###df_current.at[5, 'Current']   ########## NEED TO FIND ROW FOR IT
                ),
#### Basement Slider
                html.P('Finished Basement Square Footage',
                       className='text-center text-primary, mb-1, medium'),
                dcc.Slider(
                    id='future_basement',
                    min=0,
                    max=2000,  #### create max by adding low and high quality
                    step=10,
                    marks={
                        0: '0',
                        1250: '1250',
                        2500: '2,500',
                        5000: '5,000',
                    },
                    value=1000  ###df_current.at[5, 'Current']   ########## NEED TO FIND ROW FOR IT
                ),
#### Porch Slider
                html.P('Porch Square Footage',
                       className='text-center text-primary, mb-1, medium'),
                dcc.Slider(
                    id='future_porch',
                    min=300,
                    max=1250,
                    step=10,
                    marks={
                        0: '0',
                        1250: '1250',
                    },
                    value=100  ###df_current.at[5, 'Current']   ########## NEED TO FIND ROW FOR IT
                ),

########## QUALITY SLIDERS
                html.P('Overall Quality',
                       className='text-center text-primary, mb-1, medium'),
                dcc.Slider(
                    id='future_overall_q',
                    min=0,
                    max=100,
                    step=1,
                    marks={
                        0: '0',
                        50: '50',
                        100: '100'
                    },
                    value=50  ###df_current.at[5, 'Current']   ########## NEED TO FIND ROW FOR IT
                ),

###### NUMERIC INPUTS

#######Bedroom
                daq.NumericInput(
                    id='future_bedroom',
                    min=0,
                    max=6,
                    value=df_current.at[6, 'Current'],
                    label='Bedrooms',
                    labelPosition='top',
                ),
####### Bathroom - full
                daq.NumericInput(
                    id='future_bath_full',
                    min=1,
                    max=4,
                    value=df_current.at[5, 'Current'],
                    label = 'Bathrooms - Full',
                    labelPosition = 'top',
                ),
####### Bathroom - half
                daq.NumericInput(
                    id='future_bath_half',
                    min=0,
                    max=2,
                    value= 1,  ###df_current.at[5, 'Current'],
                    label = 'Bathrooms - Half',
                    labelPosition = 'top',
                ),
####### Fireplaces
                daq.NumericInput(
                    id='future_fireplaces',
                    min=0,
                    max=4,
                    value= 1, ### df_current.at[5, 'Current'],
                    label = 'Fireplaces',
                    labelPosition = 'top',
                ),
####### Garage
                daq.NumericInput(
                    id='future_garage',
                    min=0,
                    max=5,
                    value= 1, ### df_current.at[5, 'Current'],
                    label = 'Garage - Cars',
                    labelPosition = 'top',
                ),

##### Pool - boolean
                daq.BooleanSwitch(
                    id="pool_switch",
                    on=False,
                    color="#9B51E0",
                    label="Pool",
                    labelPosition="top"
                ),
####### Dropdown for masonry veneer
                dcc.Dropdown(
                        id='future-veneer',
                        options=[
                            {'label': 'New York City', 'value': 'NYC'},
                            {'label': 'Montreal', 'value': 'MTL'},
                            {'label': 'San Francisco', 'value': 'SF'}
                        ],
                        value='NYC'
                    )


            ],
                width={"size": 6}
            ),

            dbc.Col(children=[
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


@app.callback(
    Output('computed-table', 'data'),
    Input('daq_bath_full', 'value'),
    Input('daq_bedroom', 'value')
)
def display_output(value1, value2):
    df_future.at[5, 'CompEdit'] = value1
    df_future.at[6, 'CompEdit'] = value2
    return df_future.to_dict('records')


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