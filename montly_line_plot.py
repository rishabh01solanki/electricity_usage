import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np
import pandas as pd
from scipy.interpolate import make_interp_spline, BSpline
import calendar

df = pd.read_csv('/Users/rishabhsolanki/Desktop/Github/electricity_usage/IntervalData.csv')  # change path as needed
df['USAGE_DATE'] = pd.to_datetime(df['USAGE_DATE'])
df['DAY'] = df['USAGE_DATE'].dt.day
df['MONTH'] = df['USAGE_DATE'].dt.month


def get_daily_data(month):
    df_month = df[df['MONTH'] == month]
    daily_usage = df_month.groupby(['DAY'])['USAGE_KWH'].sum().reset_index() 
    return daily_usage  



month_to_plot = 7 # change this to the month you want to plot
daily_data = get_daily_data(month_to_plot)



# I am using quadratic spline to make the curve a bit smooth.
#TODO: wanna check if the standard deviation of the errors while using spline to smoothen. 
#should be only a visual gimmick, gives an overall power consumption profile.
xnew = np.linspace(daily_data['DAY'].min(), daily_data['DAY'].max(), 500) 
spl = make_interp_spline(daily_data['DAY'], daily_data['USAGE_KWH'], k=2)
y_smooth = spl(xnew)

fig, ax = plt.subplots()
ax.set_facecolor('lightgray')

ln, = plt.plot([], [], 'b-', animated=True)
dot, = plt.plot([], [], 'o', color='orange', animated=True)

def init():
    ax.set_xlim(1, 32)
    ax.set_ylim(0, 60)
    ax.set_xlabel('Day of the Month', fontsize=10, labelpad=4)
    ax.set_ylabel('Usage (kWh)', fontsize=10, labelpad=6)
    ax.set_title(f'Time Series analysis of power consumption for {calendar.month_name[month_to_plot]}', fontsize=12, pad=10)
    return ln, dot,

def update(frame):
    ln.set_data(xnew[:frame], y_smooth[:frame])
    dot.set_data(xnew[frame], y_smooth[frame])
    return ln, dot,

ani = FuncAnimation(fig, update, frames=len(xnew),
                    init_func=init, blit=True, interval=20, repeat=False)

ani.save('consmptn_july.gif', writer='imagemagick', fps=50)
#plt.show()

