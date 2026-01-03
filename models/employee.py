from extensions import db
from datetime import datetime

class Employee(db.Model):
    __tablename__ = 'employees'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), unique=True, nullable=False)
    
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    
    designation = db.Column(db.String(100))
    department = db.Column(db.String(100))
    # Note: changed to .date() because Postgres DATE columns don't store time
    date_of_joining = db.Column(db.Date, default=datetime.utcnow().date)
    
    phone = db.Column(db.String(20))
    address = db.Column(db.Text)
    profile_picture = db.Column(db.String(120), default='default.jpg')

    # ⚠️ COMMENT THESE OUT UNTIL THE OTHER MODELS ARE CREATED
    # attendance_records = db.relationship('Attendance', backref='employee', lazy=True)
    # leave_requests = db.relationship('Leave', backref='employee', lazy=True)
    # payroll_records = db.relationship('Payroll', backref='employee', lazy=True)

    def __repr__(self):
        return f"<Employee {self.first_name} {self.last_name}>"