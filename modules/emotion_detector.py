import os
import cv2
import requests
from fer import FER
from dotenv import load_dotenv
import logging

load_dotenv()
logging.basicConfig(level=logging.INFO)

# Emotion label mapping for consistency across all detection methods
EMOTION_MAPPING = {
    'happy': 'joy',
    'sad': 'sadness',
    'angry': 'anger',
    'fear': 'fear',
    'disgust': 'disgust',
    'surprise': 'surprise',
    'neutral': 'neutral'
}

def normalize_emotion(emotion):
    """Normalize emotion labels to match our app's emotion set"""
    if emotion is None:
        return 'neutral'
    emotion = emotion.lower()
    return EMOTION_MAPPING.get(emotion, emotion)

def detect_from_face(image_path):
    """
    Takes an image path, detects face, predicts emotion using FER.
    Returns: {"mood": "joy", "confidence": 0.85}
    """
    try:
        img = cv2.imread(image_path)
        if img is None:
            logging.error(f"Could not read image from {image_path}")
            return {"mood": "neutral", "confidence": 0.0}

        # Convert to RGB for FER
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        detector = FER(mtcnn=True)
        faces = detector.detect_emotions(img)
        logging.info(f"Detected {len(faces)} face(s)")

        if len(faces) == 0:
            logging.warning("No faces detected, returning neutral")
            return {"mood": "neutral", "confidence": 0.0}

        # Get top emotion
        dominant_emotion, score = detector.top_emotion(img)
        logging.info(f"FER output: {dominant_emotion} with score {score}")

        if dominant_emotion is None or score is None:
            return {"mood": "neutral", "confidence": 0.0}

        # Normalize emotion label
        normalized_emotion = normalize_emotion(dominant_emotion)
        
        return {"mood": normalized_emotion, "confidence": float(score)}
    
    except Exception as e:
        logging.error(f"Error in detect_from_face: {e}")
        return {"mood": "neutral", "confidence": 0.0}


def analyze_text(text):
    """
    Takes user's text, sends to HuggingFace API
    Returns: {"mood": "fear", "confidence": 0.78}
    """
    HF_TOKEN = os.getenv("HF_TOKEN")
    
    if not HF_TOKEN:
        logging.error("HF_TOKEN not found in environment variables")
        return {"mood": "neutral", "confidence": 0.0}
    
    API_URL = "https://api-inference.huggingface.co/models/j-hartmann/emotion-english-distilroberta-base"
    headers = {"Authorization": f"Bearer {HF_TOKEN}"}
    
    payload = {"inputs": text}
    
    try:
        response = requests.post(API_URL, headers=headers, json=payload, timeout=10)
        
        if response.status_code != 200:
            logging.error(f"HuggingFace API error: {response.status_code}")
            return {"mood": "neutral", "confidence": 0.0}
        
        result = response.json()
        
        # Handle HuggingFace response format
        if isinstance(result, list) and len(result) > 0:
            # Result is already sorted by score
            top = result[0][0] if isinstance(result[0], list) else result[0]
            
            emotion = top.get('label', 'neutral')
            score = top.get('score', 0.0)
            
            # Normalize emotion label
            normalized_emotion = normalize_emotion(emotion)
            
            logging.info(f"Text analysis: {normalized_emotion} with score {score}")
            return {"mood": normalized_emotion, "confidence": float(score)}
        
        logging.warning("Unexpected API response format")
        return {"mood": "neutral", "confidence": 0.0}
    
    except requests.exceptions.Timeout:
        logging.error("HuggingFace API request timed out")
        return {"mood": "neutral", "confidence": 0.0}
    except Exception as e:
        logging.error(f"Error calling HuggingFace API: {e}")
        return {"mood": "neutral", "confidence": 0.0}


def get_emotion_description(mood):
    """Get a friendly description for each emotion"""
    descriptions = {
        "joy": "You're feeling happy and positive! 😊",
        "sadness": "You're experiencing sadness. It's okay to feel this way. 💙",
        "anger": "You're feeling angry or frustrated. Let's work through this. 😤",
        "fear": "You're feeling anxious or worried. You're not alone. 😰",
        "disgust": "You're feeling uncomfortable or displeased. 😣",
        "surprise": "You're feeling surprised or astonished! 😲",
        "neutral": "You're feeling calm and balanced. 😐"
    }
    return descriptions.get(mood, "You're experiencing emotions.")


# Test function
if __name__ == "__main__":
    print("Testing emotion detector module...")
    
    # Test text analysis
    test_texts = [
        "I'm so happy today!",
        "I feel really sad and alone",
        "This makes me so angry!",
        "I'm worried about tomorrow"
    ]
    
    for text in test_texts:
        result = analyze_text(text)
        print(f"Text: '{text}' -> Mood: {result['mood']} (Confidence: {result['confidence']:.2f})")