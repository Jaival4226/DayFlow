from models.user import User, UserRole
from models.employee import Employee
from extensions import db
from flask_jwt_extended import create_access_token
from datetime import date

class AuthService:
    @staticmethod
    def generate_login_id(first_name, last_name):
        """Generates Login ID: OI + First2(First+Last) + Year + Serial"""
        company_code = "OI" 
        name_part = (first_name[:2] + last_name[:2]).upper()
        current_year = str(date.today().year)
        
        # Calculate serial number for this year
        count = User.query.filter(User.employee_id_number.like(f"%{current_year}%")).count()
        serial = str(count + 1).zfill(4)
        
        return f"{company_code}{name_part}{current_year}{serial}"

    @staticmethod
    def register_user(data):
        """Creates User and Employee profile together"""
        try:
            generated_id = AuthService.generate_login_id(data['first_name'], data['last_name'])
            
            new_user = User(
                employee_id_number=generated_id,
                email=data.get('email'),
                role=UserRole(data.get('role', 'employee')),
                is_verified=True
            )
            
            temp_password = data.get('password', "password123") 
            new_user.set_password(temp_password)
            
            db.session.add(new_user)
            db.session.flush()

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
                "login_id": generated_id
            }, 201
            
        except Exception as e:
            db.session.rollback()
            return {"message": f"Error: {str(e)}"}, 500

    @staticmethod
    def login_user(data):
        """Handles multi-ID login and creates JWT with claims"""
        login_id = data.get('login_id') 
        password = data.get('password')

        user = User.query.filter(
            (User.email == login_id) | (User.employee_id_number == login_id)
        ).first()

        if user and user.check_password(password):
            # FIX: Identity is a STRING. Role is in additional_claims.
            access_token = create_access_token(
                identity=str(user.id), 
                additional_claims={"role": user.role.value}
            )
            
            return {
                "token": access_token,
                "role": user.role.value,
                "message": "Login successful",
                "user": {
                    "id": user.employee_id_number,
                    "name": f"{user.employee_profile.first_name} {user.employee_profile.last_name}",
                    "email": user.email
                }
            }, 200
        
        return {"message": "Invalid credentials"}, 401