from extensions import db, login_manager
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
import enum

class UserRole(enum.Enum):
    ADMIN = 'Admin'
    HR = 'HR'
    EMPLOYEE = 'Employee'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    employee_id_number = db.Column(db.String(20), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(256), nullable=False)
    role = db.Column(db.Enum(UserRole), default=UserRole.EMPLOYEE, nullable=False)
    is_verified = db.Column(db.Boolean, default=False)

    employee_profile = db.relationship('Employee', backref='user', uselist=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    @property
    def name(self):
        """Helper to get full name for templates"""
        if self.employee_profile:
            return f"{self.employee_profile.first_name} {self.employee_profile.last_name}"
        return self.email

    @property
    def is_manager(self):
        return self.role in [UserRole.ADMIN, UserRole.HR]

    @property
    def is_admin(self):
        return self.role == UserRole.ADMIN