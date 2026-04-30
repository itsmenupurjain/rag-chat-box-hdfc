"""
Phase 7: Streamlit UI - Mutual Fund FAQ Assistant
Complete end-to-end RAG chat application
"""

import os
import sys
import streamlit as st
from datetime import datetime

# Add parent directories to path
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
sys.path.insert(0, project_root)
sys.path.insert(0, os.path.join(project_root, 'phase 5', 'src'))
sys.path.insert(0, os.path.join(project_root, 'phase 6', 'src'))

from retrieval_engine import RetrievalEngine
from llm_engine import LLMEngine

# Page configuration
st.set_page_config(
    page_title="HDFC Mutual Fund FAQ Assistant",
    page_icon="💰",
    layout="wide"
)


@st.cache_resource
def load_rag_system():
    """Load RAG system components (cached for performance)"""
    try:
        retrieval = RetrievalEngine()
        llm = LLMEngine()
        return retrieval, llm, True
    except Exception as e:
        return None, None, str(e)


def main():
    """Main Streamlit application"""
    
    # Custom CSS
    st.markdown("""
        <style>
        .main-header {
            background: linear-gradient(90deg, #0052CC 0%, #00B8D9 100%);
            padding: 2rem;
            border-radius: 10px;
            color: white;
            margin-bottom: 2rem;
        }
        .chat-message {
            padding: 1rem;
            border-radius: 10px;
            margin: 0.5rem 0;
        }
        .user-message {
            background-color: #E3F2FD;
            border-left: 4px solid #2196F3;
        }
        .bot-message {
            background-color: #F5F5F5;
            border-left: 4px solid #4CAF50;
        }
        .citation {
            font-size: 0.85rem;
            color: #666;
            margin-top: 0.5rem;
            font-style: italic;
        }
        </style>
    """, unsafe_allow_html=True)
    
    # Header
    st.markdown("""
        <div class="main-header">
            <h1>💰 HDFC Mutual Fund FAQ Assistant</h1>
            <p>Ask questions about HDFC Mutual Funds - Get factual, cited answers</p>
        </div>
    """, unsafe_allow_html=True)
    
    # Load RAG system
    with st.spinner("Loading RAG system..."):
        retrieval, llm, status = load_rag_system()
    
    if not retrieval or not llm:
        st.error(f"❌ Failed to load RAG system: {status}")
        st.info("Please run Phase 2-6 first to build the complete system")
        return
    
    # Sidebar
    with st.sidebar:
        st.header("⚙️ Settings")
        
        # Top K parameter
        top_k = st.slider("Number of sources to search", 1, 10, 5)
        
        # Clear chat
        if st.button("🗑️ Clear Chat"):
            st.session_state.messages = []
            st.rerun()
        
        # System info
        st.markdown("---")
        st.subheader("📊 System Info")
        st.info(f"""
        - Model: Llama 3.3 70B
        - Embeddings: all-MiniLM-L6-v2
        - Vector DB: FAISS
        - Sources: 5 HDFC Funds
        """)
        
        # Example questions
        st.markdown("---")
        st.subheader("💡 Example Questions")
        examples = [
            "What is the minimum SIP amount?",
            "What is the exit load for HDFC Mid-Cap Fund?",
            "Explain the risk factors",
            "What are the 1-year returns?",
            "What is the expense ratio?"
        ]
        
        for example in examples:
            if st.button(example, use_container_width=True):
                st.session_state.messages.append({"role": "user", "content": example})
                st.rerun()
    
    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    # Display chat messages
    for message in st.session_state.messages:
        if message["role"] == "user":
            st.markdown(f"""
                <div class="chat-message user-message">
                    <strong>You:</strong><br>
                    {message["content"]}
                </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
                <div class="chat-message bot-message">
                    <strong>Assistant:</strong><br>
                    {message["content"]}
                </div>
            """, unsafe_allow_html=True)
    
    # Chat input
    if prompt := st.chat_input("Ask about HDFC Mutual Funds..."):
        # Add user message
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # Get response from RAG system
        with st.spinner("Searching and generating response..."):
            response, results = llm.ask(prompt, retrieval, top_k=top_k)
        
        # Add assistant response
        st.session_state.messages.append({"role": "assistant", "content": response})
        
        # Rerun to display
        st.rerun()
    
    # Footer
    st.markdown("---")
    st.markdown("""
        <div style="text-align: center; color: #666; padding: 1rem;">
            <p>⚠️ Disclaimer: This assistant provides factual information only. Not investment advice.</p>
            <p>Data sourced from Groww, SEBI, and HDFC AMC official websites</p>
        </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
