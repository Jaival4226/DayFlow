from functools import wraps
from flask import jsonify
from flask_jwt_extended import get_jwt, get_jwt_identity
from models.user import User, UserRole

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # 1. Get the claims (where we now store the role)
        claims = get_jwt()
        user_role = claims.get("role")
        
        # 2. Check permission
        if user_role not in [UserRole.ADMIN.value, UserRole.HR.value]:
            return jsonify({"message": "Unauthorized. Admin or HR access required."}), 403
            
        return f(*args, **kwargs)
    return decorated_function