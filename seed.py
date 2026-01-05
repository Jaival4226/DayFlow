from app import app
from extensions import db
from models.user import User, UserRole
from models.employee import Employee
from models.payroll import Payroll
from models.attendance import Attendance
from models.leave import Leave
from models.notification import Notification
from datetime import date, datetime, timedelta, time
import random
import string

# --- CONFIGURATION ---
TOTAL_STAFF = 30
HR_OFFICER_COUNT = 5  # 5 HRs
PASSWORD = "password123"

# --- DATA POOLS ---
FIRST_NAMES = ["Aarav", "Vihaan", "Aditya", "Sai", "Reyansh", "Diya", "Ananya", "Kiara", "Pari", "Myra", "Rohan", "Vikram", "Neha", "Pooja", "Arjun", "Ishaan", "Vivaan", "Saanvi", "Aadhya", "Zara", "Kabir", "Meera", "Riya", "Krishna", "Sarthak", "Nikhil", "Kavya", "Sneha", "Manish", "Priya"]
LAST_NAMES = ["Sharma", "Patel", "Verma", "Reddy", "Singh", "Nair", "Gupta", "Kapoor", "Khan", "Joshi", "Mehta", "Malhotra", "Iyer", "Kumar", "Das", "Chopra", "Desai", "Jain", "Mishra", "Rao", "Saxena", "Yadav", "Bhatia", "Chauhan", "Dutta", "Garg", "Hegde", "Jha", "Kaur", "Lal"]

REGULAR_DEPARTMENTS = ['Engineering', 'Sales', 'Marketing', 'Finance', 'Operations', 'Legal', 'Product', 'Design']
DESIGNATIONS = {
    'HR': ['HR Manager', 'Senior Recruiter', 'HR Business Partner', 'Talent Acquisition'], 
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
BANKS = ["HDFC Bank", "ICICI Bank", "SBI", "Axis Bank", "Kotak Mahindra", "Bank of Baroda"]

# --- HELPER FUNCTIONS ---
def generate_phone():
    return f"{random.choice(['9', '8', '7', '6'])}{random.randint(100000000, 999999999)}"

def generate_pan():
    # Format: ABCDE1234F
    chars = "".join(random.choices(string.ascii_uppercase, k=5))
    nums = "".join(random.choices(string.digits, k=4))
    last = random.choice(string.ascii_uppercase)
    return f"{chars}{nums}{last}"

def generate_ifsc(bank_name):
    prefix = bank_name[:4].upper().replace(" ", "")
    if len(prefix) < 4: prefix = prefix.ljust(4, 'X')
    return f"{prefix}000{random.randint(1000, 9999)}"

def get_random_date(start_year=2020, end_year=2024):
    start = date(start_year, 1, 1)
    end = date(end_year, 12, 31)
    return start + timedelta(days=random.randint(0, (end - start).days))

# --- MAIN SEED LOGIC ---
def seed_data():
    with app.app_context():
        print("🗑️  Cleaning Database...")
        db.drop_all()
        db.create_all()

        users_created = [] # Store for final print output

        print("🚀 Creating Super Admin...")
        # 1. ADMIN USER
        admin_user = User(employee_id_number="OIADMIN001", email="admin@dayflow.com", role=UserRole.ADMIN, is_verified=True)
        admin_user.set_password(PASSWORD)
        db.session.add(admin_user)
        db.session.flush()

        admin_profile = Employee(
            user_id=admin_user.id,
            first_name="Super", last_name="Admin", designation="System Administrator", department="IT",
            date_of_joining=date(2020, 1, 1), phone=generate_phone(), monthly_wage=250000,
            address="HQ Server Room, New Delhi", profile_picture="default.jpg",
            # New Fields
            gender="Male", marital_status="Single", 
            bank_name="HDFC Bank", account_number="501000999888", ifsc_code="HDFC0001234", pan_number="ADMIN1234X",
            emergency_contact="IT Support: 1800-123-456"
        )
        db.session.add(admin_profile)
        
        # Add a Notification for Admin
        db.session.add(Notification(message="System initialized successfully.", type="Info"))
        
        users_created.append(["Super Admin", "admin@dayflow.com", "OIADMIN001", "ADMIN"])

        print(f"🌱 Generating {TOTAL_STAFF} Staff Members...")
        
        for i in range(TOTAL_STAFF):
            first = FIRST_NAMES[i % len(FIRST_NAMES)]
            last = LAST_NAMES[i % len(LAST_NAMES)]
            
            # Determine Role
            if i < HR_OFFICER_COUNT:
                role = UserRole.HR
                dept = 'HR'
                designation = DESIGNATIONS['HR'][i % len(DESIGNATIONS['HR'])]
                prefix = "HR"
                role_label = "HR"
            else:
                role = UserRole.EMPLOYEE
                dept = random.choice(REGULAR_DEPARTMENTS)
                designation = random.choice(DESIGNATIONS.get(dept, ['Associate']))
                prefix = "OI"
                role_label = "Employee"

            # Unique ID & Email
            serial = str(i+1).zfill(3)
            emp_id = f"{prefix}{first[:2].upper()}{last[:2].upper()}2026{serial}"
            email = f"{first.lower()}.{last.lower()}{random.randint(10,99)}@{random.choice(DOMAINS)}"

            # Create User
            user = User(employee_id_number=emp_id, email=email, role=role, is_verified=True)
            user.set_password(PASSWORD)
            db.session.add(user)
            db.session.flush()

            # Generate Financials
            wage = random.randint(35000, 180000)
            bank = random.choice(BANKS)
            
            # Create Employee Profile
            emp = Employee(
                user_id=user.id,
                first_name=first, last_name=last, designation=designation, department=dept,
                date_of_joining=get_random_date(2022, 2025), phone=generate_phone(),
                monthly_wage=wage, address=f"Flat {random.randint(101, 909)}, Block {random.choice(['A','B','C'])}, City Center",
                profile_picture="default.jpg",
                
                # Full Personal Details
                gender=random.choice(["Male", "Female"]),
                marital_status=random.choice(["Single", "Married", "Single"]),
                date_of_birth=get_random_date(1990, 2002),
                emergency_contact=f"Parent/Spouse: {generate_phone()}",
                
                # Full Financial Details
                bank_name=bank,
                account_number=str(random.randint(100000000000, 999999999999)),
                ifsc_code=generate_ifsc(bank),
                pan_number=generate_pan()
            )
            db.session.add(emp)
            db.session.flush() # Need ID for related tables

            # --- ADD PAYROLL (Oct, Nov, Dec) ---
            # ... (imports remain the same)

# Locate the "4. Payroll" section in seed_data() and replace the loop with:

            # 4. Payroll (Last 3 Months)
            months = [("October", 2025), ("November", 2025), ("December", 2025)]
            for m_name, m_year in months:
                # Calculations
                basic = wage * 0.50
                hra = wage * 0.20
                da = wage * 0.10
                medical = wage * 0.20
                
                pf = basic * 0.12
                pt = 200.0
                
                net = (basic + hra + da + medical) - (pf + pt)
                
                payroll = Payroll(
                    employee_id=emp.id,
                    month=m_name,
                    year=m_year,
                    basic_salary=round(basic, 2),
                    hra=round(hra, 2),
                    da=round(da, 2),
                    medical_allowance=round(medical, 2),
                    pf=round(pf, 2),
                    professional_tax=round(pt, 2),
                    other_deductions=0,
                    net_salary=round(net, 2),
                    generated_on=datetime(m_year, 12, 28)
                )
                db.session.add(payroll)

# ... (rest of the file remains the same)
            # --- ADD ATTENDANCE (Last 30 Days) ---
            today = date.today()
            for d in range(30):
                dt = today - timedelta(days=d)
                if dt.weekday() == 6: continue # Skip Sundays
                
                rand = random.random()
                is_today = (d == 0)
                
                status = 'absent'
                check_in = None
                check_out = None
                hours = 0.0

                if rand < 0.85: # Present
                    status = 'present'
                    check_in = time(9, random.randint(0, 45))
                    if is_today:
                         # Live status: 50% chance still working
                         if random.random() > 0.5: check_out = None
                         else: 
                             check_out = time(18, 0)
                             hours = 9.0
                    else:
                        check_out = time(18, 0)
                        hours = 9.0
                elif rand < 0.95: # Late
                    status = 'late'
                    check_in = time(10, random.randint(0, 30))
                    if not is_today:
                        check_out = time(18, 30)
                        hours = 8.0
                
                if status != 'absent':
                    db.session.add(Attendance(
                        employee_id=emp.id, date=dt, check_in=check_in, 
                        check_out=check_out, work_hours=hours, status=status
                    ))

            # --- ADD LEAVES (Random History) ---
            if random.random() > 0.6:
                l_status = random.choice(['Approved', 'Pending', 'Rejected'])
                start_d = get_random_date(2025, 2025)
                db.session.add(Leave(
                    employee_id=emp.id, leave_type=random.choice(['Sick', 'Paid']),
                    start_date=start_d, end_date=start_d + timedelta(days=2),
                    reason="Personal work", status=l_status, applied_on=start_d - timedelta(days=5)
                ))

            # Store for display (Save top 10)
            if i < 10: 
                users_created.append([f"{first} {last}", email, emp_id, role_label])

        db.session.commit()
        
        # --- PRINT LOGIN CHEAT SHEET ---
        print("\n" + "="*95)
        print(f"{'NAME':<20} | {'EMAIL (LOGIN ID)':<35} | {'EMP ID':<15} | {'ROLE':<10}")
        print("="*95)
        
        # Print Admin
        u = users_created[0]
        print(f"{u[0]:<20} | {u[1]:<35} | {u[2]:<15} | {u[3]:<10}")
        print("-" * 95)
        
        # Print HRs (Next 5)
        for u in users_created[1:6]:
             print(f"{u[0]:<20} | {u[1]:<35} | {u[2]:<15} | {u[3]:<10}")
        print("-" * 95)
        
        # Print Employees
        for u in users_created[6:]:
             print(f"{u[0]:<20} | {u[1]:<35} | {u[2]:<15} | {u[3]:<10}")
             
        print("="*95)
        print(f"🔑 PASSWORD FOR EVERYONE: {PASSWORD}")
        print("="*95 + "\n")

if __name__ == "__main__":
    seed_data()