
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'  # Suppress TF logging
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'  # Disable oneDNN custom operations
import streamlit as st
from modules.themes import apply_default_theme

def main():
    # Page configuration with enhanced settings
    st.set_page_config(
        page_title="Vibefy 2.0 - Emotional Wellness Companion",
        page_icon="🎵",
        layout="wide",
        initial_sidebar_state="collapsed",
        menu_items={
            'Get Help': None,
            'Report a bug': None,
            'About': None
        }
    )
    
    # Initialize session state variables
    if "mood" not in st.session_state:
        st.session_state.mood = None
    if "confidence" not in st.session_state:
        st.session_state.confidence = None
    if "user_input" not in st.session_state:
        st.session_state.user_input = ""
    if "thread_id" not in st.session_state:
        st.session_state.thread_id = None
    
    # Apply default theme
    apply_default_theme()
    
    # Main landing page content
    st.markdown("""
        <div style='text-align: center; padding: 2rem 0;'>
            <h1 style='font-size: 3.5rem; margin-bottom: 1rem; color: white; text-shadow: 2px 2px 4px rgba(0,0,0,0.3);'>
                🎵 Welcome to Vibefy 2.0
            </h1>
            <h3 style='color: #FF6B9D; margin-bottom: 2rem; text-shadow: 1px 1px 2px rgba(0,0,0,0.2);'>
                Your AI-Powered Emotional Companion
            </h3>
        </div>
    """, unsafe_allow_html=True)
    
    # How it Works
    st.markdown("""
        <div style='background: rgba(255, 255, 255, 0.1); backdrop-filter: blur(10px); border-radius: 20px; padding: 2rem; margin: 2rem 0; border: 2px solid rgba(255, 255, 255, 0.2);'>
            <h2 style='text-align: center; color: white; margin-bottom: 1.5rem;'>✨ How It Works</h2>
            <div style='text-align: center; color: white; line-height: 2;'>
                <p style='font-size: 1.1rem;'>1️⃣ <strong>Detect Your Mood</strong> - Camera, text, or manual selection</p>
                <p style='font-size: 1.1rem;'>2️⃣ <strong>Chat with Vibefy AI</strong> - Get personalized emotional support</p>
                <p style='font-size: 1.1rem;'>3️⃣ <strong>Discover Music</strong> - Mood-matched songs to enhance your wellbeing</p>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    # Feature cards
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
            <div style='text-align: center; padding: 1.5rem; background: rgba(255, 107, 157, 0.15); border-radius: 15px; border: 2px solid rgba(255, 107, 157, 0.4); transition: transform 0.3s; height: 250px; display: flex; flex-direction: column; justify-content: center;'>
                <h2 style='font-size: 3rem; margin-bottom: 1rem;'>😊</h2>
                <h4 style='color: white; margin-bottom: 0.5rem;'>Detect Your Mood</h4>
                <p style='color: rgba(255,255,255,0.9); font-size: 0.95rem;'>Use camera, text, or manual selection to identify your emotional state</p>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
            <div style='text-align: center; padding: 1.5rem; background: rgba(107, 255, 157, 0.15); border-radius: 15px; border: 2px solid rgba(107, 255, 157, 0.4); height: 250px; display: flex; flex-direction: column; justify-content: center;'>
                <h2 style='font-size: 3rem; margin-bottom: 1rem;'>💬</h2>
                <h4 style='color: white; margin-bottom: 0.5rem;'>Chat with Vibefy AI</h4>
                <p style='color: rgba(255,255,255,0.9); font-size: 0.95rem;'>Get emotional support and guidance from our empathetic AI companion</p>
            </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
            <div style='text-align: center; padding: 1.5rem; background: rgba(107, 157, 255, 0.15); border-radius: 15px; border: 2px solid rgba(107, 157, 255, 0.4); height: 250px; display: flex; flex-direction: column; justify-content: center;'>
                <h2 style='font-size: 3rem; margin-bottom: 1rem;'>🎵</h2>
                <h4 style='color: white; margin-bottom: 0.5rem;'>Discover Music</h4>
                <p style='color: rgba(255,255,255,0.9); font-size: 0.95rem;'>Receive personalized music recommendations based on your mood</p>
            </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Get Started Button
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if st.button("🚀 Get Started", use_container_width=True, type="primary"):
            st.switch_page("pages/2_detect_mood.py")
    
    # Current mood status (if already detected)
    if st.session_state.mood:
        st.markdown("<br>", unsafe_allow_html=True)
        st.info(f"🎯 Current Mood: **{st.session_state.mood.capitalize()}** (Confidence: {st.session_state.confidence:.0%})")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("🔄 Detect New Mood", use_container_width=True):
                st.switch_page("pages/2_detect_mood.py")
        with col2:
            if st.button("💬 Chat with Vibefy", use_container_width=True):
                st.switch_page("pages/3_chat.py")
        with col3:
            if st.button("🎵 Listen to Music", use_container_width=True):
                st.switch_page("pages/4_music.py")
    
    # Footer
    st.markdown("""
        <div style='text-align: center; margin-top: 4rem; padding: 2rem;'>
            <hr style='border: 1px solid rgba(255,255,255,0.1); margin-bottom: 1rem;'>
            <p style='color: rgba(255,255,255,0.6);'>Built with ❤️ using Streamlit | Vibefy 2.0</p>
            <p style='color: rgba(255,255,255,0.5); font-size: 0.9rem;'>
                🔒 Your emotions are private • Session-based • No data stored
            </p>
        </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()