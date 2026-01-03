from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from services.leave_service import LeaveService
from models.user import User, UserRole

leave_bp = Blueprint('leave', __name__)

@leave_bp.route('/apply', methods=['POST'])
@jwt_required()
def apply_leave():
    user_id = get_jwt_identity()['id']
    user = User.query.get(user_id)
    return LeaveService.apply_leave(user.employee_profile.id, request.get_json())

@leave_bp.route('/my-requests', methods=['GET'])
@jwt_required()
def get_my_leaves():
    user_id = get_jwt_identity()['id']
    user = User.query.get(user_id)
    leaves = [ {
        "type": l.leave_type, 
        "status": l.status, 
        "start": str(l.start_date)
    } for l in user.employee_profile.leave_requests ]
    return jsonify(leaves), 200

# Admin route to approve leave
@leave_bp.route('/approve/<int:leave_id>', methods=['POST'])
@jwt_required()
def approve_leave(leave_id):
    user_identity = get_jwt_identity()
    if user_identity['role'] not in [UserRole.ADMIN.value, UserRole.HR.value]:
        return jsonify({"msg": "Admins only"}), 403
    # Logic to update status would go here
    return jsonify({"msg": "Leave updated"}), 200