# 🎵 Vibefy 2.0 - Your AI-Powered Emotional Companion

![Vibefy Banner](https://img.shields.io/badge/Vibefy-2.0-FF6B9D?style=for-the-badge)
![Python](https://img.shields.io/badge/Python-3.8+-blue?style=for-the-badge&logo=python)
![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red?style=for-the-badge&logo=streamlit)

Vibefy 2.0 is a real-time emotional wellness companion that detects your mood through multiple methods and provides instant AI-powered support and personalized music recommendations.

## ✨ Features

- **🎭 Multi-Modal Mood Detection**
  - 📷 Camera-based facial emotion recognition
  - ✍️ Text sentiment analysis
  - 🎯 Manual mood selection

- **💬 AI Emotional Companion**
  - Real-time chat with mood-aware AI
  - Personalized emotional support
  - Context-aware conversations

- **🎵 Personalized Music Recommendations**
  - Mood-matched song playlists
  - YouTube integration
  - Interactive music player

- **🎨 Dynamic Mood-Responsive UI**
  - Psychology-based color themes
  - Smooth animations
  - Adaptive user experience

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- Webcam (for camera-based mood detection)
- API Keys:
  - OpenAI API key (for AI chat)
  - HuggingFace token (for text analysis)
  - YouTube API key (optional, for enhanced music search)

### Installation

1. **Clone the repository**
```bash
git clone <your-repo-url>
cd vibefy_2.0
```

2. **Create virtual environment**
```bash
python -m venv .venv

# Activate on Windows
.venv\Scripts\activate

# Activate on Mac/Linux
source .venv/bin/activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Set up environment variables**

Create a `.env` file in the root directory:
```env
OPENAI_API_KEY=your_openai_api_key_here
HF_TOKEN=your_huggingface_token_here
YOUTUBE_API_KEY=your_youtube_api_key_here
```

**IMPORTANT SECURITY NOTE:** Never commit `.env` file to Git!

5. **Configure Streamlit secrets** (alternative to .env)

Create `.streamlit/secrets.toml`:
```toml
OPENAI_API_KEY = "your_openai_api_key_here"
HF_TOKEN = "your_huggingface_token_here"
YOUTUBE_API_KEY = "your_youtube_api_key_here"
```

### Running the App

```bash
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`

## 📁 Project Structure

```
vibefy_2.0/
│
├── app.py                          # Main entry point
│
├── pages/                          # Streamlit multi-page app
│   ├── 2_detect_mood.py           # Mood detection page
│   ├── 3_chat.py                  # AI companion chat
│   └── 4_music.py                 # Music player
│
├── modules/                        # Core functionality
│   ├── __init__.py
│   ├── emotion_detector.py        # Mood detection logic
│   ├── ai_companion.py            # AI chat system
│   ├── music_service.py           # Music recommendations
│   └── themes.py                  # UI theming system
│
├── .streamlit/                     # Configuration
│   ├── config.toml                # App settings
│   └── secrets.toml               # API keys (DO NOT COMMIT!)
│
├── .env                            # Environment variables (DO NOT COMMIT!)
├── requirements.txt                # Python dependencies
├── README.md                       # This file
└── .gitignore                      # Git ignore rules
```

## 🎯 User Flow

1. **Home Page** → Welcome and feature overview
2. **Detect Mood** → Choose detection method (Camera/Text/Manual)
3. **Mood Confirmed** → See your detected emotion with themed UI
4. **Choose Action:**
   - 💬 Chat with AI for emotional support
   - 🎵 Listen to mood-matched music
   - 🔄 Detect new mood

## 🔧 Configuration

### Streamlit Config (`.streamlit/config.toml`)

```toml
[server]
headless = true
address = "0.0.0.0"
port = 8501

[browser]
serverAddress = "localhost"
gatherUsageStats = false

[theme]
primaryColor = "#FF4B4B"
backgroundColor = "#0E1117"
secondaryBackgroundColor = "#262730"
textColor = "#FAFAFA"
font = "sans serif"

[client]
showSidebarNavigation = false
```

## 🎨 Emotion Mapping

The app recognizes these emotions:

| Emotion | Color Theme | Use Case |
|---------|------------|----------|
| 😊 Joy | Pink-Orange | Amplify happiness |
| 😢 Sadness | Blue-Purple | Provide comfort |
| 😡 Anger | Red-Crimson | Ground and calm |
| 😨 Fear | Purple-Indigo | Reassure and protect |
| 😣 Disgust | Orange-Coral | Cleanse and refresh |
| 😲 Surprise | Teal-Cyan | Celebrate wonder |
| 😐 Neutral | Blue-Gray | Maintain balance |

## 🔐 Security Best Practices

1. **Never commit API keys** to version control
2. Use `.gitignore` to exclude:
   - `.env`
   - `.streamlit/secrets.toml`
   - `__pycache__/`
   - `.venv/`

3. **Rotate API keys** if accidentally exposed
4. Use environment variables for production deployment

## 🧪 Testing

### Test Individual Modules

```bash
# Test emotion detector
python modules/emotion_detector.py

# Test music service
python modules/music_service.py

# Test themes
python modules/test_themes.py
```

### Test Pages Directly

```bash
# Test mood detection
streamlit run pages/2_detect_mood.py

# Test music player
streamlit run pages/4_music.py
```

## 🐛 Troubleshooting

### Camera Not Working
- Check browser permissions for webcam access
- Ensure no other app is using the camera
- Try refreshing the page

### API Errors
- Verify API keys are correct in `.env` or `secrets.toml`
- Check API quota/limits
- Ensure internet connection is stable

### Import Errors
- Activate virtual environment
- Reinstall requirements: `pip install -r requirements.txt`
- Check Python version (3.8+ required)

### Theme Not Applying
- Clear browser cache
- Check if `modules/themes.py` is properly imported
- Verify session state is initialized

## 📝 Development Notes

### Adding New Emotions

1. Update `EMOTION_MAPPING` in `emotion_detector.py`
2. Add theme config in `MOOD_CONFIG` in `themes.py`
3. Add songs in `emotion_songs` dict in `music_service.py`
4. Update mood greetings in `3_chat.py`

### Customizing Music

Edit the `emotion_songs` dictionary in `modules/music_service.py`:

```python
"your_emotion": [
    {
        "video_id": "YouTube_ID",
        "title": "Song Title",
        "thumbnail": "https://img.youtube.com/vi/YouTube_ID/hqdefault.jpg",
        "description": "Description"
    },
    # Add more songs...
]
```

## 🤝 Contributing

This is a student project for Singapore Polytechnic AI Club. Team members:

- **Person 1:** Emotion Detection System
- **Person 2:** AI Companion Integration  
- **Person 3:** Music Service Implementation
- **Person 4:** UI/UX and Integration

## 📄 License

This project is for educational purposes. Music content is sourced from YouTube and subject to their terms of service.

## 🙏 Acknowledgments

- **FER Library** for facial emotion recognition
- **HuggingFace** for text sentiment analysis
- **OpenAI** for AI chat capabilities
- **Streamlit** for the web framework
- **YouTube** for music content

## 📧 Support

For issues or questions, please contact the development team or create an issue in the repository.

---

Built with ❤️ by Singapore Polytechnic AI Club | Vibefy 2.0