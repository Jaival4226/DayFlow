from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from services.leave_service import LeaveService
from models.user import User
from utils.decorators import admin_required 

leave_bp = Blueprint('leave', __name__)

@leave_bp.route('/apply', methods=['POST'])
@jwt_required()
def apply_leave():
    # FIXED: Identity is a string, not a dict
    user_id = get_jwt_identity()
    user = User.query.get(int(user_id))
    return LeaveService.apply_leave(user.employee_profile.id, request.get_json())

@leave_bp.route('/my-requests', methods=['GET'])
@jwt_required()
def get_my_leaves():
    user_id = get_jwt_identity()
    user = User.query.get(int(user_id))
    leaves = [ {
        "id": l.id,
        "type": l.leave_type, 
        "status": l.status, 
        "start": str(l.start_date),
        "end": str(l.end_date)
    } for l in user.employee_profile.leave_requests ]
    return jsonify(leaves), 200

@leave_bp.route('/approve/<int:leave_id>', methods=['POST'])
@jwt_required()
@admin_required
def approve_leave(leave_id):
    result, status_code = LeaveService.approve_leave(leave_id)
    return jsonify(result), status_code

@leave_bp.route('/reject/<int:leave_id>', methods=['POST'])
@jwt_required()
@admin_required
def reject_leave(leave_id):
    result, status_code = LeaveService.reject_leave(leave_id)
    return jsonify(result), status_code