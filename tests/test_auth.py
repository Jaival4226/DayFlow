def test_employee_id_format(client):
    payload = {
        "first_name": "Alice",
        "last_name": "Smith",
        "email": "alice@dayflow.com",
        "password": "SecurePassword123!",
        "role": "Employee"
    }
    response = client.post('/auth/register', json=payload)
    assert response.status_code == 201
    assert response.json['employee_id'].startswith("ALSM")

def test_login_persistence(client):
    response = client.post('/auth/login', json={
        "email": "alice@dayflow.com",
        "password": "SecurePassword123!"
    })
    assert response.status_code == 200
    assert "access_token" in response.json