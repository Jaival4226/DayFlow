from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.user import User

payroll_bp = Blueprint('payroll', __name__)

@payroll_bp.route('/my-slips', methods=['GET'])
@jwt_required()
def get_slips():
    user_id = get_jwt_identity()
    user = User.query.get(int(user_id))
    
    slips = [{
        "month": p.month,
        "year": p.year,
        "basic": p.basic_salary,
        "hra": p.hra,
        "da": p.da,
        "medical": p.medical_allowance,
        "pf": p.pf,
        "pt": p.professional_tax,
        "deductions": p.pf + p.professional_tax + p.other_deductions, # Total Deductions
        "net_salary": p.net_salary,
        "generated_on": p.generated_on.strftime("%d %b %Y")
    } for p in user.employee_profile.payroll_records]
    
    return jsonify(slips), 200