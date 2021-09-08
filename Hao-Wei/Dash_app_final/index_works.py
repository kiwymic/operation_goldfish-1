import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
import dash_table


from app import app
from app import server
from apps import maps, ml_test
# from data import loading_stuff

dropdown = dbc.DropdownMenu(
    children=[
        dbc.DropdownMenuItem("Home", href="/index"),
        dbc.DropdownMenuItem("Maps", href="/maps"),
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
    html.Div(id='page-content')
])


@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/maps':
        return maps.layout
    elif pathname == '/plans':
        return plans.layout
    else:
        return maps.layout

@app.callback(
    Output('output-container-range-slider', 'children'),
    [Input('price', 'value')])
def update_output_price_range(value):
    return ('${:,} - ${:,}'.format(value[0], value[1]))



@app.callback(
    # dash.dependencies.Output('PID_list', 'children'),
    Output("housing_id", "hideout"),
    Input('price', 'value'),
    Input('sqft', 'value'),
    Input("input_bathrooms", "value"),
    Input("input_bedrooms", "value")
)
def update_output(prices, sqfts, bathrms, bedrms):
    foo = list(maps.housing_basic[(maps.housing_basic['SalePrice'] > prices[0]) &
                       (maps.housing_basic['SalePrice'] < prices[1]) &
                       (maps.housing_basic['GrLivArea'] > sqfts[0]) &
                       (maps.housing_basic['GrLivArea'] < sqfts[1]) &
                       (maps.housing_basic['FullBath'] == bathrms) &
                       (maps.housing_basic['BedroomAbvGr'] == bedrms)]
                ['PID'])
    return dict(name=foo)


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