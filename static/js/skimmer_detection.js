/**
 * Send the captured image to the backend for analysis
 * @param {string} imageData - Base64 encoded image data
 */
function analyzeImage(imageData) {
    // Show loading spinner
    const loadingSpinner = document.getElementById('loading-spinner');
    loadingSpinner.style.display = 'block';
    
    // Prepare the request data
    const requestData = {
        image_data: imageData
    };
    
    // Send the image to the backend for analysis
    fetch('/api/analyze_image', {
        method: 'POST',
        body: JSON.stringify(requestData),
        headers: {
            'Content-Type': 'application/json'
        }
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(result => {
        loadingSpinner.style.display = 'none';
        displayResults(result);
    })
    .catch(error => {
        console.error('Error analyzing image:', error);
        loadingSpinner.style.display = 'none';
        displayError(error.message);
    });
}

/**
 * Display the analysis results in the UI
 * @param {Object} result - The analysis results from the backend
 */
function displayResults(result) {
    const analysisSection = document.getElementById('analysis-section');
    const resultTitle = document.getElementById('result-title');
    const resultMessage = document.getElementById('result-message');
    const probabilityBar = document.getElementById('probability-bar');
    const resultImage = document.getElementById('result-image');
    const resultCard = document.getElementById('result-card');
    
    // Show the analysis section
    analysisSection.style.display = 'block';
    
    if (result.success) {
        // Set the result title based on detection
        if (result.is_suspicious) {
            resultTitle.textContent = '⚠️ Potential Skimmer Detected';
            resultTitle.className = 'mb-0 text-danger';
            resultCard.className = 'card mb-3 border-danger';
        } else {
            resultTitle.textContent = '✅ No Skimmer Detected';
            resultTitle.className = 'mb-0 text-success';
            resultCard.className = 'card mb-3 border-success';
        }
        
        // Set the result message
        resultMessage.innerHTML = `<div class="alert ${result.is_suspicious ? 'alert-danger' : 'alert-success'}">${result.message}</div>`;
        
        // Update the probability bar
        const probability = result.probability;
        probabilityBar.style.width = `${probability}%`;
        probabilityBar.textContent = `${probability}%`;
        
        // Set the bar color based on probability
        if (probability > 70) {
            probabilityBar.className = 'progress-bar bg-danger';
        } else if (probability > 30) {
            probabilityBar.className = 'progress-bar bg-warning';
        } else {
            probabilityBar.className = 'progress-bar bg-success';
        }
        
        // Set the result image
        if (result.visualization) {
            resultImage.src = 'data:image/jpeg;base64,' + result.visualization;
        } else {
            resultImage.src = '';
        }
    } else {
        displayError(result.error || 'An unknown error occurred during analysis');
    }
}

/**
 * Display an error message in the UI
 * @param {string} message - The error message to display
 */
function displayError(message) {
    const analysisSection = document.getElementById('analysis-section');
    const resultTitle = document.getElementById('result-title');
    const resultMessage = document.getElementById('result-message');
    const resultCard = document.getElementById('result-card');
    
    // Show the analysis section
    analysisSection.style.display = 'block';
    
    // Set error details
    resultTitle.textContent = 'Analysis Error';
    resultTitle.className = 'mb-0 text-warning';
    resultCard.className = 'card mb-3 border-warning';
    
    resultMessage.innerHTML = `
        <div class="alert alert-warning">
            <h5><i class="fas fa-exclamation-triangle"></i> Unable to analyze image</h5>
            <p>${message}</p>
            <p>Please try again with a clearer image of the card reader.</p>
        </div>
    `;
    
    // Hide the probability bar and result image sections
    document.getElementById('probability-bar').style.width = '0%';
    document.getElementById('result-image').src = '';
}
