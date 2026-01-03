from models.payroll import Payroll
from extensions import db
from datetime import datetime

class PayrollService:
    @staticmethod
    def generate_slip(employee_id, basic_salary, allowances=0, deductions=0):
        # Calculate Net Salary
        net_salary = basic_salary + allowances - deductions
        now = datetime.now()
        
        new_payroll = Payroll(
            employee_id=employee_id,
            month=now.strftime("%B"),
            year=now.year,
            basic_salary=basic_salary,
            allowances=allowances,
            deductions=deductions,
            net_salary=net_salary
        )
        
        db.session.add(new_payroll)
        db.session.commit()
        return {"message": "Payroll generated successfully", "net_salary": net_salary}, 201