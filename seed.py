from app import app
from extensions import db
from models.user import User, UserRole
from models.employee import Employee
from datetime import date

def seed_data():
    with app.app_context():
        print("⏳ Recreating tables...")
        db.drop_all()  # Clear old data to avoid conflicts
        db.create_all()

        # 1. Create Admin
        admin = User(
            employee_id_number="ADM001",
            email="admin@dayflow.com",
            role=UserRole.ADMIN,
            is_verified=True
        )
        admin.set_password("admin123")
        db.session.add(admin)

        # 2. Create Employee User
        emp_user = User(
            employee_id_number="EMP001",
            email="manan@dayflow.com",
            role=UserRole.EMPLOYEE,
            is_verified=True
        )
        emp_user.set_password("manan123")
        db.session.add(emp_user)
        
        db.session.commit() # Save to get IDs

        # 3. Create Employee Profile
        profile = Employee(
            user_id=emp_user.id,
            first_name="Manan",
            last_name="Developer",
            designation="Backend Lead",
            department="Engineering",
            date_of_joining=date.today()
        )
        db.session.add(profile)
        db.session.commit()

        print("✅ Database Seeded!")
        print("Admin: admin@dayflow.com | User: manan@dayflow.com")

if __name__ == "__main__":
    seed_data()