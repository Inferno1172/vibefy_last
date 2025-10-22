import time
import requests
import logging
import os
import random
from openai import OpenAI, OpenAIError
from dotenv import load_dotenv
import streamlit as st

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("vibefy_debug.log"),
        logging.StreamHandler(),
    ],
)

# Initialize OpenAI client with error handling
try:
    client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
    if not client.api_key:
        raise ValueError("OpenAI API key not found")
except Exception as e:
    logging.error(f"Failed to initialize OpenAI client: {e}")
    client = None

ASSISTANT_ID = "asst_sFurPi1mR8QuB92lOmjzpJKr"

def get_or_create_thread(session_state):
    """Ensures we have one persistent thread per user session."""
    try:
        if client is None:
            raise Exception("OpenAI client not initialized. Check your API key.")

        # Create new thread if not exists or invalid
        if "thread_id" not in session_state or not session_state.thread_id:
            logging.info("Creating a new thread for session.")
            thread = client.beta.threads.create()

            if not thread or not getattr(thread, "id", None):
                raise Exception("Thread creation failed — no thread ID returned.")

            session_state.thread_id = thread.id
            logging.info(f"New thread created: {thread.id}")
        else:
            logging.debug(f"Using existing thread: {session_state.thread_id}")

        return session_state.thread_id

    except Exception as e:
        logging.exception("Error creating or retrieving thread.")
        # Return a clear failure message instead of None
        raise RuntimeError(f"Failed to initialize chat thread: {e}")


def send_message(user_message, thread_id):
    """Sends a user message and gets the assistant's reply."""
    try:
        if client is None:
            return "⚠️ AI service is currently unavailable. Please check your API configuration."
            
        logging.info(f"Sending message to assistant (thread: {thread_id})")
        
        # Add user message to thread
        client.beta.threads.messages.create(
            thread_id=thread_id,
            role="user",
            content=user_message,
        )

        # Create a run
        run = client.beta.threads.runs.create(
            thread_id=thread_id,
            assistant_id=ASSISTANT_ID,
        )
        logging.info(f"Run created: {run.id}")

        # Wait for completion with timeout
        start_time = time.time()
        timeout = 30  # 30 seconds timeout
        
        while time.time() - start_time < timeout:
            run_status = client.beta.threads.runs.retrieve(
                thread_id=thread_id,
                run_id=run.id
            )
            
            if run_status.status == "completed":
                # Get the messages
                messages = client.beta.threads.messages.list(thread_id=thread_id)
                
                # Find the latest assistant message
                for message in messages.data:
                    if message.role == "assistant":
                        if hasattr(message, 'content') and message.content:
                            reply = ""
                            for content in message.content:
                                if hasattr(content, 'text') and hasattr(content.text, 'value'):
                                    reply += content.text.value
                            if reply:
                                logging.info("Successfully received assistant reply")
                                return reply
                
                return "⚠️ No response received from assistant."
                
            elif run_status.status in ["failed", "cancelled", "expired"]:
                error_msg = f"Run failed with status: {run_status.status}"
                if hasattr(run_status, 'last_error') and run_status.last_error:
                    error_msg += f" - {run_status.last_error}"
                logging.error(error_msg)
                return f"⚠️ Sorry, I encountered an error: {error_msg}"
            
            time.sleep(1)  # Wait before checking again
        
        return "⚠️ Request timed out. Please try again."
        
    except OpenAIError as e:
        logging.exception("OpenAI API error occurred.")
        return f"⚠️ AI service error: {str(e)}"
    except Exception as e:
        logging.exception("Unexpected error occurred.")
        return f"⚠️ Unexpected error: {str(e)}"

# Fallback responses if OpenAI fails
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
    responses = FALLBACK_RESPONSES.get(mood, ["I'm here to listen. How can I support you today?"])
    return random.choice(responses)