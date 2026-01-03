from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.user import User

payroll_bp = Blueprint('payroll', __name__)

@payroll_bp.route('/my-slips', methods=['GET'])
@jwt_required()
def get_slips():
    # FIX 1: Identity is now just a string, not a dictionary
    user_id = get_jwt_identity()
    user = User.query.get(int(user_id))
    
    # FIX 2: Send ALL the fields your new Payroll UI needs
    slips = [{
        "month": p.month,
        "year": p.year,
        "basic": p.basic_salary,       # Required by frontend
        "allowances": p.allowances,    # Required by frontend
        "deductions": p.deductions,    # Required by frontend
        "net_salary": p.net_salary,
        "generated_on": p.generated_on.strftime("%d %b %Y") # Nice date format
    } for p in user.employee_profile.payroll_records]
    
    return jsonify(slips), 200