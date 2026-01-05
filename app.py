from flask import Flask, render_template
from extensions import db, login_manager
from config import Config
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from flask_migrate import Migrate # NEW: Import Migrate

# Import Blueprints
from routes.auth_routes import auth_bp
from routes.employee_routes import employee_bp
from routes.attendance_routes import attendance_bp
from routes.leave_routes import leave_bp
from routes.payroll_routes import payroll_bp

app = Flask(__name__)
CORS(app)
app.config.from_object(Config)

db.init_app(app)
migrate = Migrate(app, db) # NEW: Initialize Migrate
jwt = JWTManager(app)
login_manager.init_app(app)

# ... (rest of your file remains the same)

# --- FRONTEND ROUTES: These make the website show up ---
# @app.route('/')
# def home():
#     return render_template('login.html')

# Add this under your other page routes (around line 30)
@app.route('/signup')
def signup_page():
    return render_template('signup.html')

@app.route('/login')
def login_page():
    return render_template('login.html')

# @app.route('/dashboard')
# def dashboard_page():
#     return render_template('dashboard.html')

# @app.route('/profile')
# def profile_page():
#     return render_template('profile.html')

@app.route('/attendance')
def attendance_page():
    return render_template('attendance.html')

@app.route('/leave')
def leave_page():
    return render_template('leave.html')

@app.route('/payroll')
def payroll_page():
    return render_template('payroll.html')

# ... (imports remain the same)
from flask_login import login_required, current_user
from services.attendance_service import AttendanceService

# ... (setup code remains the same)

# --- FRONTEND ROUTES ---
@app.route('/')
def home():
    if current_user.is_authenticated:
        return render_template('dashboard.html')
    return render_template('login.html')

from models.user import User, UserRole # Ensure UserRole is imported

# ... (other imports)

@app.route('/dashboard')
@login_required
def dashboard_page():
    # 1. Get Status for EVERYONE (So the button works)
    status = AttendanceService.get_employee_current_status(current_user.employee_profile.id)
    
    # 2. Get History (Optional for Admin, but good to have)
    history = AttendanceService.get_employee_history(current_user.employee_profile.id)[:5]

    if current_user.role in [UserRole.ADMIN, UserRole.HR]:
        # PASS 'status' variable here!
        return render_template('dashboard.html', user_role='admin', status=status)
    
    return render_template('dashboard.html', user_role='employee', status=status, history=history)
# Route to view YOUR OWN profile
@app.route('/profile')
@login_required
def profile_page():
    return render_template('profile.html', emp=current_user.employee_profile)

# NEW: Route to view OTHER PEOPLE'S profiles (by clicking dashboard cards)
@app.route('/profile/<string:emp_id>')
@login_required
def view_other_profile(emp_id):
    # Find the user by their ID (e.g., OIMADE2026...)
    target_user = User.query.filter_by(employee_id_number=emp_id).first_or_404()
    return render_template('profile.html', emp=target_user.employee_profile)

# ... (keep other routes)

# --- API ROUTES ---
app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(employee_bp, url_prefix='/api/employee')
app.register_blueprint(attendance_bp, url_prefix='/api/attendance')
app.register_blueprint(leave_bp, url_prefix='/api/leave')
app.register_blueprint(payroll_bp, url_prefix='/api/payroll')

if __name__ == '__main__':
    app.run(debug=True)