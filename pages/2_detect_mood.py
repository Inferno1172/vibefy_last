import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import streamlit as st
from modules.emotion_detector import detect_from_face, analyze_text, get_emotion_description
from modules.themes import apply_mood_theme, display_mood_confirmation
import tempfile
import cv2
import numpy as np
import time
from collections import Counter
from statistics import mean
import logging
import traceback
from datetime import datetime
from modules.themes import apply_default_theme

apply_default_theme()


# Set up logging configuration
log_formatter = logging.Formatter('%(asctime)s UTC - %(levelname)s - %(message)s')
log_file = 'vibefy_debug.log'

# Create file handler
file_handler = logging.FileHandler(log_file, mode='a', encoding='utf-8')
file_handler.setFormatter(log_formatter)
file_handler.setLevel(logging.DEBUG)

# Create console handler
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setFormatter(log_formatter)
console_handler.setLevel(logging.INFO)

# Set up logger
logger = logging.getLogger('vibefy')
logger.setLevel(logging.DEBUG)
logger.addHandler(file_handler)
logger.addHandler(console_handler)

# Log startup information
logger.info(f"Mood detection page loaded by user: {os.getenv('USERNAME', 'unknown')}")
logger.info(f"Current UTC time: {datetime.utcnow().strftime('%Y-%m-%D %H:%M:%S')}")

# Page configuration
st.set_page_config(
    page_title="Detect Your Mood - Vibefy",
    page_icon="😊",
    layout="wide"
)

# Initialize session state variables
logger.debug("Initializing session state variables")
if "mood" not in st.session_state:
    logger.debug("Initializing mood in session state")
    st.session_state.mood = None
if "confidence" not in st.session_state:
    logger.debug("Initializing confidence in session state")
    st.session_state.confidence = None
if "user_input" not in st.session_state:
    logger.debug("Initializing user_input in session state")
    st.session_state.user_input = ""
if "mood_confirmed" not in st.session_state:
    logger.debug("Initializing mood_confirmed in session state")
    st.session_state.mood_confirmed = False
if "recording" not in st.session_state:
    logger.debug("Initializing recording in session state")
    st.session_state.recording = False
if "captured_results" not in st.session_state:
    logger.debug("Initializing captured_results in session state")
    st.session_state.captured_results = []

# Apply theme if mood already detected
try:
    if "mood" in st.session_state and st.session_state.mood:
        logger.debug(f"Applying existing mood theme: {st.session_state.mood}")
        apply_mood_theme(st.session_state.mood)
except Exception as e:
    logger.exception("apply_mood_theme failed at page load")
    st.error("An error occurred applying the theme. Check vibefy_debug.log for details.")

st.title("😊 Detect Your Mood")
st.write("Choose how you'd like to share your emotional state with Vibefy")

# Detection method selection
st.markdown("### Choose Your Detection Method")
option = st.radio(
    "Select one:",
    ["📷 Camera", "✍️ Text", "🎯 Manual"],
    horizontal=True,
    label_visibility="collapsed"
)

st.divider()

# CAMERA DETECTION
if option == "📷 Camera":
    logger.info("User selected camera detection method")
    st.markdown("### 📷 Camera Detection")
    st.info("🎥 Position your face in the camera and click 'Start Recording' to capture your emotion over 5 seconds.")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        if not st.session_state.recording:
            if st.button("🎬 Start 5-Second Recording", use_container_width=True, type="primary"):
                logger.info("Starting camera recording")
                st.session_state.recording = True
                st.session_state.captured_results = []
                st.session_state.mood_confirmed = False
                st.rerun()
        else:
            if st.button("⏹️ Stop Recording", use_container_width=True, type="secondary"):
                logger.info("Stopping camera recording")
                st.session_state.recording = False
                st.rerun()

    if st.session_state.recording:
        logger.debug("Camera recording in progress")
        try:
            cap = cv2.VideoCapture(0)
            
            if not cap.isOpened():
                logger.error("Failed to open webcam")
                st.error("❌ Unable to access webcam. Please check your camera permissions.")
                st.session_state.recording = False
            else:
                logger.debug("Webcam opened successfully")
                # Camera configuration
                cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
                cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
                cap.set(cv2.CAP_PROP_FPS, 30)
                
                status_placeholder = st.empty()
                status_placeholder.warning("🔴 Recording in progress... Keep your face visible!")
                
                frame_placeholder = st.empty()
                start_time = time.time()
                last_capture = 0
                frames_processed = 0
                
                while st.session_state.recording and (time.time() - start_time) < 5:
                    ret, frame = cap.read()
                    
                    if not ret:
                        logger.error("Failed to capture frame from camera")
                        st.error("❌ Failed to capture frame from camera")
                        break
                    
                    frame = cv2.resize(frame, (400, 300))
                    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    frame_rgb = cv2.flip(frame_rgb, 1)
                    frame_placeholder.image(frame_rgb, channels="RGB", width=400)
                    
                    current_time = time.time()
                    if current_time - last_capture >= 1.0 and frames_processed < 5:
                        try:
                            logger.debug(f"Processing frame {frames_processed + 1}")
                            with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as temp_file:
                                cv2.imwrite(temp_file.name, frame)
                                temp_path = temp_file.name
                            
                            mood_result = detect_from_face(temp_path)
                            logger.debug(f"Frame {frames_processed + 1} mood result: {mood_result}")
                            
                            if mood_result and (mood_result.get("mood") != "neutral" or mood_result.get("confidence", 0) > 0):
                                st.session_state.captured_results.append(mood_result)
                                status_placeholder.info(f"📸 Captured {len(st.session_state.captured_results)}/5: {mood_result.get('mood')} ({mood_result.get('confidence'):.0%})")
                            
                            os.unlink(temp_path)
                            last_capture = current_time
                            frames_processed += 1
                        except Exception as e:
                            logger.exception(f"Error processing frame {frames_processed + 1}")
                            st.error(f"Error processing frame: {str(e)}")
                    
                    time.sleep(0.01)
                
                cap.release()
                st.session_state.recording = False
                
                # Process results
                if st.session_state.captured_results:
                    logger.info("Processing captured results")
                    moods = [r["mood"] for r in st.session_state.captured_results]
                    if moods:
                        most_common_mood, count = Counter(moods).most_common(1)[0]
                        same_mood_results = [r for r in st.session_state.captured_results if r["mood"] == most_common_mood]
                        avg_conf = mean([r.get("confidence", 0.0) for r in same_mood_results])
                        
                        logger.info(f"Final mood detection: {most_common_mood} with confidence {avg_conf:.2f}")
                        st.session_state.mood = most_common_mood
                        st.session_state.confidence = avg_conf
                        st.session_state.mood_confirmed = True
                        
                        status_placeholder.empty()
                        st.rerun()
                    else:
                        logger.warning("No clear emotion detected")
                        status_placeholder.warning("⚠️ No clear emotion detected. Please try again with better lighting.")
                else:
                    logger.warning("No emotions detected")
                    status_placeholder.warning("⚠️ No emotions detected. Please ensure your face is clearly visible.")
                    
        except Exception as e:
            logger.exception("Camera error")
            st.error(f"❌ Camera error: {str(e)}")
            st.session_state.recording = False

# TEXT DETECTION
elif option == "✍️ Text":
    logger.info("User selected text detection method")
    st.markdown("### ✍️ Text Analysis")
    st.info("📝 Describe how you're feeling in your own words. Our AI will analyze the emotion in your text.")
    
    # Use a form to handle text input
    with st.form("text_analysis_form"):
        user_text = st.text_area(
            "How are you feeling right now?",
            placeholder="Example: I'm feeling overwhelmed with work and a bit anxious about the deadline...",
            height=150,
            key="text_input"
        )
        
        submit_button = st.form_submit_button(
            "🔍 Analyze My Feelings",
            use_container_width=True,
            type="primary"
        )
    
    if submit_button:
        if user_text.strip():
            with st.spinner("Analyzing your text..."):
                try:
                    logger.info(f"Analyzing text: {user_text[:50]}...")
                    mood_result = analyze_text(user_text)
                    logger.debug(f"Text analysis result: {mood_result}")
                    
                    st.session_state.mood = mood_result.get("mood")
                    st.session_state.confidence = mood_result.get("confidence")
                    st.session_state.user_input = user_text
                    st.session_state.mood_confirmed = True
                    st.rerun()
                except Exception as e:
                    logger.exception("Text analysis failed")
                    st.error("Text analysis failed. Please try again or check vibefy_debug.log")
        else:
            st.warning("⚠️ Please enter some text describing your feelings.")

# MANUAL DETECTION
elif option == "🎯 Manual":
    logger.info("User selected manual detection method")
    st.markdown("### 🎯 Manual Selection")
    st.info("🎨 Choose the emotion that best describes how you're feeling right now.")
    
    # Emotion cards with improved styling
    emotions = {
        "joy": {"emoji": "😊", "color": "#FF6B9D", "desc": "Happy, Excited, Joyful"},
        "sadness": {"emoji": "😢", "color": "#4A90E2", "desc": "Sad, Down, Melancholic"},
        "anger": {"emoji": "😡", "color": "#FF416C", "desc": "Angry, Frustrated, Irritated"},
        "fear": {"emoji": "😨", "color": "#8E2DE2", "desc": "Anxious, Worried, Scared"},
        "disgust": {"emoji": "😣", "color": "#FF8E53", "desc": "Disgusted, Uncomfortable"},
        "surprise": {"emoji": "😲", "color": "#00CDAC", "desc": "Surprised, Astonished"},
        "neutral": {"emoji": "😐", "color": "#7474BF", "desc": "Calm, Balanced, Neutral"}
    }
    
    # Create emotion selection cards in a grid
    cols = st.columns(4)
    
    for i, (mood, data) in enumerate(emotions.items()):
        with cols[i % 4]:
            # Create a clickable card with custom styling
            card_html = f"""
            <div style="
                background: linear-gradient(135deg, {data['color']}22 0%, {data['color']}11 100%);
                border: 2px solid {data['color']}44;
                border-radius: 15px;
                padding: 1rem;
                margin: 0.5rem 0;
                text-align: center;
                transition: all 0.3s ease;
                cursor: pointer;
            ">
                <div style="font-size: 3rem; margin-bottom: 0.5rem;">{data['emoji']}</div>
                <div style="font-weight: bold; margin-bottom: 0.5rem; color: white;">{mood.capitalize()}</div>
                <div style="color: rgba(255,255,255,0.8); font-size: 0.9rem;">{data['desc']}</div>
            </div>
            """
            
            # Create a clickable button with the same dimensions as the card
            if st.button(
                f"{data['emoji']}\n\n**{mood.capitalize()}**\n\n{data['desc']}",
                key=f"mood_{mood}",
                use_container_width=True
            ):
                logger.info(f"User selected mood: {mood} (manual selection)")
                st.session_state.mood = mood
                st.session_state.confidence = 1.0  # Manual selection has 100% confidence
                st.session_state.mood_confirmed = True
                st.rerun()

# MOOD CONFIRMATION DISPLAY
if st.session_state.mood_confirmed and st.session_state.mood:
    logger.info(f"Displaying mood confirmation for mood: {st.session_state.mood} with confidence: {st.session_state.confidence}")
    
    st.divider()
    st.markdown("## 🎯 Mood Detected!")
    
    # Clear any previous content that might be causing display issues
    st.empty()
    
    # Apply and display mood theme inside try/except to capture any exceptions
    try:
        logger.debug("Applying mood theme...")
        apply_mood_theme(st.session_state.mood)
        
        logger.debug("Displaying mood confirmation...")
        display_mood_confirmation(st.session_state.mood, st.session_state.confidence)
        
        logger.info("Successfully displayed mood confirmation")
    except Exception as e:
        logger.exception(f"Error in mood confirmation display: {str(e)}")
        st.error("An error occurred while showing your detected mood. Check vibefy_debug.log for details.")
    
    # Description
    try:
        logger.debug("Getting emotion description...")
        desc = get_emotion_description(st.session_state.mood)
        logger.debug(f"Retrieved description: {desc[:50]}...")
        
        st.markdown(f"""
            <div style='background: rgba(255,255,255,0.1); padding: 1rem; border-radius: 10px; margin: 1rem 0;'>
                <p style='color: white; font-size: 1.1rem; margin: 0;'>
                    {desc}
                </p>
            </div>
        """, unsafe_allow_html=True)
    except Exception as e:
        logger.exception(f"Error getting emotion description: {str(e)}")

    # Navigation buttons
    st.markdown("### 🎯 What Would You Like To Do Next?")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("💬 Chat with Vibefy AI", use_container_width=True, type="primary"):
            logger.info("User clicked 'Chat with Vibefy AI' button")
            try:
                st.switch_page("pages/3_chat.py")
            except Exception as e:
                logger.exception("Failed to navigate to chat page")
                st.error("Could not navigate to chat page; try selecting Chat from the sidebar.")
    
    with col2:
        if st.button("🎵 Listen to Music", use_container_width=True, type="primary"):
            logger.info("User clicked 'Listen to Music' button")
            try:
                st.switch_page("pages/4_music.py")
            except Exception as e:
                logger.exception("Failed to navigate to music page")
                st.error("Could not navigate to music page; try selecting Music from the sidebar.")
    
    with col3:
        if st.button("🔄 Detect Again", use_container_width=True, type="secondary"):
            logger.info("User clicked 'Detect Again' button")
            st.session_state.mood_confirmed = False
            st.session_state.mood = None
            st.session_state.confidence = None
            st.rerun()

# Navigation footer
st.divider()
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    if st.button("🏠 Back to Home", use_container_width=True):
        logger.info("User clicked 'Back to Home' button")
        try:
            st.switch_page("app.py")
        except Exception as e:
            logger.exception("Failed to navigate to home page")
            st.error("Could not navigate to home; please click the app icon in the top-left.")