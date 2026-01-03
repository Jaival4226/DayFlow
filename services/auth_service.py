from models.user import User
from flask_jwt_extended import create_access_token

class AuthService:
    @staticmethod
    def login_user(login_id, password):
        user = User.query.filter((User.email == login_id) | 
                                 (User.employee_id_number == login_id)).first()
        if user and user.check_password(password):
            token = create_access_token(identity={'id': user.id, 'role': user.role.value})
            return {"token": token, "role": user.role.value}, 200
        return {"error": "Invalid credentials"}, 401