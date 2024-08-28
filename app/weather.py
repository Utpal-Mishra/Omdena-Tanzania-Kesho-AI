# LIBRARIES

import streamlit as st

import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import tkinter
import matplotlib
matplotlib.use('TkAgg')

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
        
            
        data = pd.read_csv('locations.csv')
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
        Map = folium.Map(location=[latitude, longitude], zoom_start = 5)
        folium.Marker([latitude, longitude], popup="Tanzania", icon=folium.Icon(color="red")).add_to(Map)
        geojson_data = requests.get("https://raw.githubusercontent.com/python-visualization/folium-example-data/main/world_countries.json").json()
        folium.GeoJson(geojson_data).add_to(Map)
        folium.LayerControl().add_to(Map)
        MousePosition().add_to(Map)
        Map.add_child(folium.LatLngPopup())
                 
        # for idx, row in data.iterrows():
        #     folium.Marker([row['Latitude'], 
        #                    row['Longitude']], 
        #                    popup = "Region: " + row['Region'] + ", Council: " + row['Council']  + ", Ward: " + row['Ward']).add_to(Map)
                    
                    # Add LocateControl to the map
        # LocateControl(auto_start=True).add_to(Map)
        folium_static(Map, width = 1700, height = 750)

        # JavaScript to extract and print user's coordinates
        user_coordinates = """
            <script>
                document.addEventListener('DOMContentLoaded', function() {
                    let locateButton = document.querySelector('.leaflet-control-locate a');
                    locateButton.click();
                    navigator.geolocation.getCurrentPosition(function(position) {
                        console.log('User coordinates:', position.coords.latitude, position.coords.longitude);
                    });
                });
            </script>
        """

        # Display the JavaScript in Streamlit
        st.markdown(user_coordinates, unsafe_allow_html=True)
        # folium_static(Map)
            
        # st.divider()
        
        ###########################################################################################################
            
        
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
                    
                    Map = folium.Map(location = map_center, zoom_start = 5)
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
                    # folium_static(Map)
                    
                    st.divider() 
                    
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
                                        
                    tm = []
                    temp = []
                    prcp = []
                        
                    # Forecasting: Present Day - Next 7 Days - D = 0-7
                    for i in range(len(dt['forecast']['forecastday'])): # len(dt['forecast']['forecastday'])

                        for k in range(len(dt['forecast']['forecastday'][i]['hour'])):
                            
                            tm.append(datetime.strptime(dt['forecast']['forecastday'][i]['hour'][k]['time'], "%Y-%m-%d %H:%M"))
                            temp.append(dt['forecast']['forecastday'][i]['hour'][k]['temp_c']) # dt['forecast']['forecastday'][i]['hour'][k]['feelslike_c']
                            prcp.append(dt['forecast']['forecastday'][i]['hour'][k]["precip_in"])
    
                    X = pd.DataFrame({'time': tm, 'temp': temp, 'prcp': prcp})
                        
                    st.write('')
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
                    
                    account_sid = 'AC92ca5d0fb663ff16fc4374cea4f15e98'
                    auth_token = 'afc810efb352d0fa1960837b14d09ec0'
                    # account_sid = os.environ["ACCOUNT_SID"]
                    # auth_token = os.environ["AUTH_TOKEN"]
                    client = Client(account_sid, auth_token)
                    
                    with st.sidebar.form(key='whatsapp_form'):
                        user_number = st.text_input(':bellhop_bell: Receive WhatsApp Notifications (Enter Number with Country Code):', placeholder = 'Format: 353XXXXXXXXX')
                        submit_button = st.form_submit_button(label='Get Notified')

                    if submit_button:
                        
                        st.sidebar.info('Notifications Activated for Next 3 Hours', icon="ℹ️")
                        
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
                            
                    # # Main app logic
                    # if "whatsapp_number" not in st.session_state:
                    #     whatsapp_logo_url = "WhatsAppIcon.png"

                    #     # Layout with columns to align icon and button
                    #     col1, col2, col3 = st.columns([2.5, 0.17, 1])
                    #     with col2:
                    #         st.image(whatsapp_logo_url, width = 30)  # Display the WhatsApp icon
                    #     with col3:
                    #         if st.button("Notify Me on WhatsApp"):
                    #             get_whatsapp_number()
                    # else:
                    #     st.write(f"You will be notified on WhatsApp at {st.session_state.whatsapp_number}")
