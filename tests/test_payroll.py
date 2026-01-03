def test_salary_component_accuracy(client, admin_token):
    headers = {"Authorization": f"Bearer {admin_token}"}
    payload = {"monthly_gross": 100000}

    response = client.post('/payroll/calculate', json=payload, headers=headers)
    data = response.json

    assert data['basic'] == 40000
    assert data['hra'] == 20000
    assert data['pf'] == 4800


def test_employee_payroll_lock(client, employee_token):
    headers = {"Authorization": f"Bearer {employee_token}"}
    response = client.put('/payroll/update-structure/EMP001', headers=headers)
    assert response.status_code == 403