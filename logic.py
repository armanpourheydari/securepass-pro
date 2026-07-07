"""
Password Generator and Checker Tool
A simple tool to generate strong passwords and check their security level.
"""

import math
import random
import string
from collections import Counter

from common_passwords import COMMON_PASSWORDS

ALL_CHARS = string.ascii_letters + string.digits + "!@#$%^&*()-_=+[]{};:<>?,./"
KEYBOARD_PATTERNS = [
    "qwe",
    "wer",
    "ert",
    "rty",
    "tyu",
    "yui",
    "uio",
    "iop",
    "qwer",
    "wert",
    "erty",
    "rtyu",
    "tyui",
    "yuio",
    "uiop",
    "qwert",
    "werty",
    "ertyu",
    "rtyui",
    "tyuio",
    "yuiop",
    "qwerty",
    "wertyu",
    "ertyui",
    "rtyuio",
    "tyuiop",
    "qwertyu",
    "wertyui",
    "ertyuiop",
    "qwertyui",
    "wertyuio",
    "qwertyuio",
    "wertyuiop",
    "qwertyuiop",
    "asd",
    "sdf",
    "dfg",
    "fgh",
    "ghj",
    "hjk",
    "jkl",
    "asdf",
    "sdfg",
    "dfgh",
    "fghj",
    "ghjk",
    "hjkl",
    "asdfg",
    "sdfgh",
    "dfghj",
    "fghjk",
    "ghjkl",
    "asdfgh",
    "sdfghj",
    "dfghjk",
    "fghjkl",
    "asdfghj",
    "sdfghjk",
    "dfghjkl",
    "asdfghjk",
    "sdfghjkl",
    "asdfghjkl",
    "zxc",
    "xcv",
    "cvb",
    "vbn",
    "bnm",
    "zxcv",
    "xcvb",
    "cvbn",
    "vbnm",
    "zxcvb",
    "xcvbn",
    "cvbnm",
    "zxcvbn",
    "xcvbnm",
    "zxcvbnm",
    "qaz",
    "wsx",
    "edc",
    "rfv",
    "tgb",
    "yhn",
    "ujm",
    "qazx",
    "wsxc",
    "edcv",
    "rfvb",
    "tgbn",
    "yhnm",
    "qazxs",
    "wsxed",
    "edcrf",
    "rfvtg",
    "tgbyh",
    "yhnuj",
    "qazxsw",
    "wsxedc",
    "edcrfv",
    "rfvtgb",
    "tgbyhn",
    "yhnujm",
    "qazxsw",
    "wsxedc",
    "edcrfv",
    "rfvtgb",
    "tgbyhn",
    "yhnujm",
    "qazwsx",
    "wsxedc",
    "edcrfv",
    "rfvtgb",
    "tgbyhn",
    "yhnujm",
    "qazxswed",
    "wsxedcrf",
    "edcrfvtg",
    "rfvtgbyh",
    "tgbyhnuj",
    "poi",
    "oiu",
    "iuy",
    "uyt",
    "ytr",
    "tre",
    "rew",
    "ewq",
    "poiu",
    "oiuy",
    "iuyt",
    "uytr",
    "ytre",
    "trew",
    "rewq",
    "poiuy",
    "oiuyt",
    "iuytre",
    "uytrew",
    "ytrewq",
    "poiuyt",
    "oiuytre",
    "iuytrew",
    "uytrewq",
    "poiuytre",
    "oiuytrew",
    "iuytrewq",
    "poiuytrew",
    "oiuytrewq",
    "poiuytrewq",
    "lkj",
    "kjh",
    "jhg",
    "hgf",
    "gfd",
    "fds",
    "dsa",
    "lkjh",
    "kjhg",
    "jhgf",
    "hgfd",
    "gfds",
    "fdsa",
    "lkjhg",
    "kjhgf",
    "jhgfd",
    "hgfds",
    "gfdsa",
    "lkjhgf",
    "kjhgfd",
    "jhgfds",
    "hgfdsa",
    "lkjhgfdsa",
    "mnb",
    "nbv",
    "bvc",
    "vcx",
    "cxz",
    "mnbv",
    "nbvc",
    "bvcx",
    "vcxz",
    "mnbvc",
    "nbvcx",
    "bvcxz",
    "mnbvcx",
    "nbvcxz",
    "mnbvcxz",
]


def show_length_guide():
    """Show the input text in terminal"""
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
    "Checking whether the password contains a numeric sequence or not (True/False)"
    digits = "".join([c for c in password if c.isdigit()])
    for i in range(len(digits) - 2):
        a = int(digits[i])
        b = int(digits[i + 1])
        c = int(digits[i + 2])
        if b == a + 1 and c == b + 1:
            return True
    return False


def has_keyboard_pattern(password):
    "Checking whether the password contains a keyboard pattern or not (True or False)"
    for pattern in KEYBOARD_PATTERNS:
        if pattern in password.lower():
            return True
    return False


def has_common_password(password):
    """Checking whether the password is common or not (True/ False)"""
    password_lower = password.lower()
    min_len = 3
    for start in range(len(password_lower)):
        for end in range(start + min_len, len(password_lower) + 1):
            substring = password_lower[start:end]
            if substring in COMMON_PASSWORDS:
                return True
    return False


def has_excessive_repetition(password: str, max_repeat: int = 3) -> bool:
    """
    Check if any character repeats more than max_repeat times.

    Args:
        password (str): The password to check
        max_repeat (int): Maximum allowed repetitions (default: 3)

    Returns:
        bool: True if any character repeats more than max_repeat times
    """

    char_counts = Counter(password)
    for count in char_counts.values():
        if count > max_repeat:
            return True
    return False


def print_result(result):
    """Display password check results in a beautiful format"""
    score = result["score"]
    level = result["level"]
    suggestions = result["suggestions"]
    print("\n" + "=" * 60)
    print("🔐 PASSWORD STRENGTH REPORT")
    print("=" * 60)
    print(f"\n🔒 Your Password: {result['password']}")
    bar_length = 30
    filled = int(bar_length * score / 100)
    progress_bar = "█" * filled + "░" * (bar_length - filled)
    print(f"\n📊 Score: {score}/100")
    print(f"   [{progress_bar}]")
    print(f"   Level: {level}")
    if suggestions:
        print(f"\n💡 Suggestions ({len(suggestions)}):")
        print("-" * 60)
        for i, suggestion in enumerate(suggestions, 1):
            print(f"   {i}. {suggestion}")
    else:
        print("\n✅ No suggestions. Password looks great!")
    print("\n" + "=" * 60)


def generate_password(length: int) -> str:
    """
    Main function to generate password
    Returns a random password
    """
    password = ""
    for _ in range(length):
        password += random.choice(ALL_CHARS)
    return password


def check_password(password: str) -> dict:
    """
    Main function to Check and score passwords
    Returns socre, level and a few suggestions
    """
    suggestions = []
    length = len(password)
    length_score = min(24, length * 2)
    has_upper = any(i.isupper() for i in password)
    has_lower = any(i.islower() for i in password)
    has_digit = any(i.isdigit() for i in password)
    has_symbol = any(i in "!@#$%^&*()" for i in password)
    
    excessive_repeat = has_excessive_repetition(password, max_repeat=3)
    
    is_common = has_common_password(password)
    is_keyboard = has_keyboard_pattern(password)
    is_sequence = has_number_sequence(password)
    
    # محاسبه امتیاز هر بخش
    upper_score = has_upper * 11
    lower_score = has_lower * 5
    digit_score = has_digit * 10
    symbol_score = has_symbol * 15
    repeat_score = 5 if not excessive_repeat else 0
    common_score = 10 if not is_common else 0
    keyboard_score = 10 if not is_keyboard else 0
    sequence_score = 10 if not is_sequence else 0
    
    # جمع کل
    score = (
        length_score
        + upper_score
        + lower_score
        + digit_score
        + symbol_score
        + repeat_score
        + common_score
        + keyboard_score
        + sequence_score
    )
    score = min(100, max(0, score))
    if score == 100 and length < 16:
        score = 99
    
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
        suggestions.append(
            f"📏 {length} is Good length! 16+ characters would be even better"
        )
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
    if has_excessive_repetition(password):
        suggestions.append("♻️ Reduce repeated characters, use more variety")
    if has_common_password(password):
        suggestions.append("⚠️ Remove common words (hackers know these!)")
    return {
        "password": password,
        "score": score,
        "level": level,
        "suggestions": suggestions,
    }


def calculate_entropy(password: str) -> float:
    """Calculating password entropy based on character length and variety"""
    if not password:
        return 0.0

    char_set_size = 0
    if any(c.islower() for c in password):
        char_set_size += 26
    if any(c.isupper() for c in password):
        char_set_size += 26
    if any(c.isdigit() for c in password):
        char_set_size += 10
    if any(c in "!@#$%^&*()-_=+[]{};:<>?,./" for c in password):
        char_set_size += 32

    if char_set_size == 0:
        return 0.0

    entropy = len(password) * math.log2(char_set_size)
    return round(entropy, 2)


def format_crack_time(seconds: float) -> str:
    """
    Convert crack time in seconds to a human-readable approximate format.
    """
    if seconds <= 0:
        return "Instant"

    # تعریف واحدها
    units = [
        (60, "seconds"),
        (3600, "minutes"),
        (86400, "hours"),
        (31536000, "days"),
        (31536000 * 365, "years"),
        (31536000 * 365 * 100, "centuries"),
    ]

    # پیدا کردن واحد مناسب
    for threshold, unit in reversed(units):
        if seconds >= threshold * 10:  # تقریباً
            value = seconds / threshold
            if unit == "centuries" and value > 1000:
                return f"~10^{int(math.log10(value))} {unit}"
            if unit == "years" and value > 1000:
                return f"~{int(value):,} years"
            if unit == "days" and value > 100:
                return f"~{int(value):,} days"
            if value >= 10:
                return f"~{value:.0f} {unit}"
            return f"~{value:.1f} {unit}"

    return "~0 seconds"


def estimate_crack_time(password: str, guesses_per_second: int = 1_000_000_000) -> dict:
    """Estimating the time it takes to crack a password using the Brute-Force method"""
    if not password:
        return {"seconds": 0, "time_str": "Instant", "combinations": 0}

    char_set_size = 0
    if any(c.islower() for c in password):
        char_set_size += 26
    if any(c.isupper() for c in password):
        char_set_size += 26
    if any(c.isdigit() for c in password):
        char_set_size += 10
    if any(c in "!@#$%^&*()-_=+[]{};:<>?,./" for c in password):
        char_set_size += 32

    if char_set_size == 0:
        return {"seconds": 0, "time_str": "Instant", "combinations": 0}

    length = len(password)
    combinations = char_set_size ** length
    seconds = combinations / guesses_per_second

    time_str = format_crack_time(seconds)

    return {
        "seconds": seconds,
        "time_str": time_str,
        "combinations": combinations,
        "char_set_size": char_set_size,
        "length": length,
    }


def get_entropy_level(entropy: float) -> dict:
    """Determines the level of entropy based on its value"""
    if entropy >= 80:
        return {"level": "Excellent", "color": "#4a9eff", "emoji": "🔵"}
    elif entropy >= 60:
        return {"level": "Good", "color": "#4caf50", "emoji": "🟢"}
    elif entropy >= 40:
        return {"level": "Medium", "color": "#ffc107", "emoji": "🟡"}
    elif entropy >= 20:
        return {"level": "Weak", "color": "#ff9800", "emoji": "🟠"}
    else:
        return {"level": "Very Weak", "color": "#f44336", "emoji": "🔴"}


if __name__ == "__main__":
    select_fiture = input(
        "for chek your password enter 1 and for "
        "generate password enter somthing else: "
    )
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
