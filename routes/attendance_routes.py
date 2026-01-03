from flask import Blueprint
from flask_jwt_extended import jwt_required, get_jwt_identity
from services.attendance_service import AttendanceService
from models.user import User

attendance_bp = Blueprint('attendance', __name__)

@attendance_bp.route('/clock-in', methods=['POST'])
@jwt_required()
def clock_in():
    user_id = get_jwt_identity()['id']
    user = User.query.get(user_id)
    return AttendanceService.clock_in(user.employee_profile.id)