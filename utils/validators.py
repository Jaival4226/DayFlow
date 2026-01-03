import re

class Validators:
    @staticmethod
    def is_valid_email(email):
        pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        return re.match(pattern, email) is not None

    @staticmethod
    def is_strong_password(password):
        # Minimum 6 characters (you can make this stricter for a real app)
        return len(password) >= 6