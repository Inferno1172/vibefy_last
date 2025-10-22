import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import streamlit as st
from modules.music_service import search_songs, get_mood_keywords
from modules.themes import apply_mood_theme

# Page configuration
st.set_page_config(
    page_title="Music for Your Mood - Vibefy",
    page_icon="🎵",
    layout="wide"
)

# Check if mood is detected
if "mood" not in st.session_state or not st.session_state.mood:
    st.warning("🎯 Please detect your mood first to get personalized music recommendations!")
    if st.button("🔍 Detect My Mood"):
        st.switch_page("pages/2_detect_mood.py")
    st.stop()

# Apply mood theme
apply_mood_theme(st.session_state.mood)

# Initialize session state for music
if "current_video_index" not in st.session_state:
    st.session_state.current_video_index = 0
if "music_videos" not in st.session_state:
    st.session_state.music_videos = search_songs(st.session_state.mood, num_results=5)

# Page header
st.title("🎵 Music for Your Mood")

mood_emoji = {
    "joy": "😊",
    "sadness": "😢",
    "anger": "😡",
    "fear": "😨",
    "disgust": "😣",
    "surprise": "😲",
    "neutral": "😐"
}

st.markdown(f"""
    <div style='background: rgba(255,255,255,0.15); padding: 1.5rem; border-radius: 15px; margin-bottom: 2rem; border: 2px solid rgba(255,255,255,0.3);'>
        <h2 style='color: white; margin: 0 0 0.5rem 0;'>
            {mood_emoji.get(st.session_state.mood, '🎵')} {st.session_state.mood.capitalize()} Vibes
        </h2>
        <p style='color: rgba(255,255,255,0.9); margin: 0; font-size: 1.1rem;'>
            We've curated music to match your {st.session_state.mood} mood
        </p>
    </div>
""", unsafe_allow_html=True)

# Important playback instructions
st.info("🔊 **Click the PLAY button (▶️) on the video player below to start the music!**")
st.warning("⚠️ Music does NOT autoplay - you must click play manually")

# Current playing song
current_video = st.session_state.music_videos[st.session_state.current_video_index]

# Main player section
col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("### 🎧 Now Playing")
    
    # YouTube player
    st.video(f"https://www.youtube.com/watch?v={current_video['video_id']}")
    
    # Song info
    st.markdown(f"""
        <div style='background: rgba(255,255,255,0.1); padding: 1rem; border-radius: 10px; margin-top: 1rem;'>
            <h3 style='color: white; margin: 0 0 0.5rem 0;'>🎵 {current_video['title']}</h3>
            <p style='color: rgba(255,255,255,0.8); margin: 0;'>{current_video['description']}</p>
        </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("### 🎮 Player Controls")
    
    # Navigation buttons
    col_prev, col_next = st.columns(2)
    
    with col_prev:
        if st.button("⏮️ Previous", use_container_width=True, disabled=(st.session_state.current_video_index == 0)):
            st.session_state.current_video_index -= 1
            st.rerun()
    
    with col_next:
        if st.button("Next ⏭️", use_container_width=True, disabled=(st.session_state.current_video_index >= len(st.session_state.music_videos) - 1)):
            st.session_state.current_video_index += 1
            st.rerun()
    
    st.markdown(f"""
        <div style='text-align: center; padding: 1rem; background: rgba(255,255,255,0.1); border-radius: 10px; margin-top: 1rem;'>
            <p style='color: white; margin: 0;'>Track {st.session_state.current_video_index + 1} of {len(st.session_state.music_videos)}</p>
        </div>
    """, unsafe_allow_html=True)
    
    # Quick actions
    st.markdown("### ⚡ Quick Actions")
    
    if st.button("🔄 New Mood Detection", use_container_width=True):
        st.switch_page("pages/2_detect_mood.py")
    
    if st.button("💬 Chat with AI", use_container_width=True):
        st.switch_page("pages/3_chat.py")
    
    if st.button("🔀 Shuffle Music", use_container_width=True):
        import random
        st.session_state.music_videos = search_songs(st.session_state.mood, num_results=5)
        st.session_state.current_video_index = 0
        st.rerun()

# Playlist section
st.divider()
st.markdown("### 📻 Full Playlist")

# Display all songs in grid
cols = st.columns(3)

for i, video in enumerate(st.session_state.music_videos):
    with cols[i % 3]:
        # Highlight current song
        border_color = "rgba(255, 107, 157, 0.8)" if i == st.session_state.current_video_index else "rgba(255,255,255,0.2)"
        
        st.markdown(f"""
            <div style='background: rgba(255,255,255,0.1); border-radius: 10px; padding: 1rem; border: 2px solid {border_color}; margin-bottom: 1rem;'>
                <img src='{video['thumbnail']}' style='width: 100%; border-radius: 8px;'>
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"**{i+1}. {video['title']}**")
        st.caption(video['description'])
        
        if st.button(f"▶️ Play This Song", key=f"play_{i}", use_container_width=True, disabled=(i == st.session_state.current_video_index)):
            st.session_state.current_video_index = i
            st.rerun()

# Mood keywords info
with st.expander("🎯 How We Choose Your Music"):
    keywords = get_mood_keywords(st.session_state.mood)
    st.write(f"For your **{st.session_state.mood}** mood, we search for:")
    for keyword in keywords:
        st.write(f"- {keyword}")

# Navigation footer
st.divider()
col1, col2, col3 = st.columns(3)

with col1:
    if st.button("🏠 Home", use_container_width=True):
        st.switch_page("app.py")

with col2:
    if st.button("🔍 Change Mood", use_container_width=True):
        st.switch_page("pages/2_detect_mood.py")

with col3:
    if st.button("💬 Chat with AI", use_container_width=True):
        st.switch_page("pages/3_chat.py")

# Footer info
st.markdown("""
    <div style='text-align: center; margin-top: 2rem; padding: 1rem; color: rgba(255,255,255,0.6);'>
        <p>🎵 Enjoying the music? Your mood shapes your playlist!</p>
        <p style='font-size: 0.9rem;'>All music sourced from YouTube | Session-based recommendations</p>
    </div>
""", unsafe_allow_html=True)