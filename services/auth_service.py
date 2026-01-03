from models.user import User, UserRole
from models.employee import Employee
from extensions import db
from flask_jwt_extended import create_access_token
from datetime import date

class AuthService:
    @staticmethod
    def register_user(data):
        # 1. Check if user already exists
        if User.query.filter_by(email=data.get('email')).first():
            return {"error": "User with this email already exists"}, 400
        
        try:
            # 2. Create the User (Login Credentials)
            new_user = User(
                employee_id_number=data.get('employee_id_number'),
                email=data.get('email'),
                role=UserRole(data.get('role', 'employee')),
                is_verified=True
            )
            new_user.set_password(data.get('password'))
            db.session.add(new_user)
            db.session.flush()  # Generates ID for the profile link

            # 3. Create the Employee Profile
            new_profile = Employee(
                user_id=new_user.id,
                first_name=data.get('first_name'),
                last_name=data.get('last_name'),
                designation=data.get('designation'),
                department=data.get('department'),
                date_of_joining=date.today(),
                phone=data.get('phone')
            )
            db.session.add(new_profile)
            db.session.commit()
            
            return {"message": "Account created successfully"}, 201
            
        except Exception as e:
            db.session.rollback()
            return {"error": str(e)}, 500

    @staticmethod
    def login_user(data):
        login_id = data.get('login_id') # Can be email or employee_id
        password = data.get('password')

        # Find user by email or ID number
        user = User.query.filter(
            (User.email == login_id) | (User.employee_id_number == login_id)
        ).first()

        if user and user.check_password(password):
            # Create token with ID and Role inside the identity
            access_token = create_access_token(identity={
                'id': user.id, 
                'role': user.role.value
            })
            return {
                "access_token": access_token,
                "role": user.role.value,
                "user": {
                    "email": user.email,
                    "name": f"{user.employee_profile.first_name} {user.employee_profile.last_name}"
                }
            }, 200
        
        return {"error": "Invalid email/ID or password"}, 401