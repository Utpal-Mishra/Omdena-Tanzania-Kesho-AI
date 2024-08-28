import home
import weather
import historical
import pandas as pd
import streamlit as st

st.set_page_config(page_title="KeshoAI", layout="wide")

PAGES = {
    "About": home,
    "Weather Analysis": weather,
    "Historical View": historical
}

st.sidebar.image("Omdena.png")

st.write('')
st.write('')

st.sidebar.title('Navigation Bar')

selection = st.sidebar.selectbox("Pages: \n", list(PAGES.keys()))
page = PAGES[selection]

# data = pd.read_csv('locations.csv')
# data.drop(data.columns[[0]], axis=1, inplace=True)
# data['Region'] = data['Region'].apply(lambda x: x.title())
        
# data = data.groupby(['Region', 'Council', 'Ward']).mean().reset_index()
# data['Population'] = data['Population'].astype(int)

# st.sidebar.map(data.rename(columns = {'Latitude': 'latitude', 'Longitude': 'longitude'}), zoom = 3, size = 50)

page.app()