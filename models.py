# This file would typically contain database models
# For this simple in-memory application, we're not using a database
# But we'll define structures here for future expansion

class Report:
    """
    Represents a skimmer report from a user
    """
    def __init__(self, id, location, description, image_data, timestamp, status="Submitted"):
        self.id = id
        self.location = location
        self.description = description
        self.image_data = image_data
        self.timestamp = timestamp
        self.status = status
        
    def to_dict(self):
        return {
            'id': self.id,
            'location': self.location,
            'description': self.description,
            'image_data': self.image_data,
            'timestamp': self.timestamp,
            'status': self.status
        }
