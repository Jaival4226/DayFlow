from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.employee import Employee
from models.user import User, UserRole
from services.attendance_service import AttendanceService
from utils.decorators import admin_required
from extensions import db

employee_bp = Blueprint('employee', __name__)

# 1. LANDING PAGE: Get all employees for the grid view
@employee_bp.route('/list', methods=['GET'])
@jwt_required()
def get_employee_grid():
    """Returns data for the clickable employee cards on the landing page."""
    employees = Employee.query.all()
    grid_data = []
    
    for emp in employees:
        grid_data.append({
            "employee_id": emp.user.employee_id_number,
            "full_name": f"{emp.first_name} {emp.last_name}",
            "designation": emp.designation,
            "department": emp.department,
            # Special Condition: Backend calculates the color dot
            "status": AttendanceService.get_employee_current_status(emp.id) 
        })
        
    return jsonify(grid_data), 200

# 2. PROFILE VIEW: Get specific employee details
@employee_bp.route('/<string:emp_id>', methods=['GET'])
@jwt_required()
def get_employee_detail(emp_id):
    """Returns full profile data. Restricted fields based on role."""
    # Find user by the generated Employee ID (e.g., OIJODO20220001)
    user = User.query.filter_by(employee_id_number=emp_id).first()
    
    if not user or not user.employee_profile:
        return jsonify({"message": "Employee not found"}), 404
        
    emp = user.employee_profile
    current_user_identity = get_jwt_identity()
    
    # Base data visible to everyone
    profile_data = {
        "public_info": {
            "name": f"{emp.first_name} {emp.last_name}",
            "designation": emp.designation,
            "department": emp.department,
            "email": user.email,
            "phone": emp.phone
        }
    }

    # Special Condition: Private Info & Salary Info (Admin/HR or Self Only)
    is_admin = current_user_identity['role'] in [UserRole.ADMIN.value, UserRole.HR.value]
    is_self = current_user_identity['id'] == user.id

    if is_admin or is_self:
        profile_data["private_info"] = {
            "date_of_birth": str(emp.date_of_birth) if emp.date_of_birth else "N/A",
            "joining_date": str(emp.date_of_joining),
            "address": emp.address if hasattr(emp, 'address') else "N/A"
        }
    
    # Special Condition: Salary Info tab (Admin/HR Only - based on wireframe)
    if is_admin:
        profile_data["salary_info"] = {
            "basic_salary": emp.basic_salary if hasattr(emp, 'basic_salary') else 0,
            "bank_name": emp.bank_name if hasattr(emp, 'bank_name') else "N/A",
            "account_number": emp.account_number if hasattr(emp, 'account_number') else "N/A"
        }

    return jsonify(profile_data), 200

# 3. ADMIN: Update employee details
@employee_bp.route('/<string:emp_id>', methods=['PUT'])
@jwt