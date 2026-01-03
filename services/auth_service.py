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
            # 1. Handle Name Splitting (Full Name -> First + Last)
            full_name = data.get('full_name', '').strip()
            if ' ' in full_name:
                first_name, last_name = full_name.rsplit(' ', 1)
            else:
                first_name = full_name
                last_name = "User" # Fallback if no last name provided

            # 2. Generate ID
            generated_id = AuthService.generate_login_id(first_name, last_name)
            
            # 3. Create Login User
            new_user = User(
                employee_id_number=generated_id,
                email=data.get('email'),
                role=UserRole.EMPLOYEE, # Default to Employee for new signups
                is_verified=True
            )
            
            new_user.set_password(data.get('password'))
            
            db.session.add(new_user)
            db.session.flush() # Get the ID before creating profile

            # 4. Create Profile
            # Note: We save 'Company Name' into 'Department' to keep DB simple
            new_profile = Employee(
                user_id=new_user.id,
                first_name=first_name,
                last_name=last_name,
                designation="New Hire",
                department=data.get('company_name', 'General'), 
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
            access_token = create_access_token(
                identity=str(user.id), 
                additional_claims={"role": user.role.value}
            )
            
            # SAFE NAME CHECK
            if user.employee_profile:
                full_name = f"{user.employee_profile.first_name} {user.employee_profile.last_name}"
            else:
                full_name = "Admin User" # Fallback if profile is missing
            
            return {
                "token": access_token,
                "role": user.role.value,
                "message": "Login successful",
                "user": {
                    "id": user.employee_id_number,
                    "name": full_name,
                    "email": user.email
                }
            }, 200