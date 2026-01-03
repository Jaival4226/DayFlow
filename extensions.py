from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()

# Redirects users here if they try to access a protected page without logging in
login_manager.login_view = 'auth.login'
login_manager.login_message_category = 'warning'