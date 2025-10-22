import cv2
import numpy as np
from emotion_detector import detect_from_face, analyze_text
import logging
import os
from datetime import datetime

# Set up logging
log_formatter = logging.Formatter('%(asctime)s UTC - %(levelname)s - %(message)s')
log_file = 'vibefy_test.log'
file_handler = logging.FileHandler(log_file, mode='a', encoding='utf-8')
file_handler.setFormatter(log_formatter)
file_handler.setLevel(logging.DEBUG)

logger = logging.getLogger('vibefy_test')
logger.setLevel(logging.DEBUG)
logger.addHandler(file_handler)

def test_face_detection():
    logger.info("Starting face detection test")
    
    # Create a test image with a simple shape
    img = np.ones((300, 300, 3), dtype=np.uint8) * 255
    cv2.circle(img, (150, 150), 100, (0, 0, 0), -1)
    
    # Save test image
    test_image_path = 'test_face.jpg'
    cv2.imwrite(test_image_path, img)
    
    try:
        # Test detection
        result = detect_from_face(test_image_path)
        logger.info(f"Face detection test result: {result}")
        print(f"Face detection test result: {result}")
        
        # Cleanup
        if os.path.exists(test_image_path):
            os.remove(test_image_path)
            
    except Exception as e:
        logger.exception("Face detection test failed")
        print(f"Face detection test failed: {str(e)}")

def test_text_analysis():
    logger.info("Starting text analysis test")
    
    test_texts = [
        "I am very happy today!",
        "I feel sad and lonely",
        "This is making me angry",
        "Just a normal day",
        ""  # Test empty input
    ]
    
    for text in test_texts:
        try:
            result = analyze_text(text)
            logger.info(f"Text analysis result for '{text}': {result}")
            print(f"Text: '{text}' -> Result: {result}")
        except Exception as e:
            logger.exception(f"Text analysis failed for '{text}'")
            print(f"Text analysis failed for '{text}': {str(e)}")

if __name__ == "__main__":
    logger.info(f"Starting emotion detector tests at {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')} UTC")
    print("Running emotion detector tests...")
    
    test_face_detection()
    test_text_analysis()
    
    logger.info("Emotion detector tests completed")
    print("Tests completed. Check vibefy_test.log for detailed results.")