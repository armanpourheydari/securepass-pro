"""
gui.py
SecurePass Pro - Complete GUI with Vault Management
"""

import sys
from datetime import datetime

import pyperclip
from openpyxl import Workbook
from PyQt6.QtCore import QEasingCurve, QPropertyAnimation, Qt, QTimer, pyqtProperty
from PyQt6.QtGui import QColor, QPalette
from PyQt6.QtWidgets import (
    QApplication,
    QComboBox,
    QDialog,
    QFileDialog,
    QFrame,
    QHBoxLayout,
    QHeaderView,
    QInputDialog,
    QLabel,
    QLineEdit,
    QMainWindow,
    QMessageBox,
    QProgressBar,
    QPushButton,
    QSlider,
    QStackedWidget,
    QTableWidget,
    QTableWidgetItem,
    QTabWidget,
    QVBoxLayout,
    QWidget,
)

from controller import PasswordController


class AnimatedProgressBar(QProgressBar):
    """Custom progress bar with smooth animation"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self._target_value = 0
        self._current_value = 0
        self.animation = QPropertyAnimation(self, b"animatedValue")
        self.animation.setDuration(800)
        self.animation.setEasingCurve(QEasingCurve.Type.OutCubic)
        self.animation.valueChanged.connect(self._update_value)
        self.setRange(0, 100)

    @pyqtProperty(int)
    def animatedValue(self):
        return self._current_value

    @animatedValue.setter
    def animatedValue(self, value):
        self._current_value = value
        super().setValue(value)

    def setValue(self, value):
        self.animation.stop()
        self.animation.setStartValue(self._current_value)
        self.animation.setEndValue(value)
        self.animation.start()

    def _update_value(self, value):
        self._current_value = value
        super().setValue(value)


class DeselectableTable(QTableWidget):
    """QTableWidget that clears selection when clicking on empty area"""

    def mousePressEvent(self, event):
        if self.itemAt(event.position().toPoint()) is None:
            self.clearSelection()
        super().mousePressEvent(event)


class CardDialog(QDialog):
    """Dialog for adding/editing a credit/debit card"""

    def __init__(self, parent=None, card_data=None):
        super().__init__(parent)
        self.card_data = card_data
        self.setWindowTitle("Add Card" if not card_data else "Edit Card")
        self.setMinimumSize(350, 400)
        self.setup_ui()
        if card_data:
            self._populate_fields()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(12)

        layout.addWidget(QLabel("Card Name:"))
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Personal, Business, etc.")
        layout.addWidget(self.name_input)

        layout.addWidget(QLabel("Card Type:"))
        self.type_combo = QComboBox()
        self.type_combo.addItems(["visa", "mastercard", "amex", "discover", "other"])
        layout.addWidget(self.type_combo)

        layout.addWidget(QLabel("Card Number:"))
        self.number_input = QLineEdit()
        self.number_input.setPlaceholderText("1234 5678 9012 3456")
        layout.addWidget(self.number_input)

        layout.addWidget(QLabel("Card Holder:"))
        self.holder_input = QLineEdit()
        self.holder_input.setPlaceholderText("John Doe")
        layout.addWidget(self.holder_input)

        expiry_layout = QHBoxLayout()
        expiry_layout.addWidget(QLabel("Expiry (MM/YY):"))
        self.expiry_month = QLineEdit()
        self.expiry_month.setPlaceholderText("MM")
        self.expiry_month.setFixedWidth(70)
        expiry_layout.addWidget(self.expiry_month)
        self.expiry_year = QLineEdit()
        self.expiry_year.setPlaceholderText("YY")
        self.expiry_year.setFixedWidth(70)
        expiry_layout.addWidget(self.expiry_year)
        expiry_layout.addStretch()
        layout.addLayout(expiry_layout)

        layout.addWidget(QLabel("CVV:"))
        self.cvv_input = QLineEdit()
        self.cvv_input.setPlaceholderText("123")
        self.cvv_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.cvv_input.setMaxLength(4)
        layout.addWidget(self.cvv_input)

        btn_layout = QHBoxLayout()
        btn_layout.addStretch()
        save_btn = QPushButton("Save Card")
        save_btn.clicked.connect(self.accept)
        btn_layout.addWidget(save_btn)
        cancel_btn = QPushButton("Cancel")
        cancel_btn.clicked.connect(self.reject)
        btn_layout.addWidget(cancel_btn)
        layout.addLayout(btn_layout)

        self.setStyleSheet("""
            QDialog {
                background-color: #1a1a2e;
            }
            QLabel {
                color: #e8e8f0;
                font-family: 'Segoe UI';
                font-size: 12px;
            }
            QLineEdit, QComboBox {
                background-color: #1a1a2e;
                color: #f2c94c;
                border: 1px solid #2a2a40;
                border-radius: 6px;
                padding: 8px 12px;
                font-size: 13px;
                font-family: 'Segoe UI';
            }
            QLineEdit:focus, QComboBox:focus {
                border-color: #4a6fa5;
            }
            QPushButton {
                background-color: #4a6fa5;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 8px 20px;
                font-weight: bold;
                font-size: 13px;
            }
            QPushButton:hover {
                background-color: #5a7fb5;
            }
        """)

    def _populate_fields(self):
        self.name_input.setText(self.card_data.get("name", ""))
        self.type_combo.setCurrentText(self.card_data.get("type", "visa"))
        self.number_input.setText(self.card_data.get("number", ""))
        self.holder_input.setText(self.card_data.get("holder", ""))
        self.expiry_month.setText(self.card_data.get("expiry_month", ""))
        self.expiry_year.setText(self.card_data.get("expiry_year", ""))
        self.cvv_input.setText(self.card_data.get("cvv", ""))

    def get_data(self) -> dict:
        data = {
            "name": self.name_input.text().strip(),
            "type": self.type_combo.currentText(),
            "number": self.number_input.text().strip().replace(" ", ""),
            "holder": self.holder_input.text().strip(),
            "expiry_month": self.expiry_month.text().strip(),
            "expiry_year": self.expiry_year.text().strip(),
            "cvv": self.cvv_input.text().strip()
        }
        errors = []
        if not data["name"]:
            errors.append("Card Name")
        if not data["number"] or len(data["number"]) < 4:
            errors.append("Card Number (at least 4 digits)")
        if not data["holder"]:
            errors.append("Card Holder")
        if not data["expiry_month"] or not data["expiry_year"]:
            errors.append("Expiry Date")
        if not data["cvv"]:
            errors.append("CVV")
        
        if errors:
            raise ValueError(f"Please fill in: {', '.join(errors)}")
        
        # (اختیاری) بررسی ساده شماره کارت (فقط اعداد)
        if not data["number"].isdigit():
            raise ValueError("Card number must contain only digits")
        if not data["cvv"].isdigit():
            raise ValueError("CVV must contain only digits")
        if not data["expiry_month"].isdigit() or not data["expiry_year"].isdigit():
            raise ValueError("Expiry must be numbers")
        
        return data


class SecurePassGUI(QMainWindow):
    """Main application window"""

    def __init__(self):
        super().__init__()
        self.controller = PasswordController()
        self.master_password = None

        self.length_slider = None
        self.length_display = None
        self.password_display = None
        self.check_input = None
        self.result_frame = None
        self.score_label = None
        self.level_label = None
        self.progress_bar = None
        self.suggestions_text = None
        self.copy_btn = None
        self.strength_bar = None
        self.strength_label = None
        self.vault_table = None
        self.cards_table = None
        self.vault_content_stack = None
        self.vault_sub_tabs = None
        self.master_entry = None
        self.show_hide_btn = None
        self.export_txt_btn = None
        self.export_excel_btn = None
        self.delete_btn = None
        self.refresh_btn = None

        self.setup_window()
        self.setup_ui()
        self.center_window()

    def setup_window(self):
        self.setWindowTitle("SecurePass Pro")
        self.setMinimumSize(420, 620)
        self.setMaximumSize(540, 780)
        self.setStyleSheet(self._get_style_sheet())

    def center_window(self):
        screen = QApplication.primaryScreen().availableGeometry()
        width = int(screen.width() * 0.35)
        height = int(width * 14 / 9)
        if height > screen.height() * 0.8:
            height = int(screen.height() * 0.8)
            width = int(height * 9 / 14)
        x = (screen.width() - width) // 2
        y = (screen.height() - height) // 2
        self.setGeometry(x, y, width, height)

    def _get_style_sheet(self):
        return """
            QMainWindow {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #0f0f1a, stop:1 #1a1a2e);
            }
            QLabel {
                color: #e8e8f0;
                font-family: 'Segoe UI';
            }
            QLabel#title {
                color: #f2c94c;
                font-size: 22px;
                font-weight: bold;
                letter-spacing: 1px;
            }
            QLabel#subtitle {
                color: #8888aa;
                font-size: 10px;
                letter-spacing: 0.5px;
            }
            QLabel#section_title {
                color: #d4d4e8;
                font-size: 12px;
                font-weight: bold;
                letter-spacing: 0.3px;
            }
            QLabel#score_label {
                font-size: 18px;
                font-weight: bold;
            }
            QLabel#level_label {
                font-size: 14px;
                font-weight: bold;
            }
            QLabel#strength_label {
                font-size: 13px;
                font-weight: bold;
            }
            QLineEdit {
                background-color: #1a1a2e;
                color: #f2c94c;
                border: 2px solid #2a2a40;
                border-radius: 8px;
                padding: 10px 12px;
                font-size: 14px;
                font-family: 'Consolas';
                font-weight: bold;
            }
            QLineEdit:focus {
                border-color: #4a6fa5;
            }
            QLineEdit#check_input {
                color: #e8e8f0;
                font-family: 'Segoe UI';
                font-weight: normal;
                font-size: 13px;
                padding: 12px;
            }
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #4a6fa5, stop:1 #3a5f95);
                color: white;
                border: none;
                border-radius: 8px;
                font-family: 'Segoe UI';
                font-size: 13px;
                font-weight: bold;
                padding: 12px 16px;
                letter-spacing: 0.5px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #5a7fb5, stop:1 #4a6fa5);
            }
            QPushButton:pressed {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #3a5f95, stop:1 #2a4f85);
            }
            QPushButton#copy_btn {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #2a2a40, stop:1 #1a1a2e);
                font-size: 11px;
                padding: 8px 12px;
                border: 1px solid #3a3a52;
                border-radius: 6px;
            }
            QPushButton#copy_btn:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #3a3a52, stop:1 #2a2a40);
                border-color: #4a6fa5;
            }
            QPushButton#export_btn {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #2a5a3a, stop:1 #1a4a2a);
                font-size: 10px;
                padding: 6px 12px;
                border-radius: 6px;
            }
            QPushButton#export_btn:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #3a6a4a, stop:1 #2a5a3a);
            }
            QPushButton#delete_btn {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #a54a4a, stop:1 #8a3a3a);
            }
            QPushButton#delete_btn:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #b55a5a, stop:1 #9a4a4a);
            }
            QSlider::groove:horizontal {
                height: 5px;
                background: #2a2a40;
                border-radius: 3px;
            }
            QSlider::handle:horizontal {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #f2c94c, stop:1 #f5a623);
                width: 20px;
                height: 20px;
                margin: -8px 0;
                border-radius: 10px;
            }
            QSlider::handle:horizontal:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #f5d76e, stop:1 #f2c94c);
            }
            QProgressBar {
                border: none;
                background-color: #1a1a2e;
                border-radius: 5px;
                height: 10px;
            }
            QProgressBar::chunk {
                border-radius: 5px;
            }
            QTableWidget {
                background-color: #1a1a2e;
                color: #e8e8f0;
                border: 1px solid #2a2a40;
                border-radius: 6px;
                gridline-color: #2a2a40;
            }
            QTableWidget::item {
                padding: 6px;
            }
            QTableWidget::item:selected {
                background-color: #4a6fa5;
                color: white;
            }
            QHeaderView::section {
                background-color: #2a2a40;
                color: #f2c94c;
                padding: 8px;
                border: none;
                font-weight: bold;
            }
            QTabWidget::pane {
                border: none;
                background: transparent;
            }
            QTabBar::tab {
                background-color: #1a1a2e;
                color: #8888aa;
                padding: 8px 18px;
                border-top-left-radius: 6px;
                border-top-right-radius: 6px;
                font-family: 'Segoe UI';
                font-size: 12px;
                font-weight: bold;
                letter-spacing: 0.5px;
            }
            QTabBar::tab:selected {
                background-color: #2a2a40;
                color: #f2c94c;
            }
            QTabBar::tab:hover:!selected {
                background-color: #22223a;
                color: #b0b0c8;
            }
            QFrame#result_frame {
                background-color: #1a1a2e;
                border-radius: 10px;
                padding: 14px;
            }
            QFrame#card_frame {
                background-color: #1a1a2e;
                border: 1px solid #2a2a40;
                border-radius: 10px;
                padding: 14px;
            }
        """

    def setup_ui(self):
        central = QWidget()
        self.setCentralWidget(central)
        main_layout = QVBoxLayout(central)
        main_layout.setContentsMargins(20, 16, 20, 16)
        main_layout.setSpacing(12)

        self._build_header(main_layout)

        self.tabs = QTabWidget()
        self.tabs.addTab(self._build_generator_tab(), "Generate")
        self.tabs.addTab(self._build_checker_tab(), "Checker")

        vault_tab = QWidget()
        vault_layout = QVBoxLayout(vault_tab)
        vault_layout.setContentsMargins(0, 0, 0, 0)
        self.vault_sub_tabs = QTabWidget()
        self.vault_sub_tabs.setVisible(False)  # Initially hidden
        vault_layout.addWidget(self.vault_sub_tabs)
        self.tabs.addTab(vault_tab, "Vault")

        self.tabs.currentChanged.connect(self._on_tab_changed)
        main_layout.addWidget(self.tabs)

        self._build_footer(main_layout)

        # Build vault content after UI setup
        self._build_vault_tab()

    def _build_header(self, parent):
        header = QVBoxLayout()
        header.setSpacing(2)

        title_layout = QHBoxLayout()
        title = QLabel("SecurePass Pro")
        title.setObjectName("title")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_layout.addWidget(title)
        header.addLayout(title_layout)

        subtitle = QLabel("Enterprise-Grade Password Management")
        subtitle.setObjectName("subtitle")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        header.addWidget(subtitle)

        parent.addLayout(header)

    def _build_generator_tab(self):
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.setSpacing(10)

        card = QFrame()
        card.setObjectName("card_frame")
        card_layout = QVBoxLayout(card)
        card_layout.setSpacing(10)

        length_label = QLabel("Password Length")
        length_label.setObjectName("section_title")
        card_layout.addWidget(length_label)

        slider_layout = QHBoxLayout()
        slider_layout.setSpacing(12)

        self.length_slider = QSlider(Qt.Orientation.Horizontal)
        self.length_slider.setMinimum(6)
        self.length_slider.setMaximum(40)
        self.length_slider.setValue(16)
        self.length_slider.valueChanged.connect(self._update_length_display)

        self.length_display = QLabel("16")
        self.length_display.setStyleSheet(
            "font-size: 16px; font-weight: bold; color: #f2c94c; min-width: 34px;"
        )
        self.length_display.setAlignment(Qt.AlignmentFlag.AlignCenter)

        slider_layout.addWidget(self.length_slider)
        slider_layout.addWidget(self.length_display)
        card_layout.addLayout(slider_layout)

        generate_btn = QPushButton("Generate Secure Password")
        generate_btn.clicked.connect(self._on_generate)
        card_layout.addWidget(generate_btn)

        self.password_display = QLineEdit()
        self.password_display.setReadOnly(True)
        self.password_display.setPlaceholderText(
            "Your secure password will appear here"
        )
        card_layout.addWidget(self.password_display)

        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(8)

        self.copy_btn = QPushButton("📜 Copy")
        self.copy_btn.setObjectName("copy_btn")
        self.copy_btn.clicked.connect(self._copy_password)
        btn_layout.addWidget(self.copy_btn)

        card_layout.addLayout(btn_layout)

        strength_label = QLabel("Password Strength")
        strength_label.setObjectName("section_title")
        card_layout.addWidget(strength_label)

        self.strength_bar = AnimatedProgressBar()
        self.strength_bar.setValue(0)
        card_layout.addWidget(self.strength_bar)

        self.strength_label = QLabel("")
        self.strength_label.setObjectName("strength_label")
        self.strength_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        card_layout.addWidget(self.strength_label)

        layout.addWidget(card)
        layout.addStretch()
        return tab

    def _build_checker_tab(self):
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.setSpacing(10)

        card = QFrame()
        card.setObjectName("card_frame")
        card_layout = QVBoxLayout(card)
        card_layout.setSpacing(10)

        input_label = QLabel("Enter Password to Check")
        input_label.setObjectName("section_title")
        card_layout.addWidget(input_label)

        self.check_input = QLineEdit()
        self.check_input.setObjectName("check_input")
        self.check_input.setPlaceholderText("Type or paste password here...")
        self.check_input.setEchoMode(QLineEdit.EchoMode.Password)
        card_layout.addWidget(self.check_input)

        check_btn = QPushButton("Analyze Password")
        check_btn.clicked.connect(self._on_check)
        card_layout.addWidget(check_btn)

        layout.addWidget(card)

        self._build_result_display(layout)

        layout.addStretch()
        return tab

    def _build_vault_tab(self):
        """Build the vault tab with unlock screen and hidden sub-tabs"""
        tab = QWidget()
        vault_layout = QVBoxLayout(tab)
        vault_layout.setSpacing(0)

        self.vault_content_stack = QStackedWidget()

        # ====== UNLOCK SCREEN ======
        unlock_widget = QWidget()
        unlock_layout = QVBoxLayout(unlock_widget)
        unlock_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        unlock_layout.setSpacing(16)

        title = QLabel("Secure Vault")
        title.setStyleSheet("""
            font-size: 28px;
            font-weight: bold;
            color: #f2c94c;
            font-family: 'Segoe UI';
        """)
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        unlock_layout.addWidget(title)

        subtitle = QLabel(
            "Enter your master password to access saved passwords and cards"
        )
        subtitle.setStyleSheet("""
            font-size: 12px;
            color: #8888aa;
            font-family: 'Segoe UI';
        """)
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        unlock_layout.addWidget(subtitle)

        unlock_layout.addSpacing(10)

        # Master password entry with show/hide button
        password_layout = QHBoxLayout()
        password_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        password_layout.setSpacing(8)

        self.master_entry = QLineEdit()
        self.master_entry.setPlaceholderText("Master Password")
        self.master_entry.setEchoMode(QLineEdit.EchoMode.Password)
        self.master_entry.setStyleSheet("""
            QLineEdit {
                background-color: #1a1a2e;
                color: #f2c94c;
                border: 2px solid #2a2a40;
                border-radius: 10px;
                padding: 16px 20px;
                font-size: 16px;
                font-family: 'Segoe UI';
                max-width: 280px;
                min-height: 44px;
            }
            QLineEdit:focus {
                border-color: #4a6fa5;
            }
        """)
        self.master_entry.setMaximumWidth(280)
        self.master_entry.setMinimumHeight(44)
        self.master_entry.returnPressed.connect(self._unlock_vault_action)
        password_layout.addWidget(self.master_entry)

        self.show_hide_btn = QPushButton("👁️")
        self.show_hide_btn.setFixedSize(44, 44)
        self.show_hide_btn.setStyleSheet("""
            QPushButton {
                background-color: #2a2a40;
                color: #a0a0b8;
                border: 2px solid #2a2a40;
                border-radius: 10px;
                font-size: 18px;
                padding: 0px;
            }
            QPushButton:hover {
                background-color: #3a3a52;
                border-color: #4a6fa5;
            }
        """)
        self.show_hide_btn.setToolTip("Show/Hide password")
        self.show_hide_btn.clicked.connect(self._toggle_master_password_visibility)
        password_layout.addWidget(self.show_hide_btn)

        unlock_layout.addLayout(password_layout)

        unlock_btn = QPushButton("Unlock Vault")
        unlock_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #4a6fa5, stop:1 #3a5f95);
                color: white;
                border: none;
                border-radius: 10px;
                font-family: 'Segoe UI';
                font-size: 15px;
                font-weight: bold;
                padding: 14px 30px;
                max-width: 320px;
                min-height: 44px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #5a7fb5, stop:1 #4a6fa5);
            }
        """)
        unlock_btn.setMaximumWidth(320)
        unlock_btn.setMinimumHeight(44)
        unlock_btn.clicked.connect(self._unlock_vault_action)
        unlock_layout.addWidget(unlock_btn, alignment=Qt.AlignmentFlag.AlignCenter)

        unlock_layout.addStretch()

        # ====== VAULT CONTENT (Hidden until unlocked) ======
        content_widget = QWidget()
        content_layout = QVBoxLayout(content_widget)
        content_layout.setSpacing(10)

        # Sub-tabs for Passwords and Cards - HIDDEN initially
        self.vault_sub_tabs = QTabWidget()
        self.vault_sub_tabs.addTab(self._build_passwords_tab(), "Passwords")
        self.vault_sub_tabs.addTab(self._build_cards_tab(), "Cards")
        self.vault_sub_tabs.setVisible(False)  # 🔒 Initially hidden
        content_layout.addWidget(self.vault_sub_tabs)

        self.vault_content_stack.addWidget(unlock_widget)
        self.vault_content_stack.addWidget(content_widget)

        vault_layout.addWidget(self.vault_content_stack)

        # Add this tab to the main vault tab
        vault_tab_index = self.tabs.indexOf(self.tabs.widget(2))  # "Vault" tab index
        self.tabs.widget(vault_tab_index).layout().addWidget(tab)

    def _build_passwords_tab(self):
        """Build the passwords sub-tab inside vault"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.setSpacing(10)

        header_layout = QHBoxLayout()
        title = QLabel("Saved Passwords")
        title.setObjectName("section_title")
        header_layout.addWidget(title)
        header_layout.addStretch()

        save_btn = QPushButton("Add New")
        save_btn.setObjectName("export_btn")
        save_btn.clicked.connect(self._save_new_password)
        header_layout.addWidget(save_btn)

        self.refresh_btn = QPushButton("Refresh")
        self.refresh_btn.setObjectName("export_btn")
        self.refresh_btn.clicked.connect(self._load_vault)
        header_layout.addWidget(self.refresh_btn)

        layout.addLayout(header_layout)

        # Table
        self.vault_table = DeselectableTable()
        self.vault_table.setColumnCount(2)
        self.vault_table.setHorizontalHeaderLabels(["Name", "Password"])
        self.vault_table.horizontalHeader().setSectionResizeMode(
            0, QHeaderView.ResizeMode.ResizeToContents
        )
        self.vault_table.horizontalHeader().setSectionResizeMode(
            1, QHeaderView.ResizeMode.Stretch
        )
        self.vault_table.setAlternatingRowColors(True)
        self.vault_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.vault_table.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)
        self.vault_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.vault_table.cellClicked.connect(self._on_password_cell_clicked)
        self.vault_table.cellDoubleClicked.connect(self._edit_password)
        layout.addWidget(self.vault_table)

        btn_layout = QHBoxLayout()
        btn_layout.addStretch()
        self.delete_btn = QPushButton("Delete")
        self.delete_btn.setObjectName("delete_btn")
        self.delete_btn.clicked.connect(self._delete_selected_password)
        btn_layout.addWidget(self.delete_btn)
        layout.addLayout(btn_layout)

        return tab

    def _build_cards_tab(self):
        """Build the cards sub-tab inside vault"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.setSpacing(10)

        header_layout = QHBoxLayout()
        title = QLabel("Saved Cards")
        title.setObjectName("section_title")
        header_layout.addWidget(title)
        header_layout.addStretch()

        add_card_btn = QPushButton("Add New")
        add_card_btn.setObjectName("export_btn")
        add_card_btn.clicked.connect(self._add_new_card)
        header_layout.addWidget(add_card_btn)

        refresh_cards_btn = QPushButton("Refresh")
        refresh_cards_btn.setObjectName("export_btn")
        refresh_cards_btn.clicked.connect(self._load_cards)
        header_layout.addWidget(refresh_cards_btn)

        layout.addLayout(header_layout)

        # Cards Table
        self.cards_table = DeselectableTable()
        self.cards_table.setColumnCount(5)
        self.cards_table.setHorizontalHeaderLabels(["Name", "Type", "Number", "Expiry", "Holder"])
        self.cards_table.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.Stretch
        )
        self.cards_table.setAlternatingRowColors(True)
        self.cards_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.cards_table.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)
        self.cards_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.cards_table.cellDoubleClicked.connect(self._edit_card)
        layout.addWidget(self.cards_table)

        btn_layout = QHBoxLayout()
        btn_layout.addStretch()
        self.delete_btn_card = QPushButton("Delete")
        self.delete_btn_card.setObjectName("delete_btn")
        self.delete_btn_card.clicked.connect(self._delete_selected_card)
        btn_layout.addWidget(self.delete_btn_card)
        layout.addLayout(btn_layout)

        return tab

    def _build_result_display(self, parent):
        self.result_frame = QFrame()
        self.result_frame.setObjectName("result_frame")
        self.result_frame.setVisible(False)
        result_layout = QVBoxLayout(self.result_frame)
        result_layout.setSpacing(6)

        self.score_label = QLabel("Score: --/100")
        self.score_label.setObjectName("score_label")
        result_layout.addWidget(self.score_label)

        self.level_label = QLabel("Level: --")
        self.level_label.setObjectName("level_label")
        result_layout.addWidget(self.level_label)

        self.progress_bar = AnimatedProgressBar()
        self.progress_bar.setValue(0)
        result_layout.addWidget(self.progress_bar)

        suggestions_label = QLabel("Suggestions:")
        suggestions_label.setObjectName("section_title")
        suggestions_label.setStyleSheet("margin-top: 4px;")
        result_layout.addWidget(suggestions_label)

        self.suggestions_text = QLabel("")
        self.suggestions_text.setWordWrap(True)
        self.suggestions_text.setStyleSheet(
            "color: #a0a0b8; font-size: 11px; font-family: 'Segoe UI';"
        )
        result_layout.addWidget(self.suggestions_text)

        parent.addWidget(self.result_frame)

    def _build_footer(self, parent):
        footer = QLabel(
            "All operations are performed locally. Your passwords never leave your device."
        )
        footer.setStyleSheet("color: #606080; font-size: 8px; font-family: 'Segoe UI';")
        footer.setAlignment(Qt.AlignmentFlag.AlignCenter)
        parent.addWidget(footer)

    def _toggle_master_password_visibility(self):
        if self.master_entry.echoMode() == QLineEdit.EchoMode.Password:
            self.master_entry.setEchoMode(QLineEdit.EchoMode.Normal)
            self.show_hide_btn.setText("🙈")
            self.show_hide_btn.setToolTip("Hide password")
        else:
            self.master_entry.setEchoMode(QLineEdit.EchoMode.Password)
            self.show_hide_btn.setText("👁️")
            self.show_hide_btn.setToolTip("Show password")

    def _on_tab_changed(self, index):
        if self.tabs.tabText(index) == "Vault":
            # Reset vault state
            self.master_password = None
            self.controller.set_master_password(None)
            self.vault_content_stack.setCurrentIndex(0)
            self.vault_sub_tabs.setVisible(False)
            self.master_entry.clear()
            self.master_entry.setFocus()

    def _update_length_display(self, value):
        self.length_display.setText(str(value))

    def _on_generate(self):
        length = self.length_slider.value()
        password = self.controller.generate(length)
        self.password_display.setText(password)
        self._update_strength_meter(password)

    def _update_strength_meter(self, password):
        result = self.controller.check(password)
        score = result["score"]

        self.strength_bar.setValue(score)

        if score >= 85:
            color = "#4a9eff"
            level_text = "Excellent"
        elif score >= 70:
            color = "#4caf50"
            level_text = "Good"
        elif score >= 50:
            color = "#ffc107"
            level_text = "Medium"
        elif score >= 30:
            color = "#ff9800"
            level_text = "Weak"
        else:
            color = "#f44336"
            level_text = "Very Weak"

        self.strength_bar.setStyleSheet(
            f"QProgressBar::chunk {{ background-color: {color}; border-radius: 5px; }}"
        )
        self.strength_label.setText(f"{level_text} ({score}/100)")

    def _copy_password(self):
        pwd = self.password_display.text()
        if pwd:
            pyperclip.copy(pwd)
            self.copy_btn.setText("Copied!")
            self.copy_btn.setStyleSheet("""
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #4a8a5a, stop:1 #3a7a4a);
                color: white;
                border: none;
                border-radius: 6px;
                font-family: 'Segoe UI';
                font-size: 11px;
                padding: 8px 12px;
                font-weight: bold;
            """)
            QTimer.singleShot(1500, self._reset_copy_btn)
        else:
            QMessageBox.warning(self, "Empty", "Generate a password first!")

    def _reset_copy_btn(self):
        self.copy_btn.setText("Copy")
        self.copy_btn.setStyleSheet("")

    def _on_check(self):
        password = self.check_input.text()
        if not password:
            QMessageBox.warning(self, "Empty", "Please enter a password to check.")
            return

        result = self.controller.check(password)
        self._display_check_result(result)

    def _display_check_result(self, result):
        self.result_frame.setVisible(True)

        score = result["score"]
        level = result["level"]
        suggestions = result["suggestions"]

        self.score_label.setText(f"Score: {score}/100")
        self.level_label.setText(f"Level: {level}")

        self.progress_bar.setValue(score)

        if score >= 85:
            color = "#4a9eff"
        elif score >= 70:
            color = "#4caf50"
        elif score >= 50:
            color = "#ffc107"
        elif score >= 30:
            color = "#ff9800"
        else:
            color = "#f44336"

        self.progress_bar.setStyleSheet(
            f"QProgressBar::chunk {{ background-color: {color}; border-radius: 5px; }}"
        )

        if suggestions:
            text = "\n".join(f"• {s}" for s in suggestions)
            self.suggestions_text.setText(text)
        else:
            self.suggestions_text.setText(
                "No improvements needed. Your password is excellent!"
            )

    def _unlock_vault_action(self):
        master = self.master_entry.text()
        if not master:
            QMessageBox.warning(self, "Empty", "Please enter your master password.")
            return

        if self.controller.verify_password(master):
            self.master_password = master
            self.controller.set_master_password(master)
            self.vault_sub_tabs.setVisible(True)
            self.vault_content_stack.setCurrentIndex(1)
            self._load_vault()
            self._load_cards()
            self.master_entry.clear()
        else:
            if not self.controller.vault_exists():
                reply = QMessageBox.question(
                    self,
                    "Create New Vault",
                    "No vault found. Create a new vault with this master password?\n\n"
                    "⚠️ Make sure you remember this password!",
                    QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                )
                if reply == QMessageBox.StandardButton.Yes:
                    if self.controller.create_new_vault(master):
                        self.master_password = master
                        self.controller.set_master_password(master)
                        self.vault_sub_tabs.setVisible(True)
                        self.vault_content_stack.setCurrentIndex(1)
                        self._load_vault()
                        self._load_cards()
                        self.master_entry.clear()
                        QMessageBox.information(
                            self, "Success", "✅ Vault created successfully!"
                        )
                    else:
                        QMessageBox.warning(self, "Error", "Failed to create vault.")
            else:
                QMessageBox.warning(self, "Error", "❌ Wrong master password!")

    def _save_new_password(self):
        if not self.master_password:
            return

        name, ok = QInputDialog.getText(
            self, "Save New Password", "Enter name for this password:"
        )
        if not ok or not name:
            return

        password, ok = QInputDialog.getText(
            self, "Save New Password", "Enter password:", QLineEdit.EchoMode.Password
        )
        if not ok or not password:
            return

        try:
            self.controller.set_master_password(self.master_password)
            if self.controller.save_password(name, password):
                QMessageBox.information(self, "Success", f"Password '{name}' saved!")
                self._load_vault()
            else:
                QMessageBox.warning(self, "Error", "Failed to save password.")
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

    def _load_vault(self):
        if not self.master_password:
            return

        try:
            self.controller.set_master_password(self.master_password)
            passwords = self.controller.get_passwords()

            self.vault_table.setRowCount(len(passwords))
            for row, pwd in enumerate(passwords):
                self.vault_table.setItem(row, 0, QTableWidgetItem(pwd.get("name", "")))
                self.vault_table.setItem(
                    row, 1, QTableWidgetItem(pwd.get("password", ""))
                )

        except Exception as e:
            QMessageBox.warning(self, "Error", f"Failed to load vault: {str(e)}")

    def _on_password_cell_clicked(self, row, column):
        if column == 1:
            password_item = self.vault_table.item(row, column)
            if password_item:
                pyperclip.copy(password_item.text())
                QMessageBox.information(self, "Copied", "Password copied to clipboard!")

    def _edit_password(self, row, column):
        name_item = self.vault_table.item(row, 0)
        pass_item = self.vault_table.item(row, 1)

        if not name_item or not pass_item:
            return

        current_name = name_item.text()
        current_password = pass_item.text()

        new_name, ok = QInputDialog.getText(
            self, "Edit Password", "Name:", text=current_name
        )
        if not ok:
            return

        new_password, ok = QInputDialog.getText(
            self,
            "Edit Password",
            "Password:",
            QLineEdit.EchoMode.Password,
            text=current_password,
        )
        if not ok:
            return

        try:
            self.controller.set_master_password(self.master_password)
            if self.controller.update_password(row + 1, new_name, new_password):
                QMessageBox.information(self, "Success", "Password updated!")
                self._load_vault()
            else:
                QMessageBox.warning(self, "Error", "Failed to update password.")
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

    def _delete_selected_password(self):
        selected = self.vault_table.currentRow()
        if selected < 0:
            QMessageBox.warning(
                self, "No Selection", "Please select a password to delete."
            )
            return

        name_item = self.vault_table.item(selected, 0)
        name = name_item.text() if name_item else "Unknown"

        reply = QMessageBox.question(
            self,
            "Delete Password",
            f"Are you sure you want to delete '{name}'?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
        )

        if reply == QMessageBox.StandardButton.Yes:
            try:
                self.controller.set_master_password(self.master_password)
                if self.controller.delete_password(selected + 1):
                    QMessageBox.information(self, "Success", "Password deleted!")
                    self._load_vault()
                else:
                    QMessageBox.warning(self, "Error", "Failed to delete password.")
            except Exception as e:
                QMessageBox.critical(self, "Error", str(e))

    def _add_new_card(self):
        if not self.master_password:
            QMessageBox.warning(self, "Locked", "Please unlock vault first!")
            return

        dialog = CardDialog(self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            try:
                data = dialog.get_data()  # ممکن است خطا بدهد
            except ValueError as e:
                QMessageBox.warning(self, "Invalid Input", str(e))
                return

            try:
                self.controller.set_master_password(self.master_password)
                if self.controller.save_card(
                    data["name"], data["number"], data["holder"],
                    data["expiry_month"], data["expiry_year"], data["cvv"], data["type"]
                ):
                    QMessageBox.information(self, "Success", "Card saved successfully!")
                    self._load_cards()
                else:
                    QMessageBox.warning(self, "Error", "Failed to save card.")
            except Exception as e:
                QMessageBox.critical(self, "Error", str(e))

    def _load_cards(self):
        if not self.master_password:
            return

        try:
            self.controller.set_master_password(self.master_password)
            cards = self.controller.get_cards()

            self.cards_table.setRowCount(len(cards))
            for row, card in enumerate(cards):
                self.cards_table.setItem(row, 0, QTableWidgetItem(card.get("name", "")))
                self.cards_table.setItem(row, 1, QTableWidgetItem(card.get("type", "")))
                number = card.get("number", "")
                if len(number) >= 4:
                    masked = "•••• " + number[-4:]
                else:
                    masked = "••••"
                self.cards_table.setItem(row, 2, QTableWidgetItem(masked))
                expiry = f"{card.get('expiry_month', '')}/{card.get('expiry_year', '')}"
                self.cards_table.setItem(row, 3, QTableWidgetItem(expiry))
                self.cards_table.setItem(row, 4, QTableWidgetItem(card.get("holder", "")))
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Failed to load cards: {str(e)}")

    def _edit_card(self, row, column):
        """Edit card on double-click - uses full data from vault"""
        if not self.master_password:
            return

        try:
            self.controller.set_master_password(self.master_password)
            cards = self.controller.get_cards()
            
            if row >= len(cards):
                return
            
            card_data = cards[row]
            
            dialog = CardDialog(self, card_data)
            if dialog.exec() == QDialog.DialogCode.Accepted:
                data = dialog.get_data()
                
                if not data["name"] or not data["number"] or not data["holder"]:
                    QMessageBox.warning(self, "Error", "Name, number and holder are required!")
                    return
                
                if not data["number"].isdigit() or not data["cvv"].isdigit():
                    QMessageBox.warning(self, "Error", "Card number and CVV must contain only digits!")
                    return
                
                if self.controller.update_card(
                    row + 1, data["name"], data["number"], data["holder"],
                    data["expiry_month"], data["expiry_year"], data["cvv"], data["type"]
                ):
                    QMessageBox.information(self, "Success", "Card updated!")
                    self._load_cards()
                else:
                    QMessageBox.warning(self, "Error", "Failed to update card.")
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

    def _delete_selected_card(self):
        selected = self.cards_table.currentRow()
        if selected < 0:
            QMessageBox.warning(self, "No Selection", "Please select a card to delete.")
            return

        name_item = self.cards_table.item(selected, 0)
        name = name_item.text() if name_item else "Unknown"

        reply = QMessageBox.question(
            self,
            "Delete Card",
            f"Are you sure you want to delete card '{name}'?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
        )

        if reply == QMessageBox.StandardButton.Yes:
            try:
                self.controller.set_master_password(self.master_password)
                if self.controller.delete_card(selected + 1):
                    QMessageBox.information(self, "Success", "Card deleted!")
                    self._load_cards()
                else:
                    QMessageBox.warning(self, "Error", "Failed to delete card.")
            except Exception as e:
                QMessageBox.critical(self, "Error", str(e))

    def _export_vault_txt(self):
        if not self.master_password:
            return

        try:
            self.controller.set_master_password(self.master_password)
            passwords = self.controller.get_passwords()

            if not passwords:
                QMessageBox.warning(self, "Empty", "No passwords to export.")
                return

            file_path, _ = QFileDialog.getSaveFileName(
                self,
                "Export Vault as TXT",
                f"vault_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                "Text Files (*.txt)",
            )

            if not file_path:
                return

            with open(file_path, "w", encoding="utf-8") as f:
                f.write("=" * 60 + "\n")
                f.write("SECUREPASS PRO - VAULT EXPORT\n")
                f.write(f"Exported: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write("=" * 60 + "\n\n")

                for i, pwd in enumerate(passwords, 1):
                    f.write(f"{i:3}. Name: {pwd.get('name', '')}\n")
                    f.write(f"     Password: {pwd.get('password', '')}\n")
                    f.write("-" * 60 + "\n")

                f.write(f"\nTotal: {len(passwords)} passwords\n")

            QMessageBox.information(self, "Success", f"Vault exported to:\n{file_path}")

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to export: {str(e)}")

    def _export_vault_excel(self):
        if not self.master_password:
            return

        try:
            self.controller.set_master_password(self.master_password)
            passwords = self.controller.get_passwords()

            if not passwords:
                QMessageBox.warning(self, "Empty", "No passwords to export.")
                return

            file_path, _ = QFileDialog.getSaveFileName(
                self,
                "Export Vault as Excel",
                f"vault_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
                "Excel Files (*.xlsx)",
            )

            if not file_path:
                return

            wb = Workbook()
            ws = wb.active
            ws.title = "Vault Export"

            ws["A1"] = "#"
            ws["B1"] = "Name"
            ws["C1"] = "Password"

            for i, pwd in enumerate(passwords, 1):
                ws[f"A{i+1}"] = i
                ws[f"B{i+1}"] = pwd.get("name", "")
                ws[f"C{i+1}"] = pwd.get("password", "")

            ws.column_dimensions["A"].width = 8
            ws.column_dimensions["B"].width = 30
            ws.column_dimensions["C"].width = 40

            wb.save(file_path)
            QMessageBox.information(self, "Success", f"Vault exported to:\n{file_path}")

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to export: {str(e)}")


if __name__ == "__main__":
    app = QApplication(sys.argv)

    app.setApplicationName("SecurePass Pro")

    palette = QPalette()
    palette.setColor(QPalette.ColorRole.Window, QColor(15, 15, 26))
    palette.setColor(QPalette.ColorRole.WindowText, QColor(232, 232, 240))
    palette.setColor(QPalette.ColorRole.Base, QColor(26, 26, 46))
    palette.setColor(QPalette.ColorRole.AlternateBase, QColor(20, 20, 36))
    palette.setColor(QPalette.ColorRole.ToolTipBase, QColor(26, 26, 46))
    palette.setColor(QPalette.ColorRole.ToolTipText, QColor(232, 232, 240))
    palette.setColor(QPalette.ColorRole.Text, QColor(232, 232, 240))
    palette.setColor(QPalette.ColorRole.Button, QColor(42, 42, 64))
    palette.setColor(QPalette.ColorRole.ButtonText, QColor(232, 232, 240))
    palette.setColor(QPalette.ColorRole.BrightText, QColor(255, 255, 255))
    palette.setColor(QPalette.ColorRole.Highlight, QColor(74, 111, 165))
    palette.setColor(QPalette.ColorRole.HighlightedText, QColor(255, 255, 255))
    app.setPalette(palette)

    window = SecurePassGUI()
    window.show()
    sys.exit(app.exec())
