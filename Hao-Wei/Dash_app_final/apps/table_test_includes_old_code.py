import dash
from dash.dependencies import Input, Output, State
import dash_table
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
from collections import OrderedDict
# import dash_design_kit as ddk
import dash_daq as daq

df = pd.read_csv('./data/basic_housing.csv', index_col=0)
params = df.columns
df = df[df['PID'] == 916176125]

df_current = df.T.reset_index()
df_current.columns = ['Features', 'Current']
df_future = df_current.copy() #.drop(['Features'], axis =1)
df_future.columns = ['Features', 'CompEdit']
# df = df.join(pd.Series(name='UserEdit')).join(df1)
# df = df.join(df1)

app = dash.Dash(__name__)

app.layout = html.Div([
    dbc.Container([
        dbc.Row([
            dbc.Col(html.H3("Mapping Housing and Points of Interest in Ames, Iowa",
                            className='text-center text-primary, mb-4'),
                    width=12),

            dbc.Col(
    dash_table.DataTable(

        id='computed-table',
        columns=[
            # {"name": i, "id": i} for i in df.columns
            {'name': 'Feature',  'id': 'Features'},
            {'name': 'Current House', 'id': 'Current'},
            # {'name': 'Changes', 'id': 'UserEdit'},
            {'name': 'Future House', 'id': 'CompEdit'}
        ],
        data=df.to_dict('records'),
        editable=True

        # dropdown_conditional=[{
        #     'if': {
        #         'column_id': 'UserEdit',
        #         'filter_query': '{Features} = "FullBath"'
        #     },
        #     'options': [
        #         {'label': i, 'value': i}
        #         for i in range(-2,5,1)
        #             # '-1',
        #             # '0',
        #             # '1',
        #             # '2',
        #             # '3'
        #
        #     ]
        # }]


    # 'options':
            #     [{'label': '- 1', 'value': -1}
            #     {'label': '0', 'value': 0}
            #     {'label': '+1', 'value': 1}
            #     {'label': '+2', 'value': 2}]


    # , {
    #         'if': {
    #             'column_id': 'Neighborhood',
    #             'filter_query': '{City} eq "Montreal"'
    #         },
    #         'options': [
    #                         {'label': i, 'value': i}
    #                         for i in [
    #                             'Mile End',
    #                             'Plateau',
    #                             'Hochelaga'
    #                         ]
    #                     ]
    #     },
    #     {
    #         'if': {
    #             'column_id': 'Neighborhood',
    #             'filter_query': '{City} eq "Los Angeles"'
    #         },
    #         'options': [
    #                         {'label': i, 'value': i}
    #                         for i in [
    #                             'Venice',
    #                             'Hollywood',
    #                             'Los Feliz'
    #                         ]
    #                     ]
    #     }

    )),
# table = dbc.Table.from_dataframe(df, striped=True, bordered=True, hover=True),

#### This adds a boolean opperator

    dbc.Col(
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
        value=df.at[5, 'Current'],
        label = 'Bathrooms - Full',
        labelPosition = 'bottom',
    ),
    daq.NumericInput(
        id='daq_bedroom',
        min=0,
        max=10,
        value=df.at[6, 'Current'],
        label='Bedrooms',
        labelPosition='bottom',
    )),
            dbc.Col(


            )
])
])
])
# @app.callback(
#     Output('computed-table', 'data'),
#     Input('computed-table', 'data_timestamp'),
#     State('computed-table', 'data'))
# def update_columns(timestamp, rows):
#     for row in rows:
#         try:
#             row['CompEdit'] = float(row['UserEdit']) + float(row['Current'])
#         except:
#             row['CompEdit'] = 'NA'
#     return rows

@app.callback(
    Output('computed-table', 'data'),
    Input('daq_bath_full', 'value'),
    Input('daq_bedroom', 'value')
)
def display_output(value1, value2):
    df.at[5, 'CompEdit'] = value1
    df.at[6, 'CompEdit'] = value2 #df.at[6, 'Current'] +
    # df[df['CompEdit'] == 'FullBath'] = df[df['Current'] == 'FullBath'] + value
    # print(df['Current'] == 'FullBath')
    # print(df)
    return df.to_dict('records')


if __name__ == '__main__':
    app.run_server(debug=True)


    #
    # df = pd.DataFrame(rows, columns=[c['name'] for c in columns])
    # return {
    #     'data': [{
    #         'type': 'parcoords',
    #         'dimensions': [{
    #             'label': col['name'],
    #             'values': df[col['id']]
    #         } for col in columns]
    #     }]
    # }



#
# ,
#     dcc.Graph(id='table-editing-simple-output')

# @app.callback(
#     Output('table-editing-simple-output', 'figure'),
#     Input('table-editing-simple', 'data'),
#     Input('table-editing-simple', 'columns'))
# def display_output(rows, columns):
#     df = pd.DataFrame(rows, columns=[c['name'] for c in columns])
#     return {
#         'data': [{
#             'type': 'parcoords',
#             'dimensions': [{
#                 'label': col['name'],
#                 'values': df[col['id']]
#             } for col in columns]
#         }]
#     }

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