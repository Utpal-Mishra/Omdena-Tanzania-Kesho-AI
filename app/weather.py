# RESOURCES
# Streamlit: https://folium.streamlit.app/
# Icons: https://streamlit-emoji-shortcodes-streamlit-app-gwckff.streamlit.app/
# Metrics: https://www.youtube.com/watch?v=pWxDxhWXJos
# Visuals: https://www.youtube.com/watch?v=G9U4Uixssf0
# Animations: https://www.youtube.com/watch?v=gvfIHiqQQHY
# Animations: https://www.youtube.com/watch?v=gr_KyGfO_eU
# Animations: https://www.youtube.com/watch?v=a8KFaqsq6oE


# LIBRARIES

import streamlit as st
import os
import numpy as np
import pandas as pd

import requests

import time
from datetime import datetime, timedelta

# !conda install -c conda-forge geopy --yes
from geopy.geocoders import Nominatim

import folium
from folium.plugins import HeatMap, MousePosition, LocateControl
from streamlit_folium import folium_static

import plotly.express as px
import plotly.graph_objects as go
import plotly.figure_factory as ff
from plotly.subplots import make_subplots

from twilio.rest import Client

print('Libraries Imported\n')

###########################################
   
def app():
        
        path = os.path.dirname(__file__)
        data = pd.read_csv(path+'/locations.csv')
        data.drop(data.columns[[0]], axis=1, inplace=True)
        data['Region'] = data['Region'].apply(lambda x: x.title())
        
        data = data.groupby(['Region', 'Council', 'Ward']).mean().reset_index()
        data['Population'] = data['Population'].astype(int)
        # st.dataframe(data)
        # st.sidebar.map(data.rename(columns = {'Latitude': 'latitude', 'Longitude': 'longitude'}), zoom = 3, size = 50)
          
        ############################################################################################################
            
        address = 'Tanzania'
        geolocator = Nominatim(user_agent="four_square")
        location = geolocator.geocode(address)
        latitude = location.latitude
        longitude = location.longitude

        # # Create a folium map
        Map = folium.Map(location=[latitude, longitude], zoom_start = 7)
        
        # # Create a list of tile layers
        # tile_layers = {
        # 'Open Street Map': 'openstreetmap',
        # 'Stamen Terrain': 'Stamen Terrain',
        # 'Stamen Toner': 'Stamen Toner',
        # 'Stamen Watercolor': 'Stamen Watercolor',
        # 'CartoDB Positron': 'CartoDB positron',
        # 'CartoDB Dark Matter': 'CartoDB dark_matter',
        # 'Esri Satellite': 'https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}'
        # }

        # # Sidebar for tile layer selection
        # selected_tile = st.sidebar.selectbox('Select Tile Layer', list(tile_layers.keys())) #, index=None, placeholder="Select Map Tile")
            
        # # Add the selected tile layer
        # if selected_tile == 'Esri Satellite':
        #     folium.TileLayer(
        #         tiles=tile_layers[selected_tile],
        #         attr='Esri',
        #         name='Esri Satellite',
        #         overlay=False,
        #         control=True
        #     ).add_to(Map)
        # else:
        #     folium.TileLayer(tile_layers[selected_tile]).add_to(Map)
                               
        # for idx, row in data.iterrows():
        #     folium.Marker([row['Latitude'], 
        #                    row['Longitude']], 
        #                    popup = "Region: " + row['Region'] + ", Council: " + row['Council']  + ", Ward: " + row['Ward']).add_to(Map)
                    
                    # Add LocateControl to the map
        
        # folium_static(Map, width = 1500, height = 750)
        
        # LocateControl(auto_start=True).add_to(Map)
        # JavaScript to extract and print user's coordinates
        # user_coordinates = """
        #     <script>
        #         document.addEventListener('DOMContentLoaded', function() {
        #             let locateButton = document.querySelector('.leaflet-control-locate a');
        #             locateButton.click();
        #             navigator.geolocation.getCurrentPosition(function(position) {
        #                 console.log('User coordinates:', position.coords.latitude, position.coords.longitude);
        #             });
        #         });
        #     </script>
        # """
        
        # Display the JavaScript in Streamlit
        # st.write(user_coordinates, unsafe_allow_html=True)
        # folium_static(Map)
            
        # st.divider()
        
               
        ####################################################################################################################
            
        
        # Adding a sidebar with select boxes
        st.sidebar.header('Select a Location: ')
            
        region = st.sidebar.selectbox('Select Region', 
                                    tuple(sorted(set(list(data['Region'])))),
                                    index = None,
                                    placeholder = "Select Region",
                                    key = 's1')
        
        if region:

            # map = data.loc[(data['Region'] == region)]
            # map = map.reset_index().drop('index', axis = 1)
                                        
            council = st.sidebar.selectbox('Select Council', 
                                            tuple(sorted(set(list(data.loc[(data['Region'] == region)]['Council'])))),
                                            index=None,
                                            placeholder="Select Council")
                
            if council:
            
                map = data.loc[(data['Region'] == region) & (data['Council'] == council)]
                map = map.reset_index().drop('index', axis = 1)
                
                ############################################################################################################
        
                BASEURL = "http://api.weatherapi.com/v1"
                # st.write("BASE URL: 'http://api.weatherapi.com/v1")
                APIKEY = "6bd51cc56e814b49a4b123504240407" # "316171a92c5d458c85735242213008"
                # st.write("API KEY: ------------------------------")
                                    
                Region = []
                Council = []
                Ward = []
                Latitude = []
                Longitude = []
                WindSpeed = []
                WindDegree = []
                WindDirection = []
                Gust = []
                Pressure = []
                Precipitation = []
                Temperature = []
                Visibility = []
                Humidity = []
                Cloud = []
                UV = []
                                                        
                try:
                    for i in range(map.shape[0]):
                        
                        # URL = BASEURL + "/current.json?key=" + APIKEY + "&q=" + str(map.Latitude[i]) + str(map.Longitude[i]) + "&aqi=yes"
                        # URL = BASEURL + "/current.json?key=" + APIKEY + "&q=" + map['Ward'][i] + ', ' + map['Council'][i] + ', ' + map['Region'][i] + ', Tanzania' + "&aqi=yes"
                        URL = BASEURL + "/current.json?key=" + APIKEY + "&q=" + ', ' + map['Ward'][i] + map['Council'][i] + map['Region'][i] + ', Tanzania' + "&aqi=yes"
                        response = requests.get(URL) # HTTP request
                        
                        dt = response.json()

                        Ward.append(map['Ward'][i])
                        Council.append(map['Council'][i])
                        Region.append(map['Region'][i])
                        Latitude.append(str(map['Latitude'][i]))
                        Longitude.append(str(map['Longitude'][i]))
                        WindSpeed.append(str(dt['current']["wind_mph"]))
                        WindDegree.append(str(dt['current']["wind_degree"]))
                        WindDirection.append(dt['current']["wind_dir"])
                        Gust.append(str(dt['current']["gust_mph"]))
                        Pressure.append(str(dt['current']["pressure_mb"]))
                        Precipitation.append(str(dt['current']["precip_mm"]))
                        Temperature.append(str(dt['current']["feelslike_c"]))
                        Visibility.append(str(dt['current']["vis_miles"]))
                        Humidity.append(str(dt['current']["humidity"]))
                        Cloud.append(str(dt['current']["cloud"]))
                        UV.append(str(dt['current']["uv"]))

                    status = pd.DataFrame({'Ward': Ward,
                                        'Council': Council,
                                        'Region': Region,
                                        'Latitude': Latitude,
                                        'Longitude': Longitude,
                                        'WindSpeed': WindSpeed,
                                        'WindDegree': WindDegree,
                                        'WindDirection': WindDirection,
                                        'Gust': Gust,
                                        'Pressure': Pressure,
                                        'Precipitation': Precipitation,
                                        'Temperature': Temperature,
                                        'Visibility': Visibility,
                                        'Humidity': Humidity,
                                        'Cloud': Cloud,
                                        'UV': UV})

                    # print('Data Shape: ', status.shape)
                    # st.dataframe(status.head(20))
                                
                    ############################################################################################################
                                        
                    # Ensure that latitude, longitude, and temperature are numeric
                    status['Latitude'] = pd.to_numeric(status['Latitude']) #, errors='coerce')
                    status['Longitude'] = pd.to_numeric(status['Longitude']) #, errors='coerce')
                    status['Temperature'] = pd.to_numeric(status['Temperature']) #, errors='coerce')
                    # st.dataframe(status)
                                    
                    # Initialize the map centered around the mean of the coordinates
                    map_center = [status['Latitude'].mean(), status['Longitude'].mean()]
                    
                    Map = folium.Map(location = map_center, zoom_start = 7)
                    folium.Marker([latitude, longitude], popup="Tanzania", icon=folium.Icon(color="red")).add_to(Map)
                    folium.Marker(map_center, popup = "Region: " + region + ', ' + "Council: " + council, icon = folium.Icon(color="green")).add_to(Map)
                    
                    for idx, row in status.iterrows():
                        folium.Marker([row['Latitude'], 
                                       row['Longitude']], 
                                       popup = "Ward: " + row['Ward']).add_to(Map) # + ', ' + "Temp: " + row['Temperature'] + ' °C'
                                
                    # Prepare the heatmap data
                    heat_data = [[row['Latitude'], row['Longitude'], row['Temperature']] for index, row in status.iterrows()]
                    # st.write(heat_data)

                    # Add the heatmap layer to the map
                    HeatMap(heat_data).add_to(Map)

                    # Display the map in Streamlit
                    # folium_static(Map, width = 1500, height = 750)
                    
                    # st.divider() 
                
                except:
                    
                    st.divider()
                      
                                                            
                URL = "http://api.weatherapi.com/v1/forecast.json?key=6bd51cc56e814b49a4b123504240407&q=" + council + ", "  + region + ", Tanzania&days=7&aqi=yes&alerts=yes"
                
                # HTTP request
                response = requests.get(URL)

                if response.status_code == 200:
                    
                    dt = response.json()
                                            
                    datetime_str = dt['location']['localtime']
                    day = datetime.strptime(datetime_str, "%Y-%m-%d %H:%M").strftime("%A")
                    clock = datetime.strptime(datetime_str, "%Y-%m-%d %H:%M").strftime("%H:%M")
                              
                    d = []
                    day = []          
                    tm = []
                    temp = []
                    prcp = []
                    humid = []
                    wspd = []
                    wdir = []
                    gust = []
                        
                    # Forecasting: Present Day - Next 7 Days - D = 0-7
                    for i in range(len(dt['forecast']['forecastday'])): # len(dt['forecast']['forecastday'])

                        for k in range(len(dt['forecast']['forecastday'][i]['hour'])):
                            
                            tm.append(datetime.strptime(dt['forecast']['forecastday'][i]['hour'][k]['time'], "%Y-%m-%d %H:%M"))
                            
                            d.append(dt['forecast']['forecastday'][i]['date'])
                            day.append(datetime.strptime(dt['forecast']['forecastday'][i]['date'], "%Y-%m-%d").strftime("%A"))
                                            
                            temp.append(dt['forecast']['forecastday'][i]['hour'][k]['temp_c']) # dt['forecast']['forecastday'][i]['hour'][k]['feelslike_c']
                            prcp.append(dt['forecast']['forecastday'][i]['hour'][k]["precip_in"])
                            humid.append(dt['forecast']['forecastday'][i]['hour'][k]["humidity"])
                            wspd.append(dt['forecast']['forecastday'][i]['hour'][k]["wind_kph"])
                            wdir.append(dt['forecast']['forecastday'][i]['hour'][k]["wind_dir"])
                            gust.append(dt['forecast']['forecastday'][i]['hour'][k]["gust_kph"])
    
                    X = pd.DataFrame({'time': tm, 'date': d, 'day': day, 'temp': temp, 'prcp': prcp, 'rhum': humid, 'wspd': wspd, 'wdir': wdir, 'gust': gust})
                    
                    st.write('')
                    
                    col1, col2, col3, col4, col5, col6, col7 = st.columns(7, gap = 'small')
                    with col1:
                        st.info('Monday')
                        if (X['day'] == 'Monday').any():
                            st.metric(label = 'Avg Temp: ', value = str(round(X[X['day'] == 'Monday']['temp'].mean(), 2)) + '°C', delta = str(round(X[X['day'] == 'Mondday']['temp'].max(), 2)) + '°C', delta_color = "inverse")
                        else:
                            st.metric(label = 'Avg Temp: ', value = '--')
                        
                    with col2:
                        st.info('Tuesday')
                        if (X['day'] == 'Tuesday').any():
                            st.metric(label = 'Avg Temp: ', value = str(round(X[X['day'] == 'Tuesday']['temp'].mean(), 2)) + '°C', delta = str(round(X[X['day'] == 'Tuesday']['temp'].max(), 2)) + '°C', delta_color = "inverse")
                        else:
                            st.metric(label = 'Avg Temp: ', value = '--')
                        
                    with col3:
                        st.info('Wednesday')
                        if (X['day'] == 'Wednesday').any():
                            st.metric(label = 'Avg Temp: ', value = str(round(X[X['day'] == 'Wednesday']['temp'].mean(), 2)) + '°C', delta = str(round(X[X['day'] == 'Wednesday']['temp'].max(), 2)) + '°C', delta_color = "inverse")
                        else:
                            st.metric(label = 'Avg Temp: ', value = '--')
                        
                    with col4:
                        st.info('Thursday')
                        if (X['day'] == 'Thursday').any():
                            st.metric(label = 'Avg Temp: ', value = str(round(X[X['day'] == 'Thursday']['temp'].mean(), 2)) + '°C', delta = str(round(X[X['day'] == 'Thursday']['temp'].max(), 2)) + '°C', delta_color = "inverse")
                        else:
                            st.metric(label = 'Avg Temp: ', value = '--')
                        
                    with col5:
                        st.info('Friday')
                        if (X['day'] == 'Friday').any():
                            st.metric(label = 'Avg Temp: ', value = str(round(X[X['day'] == 'Friday']['temp'].mean(), 2)) + '°C', delta = str(round(X[X['day'] == 'Friday']['temp'].max(), 2)) + '°C', delta_color = "inverse")
                        else:
                            st.metric(label = 'Avg Temp: ', value = '--')
                        
                    with col6:
                        st.info('Saturday')
                        if (X['day'] == 'Saturday').any():
                            st.metric(label = 'Avg Temp: ', value = str(round(X[X['day'] == 'Saturday']['temp'].mean(), 2)) + '°C', delta = str(round(X[X['day'] == 'Saturday']['temp'].max(), 2)) + '°C', delta_color = "inverse")
                        else:
                            st.metric(label = 'Avg Temp: ', value = '--')
                        
                    with col7:
                        st.info('Sunday')
                        if (X['day'] == 'Sunday').any():
                            st.metric(label = 'Avg Temp: ', value = str(round(X[X['day'] == 'Sunday']['temp'].mean(), 2)) + '°C', delta = str(round(X[X['day'] == 'Sunday']['temp'].max(), 2)) + '°C', delta_color = "inverse")
                        else:
                            st.metric(label = 'Avg Temp: ', value = '--')
                    
                    st.write('')
                    
                    col1, col2 = st.columns(2, gap = 'medium')
                    
                    # PLOT: Temperature and Precipitation
        
                    with col1:
                        
                        # Create subplots with secondary y-axis
                        fig = make_subplots(specs=[[{"secondary_y": True}]])
                        fig.add_trace(go.Scatter(x = X['time'], y = X['temp'], name = 'Temperature', mode ='lines', line=dict(color = 'firebrick')), secondary_y = False)
                        fig.add_trace(go.Bar(x = X['time'], y = X['prcp'], name = 'Precipitation', marker = dict(color = 'royalblue')), secondary_y = True)

                        # Update layout
                        fig.update_layout(height=700, width=1500, title_text='Understanding Environmental Conditions and plan for Extreme Weather Events', xaxis_title='Date')
                        fig.update_xaxes(rangeslider_visible = True, showline = True, linewidth = 2, linecolor = 'black', mirror = True)
                        fig.update_yaxes(showline = True, title_text='Temperature (°C)', linewidth = 2, linecolor = 'black', secondary_y=False)
                        fig.update_yaxes(title_text='Precipitation (mm)', linewidth = 2, linecolor = 'black', secondary_y=True)
                        st.plotly_chart(fig)
                    
                        st.divider()        
                    
                    # PLOT: Temperature and Humidity
                                
                    with col2: 
                        
                        # Create subplots with secondary y-axis
                        fig = make_subplots(specs=[[{"secondary_y": True}]])
                        fig.add_trace(go.Scatter(x = X['time'], y = X['temp'], name = 'Temperature', mode ='markers+lines', line=dict(color = 'firebrick')), secondary_y = False)
                        fig.add_trace(go.Scatter(x = X['time'], y = X['rhum'], name = 'Humidity (%)', marker = dict(color = 'royalblue')), secondary_y = True)

                        # Update layout
                        fig.update_layout(height=700, width=1500, title_text='Understanding the Heat Index and Comfort Levels', xaxis_title='Date')
                        fig.update_xaxes(rangeslider_visible = True, showline = True, linewidth = 2, linecolor = 'black', mirror = True)
                        fig.update_yaxes(showline = True, title_text='Temperature (°C)', linewidth = 2, linecolor = 'black', secondary_y=False)
                        fig.update_yaxes(title_text='Humidity (%)', linewidth = 2, linecolor = 'black', secondary_y=True)
                        st.plotly_chart(fig)
                    
                        st.divider()
                    
                    col1, col2 = st.columns(2, gap = 'medium')
                    
                    # PLOT: Wind Speed and Wind Direction
                    
                    with col1: 
                                            
                        # Create subplots with secondary y-axis
                        fig = make_subplots(specs=[[{"secondary_y": True}]])
                        fig.add_trace(go.Scatter(x = X['time'], y = X['wspd'], name = 'Wind Speed (km/h)', mode ='lines', line=dict(color = 'firebrick')), secondary_y = False)
                        fig.add_trace(go.Scatter(x = X['time'], y = X['wdir'], name = 'Wind Direction (°)', marker = dict(color = 'royalblue')), secondary_y = True)

                        # Update layout
                        fig.update_layout(height=700, width=1500, title_text='Understanding Weather Patterns and Storm Tracking', xaxis_title='Date')
                        fig.update_xaxes(rangeslider_visible = True, showline = True, linewidth = 2, linecolor = 'black', mirror = True)
                        fig.update_yaxes(showline = True, title_text='Wind Speed (km/h)', linewidth = 2, linecolor = 'black', secondary_y=False)
                        fig.update_yaxes(title_text='Wind Direction (°)', linewidth = 2, linecolor = 'black', secondary_y=True)
                        st.plotly_chart(fig)
                    
                        st.divider()
                    
                    # PLOT: Precipitation and Wind Speed
                    
                    with col2: 
                                            
                        # Create subplots with secondary y-axis
                        fig = make_subplots(specs=[[{"secondary_y": True}]])
                        fig.add_trace(go.Scatter(x = X['time'], y = X['prcp'], name = 'Precipitation', marker = dict(color = 'royalblue')), secondary_y = False)
                        fig.add_trace(go.Scatter(x = X['time'], y = X['wspd'], name = 'Wind Speed (km/h)', mode = 'markers', marker = dict(size = X['wspd'], color = X['wspd'], colorscale = 'Viridis')), secondary_y = True)

                        # Update layout
                        fig.update_layout(height=700, width=1500, title_text='Understanding Overall Atmospheric Conditions', xaxis_title='Date')
                        fig.update_xaxes(rangeslider_visible = True, showline = True, linewidth = 2, linecolor = 'black', mirror = True)
                        fig.update_yaxes(showline = True, title_text='Precipitation (mm)', linewidth = 2, linecolor = 'black', secondary_y=False)
                        fig.update_yaxes(title_text='Wind Speed (km/h)', linewidth = 2, linecolor = 'black', secondary_y=True)
                        st.plotly_chart(fig)
                    
                        st.divider()
                    
                    ### WhatsApp Notification ---------------------------------------------------------------------------------------------
                    
                    update = "About Location\nCouncil:{}\nRegion : {}\nCountry: {}\nDate   : {}\nTime   : {}\n\nAbout Weather\nTemperature: {} °C\nPrecipitation: {} in\nHumidity   : {} %\nWind Speed : {} mph\nPressure   : {} inHg\n\nClouds     : {} \nHeat Index : {} °C\nDew Point  : {} °C\nVisibility : {} miles\nGust      : {} mph".format(
                        dt['location']['name'], 
                        dt['location']['region'], 
                        'Tanzania', 
                        datetime.strptime(datetime_str, "%Y-%m-%d %H:%M").strftime("%Y-%m-%d"),
                        datetime.strptime(datetime_str, "%Y-%m-%d %H:%M").strftime("%H:%M"), #dt['location']['localtime'], 
                        dt['current']['temp_c'], 
                        dt['current']["precip_in"],
                        dt['current']["humidity"],
                        dt['current']["wind_mph"], 
                        dt['current']["pressure_in"], 
                        dt['current']["condition"]['text'], 
                        dt['current']['heatindex_c'], 
                        dt['current']['dewpoint_c'], 
                        dt['current']["vis_miles"], 
                        dt['current']["gust_mph"])
                    
                    st.sidebar.write('')
                    st.sidebar.write('')
                    
                    account_sid = 'AC813a84f348a10a3521b1279686057ac4'
                    auth_token = 'c8d87bf308d7136841ea564489939298'
                    # account_sid = os.environ["ACCOUNT_SID"]
                    # auth_token = os.environ["AUTH_TOKEN"]
                    client = Client(account_sid, auth_token)
                    
                    # Function to inject custom CSS for button styling
                    def button_css():
                        st.markdown("""
                            <style>
                            .stButton button {
                                background-color: #B9060A;
                                color: white;
                                border: none;
                                padding: 5px 24px;
                                text-align: center;
                                display: inline-block;
                                font-size: 16px;
                                cursor: pointer;
                                transition-duration: 0.5s;
                            }

                            .stButton button:active {
                                background-color: green;
                            }
                            </style>
                            """, unsafe_allow_html=True)

                    # Inject CSS for button styling
                    button_css()
                    
                    with st.sidebar.form(key='whatsapp_form'):
                        user_number = st.text_input(':bellhop_bell: Get Notified (Enter Number with Country Code):', placeholder = 'Format Ex: 353XXXXXXXXX')
                        
                        submit_button_1 = st.form_submit_button(label='SMS :speech_balloon:', use_container_width=True)
                        submit_button_2 = st.form_submit_button(label='WhatsApp :speech_balloon:',use_container_width=True)
                    
                    #################################################################
                                               
                    if submit_button_1:
                        
                        st.info('Notifications Activated', icon="ℹ️")
                        
                        if user_number:
                            
                            try:
                                message = client.messages.create(
                                from_= '+12082890855',
                                body = 'Live Weather Status\n\n' + update,
                                to = '+' + str(user_number)
                                )
                                
                                message = client.messages.create(
                                from_= '+12082890855',
                                body = 'Weather Forecasting:\nFor Temperature and Precipitation\n\n',
                                to = '+' + str(user_number)
                                )
                                
                                time.sleep(1)
                                
                                current_time = datetime.strptime(datetime_str, "%Y-%m-%d %H:%M")
                                # Get the next three hours from the current time
                                time_intervals = [current_time + timedelta(hours=i) for i in range(3)]
                                
                                # Iterate through the time intervals and compare with the DataFrame times
                                for i in range(len(X)):
                                    data_time = X['time'][i]
                                    if (current_time.date() == data_time.date() and current_time.time() <= data_time.time() < time_intervals[-1].time()):
                                        # print(data_time.strftime("%H:%M"))
                                        message = client.messages.create(
                                        from_= '+12082890855',
                                        body = "Date: " + str(data_time.date()) + "\nTime: " + str(data_time.time()) + "\nT: " + str(X['temp'][i]) + " °C\nP: " + str(X['prcp'][i]) + " in\n\n",
                                        to = '+' + str(user_number)
                                        )
                                        
                                # st.success('Notifications on the way to your WhatsApp!!')
                                msg = st.toast('Notifications on the Way!!', icon='🎉')
                                time.sleep(1)
                                msg.toast('Notifications on the way!!', icon='🔥')
                                time.sleep(1)
                                msg.toast('Notifications on the Way!!', icon='🚀')
                                
                            except Exception as e:
                                st.error(f'Failed to Send Message: {e}')
                        else:
                            st.error('Please Enter a Valid WhatsApp Number.')
                           
                    
                    #################################################################
                    
                    if submit_button_2:
                        
                        st.info('Notifications Activated', icon="ℹ️")
                        
                        if user_number:
                            
                            try:
                                message = client.messages.create(
                                from_= 'whatsapp:+14155238886',
                                body = 'Live Weather Status\n\n' + update,
                                to = 'whatsapp:+' + str(user_number)
                                )
                                
                                message = client.messages.create(
                                from_= 'whatsapp:+14155238886',
                                body = 'Weather Forecasting:\nFor Temperature and Precipitation\n\n',
                                to = 'whatsapp:+' + str(user_number)
                                )
                                
                                time.sleep(1)
                                
                                current_time = datetime.strptime(datetime_str, "%Y-%m-%d %H:%M")
                                # Get the next three hours from the current time
                                time_intervals = [current_time + timedelta(hours=i) for i in range(3)]
                                
                                # Iterate through the time intervals and compare with the DataFrame times
                                for i in range(len(X)):
                                    data_time = X['time'][i]
                                    if (current_time.date() == data_time.date() and current_time.time() <= data_time.time() < time_intervals[-1].time()):
                                        # print(data_time.strftime("%H:%M"))
                                        message = client.messages.create(
                                        from_= 'whatsapp:+14155238886',
                                        body = "Date: " + str(data_time.date()) + "\nTime: " + str(data_time.time()) + "\nT: " + str(X['temp'][i]) + " °C\nP: " + str(X['prcp'][i]) + " in\n\n",
                                        to = 'whatsapp:+' + str(user_number)
                                        )
                                        
                                # st.success('Notifications on the way to your WhatsApp!!')
                                msg = st.toast('Notifications on the Way!!', icon='🎉')
                                time.sleep(1)
                                msg.toast('Notifications on the way!!', icon='🔥')
                                time.sleep(1)
                                msg.toast('Notifications on the Way!!', icon='🚀')
                                
                            except Exception as e:
                                st.error(f'Failed to Send Message: {e}')
                        else:
                            st.error('Please Enter a Valid WhatsApp Number.')
                            
                            
        # folium.TileLayer(
        #         tiles = 'https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
        #         attr='Tiles &copy; Esri &mdash; Source: Esri, i-cubed, USDA, USGS, AEX, GeoEye, Getmapping, Aerogrid, IGN, IGP, UPR-EGP, and the GIS User Community',
        #         name='Esri Satellite',
        #         overlay=True,
        #         control=True
        #     ).add_to(Map)
                
        folium.Marker([latitude, longitude], popup="Tanzania", icon=folium.Icon(color="red")).add_to(Map)
        
        geojson_data = requests.get("https://raw.githubusercontent.com/python-visualization/folium-example-data/main/world_countries.json").json()
        folium.GeoJson(geojson_data, name='Country Borders', style_function=lambda x: {'color': 'blue', 'weight': 2, 'fillOpacity': 0.1}).add_to(Map)
        folium.LayerControl().add_to(Map)
        MousePosition().add_to(Map)
        Map.add_child(folium.LatLngPopup())
                            
        col1, col2 = st.columns([5, 1], gap = "small")
        with col1:
            if region and council:
                st.subheader("{}, {} HeapMap".format(council, region))
                
            folium_static(Map, width = 1430, height = 750)
        with col2:
            st.info('ALERTS')
            st.write('No Alerts')
                        