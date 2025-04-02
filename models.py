from app import db
from datetime import datetime

class Report(db.Model):
    """
    Represents a skimmer report from a user
    """
    id = db.Column(db.Integer, primary_key=True)
    location = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=False)
    image_data = db.Column(db.Text)  # Base64 encoded image
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(50), default="Submitted")
    
    def __init__(self, location, description, image_data, status="Submitted"):
        self.location = location
        self.description = description
        self.image_data = image_data
        self.status = status
        
    def to_dict(self):
        return {
            'id': self.id,
            'location': self.location,
            'description': self.description,
            'image_data': self.image_data,
            'timestamp': self.timestamp.isoformat() if self.timestamp else None,
            'status': self.status
        }
