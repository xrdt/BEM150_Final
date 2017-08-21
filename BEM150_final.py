# BEM/Ec 150 Final Assignment
# Bianca Yang


import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
from matplotlib.finance import date2num
import datetime
import gmplot
from geopy.geocoders import Nominatim

# You can download the dataset from this link: 
# https://data.cityofnewyork.us/Public-Safety/NYPD-Motor-Vehicle-Collisions/h9gi-nx95 

# Note that you will likely not be able to run the entire script in one go 
# since the program takes up a lot of memory. 
# You should run each graph separately to avoid seg faults. 

# Reading in the data will take some time since pandas needs to parse the 
# dates. If you want to increase the speed of data retrieval, you may 
# consider writing to JSON, pickling, or writing to HDF5. 

# Don't be concened with the finance warning matplotlib raises. The notice  
# was created recently, and they haven't changed anything in the code 
# that will cause problems. 

# Show all rows when printing pandas objects 
pd.set_option('display.max_rows', None)

# Parse dates for time series 
data = pd.read_csv('NYPD_Motor_Vehicle_Collisions.csv', sep=',', header=0,\
        na_values="     ", index_col=None, parse_dates=['DATE'])

# Columns for reference
'''['DATE', 'TIME', 'BOROUGH', 'ZIP CODE', 'LATITUDE', 'LONGITUDE',
       'LOCATION', 'ON STREET NAME', 'CROSS STREET NAME', 'OFF STREET NAME',
       'NUMBER OF PERSONS INJURED', 'NUMBER OF PERSONS KILLED',
       'NUMBER OF PEDESTRIANS INJURED', 'NUMBER OF PEDESTRIANS KILLED',
       'NUMBER OF CYCLIST INJURED', 'NUMBER OF CYCLIST KILLED',
       'NUMBER OF MOTORIST INJURED', 'NUMBER OF MOTORIST KILLED',
       'CONTRIBUTING FACTOR VEHICLE 1', 'CONTRIBUTING FACTOR VEHICLE 2',
       'CONTRIBUTING FACTOR VEHICLE 3', 'CONTRIBUTING FACTOR VEHICLE 4',
       'CONTRIBUTING FACTOR VEHICLE 5', 'UNIQUE KEY', 'VEHICLE TYPE CODE 1',
       'VEHICLE TYPE CODE 2', 'VEHICLE TYPE CODE 3', 'VEHICLE TYPE CODE 4',
       'VEHICLE TYPE CODE 5']'''

# Colors for time series lines
color_fmt = ['c-', 'g-', 'm-', 'y-', 'k-']


# Trends in accident rates over the years. 
# grouped_time = data.groupby('DATE').sum()['NUMBER OF PERSONS INJURED']

# Create a time series showing the number of people injured per date 

# Tick every 6 months
months = mdates.MonthLocator(bymonthday=1, interval=6)

# Print abbrev. month name and full year
monthfmt = mdates.DateFormatter("%b %Y")
'''
fig, ax = plt.subplots(5, 1)

# Plot by borough 
grouped_boroughs = data.groupby(['BOROUGH', \
        'DATE']).sum()['NUMBER OF PERSONS INJURED']
grouped_boroughs = grouped_boroughs.unstack(level='BOROUGH')
grouped_boroughs.fillna(value=0)

i = 0
for borough in grouped_boroughs.columns:
    ax[i].plot_date(grouped_boroughs.index, \
            grouped_boroughs[borough].values, fmt=color_fmt[i], lw=.5)
    ax[i].xaxis.set_minor_locator(months)
    ax[i].xaxis.set_major_formatter(monthfmt)
    ax[i].set_title('Number of Persons Injured in ' + str(borough) \
            + ' By Time')
    i += 1

fig.text(0.5, 0.04, 'Time', ha='center')
fig.text(0.04, 0.5, 'Number of Persons Injured', \
        va='center', rotation='vertical')

plt.show()
'''

''' 
# Plot total number of people injured over time
f, ax7 = plt.subplots(1)
ax7.plot_date(grouped_boroughs.index, grouped_time, fmt='r-', lw=.5)
ax7.xaxis.set_minor_locator(months)
ax7.xaxis.set_major_formatter(monthfmt)
ax7.set_title('Total Number of Persons Injured Over Time')
plt.show()
'''

'''
# Contributing factors by date 
# Use only the top 1 factor or it segfaults due to memory issues. 
month_1 = data.groupby(['DATE', 'CONTRIBUTING FACTOR VEHICLE 1']).count() 
month_1 = month_1.unstack(level='CONTRIBUTING FACTOR VEHICLE 1')
month_1 = month_1.groupby('DATE').sum()['UNIQUE KEY']
month_1.drop('Unspecified', axis=1, inplace=True)
month_1.drop('Other Vehicular', axis=1, inplace=True)

month_1 = month_1.sort_values(month_1.index[0], axis=1, ascending=False)
print(month_1.columns)

fig, ax2 = plt.subplots()

i = 0
# Plot the top 5 contributing factors as of date 0 over the rest of the 
# time in the dataset. 
for factor in month_1.columns[:5]:
    ax2.plot_date(month_1.index, month_1[factor], fmt=color_fmt[i], lw=.5)
    i += 1

ax2.xaxis.set_minor_locator(months)
ax2.xaxis.set_major_formatter(monthfmt)
ax2.set_title('Contributing Factor by Time')
fig.text(0.5, 0.04, 'Time', ha='center')
fig.text(0.04, 0.5, 'Number of Incidents', \
        va='center', rotation='vertical')
        
ax2.legend()
plt.show()
'''

'''
# Trends in vehicle type accidents over the years
fig, ax3 = plt.subplots(5, 1)
car_1 = data.groupby(['DATE', 'VEHICLE TYPE CODE 1']).count()
car_1 = car_1.unstack(level='VEHICLE TYPE CODE 1')

car_2 = data.groupby(['DATE', 'VEHICLE TYPE CODE 2']).count()
car_2 = car_2.unstack(level='VEHICLE TYPE CODE 2')

car_all = pd.concat([car_1, car_2])
car_all = car_all.groupby('DATE').sum()['UNIQUE KEY']
car_all.drop('UNKNOWN', axis=1, inplace=True)
car_all.drop('OTHER', axis=1, inplace=True)
car_all = car_all.sort_values(car_all.index[0], axis=1, ascending=False)

i = 0
for car in car_all.columns[:5]:
    ax3[i].plot_date(car_all.index, car_all[car], fmt=color_fmt[i], lw=.5)
    ax3[i].xaxis.set_minor_locator(months)
    ax3[i].xaxis.set_major_formatter(monthfmt)
    ax3[i].set_title('Collisions by Time for ' + str(car))
    i += 1

fig.text(0.5, 0.04, 'Time', ha='center')
fig.text(0.04, 0.5, 'Number of Incidents', \
        va='center', rotation='vertical')
plt.show()
'''

'''
# Total number of people injured by vehicle type
car_injur_1 = data.groupby(['VEHICLE TYPE CODE 1', \
        'NUMBER OF PERSONS INJURED']).count()
car_injur_1 = car_injur_1.unstack(level='VEHICLE TYPE CODE 1')

car_injur_2 = data.groupby(['VEHICLE TYPE CODE 2', \
        'NUMBER OF PERSONS INJURED']).count()
car_injur_2 =car_injur_2.unstack(level='VEHICLE TYPE CODE 2')

car_injur_all = pd.concat([car_injur_1, car_injur_2])
car_injur_all = car_injur_all.groupby(car_injur_all.index).sum()['UNIQUE KEY']
car_injur_all.drop('UNKNOWN', axis=1, inplace=True)
car_injur_all.drop('OTHER', axis=1, inplace=True)
car_sum_injur = car_injur_all.sum(axis=0)
car_sum_injur = car_sum_injur.sort_values(ascending=False)
print(car_sum_injur.index)

fig, ax4 = plt.subplots()
# Bar chart 
ax4.bar(range(0, 10, 2), car_sum_injur.values[:5]) 
ax4.set_xticklabels(car_sum_injur.index[:5])
ax4.set_ylabel('Number of People Injured')
ax4.set_xticks(range(0, 10, 2))
ax4.set_title('Number of People Injured by Vehicle Type')
plt.show()
'''
