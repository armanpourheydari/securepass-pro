"""
Password Generator and Checker Tool
A simple tool to generate strong passwords and check their security level.
"""

import random
import string

from common_passwords import COMMON_PASSWORDS

ALL_CHARS = string.ascii_letters + string.digits + "!@#$%^&*()-_=+"
KEYBOARD_PATTERNS = [
    # ========== ROW 1: QWERTYUIOP ==========
    # 3 chars
    "qwe", "wer", "ert", "rty", "tyu", "yui", "uio", "iop",
    # 4 chars
    "qwer", "wert", "erty", "rtyu", "tyui", "yuio", "uiop",
    # 5 chars
    "qwert", "werty", "ertyu", "rtyui", "tyuio", "yuiop",
    # 6 chars
    "qwerty", "wertyu", "ertyui", "rtyuio", "tyuiop",
    # 7 chars
    "qwertyu", "wertyui", "ertyuiop",
    # 8 chars
    "qwertyui", "wertyuio",
    # 9 chars
    "qwertyuio", "wertyuiop",
    # 10 chars
    "qwertyuiop",

    # ========== ROW 2: ASDFGHJKL ==========
    # 3 chars
    "asd", "sdf", "dfg", "fgh", "ghj", "hjk", "jkl",
    # 4 chars
    "asdf", "sdfg", "dfgh", "fghj", "ghjk", "hjkl",
    # 5 chars
    "asdfg", "sdfgh", "dfghj", "fghjk", "ghjkl",
    # 6 chars
    "asdfgh", "sdfghj", "dfghjk", "fghjkl",
    # 7 chars
    "asdfghj", "sdfghjk", "dfghjkl",
    # 8 chars
    "asdfghjk", "sdfghjkl",
    # 9 chars
    "asdfghjkl",

    # ========== ROW 3: ZXCVBNM ==========
    # 3 chars
    "zxc", "xcv", "cvb", "vbn", "bnm",
    # 4 chars
    "zxcv", "xcvb", "cvbn", "vbnm",
    # 5 chars
    "zxcvb", "xcvbn", "cvbnm",
    # 6 chars
    "zxcvbn", "xcvbnm",
    # 7 chars
    "zxcvbnm",

    # ========== VERTICAL PATTERNS ==========
    # 3 chars (vertical)
    "qaz", "wsx", "edc", "rfv", "tgb", "yhn", "ujm",
    # 4 chars (vertical)
    "qazx", "wsxc", "edcv", "rfvb", "tgbn", "yhnm",
    # 5 chars (vertical)
    "qazxs", "wsxed", "edcrf", "rfvtg", "tgbyh", "yhnuj",
    # 6 chars (vertical)
    "qazxsw", "wsxedc", "edcrfv", "rfvtgb", "tgbyhn", "yhnujm",

    # ========== DIAGONAL PATTERNS ==========
    "qazxsw", "wsxedc", "edcrfv", "rfvtgb", "tgbyhn", "yhnujm",
    "qazwsx", "wsxedc", "edcrfv", "rfvtgb", "tgbyhn", "yhnujm",
    "qazxswed", "wsxedcrf", "edcrfvtg", "rfvtgbyh", "tgbyhnuj",

    # ========== REVERSE PATTERNS ==========
    # Reverse row 1
    "poi", "oiu", "iuy", "uyt", "ytr", "tre", "rew", "ewq",
    "poiu", "oiuy", "iuyt", "uytr", "ytre", "trew", "rewq",
    "poiuy", "oiuyt", "iuytre", "uytrew", "ytrewq",
    "poiuyt", "oiuytre", "iuytrew", "uytrewq",
    "poiuytre", "oiuytrew", "iuytrewq",
    "poiuytrew", "oiuytrewq",
    "poiuytrewq",

    # Reverse row 2
    "lkj", "kjh", "jhg", "hgf", "gfd", "fds", "dsa",
    "lkjh", "kjhg", "jhgf", "hgfd", "gfds", "fdsa",
    "lkjhg", "kjhgf", "jhgfd", "hgfds", "gfdsa",
    "lkjhgf", "kjhgfd", "jhgfds", "hgfdsa",
    "lkjhgfdsa",

    # Reverse row 3
    "mnb", "nbv", "bvc", "vcx", "cxz",
    "mnbv", "nbvc", "bvcx", "vcxz",
    "mnbvc", "nbvcx", "bvcxz",
    "mnbvcx", "nbvcxz",
    "mnbvcxz",
]


def show_length_guide():
    "Show the input text in terminal"
    print("""
╔══════════════════════════════════════════════════════════════════╗
║                   🔐  PASSWORD LENGTH GUIDE                    ║
╠══════════════════════════════════════════════════════════════════╣
║                                                                ║
║  ┌────────────┬─────────────────────┬────────────────────────┐ ║
║  │  LENGTH    │  SECURITY LEVEL     │  ESTIMATED CRACK TIME  │ ║
║  ├────────────┼─────────────────────┼────────────────────────┤ ║
║  │  8         │  🔴 Weak            │  Hours                 │ ║
║  │  10        │  🟡 Medium          │  Days                  │ ║
║  │  12        │  🟢 Good            │  ~200 years            │ ║
║  │  14        │  🟢 Strong          │  ~10,000 years         │ ║
║  │  16        │  🔵 Very Strong     │  ~1 billion years      │ ║
║  │  20        │  🏆 Unbreakable     │  Impossible!           │ ║
║  └────────────┴─────────────────────┴────────────────────────┘ ║
║                                                                ║
║  💡  PRO TIP: Minimum 12 characters for decent security      ║
║  ⭐  RECOMMENDED: 16 characters for maximum security         ║
║  🔥  Press ENTER for default (16 characters)                 ║
║                                                                ║
╚══════════════════════════════════════════════════════════════════╝
""")

def has_number_sequence(password):
    "Checking whether the password contains a numeric sequence or not"
    digits = ''.join([c for c in password if c.isdigit()])

    for i in range(len(digits) -2):
        a = int(digits[i])
        b = int(digits[i+1])
        c = int(digits[i+2])
        if b == a + 1 and c == b + 1:
            return True

    return False

def has_keyboard_pattern(password):
    "Checking whether the password contains a keyboard pattern or not"
    for pattern in KEYBOARD_PATTERNS:
        if pattern in password.lower():
            return True

    return False

def has_common_password(password):
    "Checking whether the password is common or not"
    password_lower = password.lower()
    min_len = 3
    for start in range(len(password_lower)):
        for end in range(start + min_len, len(password_lower) + 1):
            substring = password_lower[start:end]

            if substring in COMMON_PASSWORDS:
                return True
    return False

def print_result(result):
    """Display password check results in a beautiful format"""

    score = result["score"]
    level = result["level"]
    suggestions = result["suggestions"]

    # Header
    print("\n" + "="*60)
    print("🔐 PASSWORD STRENGTH REPORT")
    print("="*60)

    print(f"\n🔒 Your Password: {result['password']}")

    # Score with progress bar
    bar_length = 30
    filled = int(bar_length * score / 100)
    progress_bar = "█" * filled + "░" * (bar_length - filled)

    print(f"\n📊 Score: {score}/100")
    print(f"   [{progress_bar}]")
    print(f"   Level: {level}")

    # Suggestions
    if suggestions:
        print(f"\n💡 Suggestions ({len(suggestions)}):")
        print("-" * 60)
        for i, suggestion in enumerate(suggestions, 1):
            print(f"   {i}. {suggestion}")
    else:
        print("\n✅ No suggestions. Password looks great!")

    # Footer
    print("\n" + "="*60)

def generate_password(length):
    "main function to generate password"
    password = ""
    for _ in range(length):
        password += random.choice(ALL_CHARS)
    return password

def check_password(password):
    "main function to Check and score passwords"
    suggestions = []
    length = len(password)
    length_score = min(24, length *2)

    has_upper = any(i.isupper() for i in password)
    has_lower = any(i.islower() for i in password)
    has_digit = any(i.isdigit() for i in password)
    has_symbol = any(i in "!@#$%^&*()" for i in password)
    has_repetition = len(set(password)) < len(password)

    score = length_score + (has_upper*11) + ((not has_repetition)*5) + (has_lower*5)
    score += (has_digit*10) + (has_symbol*15) + ((not has_common_password(password))*10)
    score += ((not has_keyboard_pattern)*10) + ((not has_number_sequence)*10)

    score = min(100 , max(0,score))

    level = ""
    if 0 <= score < 30:
        level = "🔴 Very Weak"
    elif 30 <= score < 50:
        level = "🟠 Weak"
    elif 50 <= score < 70:
        level = "🟡 Medium"
    elif 70 <= score < 85:
        level = "🟢 Good"
    elif 85 <= score <= 100:
        level = "🔵 Excellent"



    if 12 <= length < 16:
        suggestions.append(f"📏 {length} is Good length! 16+ characters would be even better")
    elif 8 <= length < 12:
        suggestions.append("📐 12+ characters recommended for better security")
    elif length < 8:
        suggestions.append("🌱 Too short! Use at least 8 characters (12+ recommended)")

    if not has_upper:
        suggestions.append("⬆️ Add uppercase letters (A-Z) to make it stronger")
    if not has_lower:
        suggestions.append("⬇️ Add lowercase letters (a-z) to make it stronger")
    if not has_digit:
        suggestions.append("🔢 Add some numbers (0-9) for extra security")
    if not has_symbol:
        suggestions.append("✨ Add special characters (!@#$%^&*) to make it pop")
    if has_number_sequence(password):
        suggestions.append("🚫 Remove sequential numbers like '123' or '456'")
    if has_keyboard_pattern(password):
        suggestions.append("⌨️ Remove keyboard patterns like 'qwerty' or 'asdf'")
    if has_repetition:
        suggestions.append("♻️ Reduce repeated characters, use more variety")
    if has_common_password(password):
        suggestions.append("⚠️ Remove common words (hackers know these!)")

    return {
        "password" : password, 
        "score" : score,
        "level" : level,
        "suggestions" : suggestions
    }

if __name__ == "__main__":
    select_fiture  = input("for chek your password enter 1 and for " \
    "generate password enter somthing else: ")
    if select_fiture == "1":
        user_password = input("Enter your password: ")
        print_result(check_password(user_password))

    else:
        show_length_guide()
        while True:
            try:
                password_length = int(
                    input("Please enter your desired length password(8-64): ")
                )
                if 8 <= password_length <= 64:
                    break

                print("Please Enter a Number between 8 and 64")
            except ValueError:
                print("Please Just Enter a Number!")

        print(generate_password(password_length))
