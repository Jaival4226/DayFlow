from app import app
from extensions import db
from models.user import User, UserRole
from models.employee import Employee
from models.payroll import Payroll
from models.attendance import Attendance
from models.leave import Leave
from datetime import date, datetime, timedelta, time
import random

# --- CONFIGURATION ---
TOTAL_STAFF = 30
HR_OFFICER_COUNT = 3
PASSWORD = "password123"

# --- DATA POOLS ---
FIRST_NAMES = ["Aarav", "Vihaan", "Aditya", "Sai", "Reyansh", "Diya", "Ananya", "Kiara", "Pari", "Myra", "Rohan", "Vikram", "Neha", "Pooja", "Arjun", "Ishaan", "Vivaan", "Saanvi", "Aadhya", "Zara", "Kabir", "Meera", "Riya", "Krishna", "Sarthak", "Nikhil", "Kavya", "Sneha", "Manish", "Priya"]
LAST_NAMES = ["Sharma", "Patel", "Verma", "Reddy", "Singh", "Nair", "Gupta", "Kapoor", "Khan", "Joshi", "Mehta", "Malhotra", "Iyer", "Kumar", "Das", "Chopra", "Desai", "Jain", "Mishra", "Rao", "Saxena", "Yadav", "Bhatia", "Chauhan", "Dutta", "Garg", "Hegde", "Jha", "Kaur", "Lal"]

REGULAR_DEPARTMENTS = ['Engineering', 'Sales', 'Marketing', 'Finance', 'Operations', 'Legal', 'Product', 'Design']
DESIGNATIONS = {
    'HR': ['HR Manager', 'Senior Recruiter', 'HR Business Partner'], 
    'Engineering': ['Software Engineer', 'Backend Dev', 'Frontend Dev', 'DevOps Engineer', 'CTO'],
    'Sales': ['Sales Executive', 'Sales Manager', 'Accountant', 'Lead Generator'],
    'Marketing': ['SEO Specialist', 'Content Writer', 'Marketing Manager', 'CMO'],
    'Finance': ['Accountant', 'Financial Analyst', 'CFO'],
    'Operations': ['Operations Manager', 'Logistics Lead'],
    'Legal': ['Legal Advisor', 'Corporate Lawyer'],
    'Product': ['Product Manager', 'Product Owner'],
    'Design': ['UI/UX Designer', 'Graphic Designer']
}
DOMAINS = ["dayflow.com", "gmail.com", "outlook.com"]

def generate_phone():
    return f"{random.choice(['9', '8', '7', '6'])}{random.randint(100000000, 999999999)}"

def get_random_date(start_year=2022, end_year=2025):
    start = date(start_year, 1, 1)
    end = date(end_year, 12, 31)
    return start + timedelta(days=random.randint(0, (end - start).days))

def seed_data():
    with app.app_context():
        print("🗑️  Cleaning Database...")
        db.drop_all()
        db.create_all()

        print("🚀 Creating Super Admin...")
        admin_user = User(
            employee_id_number="OIADMIN001",
            email="admin@dayflow.com",
            role=UserRole.ADMIN,
            is_verified=True
        )
        admin_user.set_password(PASSWORD)
        db.session.add(admin_user)
        db.session.flush()

        admin_profile = Employee(
            user_id=admin_user.id,
            first_name="Super",
            last_name="Admin",
            designation="System Administrator",
            department="IT",
            date_of_joining=date(2020, 1, 1),
            phone=generate_phone(),
            monthly_wage=250000,
            address="HQ Server Room",
            profile_picture="default.jpg"
        )
        db.session.add(admin_profile)

        print(f"🌱 Generating {TOTAL_STAFF} Staff Members...")
        
        hr_created = []
        regular_created = []

        for i in range(TOTAL_STAFF):
            first = FIRST_NAMES[i % len(FIRST_NAMES)]
            last = LAST_NAMES[i % len(LAST_NAMES)]
            
            # --- ROLE LOGIC ---
            if i < HR_OFFICER_COUNT:
                role = UserRole.HR
                dept = 'HR'
                designation = DESIGNATIONS['HR'][i % len(DESIGNATIONS['HR'])]
                prefix = "HR"
            else:
                role = UserRole.EMPLOYEE
                dept = random.choice(REGULAR_DEPARTMENTS)
                designation = random.choice(DESIGNATIONS.get(dept, ['Associate']))
                prefix = "OI"

            # Generate ID & Email
            serial = str(i+1).zfill(3)
            emp_id = f"{prefix}{first[:2].upper()}{last[:2].upper()}2026{serial}"
            email = f"{first.lower()}.{last.lower()}{random.randint(1,99)}@{random.choice(DOMAINS)}"

            # 2. User Account
            user = User(
                employee_id_number=emp_id,
                email=email,
                role=role,
                is_verified=True
            )
            user.set_password(PASSWORD)
            db.session.add(user)
            db.session.flush()

            if role == UserRole.HR: hr_created.append((first, email))
            else: regular_created.append((first, email))

            # 3. Employee Profile
            wage = random.randint(35000, 180000)
            emp = Employee(
                user_id=user.id,
                first_name=first,
                last_name=last,
                designation=designation,
                department=dept,
                date_of_joining=get_random_date(),
                phone=generate_phone(),
                monthly_wage=wage,
                address=f"Flat {random.randint(101, 909)}, City Center, Sector {random.randint(1, 20)}",
                profile_picture="default.jpg"
            )
            db.session.add(emp)
            db.session.flush()

            # 4. Payroll (Last 3 Months for EVERYONE)
            months = [("October", 2025), ("November", 2025), ("December", 2025)]
            for m_name, m_year in months:
                basic = wage * 0.50
                hra = wage * 0.20
                other = wage * 0.20
                deduction = wage * 0.10
                
                payroll = Payroll(
                    employee_id=emp.id,
                    month=m_name,
                    year=m_year,
                    basic_salary=basic,
                    allowances=hra + other,
                    deductions=deduction,
                    net_salary=wage,
                    generated_on=datetime(m_year, 12, 28)
                )
                db.session.add(payroll)

            # 5. Attendance (Last 30 Days + TODAY LIVE STATUS)
            today = date.today()
            for d in range(30):
                current_date = today - timedelta(days=d)
                if current_date.weekday() == 6: continue # Skip Sundays

                # LOGIC FOR TODAY (Make some people 'Active' so green dots appear)
                is_today = (d == 0)
                
                # Randomly decide status
                rand = random.random()
                
                if rand < 0.85: # Present
                    status = 'present'
                    in_time = time(9, random.randint(0, 59))
                    
                    if is_today:
                        # 50% chance they are still working (Green Dot)
                        # 50% chance they left early/finished (Red Dot but Present)
                        if random.random() > 0.5:
                            out_time = None # Still in office!
                            hours = 0
                        else:
                            out_time = time(18, 0)
                            hours = 9.0
                    else:
                        out_time = time(18, 0)
                        hours = 9.0

                elif rand < 0.95: # Late
                    status = 'late'
                    in_time = time(10, random.randint(30, 59))
                    
                    if is_today:
                        out_time = None # Still working
                        hours = 0
                    else:
                        out_time = time(18, 30)
                        hours = 7.5
                
                else: # Absent
                    status = 'absent'
                    in_time = None
                    out_time = None
                    hours = 0

                att = Attendance(
                    employee_id=emp.id,
                    date=current_date,
                    check_in=in_time,
                    check_out=out_time,
                    work_hours=hours,
                    status=status
                )
                db.session.add(att)

            # 6. Leaves (Mix of Statuses)
            if random.random() > 0.6: 
                l_type = random.choice(['Sick', 'Paid', 'Unpaid'])
                l_status = random.choice(['Approved', 'Rejected', 'Pending'])
                start_d = get_random_date(2025, 2025)
                
                leave = Leave(
                    employee_id=emp.id,
                    leave_type=l_type,
                    start_date=start_d,
                    end_date=start_d + timedelta(days=random.randint(1, 5)),
                    reason="Medical Emergency" if l_type == 'Sick' else "Family Vacation",
                    status=l_status
                )
                db.session.add(leave)

        db.session.commit()
        print("\n✅ SEEDING COMPLETE!")
        print("-" * 60)
        print("🛡️  ADMIN LOGIN (For Dashboard Grid):")
        print("   Email: admin@dayflow.com")
        print("   Pass:  password123")
        print("-" * 60)
        print("👔 HR LOGIN (Try this to see HR Features):")
        print(f"   Email: {hr_created[0][1]}")
        print("   Pass:  password123")
        print("-" * 60)
        print("👤 EMPLOYEE LOGIN (Try this for Personal View):")
        print(f"   Email: {regular_created[0][1]}")
        print("   Pass:  password123")
        print("-" * 60)

if __name__ == "__main__":
    seed_data()