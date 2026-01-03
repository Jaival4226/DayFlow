from flask import Flask, render_template
from config import Config
from extensions import db, migrate, login_manager

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize Extensions
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)

    # Import Models so Migrate detects them
    from models import User, Employee, Attendance, Leave, Payroll

    # Register Blueprints (We will build these in Phase 2)
    # from routes.auth_routes import auth_bp
    # app.register_blueprint(auth_bp)

    @app.route('/')
    def index():
        return "Dayflow HRMS API is Running."

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)