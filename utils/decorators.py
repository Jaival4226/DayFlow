from functools import wraps
from flask import jsonify
from flask_jwt_extended import get_jwt_identity
from models.user import User, UserRole

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        identity = get_jwt_identity()
        user = User.query.get(identity['id'])
        
        # We only allow ADMIN or HR to pass this gate
        if not user or user.role not in [UserRole.ADMIN, UserRole.HR]:
            return jsonify({"error": "Unauthorized. Admin or HR access required."}), 403
            
        return f(*args, **kwargs)
    return decorated_function