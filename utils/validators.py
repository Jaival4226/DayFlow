import re
from email_validator import validate_email, EmailNotValidError

def validate_registration_data(email, password, employee_id):
    """
    Returns a list of error strings. If list is empty, data is valid.
    """
    errors = []

    # [cite_start]1. Email Validation [cite: 30, 34]
    try:
        validate_email(email)
    except EmailNotValidError:
        errors.append("Invalid email format.")

    # [cite_start]2. Password Strength (Minimum 8 chars, 1 Upper, 1 Number, 1 Special) [cite: 33]
    if len(password) < 8:
        errors.append("Password must be at least 8 characters long.")
    if not re.search(r"[A-Z]", password):
        errors.append("Password must contain at least one uppercase letter.")
    if not re.search(r"\d", password):
        errors.append("Password must contain at least one number.")
    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        errors.append("Password must contain at least one special character.")

    # 3. Employee ID Sanity Check
    if not employee_id.isalnum():
        errors.append("Employee ID should only contain letters and numbers.")

    return errors