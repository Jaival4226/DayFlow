def test_leave_application_with_types(client, employee_token):
    headers = {"Authorization": f"Bearer {employee_token}"}

    payload = {
        "leave_type": "Paid Time Off",
        "start_date": "2026-05-10",
        "end_date": "2026-05-12",
        "remarks": "Vacation",
        "has_attachment": False
    }
    response = client.post('/leave/apply', json=payload, headers=headers)
    assert response.status_code == 201
    assert response.json['status'] == "Pending"


def test_admin_leave_action_with_comments(client, admin_token):
    headers = {"Authorization": f"Bearer {admin_token}"}

    action_payload = {
        "status": "Rejected",
        "comments": "Insufficient staff on these dates"
    }
    response = client.post('/leave/update/1', json=action_payload, headers=headers)
    assert response.status_code == 200