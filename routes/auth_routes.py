from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from models.user import User
from extensions import db # Ensure this import is here too!

# This is the variable app.py is looking for!
auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    
    # Check if user exists by email or employee_id
    user = User.query.filter(
        (User.email == data.get('login_id')) | 
        (User.employee_id == data.get('login_id'))
    ).first()

    if user and user.check_password(data.get('password')):
        # Create identity for the token
        access_token = create_access_token(identity={'id': user.id, 'role': user.role_id})
        return jsonify(access_token=access_token), 200
    
    return jsonify({"msg": "Bad username or password"}), 401