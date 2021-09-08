import dash
from dash.dependencies import Input, Output
import dash_table
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd



df = pd.read_csv('./data/basic_housing.csv', index_col=0)
params = df.columns
df = df[df['PID'] == 916176125]
print(df.columns)
print(df)
print(type(df))

#df = [tuple(x) for x in df.to_records(index=False)]
# df = list(df.itertuples(index=False))

# df = [tuple(x) for x in df.to_numpy()]
# print(df)
# print(df.columns)
# print(df.T.columns)
# print(type(df))


df = df.T.reset_index()
df.columns = ['Features', 'Current']
print(df.columns)
print(df)
print(type(df))



# list_of_lists = []
# for col in df.columns:
#     currlist = list(df[col])
#     list_of_lists.append(currlist)
# df = list_of_lists
# print(df)

# df = df.T
# df = df.append(pd.Series(name='UserEdit')).append(pd.Series(name='CompEdit'))

app = dash.Dash(__name__)




app.layout = html.Div([
    dash_table.DataTable(

        id='table-editing-simple',
        columns=[{"name": i, "id": i} for i in df.columns],
        data=df.to_dict('records'),
        editable=True
    )
])

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


if __name__ == '__main__':
    app.run_server(debug=True)