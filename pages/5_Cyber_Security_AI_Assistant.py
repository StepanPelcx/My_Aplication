import streamlit as st
from openai import OpenAI

# Ensure state keys exist (in case user opens this page first)
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = ""

# Guard: if not logged in, send user back
if not st.session_state.logged_in:
    st.error("You must be logged in to use AI assistant.")
    if st.button("Go to login page"):
        st.switch_page("Home.py") # back to the first page
    st.stop()

st.header("Cyber Security AI Assistant")
#st.text("This AI Assistant is not specialyst in any fields. \nIts purpose is mainly for general questions.")

import streamlit as st
from openai import OpenAI

# Initialize OpenAI client
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# Page title
st.title("🛡 Cybersecurity AI Assistant")

# Initialize session state for messages
if 'messages' not in st.session_state:
    st.session_state.messages = [
        {
        "role": "system",
        "content": """You are a cybersecurity expert assistant.
        - Analyze incidents and threats
        - Provide technical guidance
        - Explain attack vectors and mitigations
        - Use standard terminology (MITRE ATT&CK, CVE)
        - Prioritize actionable recommendations
        Tone: Professional, technical
        Format: Clear, structured responses"""
        }
    ]

# Display all previous messages (skip system message)
for message in st.session_state.messages:
    if message["role"] != "system": # Don't display system prompt
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# Get user input
prompt = st.chat_input("Ask about cyber security")
if prompt:
    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)

    # Add user message to session state
    st.session_state.messages.append({
        "role": "user",
        "content": prompt
        })

    # Call OpenAI API
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=st.session_state.messages,
        stream=True
    )

    # Display streaming response
    with st.chat_message("assistant"):
        container = st.empty() # Create empty container
        full_reply = "" # Accumulate response

    # Process each chunk as it arrives
    for chunk in completion:
        delta = chunk.choices[0].delta
        if delta.content: # If chunk has content
            full_reply += delta.content # Add to full response
            container.markdown(full_reply) # Update display

    # Save complete response to session state
    st.session_state.messages.append({
        "role": "assistant",
        "content": full_reply
    })

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