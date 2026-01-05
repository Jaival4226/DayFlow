from models.payroll import Payroll
from extensions import db
from datetime import datetime

class PayrollService:
    @staticmethod
    def generate_slip(employee_id, monthly_wage):
        """
        Calculates salary breakdown based on Monthly Wage (CTC).
        Structure: Basic (50%), HRA (20%), DA (10%), PF (12% of Basic), Tax (Fixed 200).
        """
        # 1. Earnings Calculation
        basic = monthly_wage * 0.50
        hra = monthly_wage * 0.20
        da = monthly_wage * 0.10
        medical = monthly_wage * 0.20 # Remaining balance
        
        # 2. Deductions Calculation
        pf = basic * 0.12
        pt = 200.0 if monthly_wage > 15000 else 0.0 # Standard Professional Tax logic
        
        total_earnings = basic + hra + da + medical
        total_deductions = pf + pt
        
        net_salary = total_earnings - total_deductions
        
        now = datetime.now()
        
        new_payroll = Payroll(
            employee_id=employee_id,
            month=now.strftime("%B"),
            year=now.year,
            
            basic_salary=round(basic, 2),
            hra=round(hra, 2),
            da=round(da, 2),
            medical_allowance=round(medical, 2),
            
            pf=round(pf, 2),
            professional_tax=round(pt, 2),
            other_deductions=0,
            
            net_salary=round(net_salary, 2)
        )
        
        db.session.add(new_payroll)
        db.session.commit()
        return {"message": "Payroll generated successfully", "net_salary": net_salary}, 201