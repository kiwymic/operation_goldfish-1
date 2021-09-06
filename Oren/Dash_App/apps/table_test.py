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


app = dash.Dash(__name__)

app.layout = html.Div([
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
                width={"size": 2}
            ),
#### This adds a boolean opperator
            dbc.Col(children=[
                daq.BooleanSwitch(
                    id= "boolean_switch",
                    on=True,
                    color="#9B51E0",
                    label="Finished Basement",
                    labelPosition="top"
                ),

                daq.NumericInput(
                    id='daq_bath_full',
                    min=0,
                    max=10,
                    value=df_current.at[5, 'Current'],
                    label = 'Bathrooms - Full',
                    labelPosition = 'bottom',
                ),
                daq.NumericInput(
                    id='daq_bedroom',
                    min=0,
                    max=10,
                    value=df_current.at[6, 'Current'],
                    label='Bedrooms',
                    labelPosition='bottom',
                )
            ],
                width={"size": 2}
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
                width={"size": 2}
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