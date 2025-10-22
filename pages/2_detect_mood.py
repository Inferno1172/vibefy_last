

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

# Ensure we have a local logger so we can collect a vibefy_debug.log if something fails
logger = logging.getLogger("vibefy_pages")
if not logger.handlers:
    fh = logging.FileHandler("vibefy_debug.log")
    fh.setLevel(logging.INFO)
    formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s")
    fh.setFormatter(formatter)
    logger.addHandler(fh)
logger.setLevel(logging.INFO)

# Page configuration
st.set_page_config(
    page_title="Detect Your Mood - Vibefy",
    page_icon="😊",
    layout="wide"
)

# Apply theme if mood already detected (wrapped in try/except to avoid fatal crashes)
try:
    if "mood" in st.session_state and st.session_state.mood:
        apply_mood_theme(st.session_state.mood)
except Exception as e:
    logger.exception("apply_mood_theme failed at page load")
    st.error("An error occurred applying the theme. Check vibefy_debug.log for details.")

st.title("😊 Detect Your Mood")
st.write("Choose how you'd like to share your emotional state with Vibefy")

# Initialize session state variables
if "mood" not in st.session_state:
    st.session_state.mood = None
if "confidence" not in st.session_state:
    st.session_state.confidence = None
if "user_input" not in st.session_state:
    st.session_state.user_input = ""
if "mood_confirmed" not in st.session_state:
    st.session_state.mood_confirmed = False

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
    st.markdown("### 📷 Camera Detection")
    st.info("🎥 Position your face in the camera and click 'Start Recording' to capture your emotion over 5 seconds.")
    
    # Initialize recording state
    if "recording" not in st.session_state:
        st.session_state.recording = False
    if "captured_results" not in st.session_state:
        st.session_state.captured_results = []
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        if not st.session_state.recording:
            if st.button("🎬 Start 5-Second Recording", use_container_width=True, type="primary"):
                st.session_state.recording = True
                st.session_state.captured_results = []
                st.session_state.mood_confirmed = False
                st.rerun()
        else:
            if st.button("⏹️ Stop Recording", use_container_width=True, type="secondary"):
                st.session_state.recording = False
                st.rerun()
    
    # Camera recording logic
    if st.session_state.recording:
        try:
            cap = cv2.VideoCapture(0)
            
            if not cap.isOpened():
                st.error("❌ Unable to access webcam. Please check your camera permissions.")
                st.session_state.recording = False
            else:
                # Set camera resolution for better performance
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
                        st.error("❌ Failed to capture frame from camera")
                        break
                    
                    # Resize frame to reasonable size
                    frame = cv2.resize(frame, (400, 300))
                    
                    # Display frame with fixed size
                    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    frame_rgb = cv2.flip(frame_rgb, 1)
                    
                    # Display with controlled size
                    frame_placeholder.image(frame_rgb, channels="RGB", width=400)
                    
                    # Capture emotion every second
                    current_time = time.time()
                    if current_time - last_capture >= 1.0 and frames_processed < 5:
                        try:
                            with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as temp_file:
                                cv2.imwrite(temp_file.name, frame)
                                temp_path = temp_file.name
                            
                            mood_result = detect_from_face(temp_path)
                            if mood_result and (mood_result.get("mood") != "neutral" or mood_result.get("confidence", 0) > 0):
                                st.session_state.captured_results.append(mood_result)
                                status_placeholder.info(f"📸 Captured {len(st.session_state.captured_results)}/5: {mood_result.get('mood')} ({mood_result.get('confidence'):.0%})")
                            
                            os.unlink(temp_path)
                            last_capture = current_time
                            frames_processed += 1
                        except Exception as e:
                            logger.exception("Error processing a frame")
                            st.error(f"Error processing frame: {e}")
                    
                    time.sleep(0.01)  # Small delay to prevent overwhelming the system
                
                cap.release()
                st.session_state.recording = False
                
                # Process results
                if st.session_state.captured_results:
                    moods = [r["mood"] for r in st.session_state.captured_results]
                    if moods:
                        most_common_mood, count = Counter(moods).most_common(1)[0]
                        same_mood_results = [r for r in st.session_state.captured_results if r["mood"] == most_common_mood]
                        avg_conf = mean([r.get("confidence", 0.0) for r in same_mood_results])
                        
                        st.session_state.mood = most_common_mood
                        st.session_state.confidence = avg_conf
                        st.session_state.mood_confirmed = True
                        
                        status_placeholder.empty()
                        st.rerun()
                    else:
                        status_placeholder.warning("⚠️ No clear emotion detected. Please try again with better lighting.")
                else:
                    status_placeholder.warning("⚠️ No emotions detected. Please ensure your face is clearly visible.")
                    
        except Exception as e:
            logger.exception("Camera error")
            st.error(f"❌ Camera error: {str(e)}")
            st.session_state.recording = False

# TEXT DETECTION
elif option == "✍️ Text":
    st.markdown("### ✍️ Text Analysis")
    st.info("📝 Describe how you're feeling in your own words. Our AI will analyze the emotion in your text.")
    
    user_text = st.text_area(
        "How are you feeling right now?",
        placeholder="Example: I'm feeling overwhelmed with work and a bit anxious about the deadline...",
        height=150,
        key="text_input"
    )
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        if st.button("🔍 Analyze My Feelings", use_container_width=True, type="primary"):
            if user_text.strip():
                with st.spinner("Analyzing your text..."):
                    try:
                        mood_result = analyze_text(user_text)
                        st.session_state.mood = mood_result.get("mood")
                        st.session_state.confidence = mood_result.get("confidence")
                        st.session_state.user_input = user_text
                        st.session_state.mood_confirmed = True
                        st.rerun()
                    except Exception as e:
                        logger.exception("analyze_text failed")
                        st.error("Text analysis failed. Please try again or check vibefy_debug.log")
            else:
                st.warning("⚠️ Please enter some text describing your feelings.")

# MANUAL DETECTION
elif option == "🎯 Manual":
    st.markdown("### 🎯 Manual Selection")
    st.info("🎨 Choose the emotion that best describes how you're feeling right now.")
    
    # Emotion cards
    emotions = {
        "joy": {"emoji": "😊", "color": "#FF6B9D", "desc": "Happy, Excited, Joyful"},
        "sadness": {"emoji": "😢", "color": "#4A90E2", "desc": "Sad, Down, Melancholic"},
        "anger": {"emoji": "😡", "color": "#FF416C", "desc": "Angry, Frustrated, Irritated"},
        "fear": {"emoji": "😨", "color": "#8E2DE2", "desc": "Anxious, Worried, Scared"},
        "disgust": {"emoji": "😣", "color": "#FF8E53", "desc": "Disgusted, Uncomfortable"},
        "surprise": {"emoji": "😲", "color": "#00CDAC", "desc": "Surprised, Astonished"},
        "neutral": {"emoji": "😐", "color": "#7474BF", "desc": "Calm, Balanced, Neutral"}
    }
    
    cols = st.columns(4)
    
    for i, (mood, data) in enumerate(emotions.items()):
        with cols[i % 4]:
            if st.button(
                f"{data['emoji']}\n\n**{mood.capitalize()}**\n\n{data['desc']}",
                key=f"mood_{mood}",
                use_container_width=True
            ):
                st.session_state.mood = mood
                st.session_state.confidence = 1.0  # Manual selection has 100% confidence
                st.session_state.mood_confirmed = True
                st.rerun()
    
    st.divider()
    
    # Optional: Fine-tune confidence
    if st.session_state.mood and not st.session_state.mood_confirmed:
        confidence = st.slider(
            "How strongly do you feel this emotion?",
            0.0, 1.0, 0.8, 0.05,
            help="Slide to indicate the intensity of your feeling"
        )
        st.session_state.confidence = confidence

# MOOD CONFIRMATION DISPLAY
if st.session_state.mood_confirmed and st.session_state.mood:
    st.divider()
    st.markdown("## 🎯 Mood Detected!")
    
    # Clear any previous content that might be causing display issues
    st.empty()
    
    # Apply and display mood theme inside try/except to capture any exceptions
    try:
        apply_mood_theme(st.session_state.mood)
        display_mood_confirmation(st.session_state.mood, st.session_state.confidence)
    except Exception as e:
        logger.exception("Error rendering mood confirmation")
        st.error("An error occurred while showing your detected mood. Check vibefy_debug.log for details.")
    
    # Description
    try:
        desc = get_emotion_description(st.session_state.mood)
        st.markdown(f"""
            <div style='background: rgba(255,255,255,0.1); padding: 1rem; border-radius: 10px; margin: 1rem 0;'>
                <p style='color: white; font-size: 1.1rem; margin: 0;'>
                    {desc}
                </p>
            </div>
        """, unsafe_allow_html=True)
    except Exception:
        logger.exception("get_emotion_description failed")
    
    # Next steps
    st.markdown("### 🎯 What Would You Like To Do Next?")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("💬 Chat with Vibefy AI", use_container_width=True, type="primary"):
            # Use Streamlit's page navigation — if this raises, the try/except above prevents crash
            try:
                st.switch_page("pages/3_chat.py")
            except Exception as e:
                logger.exception("Navigation to chat failed")
                st.error("Could not navigate to chat page; try selecting Chat from the sidebar.")
    
    with col2:
        if st.button("🎵 Listen to Music", use_container_width=True, type="primary"):
            try:
                st.switch_page("pages/4_music.py")
            except Exception:
                logger.exception("Navigation to music failed")
                st.error("Could not navigate to music page; try selecting Music from the sidebar.")
    
    with col3:
        if st.button("🔄 Detect Again", use_container_width=True, type="secondary"):
            st.session_state.mood_confirmed = False
            st.session_state.mood = None
            st.session_state.confidence = None
            st.rerun()

# Navigation
st.divider()
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    if st.button("🏠 Back to Home", use_container_width=True):
        try:
            st.switch_page("app.py")
        except Exception:
            logger.exception("Navigation to app failed")
            st.error("Could not navigate to home; please click the app icon in the top-left.")