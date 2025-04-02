import os
import logging
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, session
import base64
import json
from datetime import datetime
import uuid
from utils.image_processor import process_image
from utils.skimmer_detector import detect_skimmer

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "default-secret-key-for-development")

# In-memory storage for reports
# In a production app, this would be a database
reports = []

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/detection')
def detection():
    return render_template('detection.html')

@app.route('/education')
def education():
    return render_template('education.html')

@app.route('/report')
def report():
    return render_template('report.html')

@app.route('/submit_report', methods=['POST'])
def submit_report():
    try:
        location = request.form.get('location', '')
        description = request.form.get('description', '')
        image_data = request.form.get('image_data', '')
        
        if not image_data:
            flash('Please include an image of the suspected skimmer device', 'danger')
            return redirect(url_for('report'))
        
        # Create a report
        report_id = str(uuid.uuid4())
        report = {
            'id': report_id,
            'location': location,
            'description': description,
            'image_data': image_data,
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'status': 'Submitted'
        }
        
        # Save the report (in-memory for this example)
        reports.append(report)
        
        flash('Report submitted successfully! Thank you for helping keep the community safe.', 'success')
        return redirect(url_for('index'))
    except Exception as e:
        logger.error(f"Error submitting report: {e}")
        flash('An error occurred while submitting your report. Please try again.', 'danger')
        return redirect(url_for('report'))

@app.route('/api/analyze_image', methods=['POST'])
def analyze_image():
    try:
        data = json.loads(request.data.decode('utf-8'))
        image_data = data.get('image_data', '')
        
        if not image_data:
            return jsonify({'success': False, 'error': 'No image data provided'})
        
        # Remove the data URL prefix
        if 'base64,' in image_data:
            image_data = image_data.split('base64,')[1]
        
        # Process the image
        processed_image = process_image(image_data)
        
        # Detect skimmer
        result = detect_skimmer(processed_image)
        
        return jsonify(result)
    except Exception as e:
        logger.error(f"Error analyzing image: {e}")
        return jsonify({'success': False, 'error': str(e)})

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def server_error(e):
    return render_template('500.html'), 500
