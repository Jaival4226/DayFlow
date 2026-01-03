from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from models.employee import Employee
from models.user import User, UserRole
from services.attendance_service import AttendanceService
from utils.decorators import admin_required
from extensions import db

# Define the blueprint
employee_bp = Blueprint('employee', __name__)

# ---------------------------------------------------------
# 1. LANDING PAGE: GET ALL EMPLOYEES (GRID VIEW)
# ---------------------------------------------------------
@employee_bp.route('/list', methods=['GET'])
@jwt_required()
def get_employee_grid():
    """
    Returns data for the employee cards on the landing page.
    Includes the 'status' for the UI color dots.
    """
    employees = Employee.query.all()
    grid_data = []
    
    for emp in employees:
        grid_data.append({
            "employee_id": emp.user.employee_id_number, # Generated ID (OI...)
            "full_name": f"{emp.first_name} {emp.last_name}",
            "designation": emp.designation,
            "department": emp.department,
            # Backend-calculated status dot logic
            "status": AttendanceService.get_employee_current_status(emp.id) 
        })
        
    return jsonify(grid_data), 200

# ---------------------------------------------------------
# 2. PROFILE VIEW: GET SPECIFIC EMPLOYEE DETAILS
# ---------------------------------------------------------
@employee_bp.route('/<string:emp_id>', methods=['GET'])
@jwt_required()
def get_employee_detail(emp_id):
    """
    Returns full profile data with privacy restrictions.
    Uses get_jwt() to check roles without extra DB queries.
    """
    # Look up user by the string-based Employee ID from wireframes
    user = User.query.filter_by(employee_id_number=emp_id).first()
    
    if not user or not user.employee_profile:
        return jsonify({"message": "Employee not found"}), 404
        
    emp = user.employee_profile
    
    # NEW LOGIC: Identity is a string (User ID), Role is in claims
    current_user_id = get_jwt_identity() 
    claims = get_jwt()
    current_user_role = claims.get("role")
    
    # Info visible to all employees
    profile_data = {
        "public_info": {
            "name": f"{emp.first_name} {emp.last_name}",
            "designation": emp.designation,
            "department": emp.department,
            "email": user.email,
            "phone": emp.phone
        }
    }

    # Privacy Check: Viewable only by Admin/HR or the user themselves
    is_admin = current_user_role in [UserRole.ADMIN.value, UserRole.HR.value]
    is_self = str(user.id) == str(current_user_id)

    if is_admin or is_self:
        profile_data["private_info"] = {
            "date_of_birth": str(emp.date_of_birth) if emp.date_of_birth else "N/A",
            "joining_date": str(emp.date_of_joining),
            "address": emp.address if hasattr(emp, 'address') else "N/A"
        }
        
    # Salary Info: Strictly Admin/HR Only
    if is_admin:
        profile_data["salary_info"] = {
            "monthly_wage": emp.monthly_wage if hasattr(emp, 'monthly_wage') else 0,
            "bank_name": emp.bank_name if hasattr(emp, 'bank_name') else "N/A"
        }
    
    return jsonify(profile_data), 200

# ---------------------------------------------------------
# 3. ADMIN: UPDATE EMPLOYEE DETAILS
# ---------------------------------------------------------
@employee_bp.route('/<string:emp_id>', methods=['PUT'])
@jwt_required()
@admin_required # Security gate
def update_employee(emp_id):
    """Allows Admin/HR to update core employee details."""
    user = User.query.filter_by(employee_id_number=emp_id).first()
    
    if not user or not user.employee_profile:
        return jsonify({"message": "Employee not found"}), 404
        
    emp = user.employee_profile
    data = request.get_json()
    
    # Update allowed fields
    emp.first_name = data.get('first_name', emp.first_name)
    emp.last_name = data.get('last_name', emp.last_name)
    emp.designation = data.get('designation', emp.designation)
    emp.department = data.get('department', emp.department)
    emp.phone = data.get('phone', emp.phone)
    
    db.session.commit()
    return jsonify({"message": "Employee updated successfully"}), 200