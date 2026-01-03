def test_attendance_status_indicator(client, employee_token):
    headers = {"Authorization": f"Bearer {employee_token}"}

    initial_status = client.get('/attendance/status', headers=headers)
    assert initial_status.json['dot_color'] == 'red'

    client.post('/attendance/check-in', headers=headers)

    updated_status = client.get('/attendance/status', headers=headers)
    assert updated_status.json['dot_color'] == 'green'
    assert updated_status.json['status'] == 'Present'


def test_admin_view_all_attendance(client, admin_token):
    headers = {"Authorization": f"Bearer {admin_token}"}
    response = client.get('/attendance/list/admin', headers=headers)
    assert response.status_code == 200
    assert isinstance(response.json['records'], list)