import pandas as pd
import plotly.graph_objs as go
from plotly.subplots import make_subplots

# Read in the CSV file
df = pd.read_csv('/Users/rishabhsolanki/Desktop/Github/electricity_usage/IntervalData.csv')

# convert the USAGE_DATE column to a datetime object
df['USAGE_DATE'] = pd.to_datetime(df['USAGE_DATE'])

# create a new column for the day
df['DAY'] = df['USAGE_DATE'].dt.day

def plot_monthly_usage(month):
    # filter the data for the selected month
    df_month = df[df['USAGE_DATE'].dt.month == month]

    # group the data by day and sum the usage
    daily_usage = df_month.groupby(['DAY','USAGE_START_TIME'])['USAGE_KWH'].sum().reset_index()

    # pivot the data so that the days are on the x-axis and the hours are on the y-axis
    daily_usage_pivot = daily_usage.pivot(index='USAGE_START_TIME', columns='DAY', values='USAGE_KWH')

    # create the heatmap
    fig = make_subplots(rows=1, cols=1, specs=[[{'type': 'heatmap'}]])
    fig.add_trace(go.Heatmap(z=daily_usage_pivot,
                             x=daily_usage_pivot.columns,
                             y=daily_usage_pivot.index,
                             colorscale='YlGnBu',
                             colorbar=dict(title='Usage (kWh)'),
                         hovertemplate = 'Day: %{x}<br>Time: %{y}<br>Usage (kWh): %{z}'))
    fig.update_layout(title=f'Hourly electricity usage for month {month}',
                      xaxis=dict(title='Day',
                                 tickmode='array',
                                 tickvals=list(range(1,32)),
                                 ticktext=list(range(1,32))),
                      yaxis=dict(title='Time'))

    fig.show()

plot_monthly_usage(8)
