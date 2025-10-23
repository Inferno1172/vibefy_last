# pages/3_chat.py
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import streamlit as st
from modules.themes import apply_mood_theme
from modules.ai_companion import send_message, get_fallback_response
import logging



# Local logger
logger = logging.getLogger("vibefy_pages")
if not logger.handlers:
    fh = logging.FileHandler("vibefy_debug.log")
    fh.setLevel(logging.INFO)
    logger.addHandler(fh)
logger.setLevel(logging.INFO)

# Page configuration
st.set_page_config(
    page_title="Chat with Vibefy - Your AI Companion",
    page_icon="💬",
    layout="wide"
)

# Check if mood is detected
if "mood" not in st.session_state or not st.session_state.mood:
    st.warning("🎯 Please detect your mood first before chatting!")
    if st.button("🔍 Detect My Mood"):
        try:
            st.switch_page("pages/2_detect_mood.py")
        except Exception:
            st.error("Navigation failed. Please navigate using the sidebar.")
    st.stop()

# Apply mood theme (safe)
try:
    apply_mood_theme(st.session_state.mood)
except Exception:
    logger.exception("apply_mood_theme failed in chat")
    st.error("Theme rendering failed. Continuing without mood styling.")

# Initialize chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Page header (show confidence safely)
try:
    conf_display = "{:.0%}".format(st.session_state.confidence) if isinstance(st.session_state.confidence, (int, float)) else "N/A"
except Exception:
    conf_display = "N/A"

st.title("💬 Chat with Vibefy AI")
st.markdown(f"""
    <div style='background: rgba(255,255,255,0.1); padding: 1rem; border-radius: 10px; margin-bottom: 1rem;'>
        <p style='color: white; margin: 0;'>
            🎯 Current Mood: <strong>{st.session_state.mood.capitalize()}</strong> 
            (Confidence: {conf_display})
        </p>
        <p style='color: rgba(255,255,255,0.8); margin: 0.5rem 0 0 0; font-size: 0.9rem;'>
            I'm here to listen and support you. Feel free to share what's on your mind.
        </p>
    </div>
""", unsafe_allow_html=True)

# Mood-specific greeting
MOOD_GREETINGS = {
    "joy": "😊 It's wonderful to see you in such a great mood! What's bringing you joy today?",
    "sadness": "💙 I can see you're going through a tough time. I'm here to listen. What's on your mind?",
    "anger": "🧘 I sense some frustration. It's okay to feel this way. Would you like to talk about what's bothering you?",
    "fear": "🛡️ I understand you might be feeling anxious. Let's work through this together. What's worrying you?",
    "disgust": "🌿 I notice you're feeling uncomfortable. Sometimes we need to process difficult feelings. How can I help?",
    "surprise": "🎉 You seem surprised! That can be exciting or unsettling. Tell me more about what happened.",
    "neutral": "🌊 You're in a calm state. Is there anything you'd like to explore or discuss today?"
}

# Display greeting if first time
if len(st.session_state.chat_history) == 0:
    greeting = MOOD_GREETINGS.get(st.session_state.mood, "👋 Hello! How can I support you today?")
    st.session_state.chat_history.append({
        "role": "assistant",
        "content": greeting
    })

# Chat display area
chat_container = st.container()

with chat_container:
    for message in st.session_state.chat_history:
        with st.chat_message(message["role"]):
            st.write(message["content"])

# Chat input
user_input = st.chat_input("Type your message here...")

if user_input:
    # Add user message to history
    st.session_state.chat_history.append({
        "role": "user",
        "content": user_input
    })
    
    # Display user message
    with st.chat_message("user"):
        st.write(user_input)
    
    # Get AI response
    with st.chat_message("assistant"):
        with st.spinner("Vibefy is thinking..."):
            try:
                # Ensure mood is set
                current_mood = getattr(st.session_state, 'mood', 'neutral')
                
                # Get response from Gemini
                response = send_message(user_input, st.session_state)
                
                # Display and save response
                st.write(response)
                st.session_state.chat_history.append({
                    "role": "assistant",
                    "content": response
                })
                
            except Exception as e:
                logger.exception("AI response failed")
                # Use fallback response with safe mood handling
                current_mood = getattr(st.session_state, 'mood', 'neutral')
                fallback_response = get_fallback_response(current_mood)
                st.write(fallback_response)
                st.session_state.chat_history.append({
                    "role": "assistant",
                    "content": fallback_response
                })
                st.error(f"Note: Using fallback response due to: {str(e)}")
# Sidebar with chat actions
with st.sidebar:
    st.markdown("### 💬 Chat Options")
    
    if st.button("🔄 Start New Conversation", use_container_width=True):
        st.session_state.chat_history = []
        if "thread_id" in st.session_state:
            del st.session_state.thread_id
        st.rerun()
    
    if st.button("🎵 Listen to Music", use_container_width=True):
        try:
            st.switch_page("pages/4_music.py")
        except Exception:
            st.error("Navigation failed. Use the top-left menu to go to Music.")
    
    if st.button("😊 Change Mood", use_container_width=True):
        try:
            st.switch_page("pages/2_detect_mood.py")
        except Exception:
            st.error("Navigation failed. Use the top-left menu to go back.")
    
    st.divider()
    
    st.markdown("### 💡 Chat Tips")
    st.markdown("""
    - Be honest about your feelings
    - Share as much or as little as you want
    - Ask for coping strategies
    - Request mood-lifting suggestions
    """)
    
    st.divider()
    
    st.markdown(f"""
    **Messages:** {len(st.session_state.chat_history)}
    
    **Your Mood:** {st.session_state.mood.capitalize()}
    """)

# Navigation footer
st.divider()
col1, col2, col3 = st.columns(3)

with col1:
    if st.button("🏠 Home", use_container_width=True):
        try:
            st.switch_page("app.py")
        except Exception:
            st.error("Navigation failed. Use the top-left menu to go to Home.")

with col2:
    if st.button("🔍 Detect Mood", use_container_width=True):
        try:
            st.switch_page("pages/2_detect_mood.py")
        except Exception:
            st.error("Navigation failed. Use the top-left menu to go to Detect Mood.")

with col3:
    if st.button("🎵 Music", use_container_width=True):
        try:
            st.switch_page("pages/4_music.py")
        except Exception:
            st.error("Navigation failed. Use the top-left menu to go to Music.")