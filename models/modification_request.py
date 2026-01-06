from extensions import db
from datetime import datetime
import json

class ModificationRequest(db.Model):
    __tablename__ = 'modification_requests'

    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer, db.ForeignKey('employees.id'), nullable=False)
    
    # Store the changes as a JSON string (e.g., {"bank_name": "HDFC", "account": "123"})
    changes_json = db.Column(db.Text, nullable=False)
    
    status = db.Column(db.String(20), default='Pending') # Pending, Approved, Rejected
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    employee = db.relationship('Employee', backref='modification_requests')

    def get_changes(self):
        return json.loads(self.changes_json)