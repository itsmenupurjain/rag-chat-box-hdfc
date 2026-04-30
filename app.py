import streamlit as st
import os
import time
from datetime import datetime
from src.rag_assistant import MutualFundAssistant
from src.logger import setup_logger

logger = setup_logger("streamlit_app", "app.log")

# Page Configuration
st.set_page_config(
    page_title="HDFC AI • Factual Assistant",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- ULTRA-GLOSSY FLOATING CSS ---
st.markdown("""
    <style>
    /* Hide Sidebar & Header */
    [data-testid="stSidebar"] {display: none;}
    header {visibility: hidden;}
    footer {visibility: hidden;}

    /* Background Mesh */
    .stApp {
        background: radial-gradient(circle at 20% 30%, #002b5e 0%, transparent 40%),
                    radial-gradient(circle at 80% 70%, #001a33 0%, transparent 40%),
                    #05080f;
        color: #ffffff !important;
        font-family: 'Inter', sans-serif;
    }

    /* Global Text Color Fix */
    h1, h2, h3, h4, h5, h6, p, li, span, div {
        color: white !important;
        text-shadow: 0 2px 4px rgba(0,0,0,0.5);
    }

    /* Glossy Card Styling */
    .glossy-card {
        background: rgba(255, 255, 255, 0.07);
        backdrop-filter: blur(25px) saturate(180%);
        border: 1px solid rgba(255, 255, 255, 0.2);
        border-radius: 20px;
        padding: 20px;
        box-shadow: 0 15px 35px rgba(0, 0, 0, 0.4),
                    inset 0 0 0 1px rgba(255, 255, 255, 0.1);
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
    }
    .glossy-card:hover {
        transform: translateY(-5px);
        background: rgba(255, 255, 255, 0.12);
        border: 1px solid rgba(255, 255, 255, 0.4);
    }

    /* Floating Chat Bubbles */
    .stChatMessage {
        background: rgba(255, 255, 255, 0.05) !important;
        backdrop-filter: blur(15px);
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 20px !important;
        box-shadow: 0 8px 16px rgba(0,0,0,0.2) !important;
        margin-bottom: 15px !important;
    }

    /* Custom Chat Input */
    .stChatInputContainer {
        border-radius: 50px !important;
        background: rgba(255, 255, 255, 0.05) !important;
        backdrop-filter: blur(30px);
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
        padding: 5px !important;
    }

    /* Centered Content Wrapper */
    .centered-container {
        max-width: 900px;
        margin: auto;
    }
    </style>
    """, unsafe_allow_html=True)

# Initialize Assistant
@st.cache_resource
def get_assistant():
    return MutualFundAssistant()

assistant = get_assistant()

# --- Main UI ---
st.markdown("<div class='centered-container'>", unsafe_allow_html=True)
st.title("🏦 HDFC AI Assistant")
st.markdown("<p style='font-size: 1rem; opacity: 0.7;'>Objective facts and figures for HDFC Mutual Funds.</p>", unsafe_allow_html=True)

# Session State for single chat
if "messages" not in st.session_state:
    st.session_state.messages = []

# Persistent Triggers Section
st.markdown("<br>", unsafe_allow_html=True)
cols = st.columns(3)

triggers = [
    {"icon": "📈", "label": "LATEST NAV", "query": "What is the latest NAV of HDFC Mid Cap Fund?"},
    {"icon": "💸", "label": "EXIT LOADS", "query": "Exit load for HDFC ELSS Fund?"},
    {"icon": "👤", "label": "FUND MANAGERS", "query": "Who is the manager of HDFC Focused Fund?"}
]

for i, t in enumerate(triggers):
    with cols[i]:
        st.markdown(f"""
        <div class="glossy-card" style="height: 140px; display: flex; flex-direction: column; justify-content: center; align-items: center; margin-bottom: 10px;">
            <span style="font-size: 2rem;">{t['icon']}</span>
            <p style="font-weight: bold; margin-top: 5px; font-size: 0.9rem;">{t['label']}</p>
            <p style="font-size: 0.7rem; opacity: 0.6; text-align: center;">{t['query']}</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Ask Fact", key=f"btn_{i}", use_container_width=True):
            st.session_state.messages.append({"role": "user", "content": t['query']})
            # Trigger response generation logic below
            with st.spinner("Fetching..."):
                res = assistant.ask(t['query'])
                st.session_state.messages.append({"role": "assistant", "content": res})
            st.rerun()

st.markdown("<br>", unsafe_allow_html=True)

# Display Chat History
for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        st.markdown(m["content"])

# Chat Input
if prompt := st.chat_input("Enter your query..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"): st.markdown(prompt)
    with st.chat_message("assistant"):
        with st.spinner("Processing..."):
            res = assistant.ask(prompt)
            st.markdown(res)
            st.session_state.messages.append({"role": "assistant", "content": res})

st.markdown("</div>", unsafe_allow_html=True)

# Footer Disclaimer
st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown(
    "<div style='text-align: center; opacity: 0.3; font-size: 0.7rem; color: white !important;'>"
    "FACTS-ONLY • NO INVESTMENT ADVICE"
    "</div>", 
    unsafe_allow_html=True
)
