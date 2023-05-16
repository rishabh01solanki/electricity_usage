import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.colors as mcolors
from matplotlib.animation import FuncAnimation
import calendar


df = pd.read_csv('/Users/rishabhsolanki/Desktop/Github/electricity_usage/IntervalData.csv') # change path as needed
df['USAGE_DATE'] = pd.to_datetime(df['USAGE_DATE'])
df['DAY'] = df['USAGE_DATE'].dt.day
df['MONTH'] = df['USAGE_DATE'].dt.month

# function to filter and pivot data for a selected month
def get_monthly_data(month):

    df_month = df[df['MONTH'] == month]
    daily_usage = df_month.groupby(['DAY','USAGE_START_TIME'])['USAGE_KWH'].sum().reset_index()
    daily_usage_pivot = daily_usage.pivot(index='USAGE_START_TIME', columns='DAY', values='USAGE_KWH')
    
    return daily_usage_pivot

fig, ax = plt.subplots(figsize=(9, 7))  # Adjust figure size as needed


vmin = df['USAGE_KWH'].min()
vmax = df['USAGE_KWH'].max()
norm = mcolors.Normalize(vmin=vmin, vmax=vmax)


plt.rcParams['font.size'] = 12
plt.rcParams['font.family'] = 'Arial'

def update(month):
    ax.clear()
    daily_usage_pivot = get_monthly_data(month)
    
    # Ensure a consistent plot size by using reindex to fill in any missing days or times
    days = range(1, df['DAY'].max() + 1)
    times = sorted(df['USAGE_START_TIME'].unique())
    daily_usage_pivot = daily_usage_pivot.reindex(index=times, columns=days, fill_value=0)
    
    sns.heatmap(daily_usage_pivot, cmap='YlGnBu', norm=norm, cbar=False, ax=ax)
    ax.set_title(f'Hourly Electricity Usage for {calendar.month_name[month]}', fontsize=16, fontweight='bold')
    ax.set_xlabel('Day of the Month', fontsize=14, labelpad=15)
    ax.set_ylabel('Start Time of Usage', fontsize=14, labelpad=15)


cbar = fig.colorbar(plt.cm.ScalarMappable(norm=norm, cmap='YlGnBu'), ax=ax)
cbar.set_label('Usage (kWh)', fontsize=14, labelpad = 15)  # Add a label to the colorbar

ani = FuncAnimation(fig, update, frames=range(3, 13), interval=500)
ani.save('animation.gif', writer='imagemagick', fps=2)

