import os
import logging
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, session
import base64
import json
from datetime import datetime
import sqlalchemy
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from utils.image_processor import process_image
from utils.skimmer_detector import detect_skimmer

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Setup SQLAlchemy database
class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)

# Initialize Flask app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "default-secret-key-for-development")

# Configure database
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
    "pool_recycle": 300,
    "pool_pre_ping": True,
}
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Initialize the database with the app
db.init_app(app)

# Import models after db initialization to avoid circular imports
with app.app_context():
    from models import Report
    db.create_all()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/detection')
def detection():
    return render_template('detection.html')

@app.route('/education')
def education():
    return render_template('education.html')
    
@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/report')
def report():
    return render_template('report.html')

@app.route('/reports')
def reports():
    # Fetch all reports from the database
    all_reports = Report.query.order_by(Report.timestamp.desc()).all()
    return render_template('reports.html', reports=all_reports)

@app.route('/submit_report', methods=['POST'])
def submit_report():
    try:
        location = request.form.get('location', '')
        description = request.form.get('description', '')
        image_data = request.form.get('image_data', '')
        
        if not image_data:
            flash('Please include an image of the suspected skimmer device', 'danger')
            return redirect(url_for('report'))
        
        # Create a new report using the database model
        new_report = Report(
            location=location,
            description=description,
            image_data=image_data
        )
        
        # Save the report to the database
        db.session.add(new_report)
        db.session.commit()
        
        flash('Report submitted successfully! Thank you for helping keep the community safe.', 'success')
        return redirect(url_for('index'))
    except Exception as e:
        db.session.rollback()
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
    
@app.route('/send_message', methods=['POST'])
def send_message():
    try:
        name = request.form.get('name', '')
        email = request.form.get('email', '')
        subject = request.form.get('subject', '')
        message = request.form.get('message', '')
        
        # In a real application, this would send an email or save to database
        # For now, we'll just log it and show a success message
        logger.info(f"Message received from {name} ({email}): {subject}")
        
        flash('Thank you for your message! We will get back to you soon.', 'success')
        return redirect(url_for('contact'))
    except Exception as e:
        logger.error(f"Error sending message: {e}")
        flash('An error occurred while sending your message. Please try again.', 'danger')
        return redirect(url_for('contact'))
