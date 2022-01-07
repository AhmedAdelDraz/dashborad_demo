import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
import pathlib
from app import app

# get relative data folder
PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath("../datasets").resolve()

dfv = pd.read_csv(DATA_PATH.joinpath("vgsales.csv"))  # GregorySmith Kaggle
sales_list = ["North American Sales", "EU Sales", "Japan Sales", "Other Sales",	"World Sales"]


layout = html.Div([
    dbc.Row(html.H1('Video Games Sales', style={"textAlign": "center"})),
    dbc.Row([
        dbc.Col(dcc.Dropdown(
            id='genre-dropdown', value='Strategy', clearable=False,
            options=[{'label': x, 'value': x} for x in sorted(dfv.Genre.unique())]
        ), width=2),

        dbc.Col(dcc.Dropdown(
            id='sales-dropdown', value='EU Sales', clearable=False,
            persistence=True, persistence_type='memory',
            options=[{'label': x, 'value': x} for x in sales_list]
        ), width=2),
    ]),
    dbc.Row(dcc.Graph(id='my-bar', figure={})),
])


@app.callback(
    Output(component_id='my-bar', component_property='figure'),
    [Input(component_id='genre-dropdown', component_property='value'),
     Input(component_id='sales-dropdown', component_property='value')]
)
def display_value(genre_chosen, sales_chosen):
    dfv_fltrd = dfv[dfv['Genre'] == genre_chosen]
    dfv_fltrd = dfv_fltrd.nlargest(10, sales_chosen)
    fig = px.bar(dfv_fltrd, x='Video Game', y=sales_chosen, color='Platform',template='plotly_dark')
    fig = fig.update_yaxes(tickprefix="$", ticksuffix="M")
    return fig
