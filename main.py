"""
Password Generator and Checker Tool
A simple tool to generate strong passwords and check their security level.
"""

import random
import string

ALL_CHARS = string.ascii_letters + string.digits + "!@#$%^&*()-_=+"


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


def generate_password(length):
    "main function to generate password"
    password = ""
    for _ in range(length):
        password += random.choice(ALL_CHARS)
    return password


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
