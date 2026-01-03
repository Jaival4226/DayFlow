def test_attendance_indicator_logic(client, employee_token):
    headers = {"Authorization": f"Bearer {employee_token}"}

    status = client.get('/attendance/status', headers=headers)
    assert status.json['dot_color'] == 'red'

    client.post('/attendance/check-in', headers=headers)

    updated = client.get('/attendance/status', headers=headers)
    assert updated.json['dot_color'] == 'green'


def test_rbac_attendance_view(client, employee_token):
    headers = {"Authorization": f"Bearer {employee_token}"}
    response = client.get('/attendance/all-employees', headers=headers)
    assert response.status_code == 403