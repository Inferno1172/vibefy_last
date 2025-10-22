import os
import cv2
import requests
from fer import FER
from dotenv import load_dotenv
import logging
import sys
import numpy as np
from datetime import datetime

# Set up logging with more detailed configuration
log_formatter = logging.Formatter('%(asctime)s UTC - %(levelname)s - %(message)s')
log_file = 'vibefy_debug.log'
file_handler = logging.FileHandler(log_file, mode='a', encoding='utf-8')
file_handler.setFormatter(log_formatter)
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setFormatter(log_formatter)

logger = logging.getLogger('vibefy')
logger.setLevel(logging.DEBUG)  # Set to DEBUG for more detailed logs
logger.addHandler(file_handler)
logger.addHandler(console_handler)

# Suppress TensorFlow warnings
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'

# Log startup information
logger.info(f"Emotion detector module initialized by user: {os.getenv('USERNAME', 'unknown')}")
logger.info(f"Current UTC time: {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')}")

load_dotenv()

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
        logger.debug("Received None emotion, returning 'neutral'")
        return 'neutral'
    emotion = emotion.lower()
    normalized = EMOTION_MAPPING.get(emotion, emotion)
    logger.debug(f"Normalized emotion: {emotion} -> {normalized}")
    return normalized

def detect_from_face(image_path):
    """
    Takes an image path, detects face, predicts emotion using FER.
    Returns: {"mood": "joy", "confidence": 0.85}
    """
    try:
        logger.info(f"Starting face detection for image: {image_path}")
        
        # Read image and verify it's valid
        img = cv2.imread(image_path)
        if img is None:
            logger.error(f"Could not read image from {image_path}")
            return {"mood": "neutral", "confidence": 0.0}

        # Verify image dimensions and content
        if img.size == 0 or len(img.shape) != 3:
            logger.error(f"Invalid image format or dimensions: {img.shape if img is not None else 'None'}")
            return {"mood": "neutral", "confidence": 0.0}

        # Log image properties
        logger.debug(f"Image shape: {img.shape}, dtype: {img.dtype}")

        # Convert to RGB for FER
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        # Initialize detector with MTCNN
        logger.debug("Initializing FER detector with MTCNN")
        detector = FER(mtcnn=True)
        
        # Detect faces and emotions
        logger.debug("Starting face detection")
        faces = detector.detect_emotions(img)
        logger.info(f"Detected {len(faces)} face(s)")

        if not faces:
            logger.warning("No faces detected in the image")
            return {"mood": "neutral", "confidence": 0.0}

        # Get emotions for the largest face
        largest_face = max(faces, key=lambda x: x['box'][2] * x['box'][3])
        emotions = largest_face['emotions']
        logger.debug(f"Detected emotions: {emotions}")
        
        # Find the dominant emotion
        dominant_emotion = max(emotions.items(), key=lambda x: x[1])
        emotion_label, confidence = dominant_emotion

        # Validate confidence
        if confidence < 0.1:  # Minimum confidence threshold
            logger.warning(f"Low confidence ({confidence}) for emotion: {emotion_label}")
            return {"mood": "neutral", "confidence": 0.0}

        logger.info(f"Dominant emotion: {emotion_label} with confidence: {confidence:.2f}")

        # Normalize emotion label
        normalized_emotion = normalize_emotion(emotion_label)
        
        result = {"mood": normalized_emotion, "confidence": float(confidence)}
        logger.info(f"Final result: {result}")
        return result
    
    except Exception as e:
        logger.exception(f"Error in detect_from_face: {str(e)}")
        return {"mood": "neutral", "confidence": 0.0}

def analyze_text(text):
    """
    Takes user's text, sends to HuggingFace API
    Returns: {"mood": "fear", "confidence": 0.78}
    """
    try:
        logger.info(f"Starting text analysis for input: {text[:50]}...")  # Log first 50 chars
        
        HF_TOKEN = os.getenv("HF_TOKEN")
        if not HF_TOKEN:
            logger.error("HF_TOKEN not found in environment variables")
            return {"mood": "neutral", "confidence": 0.0}
        
        if not text or not isinstance(text, str) or text.strip() == "":
            logger.error("Invalid or empty text input")
            return {"mood": "neutral", "confidence": 0.0}
        
        API_URL = "https://api-inference.huggingface.co/models/j-hartmann/emotion-english-distilroberta-base"
        headers = {"Authorization": f"Bearer {HF_TOKEN}"}
        
        logger.debug("Sending request to HuggingFace API")
        response = requests.post(
            API_URL, 
            headers=headers, 
            json={"inputs": text.strip()}, 
            timeout=10
        )
        
        if response.status_code != 200:
            logger.error(f"HuggingFace API error: {response.status_code} - {response.text}")
            return {"mood": "neutral", "confidence": 0.0}
        
        result = response.json()
        logger.debug(f"API Response: {result}")
        
        if isinstance(result, list) and len(result) > 0:
            # Result is already sorted by score
            top = result[0][0] if isinstance(result[0], list) else result[0]
            
            emotion = top.get('label', 'neutral')
            score = top.get('score', 0.0)
            
            # Validate score
            if score < 0.1:  # Minimum confidence threshold
                logger.warning(f"Low confidence in text analysis: {score}")
                return {"mood": "neutral", "confidence": 0.0}
            
            # Normalize emotion label
            normalized_emotion = normalize_emotion(emotion)
            
            final_result = {"mood": normalized_emotion, "confidence": float(score)}
            logger.info(f"Text analysis result: {final_result}")
            return final_result
        
        logger.warning(f"Unexpected API response format: {result}")
        return {"mood": "neutral", "confidence": 0.0}
    
    except requests.exceptions.Timeout:
        logger.error("HuggingFace API request timed out")
        return {"mood": "neutral", "confidence": 0.0}
    except requests.exceptions.RequestException as e:
        logger.error(f"HuggingFace API request error: {str(e)}")
        return {"mood": "neutral", "confidence": 0.0}
    except Exception as e:
        logger.exception(f"Error in text analysis: {str(e)}")
        return {"mood": "neutral", "confidence": 0.0}

def get_emotion_description(mood):
    """Get a friendly description for each emotion"""
    descriptions = {
        "joy": "You're feeling happy and positive! 😊 Let's keep these good vibes going!",
        "sadness": "You're experiencing sadness. It's okay to feel this way, and remember that this too shall pass. 💙",
        "anger": "You're feeling angry or frustrated. Let's take a deep breath and work through this together. 😤",
        "fear": "You're feeling anxious or worried. Remember, you're not alone, and it's okay to take things one step at a time. 😰",
        "disgust": "You're feeling uncomfortable or displeased. Let's focus on what we can change or improve. 😣",
        "surprise": "You're feeling surprised or astonished! Sometimes the unexpected can lead to amazing discoveries! 😲",
        "neutral": "You're feeling calm and balanced. This is a great state for reflection and mindfulness. 😐"
    }
    
    description = descriptions.get(mood, "You're experiencing emotions, and that's perfectly normal.")
    logger.debug(f"Retrieved description for mood '{mood}': {description[:30]}...")
    return description

# Test function
if __name__ == "__main__":
    logger.info("Starting emotion detector module test")
    
    print("Testing emotion detector module...")
    
    # Test text analysis
    test_texts = [
        "I'm so happy today!",
        "I feel really sad and alone",
        "This makes me so angry!",
        "I'm worried about tomorrow",
        "Just feeling normal",
        ""  # Test empty input
    ]
    
    print("\nTesting text analysis:")
    for text in test_texts:
        result = analyze_text(text)
        print(f"Text: '{text}' -> Mood: {result['mood']} (Confidence: {result['confidence']:.2f})")

    logger.info("Emotion detector module test completed")