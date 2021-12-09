# -*- coding: utf-8 -*-
"""
Created on Fri Jul 19 16:35:20 2019

@author: Marta

Script to process json file including weather data measured at Navitas rooftop
station.
 
"""

import json
import pandas as pd
import numpy as np

weather_df = pd.DataFrame(
             index=pd.Series(
                data = np.arange(0,8760*5),
                name = 'index'),
             columns = pd.Series(
                data = ['TimeStamp', 
                        'Temp', 
                        'Cloud', 
                        'WindVelocity', 
                        'WindDirection', 
                        'UV'], 
                name = 'names')
             )
            
with open('data/Weather.php.json') as json_file:
    data = json.load(json_file)
    for i,p in enumerate(data):
        weather_df['TimeStamp'][i]=p['TimeStamp']
        weather_df['Temp'][i]=p['TempAkt']
        weather_df['Cloud'][i]=p['Cloud']
        weather_df['WindVelocity'][i]=p['VindHast']
        weather_df['WindDirection'][i]=p['VindRet']
        weather_df['UV'][i]=p['UV']        

weather_df.set_index('TimeStamp', inplace=True)       
#save dataframe with weather information
weather_df.to_csv('weather_data.csv', sep=';')        