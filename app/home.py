# LIBRARIES

import streamlit as st
import pandas as pd

# !conda install -c conda-forge geopy --yes
from geopy.geocoders import Nominatim

import folium
from streamlit_folium import folium_static

print('\nLibraries Imported\n')

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
                     
        def folium_map():
            
            address = 'Tanzania'
            geolocator = Nominatim(user_agent="four_square")
            location = geolocator.geocode(address)
            latitude = location.latitude
            longitude = location.longitude

            # Create a folium map
            Map = folium.Map(location=[latitude, longitude], zoom_start = 5)
            folium.Marker([latitude, longitude], popup="Tanzania", icon=folium.Icon(color="red")).add_to(Map)
        
            # Optionally add other markers or layers
            Marker = folium.map.FeatureGroup()
            # MousePosition().add_to(Map)
            Map.add_child(folium.LatLngPopup())
            
            return Map
        
        Map = folium_map()
            
        for idx, row in data.iterrows():
            folium.Marker([row['Latitude'], 
                           row['Longitude']], 
                           popup = "Region: " + row['Region'] + ", Council: " + row['Council']  + ", Ward: " + row['Ward']).add_to(Map)
                    
        folium_static(Map)
            
        st.divider()
        
        ############################################################################################################
        
                