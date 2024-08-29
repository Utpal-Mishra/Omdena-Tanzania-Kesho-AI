# LIBRARIES

import streamlit as st

import numpy as np
import pandas as pd
import os

import requests

import time
from datetime import datetime, timedelta

# !conda install -c conda-forge geopy --yes
from geopy.geocoders import Nominatim

import folium
from folium.plugins import Fullscreen
from streamlit_folium import folium_static

import plotly.express as px
import plotly.graph_objects as go
import plotly.figure_factory as ff
from plotly.subplots import make_subplots

print('Libraries Imported\n')

###########################################
   
def app():
        
        path = os.path.dirname(__file__)
        w23 = pd.read_csv(path+'/weather2023.csv')
        w23['station_nm'] = w23['station_nm'].apply(lambda x: x.title())  
        w23['date'] = pd.to_datetime(w23['date'], format='%d-%m-%Y').dt.date
        w23['date'] = pd.to_datetime(w23['date'], errors='coerce')
        
        w22 = pd.read_csv(path+'/weather2022.csv')
        w22['station_nm'] = w22['station_nm'].apply(lambda x: x.title())  
        w22['date'] = pd.to_datetime(w22['date'], format='%d-%m-%Y').dt.date
        w22['date'] = pd.to_datetime(w22['date'], errors='coerce')
        
        w21 = pd.read_csv(path+'/weather2021.csv')
        w21['station_nm'] = w21['station_nm'].apply(lambda x: x.title())  
        w21['date'] = pd.to_datetime(w21['date'], format='%d-%m-%Y').dt.date
        w21['date'] = pd.to_datetime(w21['date'], errors='coerce')
        
        w20 = pd.read_csv(path+'/weather2020.csv')
        w20['station_nm'] = w20['station_nm'].apply(lambda x: x.title())  
        w20['date'] = pd.to_datetime(w20['date'], format='%d-%m-%Y').dt.date
        w20['date'] = pd.to_datetime(w20['date'], errors='coerce')
        
        w19 = pd.read_csv(path+'/weather2019.csv')
        w19['station_nm'] = w19['station_nm'].apply(lambda x: x.title())  
        w19['date'] = pd.to_datetime(w19['date'], format='%d-%m-%Y').dt.date
        w19['date'] = pd.to_datetime(w19['date'], errors='coerce')
        
        w = [w19, w20, w21, w22, w23]
        weatherdata = pd.concat(w, ignore_index=True)
          
        visuals = weatherdata[['date', 'temp', 'dwpt', 'rhum', 'prcp', 'wdir', 'wspd', 'pres']]       
        visuals = visuals.groupby('date').mean().reset_index()
 
        visuals['month'] = visuals['date'].dt.month 
        # # visuals['month'] = visuals['date'].apply(lambda x: int(x.split('-')[1].split('-')[0]))
        visuals['month_nm'] = visuals['date'].dt.strftime('%b')
        visuals['year'] = visuals['date'].dt.year
        
        # Function to map month to season
        def get_season(month):
            if month in [12, 1, 2]:
                return 'Winter'
            elif month in [3, 4, 5]:
                return 'Spring'
            elif month in [6, 7, 8]:
                return 'Summer'
            else:
                return 'Fall'
            
        # Add season column
        visuals['season'] = visuals['month'].apply(get_season)

        # Create Streamlit selectbox for filtering
        filter_option = st.selectbox('Select Time Frame', ['Year-wise', '6-Month-wise', 'Season-wise'])
        
        # Function to insert NaN values at year boundaries
        def boundaries(data):
            years = data['year'].unique()
            new_data = pd.DataFrame(columns = data.columns)
            for year in years:
                year_data = data[data['year'] == year]
                new_data = pd.concat([new_data, year_data, pd.DataFrame({col: [None] for col in data.columns})], ignore_index=True)
            return new_data
        
        # Filter data based on the selected option
        if filter_option == 'Year-wise':
            # Year-wise filter
            year = st.selectbox('Select Year', sorted(visuals['year'].unique()))
            filtered_data = visuals[visuals['year'] == year]
            
        elif filter_option == '6-Month-wise':
            # 6-Month-wise filter
            months = [(1, 6), (7, 12)]
            selected_months = st.selectbox('Select 6-Month Period', ['Jan-Jun', 'Jul-Dec'])
            start_month, end_month = months[0] if selected_months == 'Jan-Jun' else months[1]
            filtered_data = visuals[(visuals['month'] >= start_month) & (visuals['month'] <= end_month)]
            filtered_data = boundaries(filtered_data)
            
        elif filter_option == 'Season-wise':
            # Season-wise filter
            season = st.selectbox('Select Season', ['Winter', 'Spring', 'Summer', 'Fall'])
            filtered_data = visuals[visuals['season'] == season]
            filtered_data = boundaries(filtered_data)
                
        st.write("")
        st.write("")
        
        # PLOT: Temperature and Precipitation
        
        if st.checkbox("Understand Environmental Conditions, Optimize Agricultural Practices, Manage Natural Resources, and plan for Extreme Weather Events"):
            
            # Create subplots with secondary y-axis
            fig = make_subplots(specs=[[{"secondary_y": True}]])
            fig.add_trace(go.Scatter(x = filtered_data['date'], y = filtered_data['temp'], name = 'Temperature', mode ='lines', line=dict(color = 'firebrick')), secondary_y = False)
            fig.add_trace(go.Bar(x = filtered_data['date'], y = filtered_data['prcp'], name = 'Precipitation', marker = dict(color = 'royalblue')), secondary_y = True)

            # Update layout
            fig.update_layout(height=700, width=1500, title_text='Temperature and Precipitation Over Time: To understand Environmental Conditions, Optimize Agricultural Practices, Manage Natural Resources, and plan for Extreme Weather Events', xaxis_title='Date')
            fig.update_xaxes(rangeslider_visible = True, showline = True, linewidth = 2, linecolor = 'black', mirror = True)
            fig.update_yaxes(showline = True, title_text='Temperature (°C)', linewidth = 2, linecolor = 'black', secondary_y=False)
            fig.update_yaxes(title_text='Precipitation (mm)', linewidth = 2, linecolor = 'black', secondary_y=True)
            st.plotly_chart(fig)
        
            st.divider()        
        
        # PLOT: Temperature and Humidity
                       
        if st.checkbox("Understand the Heat Index and Comfort Levels"): 
            
            # Create subplots with secondary y-axis
            fig = make_subplots(specs=[[{"secondary_y": True}]])
            fig.add_trace(go.Scatter(x = filtered_data['date'], y = filtered_data['temp'], name = 'Temperature', mode ='markers+lines', line=dict(color = 'firebrick')), secondary_y = False)
            fig.add_trace(go.Scatter(x = filtered_data['date'], y = filtered_data['rhum'], name = 'Humidity', marker = dict(color = 'royalblue')), secondary_y = True)

            # Update layout
            fig.update_layout(height=700, width=1500, title_text='Temperature and Humidity Over Time: To understand the Heat Index and Comfort Levels', xaxis_title='Date')
            fig.update_xaxes(rangeslider_visible = True, showline = True, linewidth = 2, linecolor = 'black', mirror = True)
            fig.update_yaxes(showline = True, title_text='Temperature (°C)', linewidth = 2, linecolor = 'black', secondary_y=False)
            fig.update_yaxes(title_text='Humidity', linewidth = 2, linecolor = 'black', secondary_y=True)
            st.plotly_chart(fig)
        
            st.divider()
        
        # PLOT: Wind Speed and Wind Direction
        
        if st.checkbox("Understand Weather Patterns and Storm Tracking"): 
                                
            # Create subplots with secondary y-axis
            fig = make_subplots(specs=[[{"secondary_y": True}]])
            fig.add_trace(go.Scatter(x = filtered_data['date'], y = filtered_data['wspd'], name = 'Wind Speed (km/h)', mode ='lines', line=dict(color = 'firebrick')), secondary_y = False)
            fig.add_trace(go.Scatter(x = filtered_data['date'], y = filtered_data['wdir'], name = 'Wind Direction (°)', marker = dict(color = 'royalblue')), secondary_y = True)

            # Update layout
            fig.update_layout(height=700, width=1500, title_text='Wind Speed and Wind Direction Over Time: To understand Weather Patterns and Storm Tracking', xaxis_title='Date')
            fig.update_xaxes(rangeslider_visible = True, showline = True, linewidth = 2, linecolor = 'black', mirror = True)
            fig.update_yaxes(showline = True, title_text='Wind Speed (km/h)', linewidth = 2, linecolor = 'black', secondary_y=False)
            fig.update_yaxes(title_text='Wind Direction (°)', linewidth = 2, linecolor = 'black', secondary_y=True)
            st.plotly_chart(fig)
        
            st.divider()
        
        # PLOT: Precipitation and Wind Speed
        
        if st.checkbox("Understand Weather Patterns, Storm Tracking and Overall Atmospheric Conditions"): 
                                
            # Create subplots with secondary y-axis
            fig = make_subplots(specs=[[{"secondary_y": True}]])
            fig.add_trace(go.Scatter(x = filtered_data['date'], y = filtered_data['prcp'], name = 'Precipitation', marker = dict(color = 'royalblue')), secondary_y = False)
            fig.add_trace(go.Scatter(x = filtered_data['date'], y = filtered_data['wspd'], name = 'Wind Speed (km/h)', mode = 'markers', marker = dict(size = filtered_data['wspd'], color = filtered_data['wspd'], colorscale = 'Viridis')), secondary_y = True)

            # Update layout
            fig.update_layout(height=700, width=1500, title_text='Precipitation and Wind Speed Over Time: Weather Patterns, Storm Tracking and Overall Atmospheric Conditions', xaxis_title='Date')
            fig.update_xaxes(rangeslider_visible = True, showline = True, linewidth = 2, linecolor = 'black', mirror = True)
            fig.update_yaxes(showline = True, title_text='Precipitation', linewidth = 2, linecolor = 'black', secondary_y=False)
            fig.update_yaxes(title_text='Wind Speed (km/h)', linewidth = 2, linecolor = 'black', secondary_y=True)
            st.plotly_chart(fig)
        
            st.divider()