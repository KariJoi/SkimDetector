// Variables for camera functionality
let videoElement = null;
let canvasElement = null;
let captureButton = null;
let retryButton = null;
let captureOverlay = null;
let mediaStream = null;
let imageData = null;

// Initialize camera components
document.addEventListener('DOMContentLoaded', function() {
    // Get DOM elements
    videoElement = document.getElementById('video');
    canvasElement = document.getElementById('canvas');
    captureButton = document.getElementById('capture-btn');
    retryButton = document.getElementById('retry-btn');
    captureOverlay = document.getElementById('capture-overlay');
    
    // Initialize camera
    initCamera();
    
    // Set up event listeners
    captureButton.addEventListener('click', captureImage);
    retryButton.addEventListener('click', resetCamera);
});

/**
 * Initialize the camera stream
 */
async function initCamera() {
    try {
        // Request access to the user's camera
        const constraints = {
            video: {
                facingMode: 'environment', // Use rear camera on mobile devices
                width: { ideal: 1280 },
                height: { ideal: 720 }
            }
        };
        
        mediaStream = await navigator.mediaDevices.getUserMedia(constraints);
        
        // Set the video source to the camera stream
        videoElement.srcObject = mediaStream;
        
        // Wait for the video to be ready
        videoElement.onloadedmetadata = function() {
            videoElement.play();
        };
        
        console.log('Camera initialized successfully');
    } catch (error) {
        console.error('Error accessing camera:', error);
        alert('Unable to access camera. Please ensure you have granted camera permissions and try again.');
    }
}

/**
 * Capture an image from the video stream
 */
function captureImage() {
    // Show capture animation
    captureOverlay.classList.add('visible');
    
    // Wait a short time to show the animation
    setTimeout(() => {
        // Set canvas dimensions to match video
        canvasElement.width = videoElement.videoWidth;
        canvasElement.height = videoElement.videoHeight;
        
        // Draw the current video frame to the canvas
        const context = canvasElement.getContext('2d');
        context.drawImage(videoElement, 0, 0, canvasElement.width, canvasElement.height);
        
        // Get the image data as a base64 string
        imageData = canvasElement.toDataURL('image/jpeg');
        
        // Hide the capture animation
        captureOverlay.classList.remove('visible');
        
        // Update UI to show the captured state
        captureButton.style.display = 'none';
        retryButton.style.display = 'inline-block';
        
        // Stop the camera stream
        stopCamera();
        
        // Process the image
        analyzeImage(imageData);
    }, 300);
}

/**
 * Stop the camera stream
 */
function stopCamera() {
    if (mediaStream) {
        mediaStream.getTracks().forEach(track => track.stop());
        mediaStream = null;
    }
}

/**
 * Reset the camera to take another photo
 */
function resetCamera() {
    // Hide analysis results
    document.getElementById('analysis-section').style.display = 'none';
    document.getElementById('loading-spinner').style.display = 'none';
    
    // Reset buttons
    retryButton.style.display = 'none';
    captureButton.style.display = 'inline-block';
    
    // Restart camera
    initCamera();
}

/**
 * Clean up resources when the page is closed
 */
window.addEventListener('beforeunload', function() {
    stopCamera();
});
