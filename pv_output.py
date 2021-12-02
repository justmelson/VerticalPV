# -*- coding: utf-8 -*-
"""
Created on Wed Oct 27 09:35:59 2021

@author: justm
"""

def pv_output_front(orientation,lat,lon,weather,N):
    import pandas as pd
    import numpy as np

    
    from datetime import datetime
    from datetime import timedelta
    
    
    from solarfun import (calculate_B_0_horizontal,
                          calculate_G_ground_horizontal,                      
                          calculate_diffuse_fraction,
                          calculate_incident_angle,
                          Gaussian_tilt_orientation)
    tilt = 90
    Kt=0.7

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
                            'B_tilted', 'D_tilted', 'R_tilted', 'G_tilted','Tc','P','P_total'], 
                    name = 'names')
                )
    
    
    
    
    # Calculations
    
    
    # Calculate extraterrestrial irradiance
    timeseries['B_0_h'] = calculate_B_0_horizontal(hours, hour_0, lon, lat)  
    
    # Clearness index is assumed to be equal to 0.7 at every hour
    timeseries['K_t']=Kt*np.ones(len(hours))  
    
    # Calculate global horizontal irradiance on the ground
    [timeseries['G_ground_h'], timeseries['solar_altitude']] = calculate_G_ground_horizontal(hours, hour_0, lon, lat, timeseries['K_t'])
    
    # # Calculate diffuse fraction -#What model are we using???? - solarfun function seems to not use Page model Fd=1-1.14K
    timeseries['F'] = calculate_diffuse_fraction(hours, hour_0, lon, lat, timeseries['K_t'])
    
    # # Calculate direct and diffuse irradiance on the horizontal surface
    timeseries['B_ground_h']=[x*(1-y) for x,y in zip(timeseries['G_ground_h'], timeseries['F'])]
    timeseries['D_ground_h']=[x*y for x,y in zip(timeseries['G_ground_h'], timeseries['F'])]
    
    # Cloud cover calculations
    weather['FD']=weather['Cloud']/100 #FD=Cloudcover/100
    timeseries['FD']=weather['FD'] #copy columns to the timeseries dataframe
    timeseries['D_ground_h']=timeseries['G_ground_h']*timeseries['FD'] #Diffusive is diffusive fraction * global irradiance
    timeseries['B_ground_h']=(1-timeseries['FD'])*timeseries['G_ground_h'] #direct is the rest
    
    
    rho=0.05
    #Calculate incident angle
    timeseries['incident_angle'] = calculate_incident_angle(hours, hour_0, lon, lat,  tilt, orientation)
    
    #Calculate Direct (B) irradiance on solar panel 
    for i in timeseries.index:
      if np.cos(timeseries['incident_angle'][i]/180*np.pi) > 0:
          timeseries['B_tilted'][i]=np.cos(timeseries['incident_angle'][i]/180*np.pi)*timeseries['B_ground_h'][i]
      else:
          timeseries['B_tilted'][i]=0
    #
    #Calculate diffuse (D) irradiance on solar panel ##ISOTROPIC
    timeseries['D_tilted']=[x*(1-np.cos(tilt/180*np.pi))/2 for x in timeseries['D_ground_h']]
    
    #Calculate albedo (R)
    timeseries['R_tilted']=[rho*x*(1-np.cos(tilt/180*np.pi))/2 for x in timeseries['G_ground_h']]
    
    #Calculate global irradiance on solar panel
    timeseries['G_tilted']=timeseries['B_tilted']+timeseries['D_tilted']+timeseries['R_tilted']
    
    # produced power
    Pmax=430
    NOCT=43
    gamma=-0.34/100
    TcSTC=25

    #Cell temperature:
    #Tc=Tair+(NOCT-20)*G/800
    timeseries['Tc']=[x+(NOCT-20)*y/800 for x,y in zip(weather['Temp'],timeseries['G_tilted'])]
    
    #Produced power
    #P=G/N*(1+gamma*(Tc-TcSTC))*Pmax
    timeseries['P']=[y/1000*(1+gamma*(x-TcSTC))*Pmax for x,y in zip(timeseries['Tc'],timeseries['G_tilted'])]
    timeseries['P_total']=[x*N for x in timeseries['P']]
    
    P_total_front = sum(timeseries['P_total'])/1000 # Yearly power output in kW
    
    return P_total_front


#%%
def pv_output_rear(orientation,lat,lon,weather,N):
    import pandas as pd
    import numpy as np
    # import matplotlib.pyplot as plt
    # import matplotlib.gridspec as gridspec
    # import matplotlib.dates as mdates
    
    from datetime import datetime
    from datetime import timedelta
    
    
    from solarfun import (calculate_B_0_horizontal,
                          calculate_G_ground_horizontal,                      
                          calculate_diffuse_fraction,
                          calculate_incident_angle)
    tilt = 90
    Kt=0.7
    bifaciality_factor = 0.7
    
    # Inverting orientation to panels on the other vertical side
    if orientation > 0:
        orientation = orientation - 180
    else:
        orientation = orientation + 180
            
    year = 2018
    hour_0 = datetime(year,1,1,0,0,0) - timedelta(hours=1)
    
    hours = [datetime(year,1,1,0,0,0) 
             + timedelta(hours=i) for i in range(0,24*365)]
    # hours_str = [hour.strftime("%Y-%m-%d %H:%M ") for hour in hours]
    
    timeseries = pd.DataFrame(
                index=pd.Series(
                    data = hours,
                    name = 'utc_time'),
                columns = pd.Series(
                    data = ['B_0_h', 'K_t', 'G_ground_h', 'solar_altitude', 'F', 
                            'B_ground_h', 'D_ground_h', 'incident_angle', 
                            'B_tilted', 'D_tilted', 'R_tilted', 'G_tilted','Tc','P','P_total'], 
                    name = 'names')
                )
    
    
    
    
    #%% Calculations
    
    # Calculate extraterrestrial irradiance
    timeseries['B_0_h'] = calculate_B_0_horizontal(hours, hour_0, lon, lat)  
    
    # # Clearness index is assumed to be equal to 0.7 at every hour
    timeseries['K_t']=Kt*np.ones(len(hours))  
    
    # Calculate global horizontal irradiance on the ground
    [timeseries['G_ground_h'], timeseries['solar_altitude']] = calculate_G_ground_horizontal(hours, hour_0, lon, lat, timeseries['K_t'])
    
    # # Calculate diffuse fraction -#What model are we using???? - solarfun function seems to not use Page model Fd=1-1.14K
    timeseries['F'] = calculate_diffuse_fraction(hours, hour_0, lon, lat, timeseries['K_t'])
    
    # # Calculate direct and diffuse irradiance on the horizontal surface
    timeseries['B_ground_h']=[x*(1-y) for x,y in zip(timeseries['G_ground_h'], timeseries['F'])]
    timeseries['D_ground_h']=[x*y for x,y in zip(timeseries['G_ground_h'], timeseries['F'])]
    
    # Cloud cover calculations
    weather['FD']=weather['Cloud']/100 #FD=Cloudcover/100
    timeseries['FD']=weather['FD'] #copy columns to the timeseries dataframe
    timeseries['D_ground_h']=timeseries['G_ground_h']*timeseries['FD'] #Diffusive is diffusive fraction * global irradiance
    timeseries['B_ground_h']=(1-timeseries['FD'])*timeseries['G_ground_h'] #direct is the rest
    
    
    rho=0.05
    #Calculate incident angle
    timeseries['incident_angle'] = calculate_incident_angle(hours, hour_0, lon, lat,  tilt, orientation)
    
    #Calculate Direct (B) irradiance on solar panel 
    for i in timeseries.index:
      if np.cos(timeseries['incident_angle'][i]/180*np.pi) > 0:
          timeseries['B_tilted'][i]=np.cos(timeseries['incident_angle'][i]/180*np.pi)*timeseries['B_ground_h'][i]
      else:
          timeseries['B_tilted'][i]=0
    #
    #Calculate diffuse (D) irradiance on solar panel ##ISOTROPIC
    timeseries['D_tilted']=[x*(1-np.cos(tilt/180*np.pi))/2 for x in timeseries['D_ground_h']]
    
    #Calculate albedo (R)
    timeseries['R_tilted']=[rho*x*(1-np.cos(tilt/180*np.pi))/2 for x in timeseries['G_ground_h']]
    
    #Calculate global irradiance on solar panel
    timeseries['G_tilted']=timeseries['B_tilted']+timeseries['D_tilted']+timeseries['R_tilted']
    
    #%% produced power
    Pmax=430
    NOCT=43
    gamma=-0.34/100
    TcSTC=25

    #Cell temperature:
    #Tc=Tair+(NOCT-20)*G/800
    timeseries['Tc']=[x+(NOCT-20)*y/800 for x,y in zip(weather['Temp'],timeseries['G_tilted'])]
    
    #Produced power
    #P=G/N*(1+gamma*(Tc-TcSTC))*Pmax
    timeseries['P']=[y/1000*(1+gamma*(x-TcSTC))*Pmax for x,y in zip(timeseries['Tc'],timeseries['G_tilted'])]
    timeseries['P_total']=[x*N for x in timeseries['P']]
        
    P_total_rear = (sum(timeseries['P_total'])/1000)*bifaciality_factor # Yearly power output in kW
    
    return P_total_rear