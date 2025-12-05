import streamlit as st
import pandas as pd
import numpy as np
from openai import OpenAI
from data.tickets import get_all_tickets
from user_handling.db import connect_database

st.set_page_config(page_title="🎟️📊📈Tickets Analytics📈📊🎟️", page_icon="📊📈", layout="wide")

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




st.header("🎟️📊📈Tickets Analytics📈📊🎟️")



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


col1, col2 = st.columns(2)

with col1:
    pass


with col2:  
    client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

    st.title("🔍 AI Tickets Analyzer")

    # ═══════════════════════════════════════════════# STEP 1: Fetch tickets from Week 8 database# ═══════════════════════════════════════════════
    tickets = get_all_tickets()
    conn = connect_database()

    tickets = tickets.to_dict(orient="records") 
    if tickets:
        # Let user select an incident
        ticket_options = [
            f"{t['ticket_id']}: {t['subject']} ({t['category']}) - {t['priority']}" 
            for t in tickets
        ]
        
        selected_idx = st.selectbox(
            "Select a ticket to analyze:",
            range(len(tickets)),
            format_func=lambda i: ticket_options[i]
        )
        
        ticket = tickets[selected_idx]
        
        # Display dataset details
        st.subheader("📋 Ticket Details")
        st.write(f"**Ticket ID:** {ticket['ticket_id']}")
        st.write(f"**Priority:** {ticket['priority']}")
        st.write(f"**Status:** {ticket['status']}")
        st.write(f"**Category:** {ticket['category']}")
        st.write(f"**Subject:** {ticket['subject']}")
        st.write(f"**Description:** {ticket['description']}")
        st.write(f"**Created Date:** {ticket['created_date']}")
        st.write(f"**Resolved Date:** {ticket.get('resolved_date', 'N/A')}")
        st.write(f"**Assigned To:** {ticket['assigned_to']}")
        
        # ═══════════════════════════════════════════════# STEP 2: Analyze with AI# ═══════════════════════════════════════════════
        if st.button("🤖 Analyze with AI", type="primary"):
            with st.spinner("AI analyzing ticket..."):
                
                # Create analysis prompt
                analysis_prompt = f"""You are an IT support expert. Analyze this IT ticket:

            Ticket ID: {ticket['ticket_id']}
            Priority: {ticket['priority']}
            Status: {ticket['status']}
            Category: {ticket['category']}
            Subject: {ticket['subject']}
            Description: {ticket['description']}
            Created Date: {ticket['created_date']}
            Resolved Date: {ticket.get('resolved_date', 'N/A')}
            Assigned To: {ticket['assigned_to']}

            Provide:
            1. Recommended troubleshooting or resolution steps
            2. Root cause analysis (if possible)
            3. Risk assessment or potential escalation
            4. Suggestions for process improvement or automation
            5. Any other insights relevant for IT operations
            """
                # Call ChatGPT API
                response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[
                        {
                            "role": "system",
                            "content": "You are an IT support and operations expert."
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
            

