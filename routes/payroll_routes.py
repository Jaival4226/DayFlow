from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.user import User

payroll_bp = Blueprint('payroll', __name__)

@payroll_bp.route('/my-slips', methods=['GET'])
@jwt_required()
def get_slips():
    user_id = get_jwt_identity()['id']
    user = User.query.get(user_id)
    
    slips = [{
        "month": p.month,
        "year": p.year,
        "net_salary": p.net_salary,
        "generated_on": str(p.generated_on)
    } for p in user.employee_profile.payroll_records]
    
    return jsonify(slips), 200