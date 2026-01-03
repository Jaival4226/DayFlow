from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from services.attendance_service import AttendanceService
from models.user import User
from extensions import db

attendance_bp = Blueprint('attendance', __name__)

# 1. CLOCK-IN: The logic to turn the status dot GREEN
@attendance_bp.route('/clock-in', methods=['POST'])
@jwt_required()
def clock_in():
    """
    Handles the backend logic for marking an employee as present.
    The 'identity' from JWT is now a string (User ID).
    """
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    
    if not user or not user.employee_profile:
        return jsonify({"message": "Employee profile not found"}), 404

    # Call the service to handle database logic
    result, status_code = AttendanceService.clock_in(user.employee_profile.id)
    return jsonify(result), status_code

# 2. CLOCK-OUT: The logic to finalize work hours
@attendance_bp.route('/clock-out', methods=['POST'])
@jwt_required()
def clock_out():
    """Handles the backend logic for checking out."""
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    
    if not user or not user.employee_profile:
        return jsonify({"message": "Employee profile not found"}), 404

    result, status_code = AttendanceService.clock_out(user.employee_profile.id)
    return jsonify(result), status_code

# 3. HISTORY: Get logs for the current user
@attendance_bp.route('/my-history', methods=['GET'])
@jwt_required()
def get_history():
    """Returns the attendance list for the logged-in user."""
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    
    # Logic to fetch records from the service
    history = AttendanceService.get_employee_history(user.employee_profile.id)
    return jsonify(history), 200