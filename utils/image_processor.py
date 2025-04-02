import base64
import cv2
import numpy as np
import logging

logger = logging.getLogger(__name__)

def process_image(base64_image):
    """
    Process the base64 encoded image using OpenCV
    
    Args:
        base64_image (str): Base64 encoded image data
        
    Returns:
        numpy.ndarray: Processed image
    """
    try:
        # Decode base64 image
        img_data = base64.b64decode(base64_image)
        nparr = np.frombuffer(img_data, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        
        if img is None:
            logger.error("Failed to decode image")
            return None
        
        # Resize the image to a standard size
        img = cv2.resize(img, (640, 480))
        
        # Convert to grayscale
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
        # Apply some noise reduction
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        
        # Apply histogram equalization to improve contrast
        equalized = cv2.equalizeHist(blurred)
        
        # Apply edge detection
        edges = cv2.Canny(equalized, 50, 150)
        
        # This would normally be more sophisticated
        # For now, we'll return the processed image
        return {
            'original': img,
            'gray': gray,
            'edges': edges
        }
    except Exception as e:
        logger.error(f"Error processing image: {e}")
        return None
