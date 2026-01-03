from flask import Flask, render_template # MANDATORY: Added render_template
from extensions import db, login_manager 
from config import Config 
from flask_jwt_extended import JWTManager
from flask_cors import CORS 

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
jwt = JWTManager(app)
login_manager.init_app(app)

# --- FRONTEND ROUTES: These make the website show up ---
@app.route('/')
def home():
    return render_template('login.html')

@app.route('/login')
def login_page():
    return render_template('login.html')

@app.route('/dashboard')
def dashboard_page():
    return render_template('dashboard.html')

@app.route('/profile')
def profile_page():
    return render_template('profile.html')

@app.route('/attendance')
def attendance_page():
    return render_template('attendance.html')

@app.route('/leave')
def leave_page():
    return render_template('leave.html')

@app.route('/payroll')
def payroll_page():
    return render_template('payroll.html')

# --- API ROUTES ---
app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(employee_bp, url_prefix='/api/employee')
app.register_blueprint(attendance_bp, url_prefix='/api/attendance')
app.register_blueprint(leave_bp, url_prefix='/api/leave')
app.register_blueprint(payroll_bp, url_prefix='/api/payroll')

if __name__ == '__main__':
    app.run(debug=True)