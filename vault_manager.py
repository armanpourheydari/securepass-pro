"""
vault_manager.py
Manage password vault with master password verification
"""

import json
import os
from datetime import datetime

from crypto_utils import decrypt_password, encrypt_password

DATA_DIR = "data"
os.makedirs(DATA_DIR, exist_ok=True)
STORAGE_FILE = os.path.join(DATA_DIR, "passwords.vault")
VERIFICATION_FILE = os.path.join(DATA_DIR, "vault.verify")
VERIFICATION_PASSWORD = "SecurePassProMasterKey2024!"


def _get_verification_password() -> str:
    return VERIFICATION_PASSWORD


def create_vault(master_password: str) -> bool:
    try:
        verify_text = _get_verification_password()
        encrypted_verify = encrypt_password(verify_text, master_password)
        with open(VERIFICATION_FILE, "w", encoding="utf-8") as f:
            f.write(encrypted_verify)
        _save_vault({"passwords": [], "cards": []}, master_password)
        return True
    except Exception:
        return False


def verify_master_password(master_password: str) -> bool:
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
    return os.path.exists(STORAGE_FILE) and os.path.exists(VERIFICATION_FILE)


def _load_vault(master_password: str) -> dict:
    """Load and decrypt vault file. Returns dict with 'passwords' and 'cards'."""
    if not os.path.exists(STORAGE_FILE):
        return {"passwords": [], "cards": []}
    with open(STORAGE_FILE, "r", encoding="utf-8") as f:
        encrypted_data = f.read()
    try:
        decrypted = decrypt_password(encrypted_data, master_password)
        data = json.loads(decrypted)
        if isinstance(data, list):
            return {"passwords": data, "cards": []}
        if "passwords" not in data:
            data["passwords"] = []
        if "cards" not in data:
            data["cards"] = []
        return data
    except Exception:
        return {"passwords": [], "cards": []}


def _save_vault(data: dict, master_password: str) -> None:
    """Encrypt and save vault file. data must be a dict."""
    json_data = json.dumps(data, indent=2, ensure_ascii=False)
    encrypted = encrypt_password(json_data, master_password)
    with open(STORAGE_FILE, "w", encoding="utf-8") as f:
        f.write(encrypted)


def save_password_to_vault(name: str, password: str, master_password: str) -> bool:
    try:
        if not verify_master_password(master_password):
            return False
        data = _load_vault(master_password)
        for entry in data["passwords"]:
            if entry["name"].lower() == name.lower():
                entry["password"] = password
                _save_vault(data, master_password)
                return True
        entry = {"id": len(data["passwords"]) + 1, "name": name, "password": password}
        data["passwords"].append(entry)
        _save_vault(data, master_password)
        return True
    except Exception:
        return False


def get_all_passwords(master_password: str) -> list:
    try:
        if not verify_master_password(master_password):
            return []
        data = _load_vault(master_password)
        return data.get("passwords", [])
    except Exception:
        return []


def delete_password_from_vault(password_id: int, master_password: str) -> bool:
    try:
        if not verify_master_password(master_password):
            return False
        data = _load_vault(master_password)
        new_passwords = [p for p in data["passwords"] if p["id"] != password_id]
        if len(new_passwords) == len(data["passwords"]):
            return False
        data["passwords"] = new_passwords
        _save_vault(data, master_password)
        return True
    except Exception:
        return False


def update_password_in_vault(
    password_id: int, new_name: str, new_password: str, master_password: str
) -> bool:
    try:
        if not verify_master_password(master_password):
            return False
        data = _load_vault(master_password)
        for entry in data["passwords"]:
            if entry["id"] == password_id:
                entry["name"] = new_name
                entry["password"] = new_password
                _save_vault(data, master_password)
                return True
        return False
    except Exception:
        return False


def save_card_to_vault(
    card_name: str,
    card_number: str,
    card_holder: str,
    expiry_month: str,
    expiry_year: str,
    cvv: str,
    card_type: str,
    master_password: str,
) -> bool:
    try:
        if not verify_master_password(master_password):
            return False

        data = _load_vault(master_password)

        for card in data["cards"]:
            if card["name"].lower() == card_name.lower():
                return False

        encrypted_number = encrypt_password(card_number, master_password)
        encrypted_holder = encrypt_password(card_holder, master_password)
        encrypted_cvv = encrypt_password(cvv, master_password)

        entry = {
            "id": len(data["cards"]) + 1,
            "name": card_name,
            "type": card_type,
            "number": encrypted_number,
            "holder": encrypted_holder,
            "expiry_month": expiry_month,
            "expiry_year": expiry_year,
            "cvv": encrypted_cvv,
            "created": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        }

        data["cards"].append(entry)
        _save_vault(data, master_password)
        return True
    except Exception:
        return False


def get_all_cards(master_password: str) -> list:
    try:
        if not verify_master_password(master_password):
            return []
        data = _load_vault(master_password)
        cards = []
        for card in data.get("cards", []):
            card_copy = card.copy()
            try:
                card_copy["number"] = decrypt_password(card["number"], master_password)
                card_copy["holder"] = decrypt_password(card["holder"], master_password)
                card_copy["cvv"] = decrypt_password(card["cvv"], master_password)
            except Exception:
                card_copy["number"] = "••••"
                card_copy["holder"] = "••••"
                card_copy["cvv"] = "••••"
            cards.append(card_copy)
        return cards
    except Exception:
        return []


def delete_card_from_vault(card_id: int, master_password: str) -> bool:
    try:
        if not verify_master_password(master_password):
            return False
        data = _load_vault(master_password)
        new_cards = [c for c in data["cards"] if c["id"] != card_id]
        if len(new_cards) == len(data["cards"]):
            return False
        data["cards"] = new_cards
        _save_vault(data, master_password)
        return True
    except Exception:
        return False


def update_card_in_vault(
    card_id: int,
    card_name: str,
    card_number: str,
    card_holder: str,
    expiry_month: str,
    expiry_year: str,
    cvv: str,
    card_type: str,
    master_password: str,
) -> bool:
    try:
        if not verify_master_password(master_password):
            return False
        data = _load_vault(master_password)
        for card in data["cards"]:
            if card["id"] == card_id:
                card["name"] = card_name
                card["type"] = card_type
                card["number"] = card_number
                card["holder"] = card_holder
                card["expiry_month"] = expiry_month
                card["expiry_year"] = expiry_year
                card["cvv"] = cvv
                _save_vault(data, master_password)
                return True
        return False
    except Exception:
        return False
