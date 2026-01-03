from extensions import db
from datetime import datetime

class Leave(db.Model):
    __tablename__ = 'leaves'

    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer, db.ForeignKey('employees.id'), nullable=False)
    
    # [cite_start]Leave Types: Paid, Sick, Unpaid [cite: 81]
    leave_type = db.Column(db.String(50), nullable=False)
    
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    reason = db.Column(db.Text)
    
    # [cite_start]Status: Pending, Approved, Rejected [cite: 84-87]
    status = db.Column(db.String(20), default='Pending')
    
    admin_comments = db.Column(db.Text)
    applied_on = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Leave {self.leave_type} : {self.status}>"