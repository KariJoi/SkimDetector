import cv2
import numpy as np
import logging
import base64

logger = logging.getLogger(__name__)

def detect_skimmer(processed_images):
    """
    Detect potential skimming devices in the processed images
    
    Args:
        processed_images (dict): Dictionary containing processed images
        
    Returns:
        dict: Detection results
    """
    if processed_images is None:
        return {
            'success': False,
            'error': 'Could not process image'
        }
    
    try:
        # Extract processed images
        original = processed_images.get('original')
        edges = processed_images.get('edges')
        
        # In a real application, this would involve more sophisticated
        # techniques like feature matching, machine learning, etc.
        # For this demo, we'll use a simple approach
        
        # Count the number of edge pixels as a simple metric
        edge_count = np.count_nonzero(edges)
        
        # The threshold would typically be determined through training and testing
        # This is just a placeholder value for demonstration
        threshold = 10000
        
        # Analyze the edges for irregular patterns
        # More edge pixels might indicate additional attached hardware
        is_suspicious = edge_count > threshold
        
        # Generate a probability (this would normally be from a model)
        # Just for demonstration purposes
        if is_suspicious:
            probability = min(0.6 + (edge_count - threshold) / 50000, 0.95)
        else:
            probability = max(0.1, edge_count / threshold * 0.5)
        
        # Create a visualization
        visualization = original.copy()
        
        # Highlight regions of interest
        # This would normally be based on actual detection results
        if is_suspicious:
            # Draw rectangles around potential skimming areas
            height, width = original.shape[:2]
            cv2.rectangle(visualization, 
                         (int(width * 0.2), int(height * 0.4)), 
                         (int(width * 0.8), int(height * 0.6)), 
                         (0, 0, 255), 2)
        
        # Convert the visualization for return
        _, buffer = cv2.imencode('.jpg', visualization)
        visualization_b64 = base64.b64encode(buffer).decode('utf-8')
        
        return {
            'success': True,
            'is_suspicious': is_suspicious,
            'probability': round(probability * 100, 2),
            'visualization': visualization_b64,
            'message': _get_result_message(is_suspicious, probability)
        }
    except Exception as e:
        logger.error(f"Error detecting skimmer: {e}")
        return {
            'success': False,
            'error': str(e)
        }

def _get_result_message(is_suspicious, probability):
    """Generate an appropriate message based on detection results"""
    if is_suspicious:
        if probability > 0.8:
            return "High probability of a skimming device detected! Exercise caution and report this to the establishment and local authorities."
        elif probability > 0.6:
            return "Possible skimming device detected. Inspect the card reader carefully before use and consider reporting it."
        else:
            return "Some suspicious features detected. Examine the card reader for any unusual attachments."
    else:
        if probability < 0.2:
            return "No suspicious features detected. The card reader appears normal."
        else:
            return "Low probability of a skimming device. The card reader likely does not have a skimmer, but always stay vigilant."
