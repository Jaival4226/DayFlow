import os
from dotenv import load_dotenv

# Find the absolute path of the folder containing this file
basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))

class Config:
    # 1. DATABASE CONFIGURATION
    # If DATABASE_URL exists in .env, use it. 
    # Otherwise, automatically create an absolute path to instance/app.db
    env_db_url = os.getenv('DATABASE_URL')
    
    if env_db_url:
        SQLALCHEMY_DATABASE_URI = env_db_url
    else:
        # This creates a robust absolute path for Windows (S:/Code/Hackathon/...)
        instance_path = os.path.join(basedir, 'instance', 'app.db')
        SQLALCHEMY_DATABASE_URI = 'sqlite:///' + instance_path
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # 2. SECURITY CONFIGURATION
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'dev-jwt-key-123')
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-123')