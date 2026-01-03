from flask import Blueprint, request, jsonify
from flask_login import login_user, logout_user, login_required
from services.auth_service import AuthService
from models.user import User

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    if not data:
        return jsonify({"message": "Invalid request"}), 400
    
    result, status_code = AuthService.register_user(data)
    return jsonify(result), status_code

from flask import Blueprint, request, jsonify
from flask_login import login_user, logout_user, login_required # Import these
from services.auth_service import AuthService
from models.user import User


# ... (register route stays the same)

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    
    # 1. Check if data exists
    if not data:
        return jsonify({"message": "Invalid request format"}), 400

    # 2. Find the user manually to log them in for the session (HTML)
    user = User.query.filter(
        (User.email == data.get('login_id')) | 
        (User.employee_id_number == data.get('login_id'))
    ).first()

    if user and user.check_password(data.get('password')):
        # CRITICAL: This line tells Flask "This user is logged in" for the templates
        login_user(user) 
        
        # 3. Proceed with generating the Token for the API
        result, status_code = AuthService.login_user(data)
        return jsonify(result), status_code
    
    return jsonify({"message": "Invalid credentials"}), 401

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return jsonify({"message": "Logged out successfully"}), 200