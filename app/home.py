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

# !conda install -c conda-forge geopy --yes
from geopy.geocoders import Nominatim

import folium
from folium.plugins import HeatMap
from streamlit_folium import folium_static


print('Libraries Imported\n')

###########################################
   
def app():
        
    st.write("")
    col1, col2 = st.columns(2)

    with col1:
        st.image("Omdena.png")

    with col2:
        st.image('Tanzania.png', width = 130)

    st.title("Omdena - KeshoAI")
    st.header("Omdena Partners with EIT Climate-KIC and Sahara Ventures to Host The First Grassroots AI Climathon Event in Tanzania")
    
    tab1, tab2 = st.tabs(["About :information_source:", "Weather Analysis :cloud:"])
 
    ###########################################################################################################
    
    with tab1: 
        st.subheader("SUMMARY:\nWe are planning to build a 24-hour AI-powered precision early warning system designed to predict and provide timely alerts for extreme weather conditions in Tanzania. This system will utilize data from the Tanzania Meteorological Authority (TMA) and historical data to predict floods, heavy rains, and heat waves, delivering tailored and precise alerts to individuals via SMS, enhancing preparedness and response to weather-related disasters.\n\n")
        st.subheader("PROBLEM: \n**Why are we doing this?**\nUnpredictable weather conditions caused by climate change are leading to severe adverse effects such as floods, heat waves, and other extreme weather events in Tanzania. These conditions result in significant property damage, displacements, and fatalities. Currently, there is a lack of tailored preparedness measures, specific location pinpointing, and timely alerts, leading to inadequate disaster response and low accessibility of vital information.\n\n")
        st.subheader("GOAL: \n**SMART: Specific, Measurable, Attainable, Relevant, and Time-bound**\n\n**Specific:**\nDevelop a robust AI-powered early warning system to predict extreme weather conditions, specifically floods, heavy rains, and heat waves, in Tanzania. This system will leverage data from the Tanzania Meteorological Authority (TMA) and historical weather data to provide accurate and timely alerts eventually via SMS to residents, enhancing their preparedness and response to weather-related disasters.\n\n**Measureable**\ni. Achieve a prediction accuracy of at least 80% for floods, heavy rains, and heat waves within the first 8 weeks of model development\nii. Develop and deploy a user-friendly dashboard that visualizes weather predictions and system performance (a dashboard example for inspiration can be found here).\n\n**Achievable**\nUtilize existing machine learning frameworks and pre-trained models for weather prediction. Collaborate with TMA for access to historical weather data and leverage the expertise of Omdena's global network of AI specialists and data scientists to ensure the project's success.\n\n**Relevant**\nThis project addresses the critical need for timely and accurate weather information in Tanzania, which is prone to extreme weather events due to climate change. By providing early warnings, the system will help save lives, reduce property damage, and improve disaster responsiveness, aligning with the goals of local government authorities and NGOs working on climate resilience.\n\n**Time-Bound**\nComplete the development and initial deployment of the Kesho AI system within 8 +2 weeks\n\n")
        
        st.divider() 
        
        data = pd.read_csv('locations.csv')
        data.drop(data.columns[[0]], axis=1, inplace=True)
        data['Region'] = data['Region'].apply(lambda x: x.title())
        
        data = data.groupby(['Region', 'Council', 'Ward']).mean().reset_index()
        data['Population'] = data['Population'].astype(int)
        # st.dataframe(data)
        
    with tab2:
        
        ############################################################################################################
            
        address = 'Tanzania'
        geolocator = Nominatim(user_agent="four_square")
        location = geolocator.geocode(address)
        latitude = location.latitude
        longitude = location.longitude

        # # Create a folium map
        # Map = folium.Map(location=[latitude, longitude], zoom_start = 5)
        # folium.Marker([latitude, longitude], popup="Tanzania", icon=folium.Icon(color="red")).add_to(Map)
        
        # # Optionally add other markers or layers
        # Marker = folium.map.FeatureGroup()
        # # MousePosition().add_to(Map)
        # Map.add_child(folium.LatLngPopup())
                 
        # # for idx, row in data.iterrows():
        # #     folium.Marker([row['Latitude'], 
        # #                    row['Longitude']], 
        # #                    popup = "Region: " + row['Region'] + ", Council: " + row['Council']  + ", Ward: " + row['Ward']).add_to(Map)
                    
        # folium_static(Map)
            
        # st.divider()
        
        ###########################################################################################################
        
        # st.sidebar.image("Omdena.png")    
        
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
                    folium_static(Map)
                    
                    st.divider() 
                    
                except:
                        
                    st.divider() 
                
                        
        # ############################################################################################################
        