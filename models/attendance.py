from extensions import db
from datetime import datetime

class Attendance(db.Model):
    __tablename__ = 'attendance'

    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer, db.ForeignKey('employees.id'), nullable=False)
    
    date = db.Column(db.Date, nullable=False, default=datetime.utcnow)
    check_in_time = db.Column(db.Time, nullable=True)
    check_out_time = db.Column(db.Time, nullable=True)
    
    # [cite_start]Status: Present, Absent, Half-day, Leave [cite: 70-73]
    status = db.Column(db.String(20), default='Absent') 
    
    def __repr__(self):
        return f"<Attendance {self.date} - {self.status}>"