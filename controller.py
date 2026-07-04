"""
controller.py
Bridge between GUI and Logic
"""

from logic import check_password, generate_password
from vault_manager import (
    create_vault,
    delete_password_from_vault,
    get_all_passwords,
    save_password_to_vault,
    update_password_in_vault,
    vault_exists,
    verify_master_password,
)


class PasswordController:
    """Controller that connects GUI with Logic"""

    def __init__(self):
        self._master_password = None

    # ========== BASIC ==========
    def generate(self, length: int) -> str:
        return generate_password(length)

    def check(self, password: str) -> dict:
        return check_password(password)

    # ========== MASTER PASSWORD ==========
    def set_master_password(self, password: str) -> None:
        self._master_password = password

    def verify_password(self, password: str) -> bool:
        """Verify if master password is correct"""
        return verify_master_password(password)

    def create_new_vault(self, password: str) -> bool:
        """Create a new vault with master password"""
        return create_vault(password)

    def vault_exists(self) -> bool:
        """Check if vault exists"""
        return vault_exists()

    def is_unlocked(self) -> bool:
        return self._master_password is not None

    # ========== VAULT ==========
    def save_password(self, name: str, password: str) -> bool:
        if not self._master_password:
            raise ValueError("Master password not set!")
        return save_password_to_vault(name, password, self._master_password)

    def get_passwords(self) -> list:
        if not self._master_password:
            raise ValueError("Master password not set!")
        return get_all_passwords(self._master_password)

    def delete_password(self, password_id: int) -> bool:
        if not self._master_password:
            raise ValueError("Master password not set!")
        return delete_password_from_vault(password_id, self._master_password)

    def update_password(
        self, password_id: int, new_name: str, new_password: str
    ) -> bool:
        if not self._master_password:
            raise ValueError("Master password not set!")
        return update_password_in_vault(
            password_id, new_name, new_password, self._master_password
        )
