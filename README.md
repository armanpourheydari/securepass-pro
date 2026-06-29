# 🔐 SecurePass Pro

<div align="center">

**Enterprise-grade password management tool with generator and strength checker**

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![PyQt6](https://img.shields.io/badge/PyQt6-6.5.0+-green.svg)](https://riverbankcomputing.com/software/pyqt/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

</div>

---

## 📖 About

SecurePass Pro is a powerful desktop application for **generating secure passwords** and **checking password strength**. It provides real-time feedback, detailed suggestions, and a modern dark-themed GUI.

**Perfect for:** Individuals, developers, and organizations who want to improve their password security.

---

## ✨ Features

### 🔐 Password Generator
- Generate strong, random passwords (6-40 characters)
- Real-time strength meter with animated progress bar
- Copy to clipboard with one click
- Password history with export (TXT / Excel)

### 🛡️ Password Checker
- Analyze password strength with 0-100 scoring
- Check for:
  - Common words and patterns
  - Keyboard sequences (qwerty, asdf)
  - Sequential numbers (123, 456)
  - Character variety (uppercase, lowercase, digits, symbols)
- Get actionable improvement suggestions
- Export security report as TXT

### 📊 Scoring System

| Score Range | Level | Status |
|-------------|-------|--------|
| 85-100 | 🔵 Excellent | Very Strong |
| 70-84  | 🟢 Good      | Strong |
| 50-69  | 🟡 Medium    | Decent |
| 30-49  | 🟠 Weak      | Needs improvement |
| 0-29   | 🔴 Very Weak | Change immediately |

---

## 🚀 Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### 1. Clone the repository and run program

```bash
git clone https://github.com/armanpourheydari/securepass-pro.git
cd securepass-pro
python main.py