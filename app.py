from flask import Flask
from extensions import db, login_manager 
from config import Config 
from flask_jwt_extended import JWTManager
from flask_cors import CORS 

# Import all Blueprints - FIXED NAMES HERE
from routes.auth_routes import auth_bp
from routes.employee_routes import employee_bp # Changed from emp_bp
from routes.attendance_routes import attendance_bp
from routes.leave_routes import leave_bp
from routes.payroll_routes import payroll_bp

app = Flask(__name__)
CORS(app) 

app.config.from_object(Config)

db.init_app(app)
jwt = JWTManager(app)
login_manager.init_app(app)

@app.route('/')
def home():
    return {"message": "DayFlow Backend is running!"}, 200

# Register Blueprints - FIXED NAMES HERE
app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(employee_bp, url_prefix='/api/employee') # Changed from emp_bp
app.register_blueprint(attendance_bp, url_prefix='/api/attendance')
app.register_blueprint(leave_bp, url_prefix='/api/leave')
app.register_blueprint(payroll_bp, url_prefix='/api/payroll')

if __name__ == '__main__':
    with app.app_context():
        db.create_all() # Synchronizes database with your models
    app.run(debug=True)