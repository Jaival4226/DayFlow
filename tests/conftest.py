import pytest
from app import create_app
from extensions import db
from models.user import User

@pytest.fixture(scope='session')
def app():
    app = create_app('testing')
    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def admin_token(client):
    client.post('/auth/register', json={
        "first_name": "Admin",
        "last_name": "User",
        "email": "hr@dayflow.com",
        "password": "SecurePassword123!",
        "role": "HR"
    })
    response = client.post('/auth/login', json={
        "email": "hr@dayflow.com",
        "password": "SecurePassword123!"
    })
    return response.json['access_token']

@pytest.fixture
def employee_token(client):
    client.post('/auth/register', json={
        "first_name": "John",
        "last_name": "Doe",
        "email": "john@dayflow.com",
        "password": "Password123!",
        "role": "Employee"
    })
    response = client.post('/auth/login', json={
        "email": "john@dayflow.com",
        "password": "Password123!"
    })
    return response.json['access_token']