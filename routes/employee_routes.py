from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from services.attendance_service import AttendanceService
from services.leave_service import LeaveService
from models.user import User

emp_bp = Blueprint('employee', __name__)

# Helper to get Employee ID from current JWT User
def get_current_emp_id():
    user_identity = get_jwt_identity()
    user = User.query.get(user_identity['id'])
    return user.employee_profile.id

@emp_bp.route('/attendance/clock-in', methods=['POST'])
@jwt_required()
def clock_in():
    return AttendanceService.clock_in(get_current_emp_id())

@emp_bp.route('/attendance/clock-out', methods=['POST'])
@jwt_required()
def clock_out():
    return AttendanceService.clock_out(get_current_emp_id())

@emp_bp.route('/leave/apply', methods=['POST'])
@jwt_required()
def apply_leave():
    return LeaveService.apply_leave(get_current_emp_id(), request.get_json())

@emp_bp.route('/test', methods=['GET'])
def test():
    return jsonify({"status": "Success", "message": "Employee Routes are Live!"}), 200