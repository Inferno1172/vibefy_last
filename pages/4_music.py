# import sys
# import os
# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# from dotenv import load_dotenv
# import streamlit as st
# from modules.music_service import search_songs, get_mood_keywords
# from modules.themes import apply_mood_theme

# import tomllib
# from pathlib import Path



# YOUTUBE_API_KEY =  "AIzaSyDXUZH6L0_JCa6AVwCznvd00YcIv71OrQQ"

# # Page configuration
# st.set_page_config(
#     page_title="Music for Your Mood - Vibefy",
#     page_icon="🎵",
#     layout="wide"
# )

# # Check if mood is detected
# if "mood" not in st.session_state or not st.session_state.mood:
#     st.warning("🎯 Please detect your mood first to get personalized music recommendations!")
#     if st.button("🔍 Detect My Mood"):
#         st.switch_page("pages/2_detect_mood.py")
#     st.stop()

# # Apply mood theme
# apply_mood_theme(st.session_state.mood)

# # Initialize session state for music
# if "current_video_index" not in st.session_state:
#     st.session_state.current_video_index = 0
# if "music_videos" not in st.session_state:
#     mood_keywords = get_mood_keywords(st.session_state.mood)
#     st.session_state.music_videos = search_songs(mood_keywords, YOUTUBE_API_KEY)

# # Page header
# st.title("🎵 Music for Your Mood")

# mood_emoji = {
#     "joy": "😊",
#     "sadness": "😢",
#     "anger": "😡",
#     "fear": "😨",
#     "disgust": "😣",
#     "surprise": "😲",
#     "neutral": "😐"
# }

# st.markdown(f"""
#     <div style='background: rgba(255,255,255,0.15); padding: 1.5rem; border-radius: 15px; margin-bottom: 2rem; border: 2px solid rgba(255,255,255,0.3);'>
#         <h2 style='color: white; margin: 0 0 0.5rem 0;'>
#             {mood_emoji.get(st.session_state.mood, '🎵')} {st.session_state.mood.capitalize()} Vibes
#         </h2>
#         <p style='color: rgba(255,255,255,0.9); margin: 0; font-size: 1.1rem;'>
#             We've curated music to match your {st.session_state.mood} mood
#         </p>
#     </div>
# """, unsafe_allow_html=True)

# # Important playback instructions
# st.info("🔊 **Click the PLAY button (▶️) on the video player below to start the music!**")
# st.warning("⚠️ Music does NOT autoplay - you must click play manually")

# # Current playing song
# current_video = st.session_state.music_videos[st.session_state.current_video_index]

# # Main player section
# col1, col2 = st.columns([2, 1])

# with col1:
#     st.markdown("### 🎧 Now Playing")
    
#     # YouTube player
#     st.video(f"https://www.youtube.com/watch?v={current_video['video_id']}")
    
#     # Song info
#     st.markdown(f"""
#         <div style='background: rgba(255,255,255,0.1); padding: 1rem; border-radius: 10px; margin-top: 1rem;'>
#             <h3 style='color: white; margin: 0 0 0.5rem 0;'>🎵 {current_video['title']}</h3>
#             <p style='color: rgba(255,255,255,0.8); margin: 0;'>{current_video['description']}</p>
#         </div>
#     """, unsafe_allow_html=True)

# with col2:
#     st.markdown("### 🎮 Player Controls")
    
#     # Navigation buttons
#     col_prev, col_next = st.columns(2)
    
#     with col_prev:
#         if st.button("⏮️ Previous", use_container_width=True, disabled=(st.session_state.current_video_index == 0)):
#             st.session_state.current_video_index -= 1
#             st.rerun()
    
#     with col_next:
#         if st.button("Next ⏭️", use_container_width=True, disabled=(st.session_state.current_video_index >= len(st.session_state.music_videos) - 1)):
#             st.session_state.current_video_index += 1
#             st.rerun()
    
#     st.markdown(f"""
#         <div style='text-align: center; padding: 1rem; background: rgba(255,255,255,0.1); border-radius: 10px; margin-top: 1rem;'>
#             <p style='color: white; margin: 0;'>Track {st.session_state.current_video_index + 1} of {len(st.session_state.music_videos)}</p>
#         </div>
#     """, unsafe_allow_html=True)
    
#     # Quick actions
#     st.markdown("### ⚡ Quick Actions")
    
#     if st.button("🔄 New Mood Detection", use_container_width=True):
#         st.switch_page("pages/2_detect_mood.py")
    
#     if st.button("💬 Chat with AI", use_container_width=True, key="chat_button_quick"):
#         st.switch_page("pages/3_chat.py")
    
#     if st.button("🔀 Shuffle Music", use_container_width=True):
#         import random
#         mood_keywords = get_mood_keywords(st.session_state.mood)
#         st.session_state.music_videos = search_songs(mood_keywords, YOUTUBE_API_KEY)
#         st.session_state.current_video_index = 0
#         st.rerun()

# # Playlist section
# st.divider()
# st.markdown("### 📻 Full Playlist")

# # Display all songs in grid
# cols = st.columns(3)

# for i, video in enumerate(st.session_state.music_videos):
#     with cols[i % 3]:
#         # Highlight current song
#         border_color = "rgba(255, 107, 157, 0.8)" if i == st.session_state.current_video_index else "rgba(255,255,255,0.2)"
        
#         st.markdown(f"""
#             <div style='background: rgba(255,255,255,0.1); border-radius: 10px; padding: 1rem; border: 2px solid {border_color}; margin-bottom: 1rem;'>
#                 <img src='{video['thumbnail']}' style='width: 100%; border-radius: 8px;'>
#             </div>
#         """, unsafe_allow_html=True)
        
#         st.markdown(f"**{i+1}. {video['title']}**")
#         st.caption(video['description'])
        
#         if st.button(f"▶️ Play This Song", key=f"play_{i}", use_container_width=True, disabled=(i == st.session_state.current_video_index)):
#             st.session_state.current_video_index = i
#             st.rerun()

# # Mood keywords info
# with st.expander("🎯 How We Choose Your Music"):
#     keywords = get_mood_keywords(st.session_state.mood)
#     st.write(f"For your **{st.session_state.mood}** mood, we search for:")
#     for keyword in keywords:
#         st.write(f"- {keyword}")

# # Navigation footer
# st.divider()
# col1, col2, col3 = st.columns(3)

# with col1:
#     if st.button("🏠 Home", use_container_width=True):
#         st.switch_page("app.py")

# with col2:
#     if st.button("🔍 Change Mood", use_container_width=True):
#         st.switch_page("pages/2_detect_mood.py")

# with col3:
#     if st.button("💬 Chat with AI", use_container_width=True, key="chat_button_footer"):
#         st.switch_page("pages/3_chat.py")

# # Footer info
# st.markdown("""
#     <div style='text-align: center; margin-top: 2rem; padding: 1rem; color: rgba(255,255,255,0.6);'>
#         <p>🎵 Enjoying the music? Your mood shapes your playlist!</p>
#         <p style='font-size: 0.9rem;'>All music sourced from YouTube | Session-based recommendations</p>
#     </div>
# """, unsafe_allow_html=True)

import sys
import os
import streamlit as st
from pathlib import Path
import tomllib

# Ensure modules path is correct
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from modules.music_service import search_songs, get_mood_keywords
from modules.themes import apply_mood_theme

# Load API key from secret.toml (optional)
secret_path = Path(__file__).parent.parent / "secret.toml"
if secret_path.exists():
    with open(secret_path, "rb") as f:
        secrets = tomllib.load(f)
        YOUTUBE_API_KEY = secrets.get("YOUTUBE_API_KEY", "")
else:
    YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY", "YOUR_FALLBACK_KEY")

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
if "music_videos" not in st.session_state:
    mood_keywords = get_mood_keywords(st.session_state.mood)
    search_query = " ".join(mood_keywords[:2])  # combine top 2 mood keywords
    st.session_state.music_videos = search_songs(search_query, YOUTUBE_API_KEY)
    st.session_state.current_video_index = 0

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
            We've curated live YouTube music to match your {st.session_state.mood} mood
        </p>
    </div>
""", unsafe_allow_html=True)

st.info("🔊 **Click PLAY on the video to start the music!** (YouTube autoplay is disabled)")

# Main player
videos = st.session_state.music_videos
if not videos:
    st.error("No music found. Try again or check your API key.")
    st.stop()

current_index = st.session_state.current_video_index
current_video = videos[current_index]

col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("### 🎧 Now Playing")
    st.video(current_video["url"])
    st.markdown(f"**{current_video['title']}**")

with col2:
    st.markdown("### 🎮 Controls")
    col_prev, col_next = st.columns(2)

    with col_prev:
        if st.button("⏮️ Previous", use_container_width=True, disabled=(current_index == 0)):
            st.session_state.current_video_index -= 1
            st.rerun()

    with col_next:
        if st.button("Next ⏭️", use_container_width=True, disabled=(current_index >= len(videos) - 1)):
            st.session_state.current_video_index += 1
            st.rerun()

    st.markdown(f"<p style='text-align:center;'>Track {current_index + 1} of {len(videos)}</p>", unsafe_allow_html=True)

    st.markdown("### ⚡ Quick Actions")
    if st.button("🔄 Redetect Mood", use_container_width=True):
        st.switch_page("pages/2_detect_mood.py")
    if st.button("💬 Chat with AI", use_container_width=True,  key="chat_button_footer"):
        st.switch_page("pages/3_chat.py")
    if st.button("🔀 Refresh Music", use_container_width=True):
        mood_keywords = get_mood_keywords(st.session_state.mood)
        query = " ".join(mood_keywords[:2])
        st.session_state.music_videos = search_songs(query, YOUTUBE_API_KEY)
        st.session_state.current_video_index = 0
        st.rerun()

# Playlist section
st.divider()
st.markdown("### 📻 Full Playlist")

cols = st.columns(3)
for i, video in enumerate(videos):
    with cols[i % 3]:
        border = "3px solid #ff6b9d" if i == current_index else "1px solid rgba(255,255,255,0.2)"
        st.markdown(f"""
            <div style='border:{border}; border-radius:10px; padding:0.5rem; margin-bottom:1rem;'>
                <p style='color:white; font-weight:bold;'>{i+1}. {video['title']}</p>
            </div>
        """, unsafe_allow_html=True)
        if st.button(f"▶️ Play", key=f"play_{i}", use_container_width=True, disabled=(i == current_index)):
            st.session_state.current_video_index = i
            st.rerun()

# Mood keywords info
with st.expander("🎯 How We Choose Your Music"):
    st.write(f"For your **{st.session_state.mood}** mood, we searched using:")
    for keyword in get_mood_keywords(st.session_state.mood):
        st.write(f"- {keyword}")

# Footer
st.divider()
col1, col2, col3 = st.columns(3)
with col1:
    if st.button("🏠 Home", use_container_width=True):
        st.switch_page("app.py")
with col2:
    if st.button("🔍 Change Mood", use_container_width=True):
        st.switch_page("pages/2_detect_mood.py")
with col3:
    if st.button("💬 Chat with AI", use_container_width=True, key="chat_button_quick"):
        st.switch_page("pages/3_chat.py")

st.markdown("""
    <div style='text-align:center; margin-top:2rem; color:rgba(255,255,255,0.6);'>
        <p>🎵 Enjoying your {mood_emoji.get(st.session_state.mood, '🎵')} vibes? Your mood shapes your playlist!</p>
        <p style='font-size:0.9rem;'>Powered by YouTube Data API | Vibefy 🎧</p>
    </div>
""", unsafe_allow_html=True)
