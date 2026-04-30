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

# --- ULTRA-GLOSSY LINE-ART CSS ---
st.markdown("""
    <style>
    /* Hide Sidebar & Header */
    [data-testid="stSidebar"] {display: none;}
    header {visibility: hidden;}
    footer {visibility: hidden;}

    /* Background Mesh - Darker for contrast */
    .stApp {
        background: radial-gradient(circle at 10% 10%, #001a33 0%, transparent 40%),
                    radial-gradient(circle at 90% 90%, #000d1a 0%, transparent 40%),
                    #020408;
        color: #ffffff !important;
        font-family: 'Inter', sans-serif;
    }

    /* LEGIBILITY FIX: All text forced to White with Shadows */
    h1, h2, h3, h4, h5, h6, p, li, span, div, label, .stMarkdown {
        color: #ffffff !important;
        text-shadow: 0 2px 8px rgba(0,0,0,0.9), 0 1px 2px rgba(0,0,0,0.5) !important;
    }

    /* Glossy Card Styling with Specular Highlight */
    .glossy-card {
        background: rgba(255, 255, 255, 0.03);
        backdrop-filter: blur(30px) saturate(200%);
        border: 1px solid rgba(255, 255, 255, 0.25);
        border-radius: 24px;
        padding: 25px;
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.6),
                    inset 0 0 20px rgba(255, 255, 255, 0.05);
        transition: all 0.5s cubic-bezier(0.23, 1, 0.32, 1);
        position: relative;
        overflow: hidden;
    }
    .glossy-card::before {
        content: "";
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: linear-gradient(
            45deg,
            transparent,
            rgba(255, 255, 255, 0.1),
            transparent
        );
        transform: rotate(45deg);
        transition: 0.5s;
    }
    .glossy-card:hover {
        transform: translateY(-8px) scale(1.02);
        border: 1px solid rgba(255, 255, 255, 0.5);
        background: rgba(255, 255, 255, 0.08);
        box-shadow: 0 30px 60px rgba(0, 0, 0, 0.8);
    }
    .glossy-card:hover::before {
        left: 100%;
    }

    /* Line Art Icon Container */
    .line-icon {
        width: 48px;
        height: 48px;
        stroke: #ffffff;
        stroke-width: 1.5;
        fill: none;
        margin-bottom: 15px;
        filter: drop-shadow(0 0 8px rgba(255,255,255,0.4));
    }

    /* Floating Chat Bubbles */
    .stChatMessage {
        background: rgba(255, 255, 255, 0.04) !important;
        backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 255, 255, 0.15) !important;
        border-radius: 20px !important;
        margin-bottom: 20px !important;
        padding: 15px !important;
    }

    /* Custom Chat Input */
    [data-testid="stBottom"], [data-testid="stChatInput"], .stChatInput {
        background: transparent !important;
    }
    div[data-testid="stBottomBlockContainer"] {
        background: transparent !important;
    }
    .stChatInputContainer {
        border-radius: 50px !important;
        background: rgba(255, 255, 255, 0.05) !important;
        backdrop-filter: blur(40px);
        border: 1px solid rgba(255, 255, 255, 0.15) !important;
    }
    .stChatInput textarea {
        color: #ffffff !important;
        caret-color: #ffffff !important;
    }
    .stChatInput textarea::placeholder {
        color: rgba(255, 255, 255, 0.4) !important;
    }

    /* Centered Content Wrapper */
    .centered-container {
        max-width: 950px;
        margin: auto;
        padding: 40px 20px;
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
st.markdown("<h1 style='text-align: center; font-size: 3rem; font-weight: 800; letter-spacing: -1px;'>🏦 HDFC AI</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-size: 1.1rem; opacity: 0.8; margin-bottom: 50px;'>Ultra-Premium Factual Mutual Fund Intel.</p>", unsafe_allow_html=True)

# Session State for single chat
if "messages" not in st.session_state:
    st.session_state.messages = []

# Persistent Triggers Section (Line Art Icons)
cols = st.columns(3)

triggers = [
    {
        "svg": '<svg class="line-icon" viewBox="0 0 24 24"><path d="M22 7L13.5 15.5L8.5 10.5L2 17"></path><path d="M16 7H22V13"></path></svg>',
        "label": "LATEST NAV", 
        "query": "What is the latest NAV of HDFC Mid Cap Fund?"
    },
    {
        "svg": '<svg class="line-icon" viewBox="0 0 24 24"><rect x="2" y="4" width="20" height="16" rx="2"></rect><path d="M7 15h0M2 9.5h20"></path></svg>',
        "label": "EXIT LOADS", 
        "query": "Exit load for HDFC ELSS Fund?"
    },
    {
        "svg": '<svg class="line-icon" viewBox="0 0 24 24"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path><circle cx="12" cy="7" r="4"></circle></svg>',
        "label": "FUND MANAGERS", 
        "query": "Who is the manager of HDFC Focused Fund?"
    }
]

for i, t in enumerate(triggers):
    with cols[i]:
        st.markdown(f"""
        <div class="glossy-card" style="height: 180px; display: flex; flex-direction: column; justify-content: center; align-items: center;">
            {t['svg']}
            <p style="font-weight: bold; margin: 0; font-size: 0.95rem; letter-spacing: 1px;">{t['label']}</p>
            <p style="font-size: 0.75rem; opacity: 0.6; text-align: center; margin-top: 8px;">{t['query']}</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Query Fact", key=f"btn_{i}", use_container_width=True):
            st.session_state.messages.append({"role": "user", "content": t['query']})
            with st.spinner("Accessing Vault..."):
                res = assistant.ask(t['query'])
                st.session_state.messages.append({"role": "assistant", "content": res})
            st.rerun()

st.markdown("<br><hr style='border: 0; border-top: 1px solid rgba(255,255,255,0.1); margin: 40px 0;'><br>", unsafe_allow_html=True)

# Display Chat History
for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        st.markdown(m["content"])

# Chat Input
if prompt := st.chat_input("Ask about any HDFC scheme..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"): st.markdown(prompt)
    with st.chat_message("assistant"):
        with st.spinner("Retrieving facts..."):
            res = assistant.ask(prompt)
            st.markdown(res)
            st.session_state.messages.append({"role": "assistant", "content": res})

st.markdown("</div>", unsafe_allow_html=True)

# Footer Disclaimer
st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown(
    "<div style='text-align: center; opacity: 0.4; font-size: 0.75rem; color: #ffffff !important; letter-spacing: 2px;'>"
    "SECURE • FACTUAL • NON-ADVISORY"
    "</div>", 
    unsafe_allow_html=True
)
