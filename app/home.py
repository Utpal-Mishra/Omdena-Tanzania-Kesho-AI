# RESOURCES
# Timeline: https://github.com/giswqs/streamlit-timeline
# LIBRARIES

import streamlit as st
import streamlit.components.v1 as components
import os

   
def app():
        
    st.write("")
    col1, col2, col3 = st.columns(3, gap = "small")#, vertical_alignment = "center")

    with col1:

        path = os.path.dirname(__file__)
        st.image(path+'/Omdena.png')

    with col2:
        path = os.path.dirname(__file__)
        st.image(path+'/Kesho.png')        

    with col3:
        path = os.path.dirname(__file__)
        st.image(path+'/Tanzania.png', width = 200)

    # st.title("Omdena - KeshoAI")
    st.header("Omdena Partners with EIT Climate-KIC and Sahara Ventures to Host The First Grassroots AI Climathon Event in Tanzania")
     
    ###########################################################################################################
    
    st.subheader("SUMMARY:\nWe are planning to build a 24-hour AI-powered precision early warning system designed to predict and provide timely alerts for extreme weather conditions in Tanzania. This system will utilize data from the Tanzania Meteorological Authority (TMA) and historical data to predict floods, heavy rains, and heat waves, delivering tailored and precise alerts to individuals via SMS, enhancing preparedness and response to weather-related disasters.\n\n")
    st.subheader("PROBLEM: \n**Why are we doing this?**\nUnpredictable weather conditions caused by climate change are leading to severe adverse effects such as floods, heat waves, and other extreme weather events in Tanzania. These conditions result in significant property damage, displacements, and fatalities. Currently, there is a lack of tailored preparedness measures, specific location pinpointing, and timely alerts, leading to inadequate disaster response and low accessibility of vital information.\n\n")
    st.subheader("GOAL: \n**SMART: Specific, Measurable, Attainable, Relevant, and Time-bound**\n\n**Specific:**\nDevelop a robust AI-powered early warning system to predict extreme weather conditions, specifically floods, heavy rains, and heat waves, in Tanzania. This system will leverage data from the Tanzania Meteorological Authority (TMA) and historical weather data to provide accurate and timely alerts eventually via SMS to residents, enhancing their preparedness and response to weather-related disasters.\n\n**Measureable**\ni. Achieve a prediction accuracy of at least 80% for floods, heavy rains, and heat waves within the first 8 weeks of model development\nii. Develop and deploy a user-friendly dashboard that visualizes weather predictions and system performance (a dashboard example for inspiration can be found here).\n\n**Achievable**\nUtilize existing machine learning frameworks and pre-trained models for weather prediction. Collaborate with TMA for access to historical weather data and leverage the expertise of Omdena's global network of AI specialists and data scientists to ensure the project's success.\n\n**Relevant**\nThis project addresses the critical need for timely and accurate weather information in Tanzania, which is prone to extreme weather events due to climate change. By providing early warnings, the system will help save lives, reduce property damage, and improve disaster responsiveness, aligning with the goals of local government authorities and NGOs working on climate resilience.\n\n**Time-Bound**\nComplete the development and initial deployment of the Kesho AI system within 8 +2 weeks\n\n")
        
    # # parameters
    # CDN_LOCAL = False
    # CDN_PATH = 'https://cdn.knightlab.com/libs/timeline3/latest'
    # CSS_PATH = 'timeline3/css/timeline.css'
    # JS_PATH = 'timeline3/js/timeline.js'

    # SOURCE_TYPE = 'json' # json or gdocs
    # GDOCS_PATH = 'https://docs.google.com/spreadsheets/u/1/d/1xuY4upIooEeszZ_lCmeNx24eSFWe0rHe9ZdqH2xqVNk/pubhtml' # example url
    # JSON_PATH = os.path.join(os.getcwd(), 'timeline_nlp.json') # example json
        
    # TL_HEIGHT = 500 # px


    # # load data
    # json_text = ''
    # if True: #SOURCE_TYPE == 'json':
    #     with open(JSON_PATH, "r") as f:
    #         json_text = f.read()
    #         print(json_text)
    #         source_param = 'timeline_json'
    #         source_block = f'var {source_param} = {json_text};'
    # elif SOURCE_TYPE == 'gdocs':
    #     source_param = f'"{GDOCS_PATH}"'
    #     source_block = ''


    # # load css + js
    # if CDN_LOCAL:
    #     with open(CSS_PATH, "r") as f:
    #         css_text = f.read()
    #         css_block = f'<head><style>{css_text}</style></head>'

    #     with open(JS_PATH, "r") as f:
    #         js_text = f.read()
    #         js_block  = f'<script type="text/javascript">{js_text}</script>'
    # else:
    #     css_block = f'<link title="timeline-styles" rel="stylesheet" href="{CDN_PATH}/css/timeline.css">'
    #     js_block  = f'<script src="{CDN_PATH}/js/timeline.js"></script>'


    # # write html block
    # htmlcode = css_block + ''' 
    # ''' + js_block + '''

    #     <div id='timeline-embed' style="width: 100%; height: ''' + str(TL_HEIGHT) +'''px; margin: 1px;"></div>

    #     <script type="text/javascript">
    #         var additionalOptions = {
    #             start_at_end: false, is_embed:true,
    #         }
    #         '''+source_block+'''
    #         timeline = new TL.Timeline('timeline-embed', '''+source_param+''', additionalOptions);
    #     </script>'''


    # # UI sections
    # components.html(htmlcode, height=TL_HEIGHT,)

    # st.divider() 
    