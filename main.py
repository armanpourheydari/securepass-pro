"""
main securepass-pro executer
"""

import sys

from PyQt6.QtWidgets import QApplication

from gui import SecurePassGUI


def main():
    "execute program"
    app = QApplication(sys.argv)
    window = SecurePassGUI()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
