from models.user import User, UserRole
from models.employee import Employee
from extensions import db
from flask_jwt_extended import create_access_token
from datetime import date
import sqlalchemy

class AuthService:
    @staticmethod
    def generate_login_id(first_name, last_name):
        """Generates Login ID: OI + First2(First+Last) + Year + Serial"""
        company_code = "OI" # Based on 'Odoo India' example in your wireframe
        name_part = (first_name[:2] + last_name[:2]).upper()
        current_year = str(date.today().year)
        
        # Calculate serial number for this year
        count = User.query.filter(User.employee_id_number.like(f"%{current_year}%")).count()
        serial = str(count + 1).zfill(4)
        
        return f"{company_code}{name_part}{current_year}{serial}"

    @staticmethod
    def register_user(data):
        # NOTE: Wireframe states normal users cannot register themselves.
        # This route should typically be protected or used by HR/Admin.
        try:
            # 1. Generate the special Login ID from wireframe requirements
            generated_id = AuthService.generate_login_id(data['first_name'], data['last_name'])
            
            # 2. Create the User (Login Credentials)
            new_user = User(
                employee_id_number=generated_id,
                email=data.get('email'),
                role=UserRole(data.get('role', 'employee')),
                is_verified=True
            )
            
            # Wireframe Note: Password should be auto-generated for the first time
            # We'll use a temporary one or take it from data if provided by Admin
            temp_password = data.get('password', "Welcome@123") 
            new_user.set_password(temp_password)
            
            db.session.add(new_user)
            db.session.flush()

            # 3. Create the Employee Profile
            new_profile = Employee(
                user_id=new_user.id,
                first_name=data['first_name'],
                last_name=data['last_name'],
                designation=data.get('designation', 'Trainee'),
                department=data.get('department', 'General'),
                date_of_joining=date.today(),
                phone=data.get('phone')
            )
            db.session.add(new_profile)
            db.session.commit()
            
            return {
                "message": "User created successfully",
                "login_id": generated_id,
                "temp_password": temp_password
            }, 201
            
        except Exception as e:
            db.session.rollback()
            return {"message": f"Error: {str(e)}"}, 500

    @staticmethod
    def login_user(data):
        login_id = data.get('login_id') # Supports generated ID or Email
        password = data.get('password')

        user = User.query.filter(
            (User.email == login_id) | (User.employee_id_number == login_id)
        ).first()

        if user and user.check_password(password):
            access_token = create_access_token(identity={'id': user.id, 'role': user.role.value})
            
            # Match exact JSON format for main.js and landing page requirements
            return {
                "token": access_token,
                "role": user.role.value,
                "message": "Login successful",
                "user": {
                    "id": user.employee_id_number,
                    "name": f"{user.employee_profile.first_name} {user.employee_profile.last_name}",
                    "email": user.email,
                    "avatar_status": "green" # Defaulting to green (present) as per wireframe
                }
            }, 200
        
        return {"message": "Invalid credentials"}, 401