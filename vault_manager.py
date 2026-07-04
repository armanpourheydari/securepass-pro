"""
vault_manager.py
Manage password vault with master password verification
"""

import json
import os

from crypto_utils import decrypt_password, encrypt_password

DATA_DIR = "data"
os.makedirs(DATA_DIR, exist_ok=True)
STORAGE_FILE = os.path.join(DATA_DIR, "passwords.vault")
VERIFICATION_FILE = os.path.join(DATA_DIR, "vault.verify")
VERIFICATION_PASSWORD = "SecurePassProMasterKey2024!"


def _get_verification_password() -> str:
    """Return the verification password"""
    return VERIFICATION_PASSWORD


def create_vault(master_password: str) -> bool:
    """Create a new vault with master password"""
    try:
        verify_text = _get_verification_password()
        encrypted_verify = encrypt_password(verify_text, master_password)
        with open(VERIFICATION_FILE, "w", encoding="utf-8") as f:
            f.write(encrypted_verify)
        _save_vault([], master_password)
        return True
    except Exception:
        return False


def verify_master_password(master_password: str) -> bool:
    """Verify if master password is correct"""
    if not os.path.exists(VERIFICATION_FILE):
        return False
    try:
        with open(VERIFICATION_FILE, "r", encoding="utf-8") as f:
            encrypted_verify = f.read()
        decrypted = decrypt_password(encrypted_verify, master_password)
        return decrypted == _get_verification_password()
    except Exception:
        return False


def vault_exists() -> bool:
    """Check if vault exists"""
    return os.path.exists(STORAGE_FILE) and os.path.exists(VERIFICATION_FILE)


def _load_vault(master_password: str) -> list:
    """Load and decrypt vault file"""
    if not os.path.exists(STORAGE_FILE):
        return []
    with open(STORAGE_FILE, "r", encoding="utf-8") as f:
        encrypted_data = f.read()
    try:
        decrypted = decrypt_password(encrypted_data, master_password)
        return json.loads(decrypted)
    except Exception:
        return []


def _save_vault(data: list, master_password: str) -> None:
    """Encrypt and save vault file"""
    json_data = json.dumps(data, indent=2, ensure_ascii=False)
    encrypted = encrypt_password(json_data, master_password)
    with open(STORAGE_FILE, "w", encoding="utf-8") as f:
        f.write(encrypted)


def save_password_to_vault(name: str, password: str, master_password: str) -> bool:
    """Save a password to the vault"""
    try:
        if not verify_master_password(master_password):
            return False
        data = _load_vault(master_password)
        for entry in data:
            if entry["name"].lower() == name.lower():
                entry["password"] = password
                _save_vault(data, master_password)
                return True
        entry = {"id": len(data) + 1, "name": name, "password": password}
        data.append(entry)
        _save_vault(data, master_password)
        return True
    except Exception:
        return False


def get_all_passwords(master_password: str) -> list:
    """Get all passwords from the vault (decrypted)"""
    try:
        if not verify_master_password(master_password):
            return []
        return _load_vault(master_password)
    except Exception:
        return []


def delete_password_from_vault(password_id: int, master_password: str) -> bool:
    """Delete a password from the vault by ID"""
    try:
        if not verify_master_password(master_password):
            return False
        data = _load_vault(master_password)
        new_data = [p for p in data if p["id"] != password_id]
        if len(new_data) == len(data):
            return False
        _save_vault(new_data, master_password)
        return True
    except Exception:
        return False


def update_password_in_vault(
    password_id: int, new_name: str, new_password: str, master_password: str
) -> bool:
    """Update a password in the vault"""
    try:
        if not verify_master_password(master_password):
            return False
        data = _load_vault(master_password)
        for entry in data:
            if entry["id"] == password_id:
                entry["name"] = new_name
                entry["password"] = new_password
                _save_vault(data, master_password)
                return True
        return False
    except Exception:
        return False
