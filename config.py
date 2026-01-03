import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # 1. Basic Flask Config
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-key-please-change'
    
    # 2. Database Config
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # 3. Security Enhancements
    # Session Cookie Security (Prevents JS access & CSRF)
    SESSION_COOKIE_HTTPONLY = True 
    SESSION_COOKIE_SAMESITE = 'Lax' 
    # Only set Secure to True if you are using HTTPS (Production)
    SESSION_COOKIE_SECURE = os.environ.get('FLASK_ENV') == 'production'
    
    # 4. File Upload Config
    MAX_CONTENT_LENGTH = 2 * 1024 * 1024  # Max 2MB for profile pics