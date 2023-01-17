# import necessary libraries
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


# Read in the CSV file
df = pd.read_csv('/Users/rishabhsolanki/Desktop/Github/electricity_usage/IntervalData.csv')

# convert the USAGE_DATE column to a datetime object
df['USAGE_DATE'] = pd.to_datetime(df['USAGE_DATE'])

# create a new column for the day
df['DAY'] = df['USAGE_DATE'].dt.day

# function to plot the usage for a selected month
def plot_monthly_usage(month):
    # filter the data for the selected month
    df_month = df[df['USAGE_DATE'].dt.month == month]

    # group the data by day and sum the usage
    daily_usage = df_month.groupby(['DAY','USAGE_START_TIME'])['USAGE_KWH'].sum().reset_index()

    # pivot the data so that the days are on the x-axis and the hours are on the y-axis
    daily_usage_pivot = daily_usage.pivot(index='USAGE_START_TIME', columns='DAY', values='USAGE_KWH')

    # create the heatmap
    sns.heatmap(daily_usage_pivot, cmap='YlGnBu')
    plt.title(f'Hourly electricity usage for August')
    plt.xlabel('Day')
    plt.ylabel('Time')

    # show the plot
    plt.show()

plot_monthly_usage(8)



