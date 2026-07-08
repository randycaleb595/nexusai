import streamlit as st

import streamlit as st

# Force a clean black background page configuration
st.set_page_config(
    page_title="NEXUS AI", 
    layout="centered", 
    initial_sidebar_state="collapsed"
)

# Custom CSS styling to make the background strictly black and fonts completely sans-serif
st.markdown(
    """
    <style>
    /* Force main app background to black */
    .stApp {
        background-color: #000000;
    }
    
    /* Center text block and use clean sans-serif fonts */
    .brand-container {
        text-align: center;
        margin-top: 120px;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    }
    
    /* Huge Green Nexus AI Title in Sans-Serif */
    .main-title {
        color: #00FF66;
        font-size: 72px;
        font-weight: 800; /* Bold and clean sans-serif */
        letter-spacing: -1px; /* Modern tight spacing style */
        margin-bottom: 5px;
        padding-bottom: 0px;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    }
    
    /* Green Sans-Serif Subtitle */
    .sub-title {
        color: #00FF66;
        font-size: 22px;
        font-weight: 400;
        margin-top: 0px;
        padding-top: 0px;
        opacity: 0.85;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    }
    </style>
    """,
    unsafe_allow_url=True
)

# Render your layout components onto the black background
st.markdown(
    """
    <div class="brand-container">
        <h1 class="main-title">NEXUS AI</h1>
        <p class="sub-title">math made easier</p>
    </div>
    """, 
    unsafe_allow_url=True
)
