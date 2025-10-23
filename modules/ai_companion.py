import time
import requests
import logging
import os
import random
import google.generativeai as genai
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("vibefy_debug.log"),
        logging.StreamHandler(),
    ],
)

# Initialize Gemini client with error handling
try:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    # Test the configuration
    model = genai.GenerativeModel('gemini-2.5-flash')
except Exception as e:
    logging.error(f"Failed to initialize Gemini client: {e}")
    genai = None

# System instructions for mood-based companion
SYSTEM_INSTRUCTIONS = """
You are Vibefy, an empathetic AI companion designed to support users based on their current mood. 
Your role is to provide emotional support, active listening, and helpful responses tailored to the user's emotional state.

Guidelines:
- Always acknowledge the user's current mood in your responses
- Be empathetic, supportive, and non-judgmental
- Offer coping strategies when appropriate
- Suggest mood-appropriate activities or reflections
- Keep responses conversational and natural
- If the mood is negative, focus on validation and support
- If the mood is positive, celebrate and amplify the good feelings
- For neutral moods, offer gentle exploration or mindfulness

Remember: You're here to listen, support, and help users process their emotions.
"""

# Store chat history in session state (no need for threads like OpenAI)
def initialize_chat_session(session_state):
    """Initialize Gemini chat session with system instructions"""
    try:
        if genai is None:
            raise Exception("Gemini client not initialized. Check your API key.")
        
        # Create a new chat model with system instructions
        model = genai.GenerativeModel(
            model_name='gemini-2.5-flash',  # or 'gemini-pro'
            system_instruction=SYSTEM_INSTRUCTIONS
        )
        
        # Start a new chat session
        chat_session = model.start_chat(history=[])
        
        # Store in session state
        session_state.gemini_chat = chat_session
        logging.info("New Gemini chat session initialized")
        
        return chat_session
        
    except Exception as e:
        logging.exception("Error initializing Gemini chat session")
        raise RuntimeError(f"Failed to initialize chat: {e}")

def get_or_create_chat(session_state):
    """Get existing chat session or create new one"""
    if "gemini_chat" not in session_state:
        return initialize_chat_session(session_state)
    return session_state.gemini_chat

def send_message(user_message, session_state):
    """Send message to Gemini and get response"""
    try:
        if genai is None:
            return "⚠️ AI service is currently unavailable. Please check your API configuration."
            
        logging.info("Sending message to Gemini")
        
        # Get or create chat session
        chat_session = get_or_create_chat(session_state)
        
        # Safely add mood context to the message
        mood = getattr(session_state, 'mood', None)
        if mood and user_message:
            mood_context = f"[User's current mood: {mood}] "
            full_message = mood_context + user_message
        else:
            # Use original message if mood is not available
            full_message = user_message if user_message else "Hello"
        
        # Send message to Gemini
        response = chat_session.send_message(full_message)
        
        logging.info("Successfully received Gemini response")
        return response.text
        
    except Exception as e:
        logging.exception("Gemini API error occurred")
        return f"⚠️ AI service error: {str(e)}"

# Fallback responses (keep the same)
FALLBACK_RESPONSES = {
    "joy": [
        "It's wonderful to see you feeling happy! What's bringing you joy today?",
        "Your positive energy is contagious! Tell me more about what's making you smile.",
        "Happiness looks good on you! Want to share what's making your day great?"
    ],
    "sadness": [
        "I'm here for you during this tough time. It's okay to feel sad.",
        "Your feelings are valid. Would you like to talk about what's on your mind?",
        "Sometimes we need to sit with our sadness. I'm here to listen whenever you're ready."
    ],
    "anger": [
        "I sense you're feeling frustrated. It's okay to feel this way.",
        "Anger can be overwhelming. Let's work through this together.",
        "I'm here to help you process these feelings. What's bothering you?"
    ],
    "fear": [
        "I understand you might be feeling anxious. Let's work through this together.",
        "It's okay to feel scared sometimes. What's worrying you?",
        "You're safe here. Let's talk about what's making you feel fearful."
    ],
    "disgust": [
        "I notice you're feeling uncomfortable. Sometimes we need to process difficult feelings.",
        "It's okay to feel disgusted. What's causing these feelings?",
        "Let's work through this discomfort together."
    ],
    "surprise": [
        "You seem surprised! That can be exciting or unsettling.",
        "Surprises can be wonderful or challenging. Tell me more about what happened.",
        "Life is full of unexpected moments. How are you feeling about this surprise?"
    ],
    "neutral": [
        "You're in a calm state. Is there anything you'd like to explore or discuss today?",
        "Peace and balance are wonderful. What's on your mind?",
        "It's nice to have moments of calm. How can I support you today?"
    ]
}

def get_fallback_response(mood):
    """Get a fallback response when AI is unavailable"""
    # Handle case where mood might be None
    if not mood:
        mood = "neutral"
    responses = FALLBACK_RESPONSES.get(mood, ["I'm here to listen. How can I support you today?"])
    return random.choice(responses)