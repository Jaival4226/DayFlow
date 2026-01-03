def test_salary_calculation_logic(client, admin_token):
    headers = {"Authorization": f"Bearer {admin_token}"}

    payload = {"monthly_gross": 50000}
    response = client.post('/payroll/calculate', json=payload, headers=headers)

    data = response.json
    assert data['basic'] == 20000
    assert data['hra'] == 10000
    assert data['conveyance'] == 1600


def test_payroll_tab_visibility(client, employee_token):
    headers = {"Authorization": f"Bearer {employee_token}"}
    response = client.get('/employee/profile/tabs', headers=headers)

    tabs = response.json['available_tabs']
    assert "Salary Info" not in tabs