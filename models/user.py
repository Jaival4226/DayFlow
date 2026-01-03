from extensions import db, login_manager
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
import enum

# Define strict roles
class UserRole(enum.Enum):
    ADMIN = 'Admin'       # Full Access (Manages employees, approves leave)
    HR = 'HR'             # Full Access (Same privileges as Admin)
    EMPLOYEE = 'Employee' # Limited Access (View profile, apply for leave)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    
    # Auth Details
    employee_id_number = db.Column(db.String(20), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(256), nullable=False)
    
    # Role Management
    role = db.Column(db.Enum(UserRole), default=UserRole.EMPLOYEE, nullable=False)
    
    # Security: Email Verification
    is_verified = db.Column(db.Boolean, default=False)

    # Relationship to Employee Profile
    employee_profile = db.relationship('Employee', backref='user', uselist=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    # --- Helper Methods for Access Control ---
    
    @property
    def is_manager(self):
        """Returns True if user is Admin OR HR."""
        return self.role in [UserRole.ADMIN, UserRole.HR]

    @property
    def is_admin(self):
        """Strictly checks for Admin role."""
        return self.role == UserRole.ADMIN