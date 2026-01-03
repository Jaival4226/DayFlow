from app import app
from extensions import db
from models.user import User, UserRole
from models.employee import Employee
from datetime import date

def seed_data():
    with app.app_context():
        print("⏳ Recreating tables...")
        db.drop_all()  
        db.create_all()

        # 1. Create Admin (Matches Wireframe Generated ID Style)
        admin = User(
            employee_id_number="OIADMI20260001", 
            email="admin@dayflow.com",
            role=UserRole.ADMIN,
            is_verified=True
        )
        admin.set_password("password123") # Standardizing for testing
        db.session.add(admin)

        # 2. Create Manan (Employee)
        emp_user = User(
            employee_id_number="OIMADE20260002",
            email="manan@dayflow.com",
            role=UserRole.EMPLOYEE,
            is_verified=True
        )
        emp_user.set_password("password123")
        db.session.add(emp_user)
        
        db.session.commit() 

        # 3. Create Manan's Profile
        profile = Employee(
            user_id=emp_user.id,
            first_name="Manan",
            last_name="Developer",
            designation="Backend Lead",
            department="Engineering",
            date_of_joining=date.today(),
            phone="9876543210"
        )
        db.session.add(profile)
        db.session.commit()

        print("✅ Database Seeded Successfully!")
        print("Standard Password for both: password123")
        print(f"Manan ID: {emp_user.employee_id_number}")

if __name__ == "__main__":
    seed_data()