from flask import Flask
from extensions import db, login_manager # Included login_manager for User model
from config import Config 
from flask_jwt_extended import JWTManager
from flask_cors import CORS # Highly recommended for frontend connection

# Import all Blueprints
from routes.auth_routes import auth_bp
from routes.employee_routes import emp_bp
from routes.attendance_routes import attendance_bp
from routes.leave_routes import leave_bp
from routes.payroll_routes import payroll_bp

app = Flask(__name__)
CORS(app) # Allows Jaival's frontend to talk to your backend

# Apply Configuration
app.config.from_object(Config)

# Initialize Extensions
db.init_app(app)
jwt = JWTManager(app)
login_manager.init_app(app)

@app.route('/')
def home():
    return {"message": "DayFlow Backend is running!"}, 200

# Register Blueprints with clean URL prefixes
app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(emp_bp, url_prefix='/api/employee')
app.register_blueprint(attendance_bp, url_prefix='/api/attendance')
app.register_blueprint(leave_bp, url_prefix='/api/leave')
app.register_blueprint(payroll_bp, url_prefix='/api/payroll')

if __name__ == '__main__':
    with app.app_context():
        # This creates all tables in PostgreSQL based on your models
        db.create_all()
    app.run(debug=True)