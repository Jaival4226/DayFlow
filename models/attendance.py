from extensions import db
from datetime import datetime

class Attendance(db.Model):
    __tablename__ = 'attendance'

    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer, db.ForeignKey('employees.id'), nullable=False)
    date = db.Column(db.Date, nullable=False, default=datetime.utcnow)
    check_in = db.Column(db.Time, nullable=True) 
    check_out = db.Column(db.Time, nullable=True)
    
    # NEW: Added for calculation support
    work_hours = db.Column(db.Float, default=0.0) 
    
    status = db.Column(db.String(20), default='absent') 

    def __repr__(self):
        return f"<Attendance {self.date} - {self.status}>"