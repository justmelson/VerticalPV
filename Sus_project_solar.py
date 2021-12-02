# -*- coding: utf-8 -*-
"""
Created on Sun Oct 24 17:08:37 2021

@author: justm
"""


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import matplotlib.dates as mdates

from datetime import datetime
from datetime import timedelta



from pv_output import (pv_output_front, pv_output_rear)
pd.options.mode.chained_assignment = None  # default='warn'


#%% Input data 
# tilt representes inclination of the solar panel (in degress), orientation
# in degress (south=0)
tilt=90
orientation=90
lat = 56.162939 # latitude of Aarhus
lon = 10.203921 # longitude of Aarhus
Kt=0.7

A_module = 2.111*1.046  # m^2
A_shelter = 70*4        # m^2

N = 128  #round(A_shelter/A_module) #number of panels


P_rated = 0.430*N # rated power of system [kWpeak]

# inverter efficiency 93,5%


#%% Timeseries initialization
year = 2018
hour_0 = datetime(year,1,1,0,0,0) - timedelta(hours=1)

hours = [datetime(year,1,1,0,0,0) 
         + timedelta(hours=i) for i in range(0,24*365)]
hours_str = [hour.strftime("%Y-%m-%d %H:%M ") for hour in hours]

timeseries = pd.DataFrame(
            index=pd.Series(
                data = hours,
                name = 'utc_time'),
            columns = pd.Series(
                data = ['B_0_h', 'K_t', 'G_ground_h', 'solar_altitude', 'F', 
                        'B_ground_h', 'D_ground_h', 'incident_angle', 
                        'B_tilted', 'D_tilted', 'R_tilted', 'G_tilted'], 
                name = 'names'))


#%%
# Weather data of cloud cover

weather = pd.read_csv('https://raw.githubusercontent.com/martavp/SOLAR_ENERGY_project/master/weather_station/weather_data.csv',sep=';',index_col=0)
weather.index = pd.to_datetime(weather.index) #Reindex to datetime datatype
weather = weather[~weather.index.duplicated()] #Remove apparent duplicate
weather=weather[:-1] #remove last value, thats corrupt
weather=weather.reindex(timeseries.index, method='nearest') #convert time to same time as timeseries. Fill NaN values with "nearest"


#%% Calculations

# Power output
# P_total = np.zeros(360)
# P_total_front = np.zeros(360)
# P_total_rear = np.zeros(360)

# ori = np.arange(-180,180,1)
# for i in range(360):
#     P_total_front[i] = pv_output_front(ori[i],lat,lon,weather,N)
#     P_total_rear[i] = pv_output_rear(ori[i],lat,lon,weather,N)
#     P_total[i] = (P_total_front[i]+P_total_rear[i]) # [kW]
#     print(i)

P_total_front = pv_output_front(orientation,lat,lon,weather,N)
P_total_rear = pv_output_rear(orientation,lat,lon,weather,N)
P_total = (P_total_front+P_total_rear) # [kW]

a = (P_total-P_total*0.85)/30
P = np.zeros(30)
for i in range(30):
    if i == 0:
        P[i] = P_total
    else:
        P[i] = P[i-1]-a

P_lifetime = sum(P) # efficiency drops linearly to 85% at 30 years, this has to be taken into account 
# # Emissions
# GWP_PV = np.zeros(360) 
# GWP_DK = np.zeros(360)
# GWP_delta = np.zeros(360)

# for i in range(360):
#     GWP_PV[i] = 0.0684*P_total[i]   # kg CO2 eq./kW * kW
#     GWP_DK[i] = 0.371*P_total[i]    # kg CO2 eq./kW * kW
#     GWP_delta[i] = GWP_DK[i]-GWP_PV[i]

GHG_emissions = 57*P_rated      # GHG emissions kg/kW*kW
El_consumption = 89*P_rated     # Electricity consumption per kW module in kWh
Water_consumption = 932*P_rated # Water consumption per kW module in kg
#%% Plotting
# plt.rcParams["figure.figsize"] = (15,5)
# # plot
# plt.figure(figsize=(20, 10),dpi=400)

# gs1 = gridspec.GridSpec(2, 2)
# gs1.update(wspace=0.3, hspace=0.3)
# ax1 = plt.subplot(gs1[0,0])
# ax1.plot(timeseries['G_ground_h']['2018-01-01 00:00':'2018-12-30 00:00'], 
#          label='Radiation', color='orange')
# #ax1.plot(timeseries['2018-02-01 00:00':'2018-02-08 00:00'].index,timeseries.loc['2018-06-01 00:00':'2018-06-08 00:00','G_ground_h'].values, 
# #         label='June', color= 'orange') #Use february as x axis, but plot july as the y points
# plt.title('Global radiation on a horizontal surface 2018')
# ax1.legend(fancybox=True, shadow=True,fontsize=12, loc='upper right')
# ax1.set_ylabel('W/m2')
# date_form = mdates.DateFormatter("%d")
# #ax1.xaxis.set_major_formatter(date_form)

# plt.figure(dpi=400)
# plt.plot(GWP_PV,c="red",linewidth=4.0)
# plt.plot(GWP_DK,c="blue",linewidth=4.0)
# plt.plot(GWP_delta,c="g",linewidth=4.0)
# plt.xlabel("Orientation of front panel (0=South)")
# plt.ylabel("GWP [kg CO2 eq.]")
# plt.grid()

# plt.figure(dpi=400)
# plt.plot(P_total,c="salmon",linewidth=7.0,label="Total")
# plt.plot(P_total_front,linewidth=3.0,label="Front")
# plt.plot(P_total_rear,c="r",linewidth=3.0,label = "rear")
# plt.xlabel("Orientation of front panel (0=South)")
# plt.ylabel("Yearly output [kWh]")
# plt.axvline(90,c="chartreuse")
# plt.legend()


# P_min = min(P_total)
# P_max = max(P_total)
# P_delta = P_max - P_min
# gain = P_delta/P_min * 100




#%% PV GHG calcs



print("Yearly power output =","%.1f"% P_total,"kWh")

e_pv = 0.0536
E_total = 10000*e_pv*30 # total emission of 10 kWpeak system [t]

e_kwp = E_total/10

#E_VBPV = e_kwp*P_rated # total emissions of case system over 30 year lifetime [kgCO2eq] 
E_VBPV = 71368 # from analysis


e_VBPV = E_VBPV/P_lifetime # emission of VB[kgCO2eq/kWh]

e_DK = 0.117 # Danish grid mix[kgCO2eq/kWh]

e_delta = e_DK-e_VBPV # saved emissions [kgCO2eq/kWh]

n = E_VBPV/e_DK 

payback = n/P_total # payback time in years

print("payback time =","%.1f"% payback,"years")

#%% Sensitivity 

e_2050 = 0.0249 # kgCO2eq/kWh
e_2020 = 0.373  # kgCO2eq/kWh

a = (e_2050-e_2020)/30
e = np.zeros(30)
for i in range(30):
    e[i] = a*i+e_2020   # DK gridmix kgCO2eq/kWh.

years = range(2020,2050,1)
plt.figure(dpi=400)
plt.plot(years,e)

e_delta = np.zeros(30)
n = np.zeros(30)
payback = np.zeros(30)

for i in range(len(years)):
    n[i] = E_VBPV/e[i]
    payback[i] = n[i]/P_total # payback time in years

plt.figure(dpi=400)
plt.plot(years,payback,label="Payback time")
plt.axhline(30,label="Lifetime of PV system",c="r")
plt.xlabel("Year installed") 
plt.ylabel("Years")
plt.legend()
plt.grid()

plt.figure(dpi=400)
plt.plot(years,e,label="Danish grid emissions")
plt.axhline(30,label="Lifetime of PV system",c="r")
plt.xlabel("Year installed") 
plt.ylabel("\frac{kgCO2eq}{kWh}")
plt.legend()
plt.grid()