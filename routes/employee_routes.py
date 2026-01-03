import os
from flask import Blueprint, jsonify, request, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from models.employee import Employee
from models.user import User, UserRole
from services.attendance_service import AttendanceService
from utils.decorators import admin_required
from extensions import db
from werkzeug.utils import secure_filename

employee_bp = Blueprint('employee', __name__)
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# ---------------------------------------------------------
# 1. LANDING PAGE: GET ALL EMPLOYEES (GRID VIEW)
# ---------------------------------------------------------
@employee_bp.route('/list', methods=['GET'])
@jwt_required()
def get_employee_grid():
    employees = Employee.query.all()
    grid_data = []
    
    # ... inside get_employee_grid() ...

    for emp in employees:
        grid_data.append({
            "employee_id": emp.user.employee_id_number,
            "full_name": f"{emp.first_name} {emp.last_name}",
            "designation": emp.designation,
            "department": emp.department,
            "status": AttendanceService.get_employee_current_status(emp.id),
            "profile_picture": emp.profile_picture  # <--- ADD THIS LINE
        })
        
    return jsonify(grid_data), 200

# ---------------------------------------------------------
# 2. PROFILE VIEW
# ---------------------------------------------------------
@employee_bp.route('/<string:emp_id>', methods=['GET'])
@jwt_required()
def get_employee_detail(emp_id):
    user = User.query.filter_by(employee_id_number=emp_id).first()
    
    if not user or not user.employee_profile:
        return jsonify({"message": "Employee not found"}), 404
        
    emp = user.employee_profile
    current_user_id = get_jwt_identity() 
    claims = get_jwt()
    
    profile_data = {
        "public_info": {
            "name": f"{emp.first_name} {emp.last_name}",
            "designation": emp.designation,
            "department": emp.department,
            "email": user.email,
            "phone": emp.phone
        }
    }
    return jsonify(profile_data), 200

# ---------------------------------------------------------
# 3. UPDATE PROFILE (Logic for the Edit Modal)
# ---------------------------------------------------------
import time # Add this import at the top

# ... (keep existing imports)

@employee_bp.route('/update-profile', methods=['POST'])
@jwt_required()
def update_profile():
    user_id = get_jwt_identity()
    user = User.query.get(int(user_id))
    
    if not user or not user.employee_profile:
        return jsonify({"message": "Profile not found"}), 404

    emp = user.employee_profile

    # 1. Update Text Fields
    if 'phone' in request.form:
        emp.phone = request.form['phone']
    if 'address' in request.form:
        emp.address = request.form['address']

    # 2. Handle Image Upload
    if 'profile_picture' in request.files:
        file = request.files['profile_picture']
        
        # Check if user actually selected a file
        if file.filename == '':
            return jsonify({"message": "No file selected"}), 400
            
        if file and allowed_file(file.filename):
            # FIX: Add Timestamp to force unique filename (Avoids Cache Issues)
            timestamp = int(time.time())
            ext = file.filename.rsplit('.', 1)[1].lower()
            filename = secure_filename(f"user_{user.id}_{timestamp}.{ext}")
            
            # Ensure upload folder exists
            upload_path = current_app.config['UPLOAD_FOLDER']
            if not os.path.exists(upload_path):
                os.makedirs(upload_path)
                
            # Save file
            file.save(os.path.join(upload_path, filename))
            
            # Update DB
            emp.profile_picture = filename
        else:
            return jsonify({"message": "Invalid file type. Allowed: png, jpg, jpeg, gif"}), 400

    db.session.commit()
    
    # Return the new URL so frontend can update immediately
    return jsonify({
        "message": "Profile updated successfully!", 
        "image_url": emp.profile_picture
    }), 200