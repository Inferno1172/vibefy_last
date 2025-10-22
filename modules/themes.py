# modules/themes.py
import streamlit as st
import requests
import json
import time

# Psychology-based mood configuration
MOOD_CONFIG = {
    "joy": {
        "approach": "amplify",
        "gradient": "linear-gradient(135deg, #FF6B9D 0%, #FF8E53 100%)",
        "primary": "#FF6B9D",
        "secondary": "#FF8E53",
        "lottie_url": "https://assets1.lottiefiles.com/packages/lf20_obhph3sh.json",
        "message": "✨ Your happiness is contagious! Let's celebrate this moment!",
        "emoji": "😊",
        "suggestions": [
            "🎵 Listen to upbeat music to keep the good vibes going!",
            "📞 Share this happiness with someone you care about",
            "💃 Do a little happy dance - you deserve it!"
        ]
    },
    "surprise": {
        "approach": "amplify",
        "gradient": "linear-gradient(135deg, #00CDAC 0%, #02AAB0 100%)",
        "primary": "#00CDAC",
        "secondary": "#02AAB0",
        "lottie_url": "https://assets1.lottiefiles.com/packages/lf20_gn0tojcq.json",
        "message": "🎉 Life is full of wonderful surprises!",
        "emoji": "😲",
        "suggestions": [
            "📸 Capture this moment to remember it",
            "🎊 Share the excitement with friends",
            "🌟 Embrace the unexpected joy!"
        ]
    },
    "sadness": {
        "approach": "soothe",
        "gradient": "linear-gradient(135deg, #4A90E2 0%, #7B68EE 100%)",
        "primary": "#4A90E2",
        "secondary": "#7B68EE",
        "lottie_url": "https://assets1.lottiefiles.com/packages/lf20_2cwBvk.json",
        "message": "💙 It's okay to feel this way. You're not alone in this.",
        "emoji": "😢",
        "suggestions": [
            "🫂 Remember it's okay to not be okay sometimes",
            "📓 Journaling can help process these feelings",
            "🌿 A short walk in nature might help clear your mind"
        ]
    },
    "fear": {
        "approach": "calm",
        "gradient": "linear-gradient(135deg, #8E2DE2 0%, #4A00E0 100%)",
        "primary": "#8E2DE2",
        "secondary": "#4A00E0",
        "lottie_url": "https://assets1.lottiefiles.com/packages/lf20_6eVAs1PluP.json",
        "message": "🛡️ You're safe here. Let's work through this together.",
        "emoji": "😨",
        "suggestions": [
            "🛡️ Break big worries into smaller, manageable steps",
            "📝 Write down what you can and cannot control",
            "🌅 Remember that this feeling will pass"
        ]
    },
    "anger": {
        "approach": "ground",
        "gradient": "linear-gradient(135deg, #FF416C 0%, #FF4B2B 100%)",
        "primary": "#FF416C",
        "secondary": "#FF4B2B",
        "lottie_url": "https://assets1.lottiefiles.com/packages/lf20_tll0j2bj.json",
        "message": "🧘 Breathe with me. You have the strength to handle this.",
        "emoji": "😡",
        "suggestions": [
            "💨 Try some deep breathing exercises",
            "🎯 Channel this energy into physical activity",
            "🕰️ Take a moment before responding to situations"
        ]
    },
    "neutral": {
        "approach": "balance",
        "gradient": "linear-gradient(135deg, #7474BF 0%, #348AC7 100%)",
        "primary": "#7474BF",
        "secondary": "#348AC7",
        "lottie_url": "https://assets1.lottiefiles.com/packages/lf20_uqfbgaux.json",
        "message": "🌊 Peace and calm. Enjoy this moment of balance.",
        "emoji": "😐",
        "suggestions": [
            "☕ Take a mindful break to appreciate the present",
            "🎨 Engage in a creative activity",
            "📖 Read something inspiring"
        ]
    }
}

def load_lottie_url(url):
    """Load Lottie animation from URL"""
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            return response.json()
    except:
        pass
    return None

def apply_default_theme():
    """Apply the default black theme for home page"""
    st.markdown("""
        <style>
        .stApp {
            background: #000000 !important;
            color: white;
        }
        
        .main {
            background: #000000 !important;
        }
        
        .stButton button {
            background: linear-gradient(135deg, #FF6B9D 0%, #FF8E53 100%);
            color: white;
            border: none;
            padding: 0.75rem 2rem;
            border-radius: 50px;
            font-size: 1.1rem;
            font-weight: 600;
            transition: all 0.3s ease;
            box-shadow: 0 4px 15px rgba(255, 107, 157, 0.3);
        }
        
        .stButton button:hover {
            transform: translateY(-2px);
            box-shadow: 0 10px 25px rgba(255, 107, 157, 0.4);
        }
        
        /* Ensure all text is visible on black background */
        .stMarkdown, .stText, .stTitle, .stHeader {
            color: white !important;
        }
        
        /* Fix for any white backgrounds in components */
        .stAlert, .stInfo, .stWarning, .stSuccess, .stError {
            background-color: rgba(255, 255, 255, 0.1) !important;
            color: white !important;
        }
        </style>
    """, unsafe_allow_html=True)

def apply_mood_theme(mood):
    """Apply mood theme with black base and gradient overlay"""
    config = MOOD_CONFIG.get(mood, MOOD_CONFIG["neutral"])
    
    css = f"""
    <style>
    .stApp {{
        background: #000000 !important;
        position: relative;
    }}
    
    .stApp::before {{
        content: '';
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: {config['gradient']};
        opacity: 0.3;
        z-index: -1;
        animation: gradientShift 15s ease infinite;
    }}
    
    .mood-header {{
        background: rgba(0, 0, 0, 0.7);
        backdrop-filter: blur(15px);
        border-radius: 25px;
        padding: 2rem;
        margin: 1rem 0;
        border: 2px solid {config['primary']};
        animation: slideUp 1s ease-out;
    }}
    
    .mood-card {{
        background: rgba(0, 0, 0, 0.6);
        border-radius: 20px;
        padding: 1.5rem;
        border-left: 6px solid {config['primary']};
        margin: 1rem 0;
        backdrop-filter: blur(10px);
        animation: fadeIn 1.5s ease-out;
    }}
    
    @keyframes gradientShift {{
        0% {{ background-position: 0% 50%; }}
        50% {{ background-position: 100% 50%; }}
        100% {{ background-position: 0% 50%; }}
    }}
    
    @keyframes slideUp {{
        from {{ opacity: 0; transform: translateY(30px); }}
        to {{ opacity: 1; transform: translateY(0); }}
    }}
    
    @keyframes fadeIn {{
        from {{ opacity: 0; }}
        to {{ opacity: 1; }}
    }}
    
    /* Ensure text visibility */
    .stMarkdown, .stText, .stTitle, .stHeader, .stSubheader {{
        color: white !important;
    }}

    /* Style text input and text area */
    .stTextInput input, .stTextArea textarea {{
        background: rgba(255, 255, 255, 0.1) !important;
        color: white !important;
        border: 1px solid {config['primary']} !important;
        border-radius: 10px;
        padding: 1rem;
        font-size: 1rem;
        transition: all 0.3s ease;
    }}

    .stTextArea textarea:focus {{
        box-shadow: 0 0 0 2px {config['primary']}44 !important;
        border-color: {config['primary']} !important;
    }}

    /* Style selectboxes and radio buttons */
    .stSelectbox select, .stRadio label {{
        color: white !important;
    }}

    /* Style form submit button */
    [data-testid="stForm"] {{
        border-color: {config['primary']}44 !important;
        border-radius: 15px;
        padding: 1.5rem;
        background: rgba(255, 255, 255, 0.05);
    }}

    /* Style manual selection cards */
    [data-testid="stHorizontalBlock"] {{
        gap: 1rem;
    }}

    .stButton button {{
        background: rgba(255, 255, 255, 0.1);
        border: 2px solid {config['primary']}44;
        color: white !important;
        padding: 1.5rem;
        border-radius: 15px;
        transition: all 0.3s ease;
        height: 100%;
        width: 100%;
    }}

    .stButton button:hover {{
        transform: translateY(-2px);
        background: rgba(255, 255, 255, 0.15);
        border-color: {config['primary']};
        box-shadow: 0 4px 15px {config['primary']}33;
    }}

    /* Improve visibility of all text */
    .stText, .stMarkdown {{
        color: rgba(255, 255, 255, 0.9) !important;
    }}

    /* Style info boxes */
    .stAlert {{
        background: rgba(255, 255, 255, 0.1) !important;
        border-color: {config['primary']}44 !important;
        color: white !important;
    }}
    </style>
    """
    return css

    
    st.markdown(css, unsafe_allow_html=True)
    return config

def display_mood_confirmation(mood, confidence):
    """Show beautiful mood confirmation with psychology-appropriate animation"""
    config = MOOD_CONFIG.get(mood, MOOD_CONFIG["neutral"])
    
    # Safely format confidence for display (avoid crash if None or invalid)
    try:
        if isinstance(confidence, (int, float)):
            confidence_text = "{:.0%}".format(confidence)
        else:
            confidence_text = "N/A"
    except Exception:
        confidence_text = "N/A"
    
    # Use a simple container to ensure content displays
    container = st.container()
    
    with container:
        # Show emoji animation instead of Lottie to avoid component issues
        st.markdown(f"""
            <div style="text-align: center; margin-bottom: 2rem;">
                <h1 style="font-size: 8rem; margin: 0; animation: float 3s ease-in-out infinite;">{config['emoji']}</h1>
            </div>
            
            <style>
            @keyframes float {{
                0%, 100% {{ transform: translateY(0px); }}
                50% {{ transform: translateY(-20px); }}
            }}
            </style>
        """, unsafe_allow_html=True)
    
    # Mood confirmation card
    st.markdown(f"""
    <div class="mood-header">
        <div style="text-align: center;">
            <h2 style="color: white; margin: 1rem 0; font-weight: 700; text-shadow: 2px 2px 4px rgba(0,0,0,0.3);">
                {mood.capitalize()} Detected
            </h2>
            <div style="background: rgba(255, 255, 255, 0.25); border-radius: 25px; padding: 0.8rem 2rem; display: inline-block; backdrop-filter: blur(10px);">
                <span style="color: white; font-size: 1.1rem; font-weight: 600;">Confidence: {confidence_text}</span>
            </div>
            <p style="color: rgba(255, 255, 255, 0.95); font-size: 1.3rem; margin-top: 1.5rem; font-weight: 500;">
                {config['message']}
            </p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Show suggestions
    show_mood_suggestions(mood)

def show_mood_suggestions(mood):
    """Show psychology-appropriate suggestions"""
    config = MOOD_CONFIG.get(mood, MOOD_CONFIG["neutral"])
    
    st.markdown("""
    <div class="mood-card">
        <h3 style="color: white; margin-bottom: 1rem;">💡 Suggestions for You</h3>
    """, unsafe_allow_html=True)
    
    for suggestion in config["suggestions"]:
        st.markdown(f"""
        <div style="background: rgba(255,255,255,0.1); padding: 1rem; border-radius: 10px; margin: 0.5rem 0; border-left: 4px solid {config['primary']};">
            <p style="color: white; margin: 0; font-size: 1rem;">{suggestion}</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)

def get_mood_emoji(mood):
    """Get emoji for mood"""
    return MOOD_CONFIG.get(mood, MOOD_CONFIG["neutral"])["emoji"]

def get_mood_color(mood, color_type="primary"):
    """Get color for mood"""
    config = MOOD_CONFIG.get(mood, MOOD_CONFIG["neutral"])
    return config.get(color_type, config["primary"])