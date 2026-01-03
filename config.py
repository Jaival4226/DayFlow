import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Database Configuration
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Security Configuration
    JWT_SECRET_KEY = os.getenv('SECRET_KEY')
    SECRET_KEY = os.getenv('SECRET_KEY')