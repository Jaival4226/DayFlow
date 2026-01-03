import pytest

def test_login_id_generation(client):
    reg_payload = {
        "first_name": "John",
        "last_name": "Doe",
        "email": "j.doe@dayflow.com",
        "password": "SecurePassword123!",
        "role": "Employee"
    }
    response = client.post('/auth/register', json=reg_payload)
    assert response.status_code == 201
    assert "JODO" in response.json['employee_id']

def test_login_redirection(client):
    login_payload = {
        "email": "admin@dayflow.com",
        "password": "SecurePassword123!"
    }
    response = client.post('/auth/login', json=login_payload)
    assert response.status_code == 200
    assert response.json['redirect'] == '/dashboard'