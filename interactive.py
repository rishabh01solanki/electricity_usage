import pandas as pd
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objects as go

df = pd.read_csv('/Users/rishabhsolanki/Desktop/Github/electricity_usage/IntervalData.csv')
df['USAGE_DATE'] = pd.to_datetime(df['USAGE_DATE'])
df['DAY'] = df['USAGE_DATE'].dt.day
df['MONTH'] = df['USAGE_DATE'].dt.month
df['YEAR'] = df['USAGE_DATE'].dt.year

app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("Electricity Usage Dashboard", style={'text-align': 'center'}),
    
    dcc.Dropdown(id="slct_month",
                 options=[
                     {"label": "January", "value": 1},
                     {"label": "February", "value": 2},
                     {"label": "March", "value": 3},
                     {"label": "April", "value": 4},
                     {"label": "May", "value": 5},
                     {"label": "June", "value": 6},
                     {"label": "July", "value": 7},
                     {"label": "August", "value": 8},
                     {"label": "September", "value": 9},
                     {"label": "October", "value": 10},
                     {"label": "November", "value": 11},
                     {"label": "December", "value": 12}],
                 multi=False,
                 value=5,
                 style={'width': "40%"}
                 ),

    html.Div(id='output_container', children=[]),
    html.Br(),

    dcc.Graph(id='my_heatmap', figure={}),
    dcc.Graph(id='my_lineplot', figure={})

])


@app.callback(
    [Output(component_id='output_container', component_property='children'),
     Output(component_id='my_heatmap', component_property='figure'),
     Output(component_id='my_lineplot', component_property='figure')],
    [Input(component_id='slct_month', component_property='value')]
)
def update_graph(option_slctd):
    print(option_slctd)
    print(type(option_slctd))

    container = "The month chosen by user was: {}".format(option_slctd)

    dff = df.copy()
    dff = dff[dff["MONTH"] == option_slctd]

    daily_usage = dff.groupby(['DAY','USAGE_START_TIME'])['USAGE_KWH'].sum().reset_index()
    daily_usage_pivot = daily_usage.pivot(index='USAGE_START_TIME', columns='DAY', values='USAGE_KWH')

    heatmap_fig = go.Figure(data=go.Heatmap(
                   z=daily_usage_pivot.values,
                   x=daily_usage_pivot.columns,
                   y=daily_usage_pivot.index,
                   colorscale='Viridis'))

    # Add labels to the heatmap
    heatmap_fig.update_layout(
        title='Hourly Electricity Usage Heatmap',
        xaxis_title='Day of the Month',
        yaxis_title='Start Time of Usage',
    )

    daily_usage = dff.groupby(['USAGE_DATE'])['USAGE_KWH'].sum().reset_index()

    lineplot_fig = go.Figure()
    lineplot_fig.add_trace(go.Scatter(x=daily_usage['USAGE_DATE'], y=daily_usage['USAGE_KWH'],
                        mode='lines',
                        name='lines'))

    # Add labels to the line plot
    lineplot_fig.update_layout(
        title='Daily Total Electricity Usage',
        xaxis_title='Date',
        yaxis_title='Total Usage (KWh)',
    )

    return container, heatmap_fig, lineplot_fig



if __name__ == '__main__':
    app.run_server(debug=False)

