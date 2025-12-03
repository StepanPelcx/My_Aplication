import streamlit as st
import pandas as pd
import numpy as np
from openai import OpenAI
from user_handling.db import connect_database
from data.incidents import get_all_incidents


st.set_page_config(page_title="🛡️📋Cyber Security Dashboard📋🛡️", page_icon="🛡️📋", layout="wide")

# Ensure state keys exist (in case user opens this page first)
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = ""

# Guard: if not logged in, send user back
if not st.session_state.logged_in:
    st.error("You must be logged in to view the dashboard.")
    if st.button("Go to login page"):
        st.switch_page("Home.py") # back to the first page
    st.stop()


st.header("🛡️📋Cyber Security Dashboard📋🛡️")


client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

st.title("🔍 AI Incident Analyzer")

# ═══════════════════════════════════════════════# STEP 1: Fetch incident from Week 8 database# ═══════════════════════════════════════════════
incidents = get_all_incidents()
conn = connect_database()

if not incidents.empty:
    # Let user select an incident
    incident_options = [
        f"{inc['id']}: {inc['incident_type']} - {inc['severity']}"for inc in incidents
    ]
    
    selected_idx = st.selectbox(
        "Select incident to analyze:",
        range(len(incidents)),
        format_func=lambda i: incident_options[i]
    )
    
    incident = incidents[selected_idx]
    
    # Display incident details
    st.subheader("📋 Incident Details")
    st.write(f"**Type:** {incident['incident_type']}")
    st.write(f"**Severity:** {incident['severity']}")
    st.write(f"**Description:** {incident['description']}")
    st.write(f"**Status:** {incident['status']}")
    
    # ═══════════════════════════════════════════════# STEP 2: Analyze with AI# ═══════════════════════════════════════════════
    if st.button("🤖 Analyze with AI", type="primary"):
        with st.spinner("AI analyzing incident..."):
            
            # Create analysis prompt
            analysis_prompt = f"""Analyze this cybersecurity incident:

    Type: {incident['incident_type']}
    Severity: {incident['severity']}
    Description: {incident['description']}
    Status: {incident['status']}

    Provide:
    1. Root cause analysis
    2. Immediate actions needed
    3. Long-term prevention measures
    4. Risk assessment"""# Call ChatGPT API
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {
                        "role": "system",
                        "content": "You are a cybersecurity expert."
                    },
                    {
                        "role": "user",
                        "content": analysis_prompt
                    }
                ]
            )
            
            # Display AI analysis
            st.subheader("🧠 AI Analysis")
            st.write(response.choices[0].message.content)
            
            # Optional: Save analysis back to database# update_incident_analysis(conn, incident['id'], analysis)



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