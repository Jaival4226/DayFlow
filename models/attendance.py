from extensions import db
from datetime import datetime

class Attendance(db.Model):
    __tablename__ = 'attendance'

    id = db.Column(db.Integer, primary_key=True)
    
    # FIXED: Variable name changed to singular 'employee_id' 
    # This must match Attendance.query.filter_by(employee_id=...)
    employee_id = db.Column(db.Integer, db.ForeignKey('employees.id'), nullable=False)
    
    date = db.Column(db.Date, nullable=False, default=datetime.utcnow)
    check_in = db.Column(db.Time, nullable=True) 
    check_out = db.Column(db.Time, nullable=True)
    
    # Status matches your wireframe dots: present, absent, on_leave
    status = db.Column(db.String(20), default='absent') 
    
    def __repr__(self):
        return f"<Attendance {self.date} - {self.status}>"