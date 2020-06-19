import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

df = pd.read_csv('data/avocado.csv', parse_dates=['Date'])
df.drop('Unnamed: 0', axis=1, inplace=True)
df = df.sort_values(by=['Date', 'type'])

app = dash.Dash(__name__)
server = app.server

region_names = df.region.unique()
region_names.sort()

total_volume = df.groupby(['year', 'region','type'])['Total Volume'].sum()
total_volume = total_volume.reset_index()

volume_fig = px.bar(
    total_volume.groupby(['year','type']).sum().reset_index(), 
    x='year', 
    y='Total Volume', 
    color='type', 
    # barmode='group', 
    labels={'year':'Year'},
    title = 'Avocado volume per year and type'
)
volume_fig.update_layout(xaxis_type='category', plot_bgcolor="white")

app.layout = html.Div([
    
    html.H1('Avocado\'s across the US', className="app-header"),

    dcc.Graph(
        id='volume-bar-graph',
        figure = volume_fig
    ),

    html.Div([
        html.H2('Avocado\'s within US region', className="app-header")
    ]),

    html.Div([
        html.Div([
            html.H3('Select a state:')
        ], 
        ),

        dcc.Dropdown(
        className="state-dropdown",
        id='region-select', 
        options=[{'label': region, 'value': region} for region in region_names],
        value=region_names[0],
        clearable=False,
        )], className='dropdown'),

    html.Div([
        html.Div([
            dcc.Graph(id='price-graph')
        ]),

        html.Div([
            dcc.Graph(id='region-volume-bar-graph')
        ])
        
    ], className="double-graph")
])


@app.callback(
    Output('price-graph', 'figure'),
    [Input('region-select', 'value')]
)
def update_graph(region_name):
    df_subset = df[df['region'] == region_name]
    fig = px.line(
        df_subset,
        x='Date', 
        y = 'AveragePrice', 
        color='type', 
        labels={'AveragePrice':'Average Price (USD)'},
        title='Average Avocado Price per Region')
    fig.update_layout(yaxis=dict(range=[0,3.5]))
    return fig

@app.callback(
    Output('region-volume-bar-graph', 'figure'),
    [Input('region-select', 'value')]
)
def update_graph(region_name):
    df_subset = total_volume[total_volume['region'] == region_name]
    fig = px.bar(
        df_subset,
        x='year', 
        y = 'Total Volume', 
        color='type', 
        labels={'year':'Year'},
        title='Total Volume per Region')
    fig.update_layout(xaxis_type='category', plot_bgcolor="white")
    return fig


if __name__ == '__main__':
    app.run_server(debug=True)