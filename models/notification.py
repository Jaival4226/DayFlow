from extensions import db
from datetime import datetime

class Notification(db.Model):
    __tablename__ = 'notifications'

    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.String(255), nullable=False)
    is_read = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Who is this notification for? (Usually Admin)
    # For simplicity, we can make it a "Global Admin" notification or link to a specific user
    # Here we just store it broadly.
    type = db.Column(db.String(50), default='Alert') # Alert, Info, Success

    def __repr__(self):
        return f"<Notification {self.message}>"