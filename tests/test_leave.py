def test_leave_workflow(client, employee_token, admin_token):
    emp_headers = {"Authorization": f"Bearer {employee_token}"}
    adm_headers = {"Authorization": f"Bearer {admin_token}"}

    leave_app = client.post('/leave/apply', headers=emp_headers, json={
        "type": "Paid Time Off",
        "start_date": "2026-05-01",
        "end_date": "2026-05-03"
    })
    leave_id = leave_app.json['id']

    client.post(f'/leave/approve/{leave_id}', headers=adm_headers, json={
        "status": "Approved",
        "remarks": "Approved by HR"
    })

    final_status = client.get(f'/leave/status/{leave_id}', headers=emp_headers)
    assert final_status.json['status'] == "Approved"