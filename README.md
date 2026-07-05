# 🔐 SecurePass Pro

<div align="center">

**Enterprise-grade password management tool with generator, strength checker, and secure vault**

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![PyQt6](https://img.shields.io/badge/PyQt6-6.5.0+-green.svg)](https://riverbankcomputing.com/software/pyqt/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Encryption](https://img.shields.io/badge/Encryption-AES--256--GCM-blueviolet.svg)](https://en.wikipedia.org/wiki/Advanced_Encryption_Standard)

</div>

---

## 📖 About

SecurePass Pro is a powerful desktop application for **generating secure passwords**, **checking password strength**, and **securely storing them** in an encrypted vault. It provides real-time feedback, detailed suggestions, and a modern dark-themed GUI.

**Perfect for:** Individuals, developers, and organizations who want to improve their password security.

---

## ✨ Features

### 🔐 Password Generator
- Generate strong, random passwords (6-40 characters)
- Real-time strength meter with animated progress bar
- Copy to clipboard with one click

### 🛡️ Password Checker
- Analyze password strength with 0-100 scoring
- Check for:
  - Common words and patterns
  - Keyboard sequences (qwerty, asdf)
  - Sequential numbers (123, 456)
  - Character variety (uppercase, lowercase, digits, symbols)
- Get actionable improvement suggestions

### 📂 Secure Vault
- Save passwords with **AES-256 encryption**
- Master password protection
- View, edit, and delete saved passwords
- Single-click copy from vault
- Export vault as TXT or Excel
- Double-click to edit entries

### 💳 Card Manager
- Save credit/debit card information securely
- AES-256-GCM encryption for sensitive data (card number, CVV, holder name)
- View masked card numbers (only last 4 digits visible)
- Export cards as TXT or Excel

### 📝 Secure Notes
- Store encrypted text notes
- Title, full content, and preview columns
- Preview button to view full content in a popup
- Double-click to edit notes
- Export notes as TXT or Excel

### 📊 Scoring System

| Score Range | Level | Status |
|-------------|-------|--------|
| 85-100 | 🔵 Excellent | Very Strong |
| 70-84  | 🟢 Good      | Strong |
| 50-69  | 🟡 Medium    | Decent |
| 30-49  | 🟠 Weak      | Needs improvement |
| 0-29   | 🔴 Very Weak | Change immediately |

---

## 🏗️ Project Structure

```
securepass-pro
├── .git
├── .gitignore
├── LICENSE
├── README.md
├── common_passwords.py
├── controller.py
├── crypto_utils.py
├── data
├── gui.py
├── logic.py
├── main.py
├── pyproject.toml
├── requirements.txt
├── tests
│   ├── __init__.py
│   ├── test_crypto.py
│   ├── test_logic.py
│   └── test_vault.py
└── vault_manager.py
```

---

## 🚀 Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### 1. Clone the repository

```bash
git clone https://github.com/armanpourheydari/securepass-pro.git
cd securepass-pro
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Run the application

```bash
python main.py
```

---

## 🔒 Security

- **AES-256-GCM** encryption for all stored passwords, cards, and notes
- Master password is **never stored** (only verification token)
- All encryption happens **locally** on your device
- No data is ever sent to any server

---

## 🧪 Running Tests

```bash
python -m unittest discover tests/
```

---

## 🤝 Contributing

Contributions are welcome! Feel free to open issues or submit pull requests.

---

## 📜 License

Distributed under the MIT License. See [LICENSE](LICENSE) for more information.

---

## 📧 Contact

GitHub: [@armanpourheydari](https://github.com/armanpourheydari)  
Email: [arman.pourheydari@gmail.com](mailto:arman.pourheydari@gmail.com)  
Project Link: [https://github.com/armanpourheydari/securepass-pro](https://github.com/armanpourheydari/securepass-pro)

---

<div align="center">

**Made with ❤️ for better password security**

</div>
