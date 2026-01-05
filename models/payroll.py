from extensions import db
from datetime import datetime

class Payroll(db.Model):
    __tablename__ = 'payroll'

    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer, db.ForeignKey('employees.id'), nullable=False)
    
    month = db.Column(db.String(20), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    
    # --- EARNINGS ---
    basic_salary = db.Column(db.Float, nullable=False)
    hra = db.Column(db.Float, default=0.0)       # House Rent Allowance
    da = db.Column(db.Float, default=0.0)        # Dearness Allowance
    medical_allowance = db.Column(db.Float, default=0.0)
    
    # --- DEDUCTIONS ---
    pf = db.Column(db.Float, default=0.0)        # Provident Fund
    professional_tax = db.Column(db.Float, default=0.0)
    other_deductions = db.Column(db.Float, default=0.0)
    
    net_salary = db.Column(db.Float, nullable=False)
    
    generated_on = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Payroll {self.month} {self.year}>"