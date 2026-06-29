"""
main controller for connect logic.py and gui.py
"""
from logic import check_password, generate_password


class PasswordController:
    "main calss for use password functions"
    def generate(self, length) -> str:
        "call function of generation"
        return generate_password(length)
    def check(self, password : str) -> dict:
        "call function of checking"
        return check_password(password)
