import streamlit as st 
from streamlit_option_menu import option_menu

from PIL import Image
img=Image.open('logo-GlobalEHR.png')

from REDGDPS.main_redgdps import main_redgdps_function
from SEARCH_ENGINE.main_search_engine import main_search_engine_function
from HOME_PAGE.main_dashborad import main_dashboard_function

st.set_page_config(page_title = "Doctor Portal", page_icon = img, layout = "wide")

col1, col2, col3 = st.columns([1,3,1])
with col2:
    selected=option_menu(
        menu_title=None,
        options=["HOME", "Clinical Registers", "SEARCH ENGINE"],
        icons=["house", "capsule-pill", "search"],
        menu_icon="cast",
        default_index=0,
        orientation="horizontal",
        
        styles={
                    "container": {"margin": "0px !important","padding": "0!important", "align-items": "stretch", "background-color": "#fafafa"},
                    "icon": {"color": "orange", "font-size": "25px"},
                    "nav-link": {
                        "font-size": "18px",
                        "text-align": "center",
                        "margin": "0px",
                        "--hover-color": "#eee",
                    },
                    "nav-link-selected": {"background-color": "green"},
                },
    )

if selected=="HOME":
    main_dashboard_function()

if selected=="Clinical Registers":
    main_redgdps_function()

if selected=="SEARCH ENGINE":
    main_search_engine_function()