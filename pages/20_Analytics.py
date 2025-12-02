import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="Analytics", page_icon="📊📈🔎", layout="wide")

# Ensure state keys exist (in case user opens this page first)
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = ""

# Guard: if not logged in, send user back
if not st.session_state.logged_in:
    st.error("You must be logged in to access the analytics.")
    if st.button("Go to login page"):
        st.switch_page("Home.py") # back to the first page
    st.stop()

# If logged in, show dashboard content
st.title("📊📈🔎 Analytics")

# Sidebar logout button
with st.sidebar:
    if st.button("Log out   ➜]"):
        st.session_state.logged_in = False
        st.session_state.username = ""
        st.info("You have been logged out.")
        st.switch_page("Home.py")

    if not st.session_state.logged_in:
        st.error("You must be logged in...")
        st.switch_page("Home.py")
        st.stop()