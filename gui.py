"""
SecurePass Pro - Enterprise-Grade Password Manager
Modern, vertical GUI with smooth animations and professional design
"""

import sys
import os
from datetime import datetime
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QSlider, QProgressBar,
    QTabWidget, QFrame, QMessageBox, QListWidget, QListWidgetItem,
    QPushButton, QFileDialog
)
from PyQt6.QtCore import Qt, QPropertyAnimation, QEasingCurve, pyqtProperty, QTimer, QPoint
from PyQt6.QtGui import QPalette, QColor, QAction, QCursor
import pyperclip
from openpyxl import Workbook

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
        self._target_value = value
        self.animation.stop()
        self.animation.setStartValue(self._current_value)
        self.animation.setEndValue(value)
        self.animation.start()

    def _update_value(self, value):
        self._current_value = value
        super().setValue(value)


class ClickableListWidget(QListWidget):
    """Custom list widget with hover delete button"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent_widget = parent
        self.setMouseTracking(True)
        self._hovered_index = None

    def mouseMoveEvent(self, event):
        index = self.indexAt(event.position().toPoint())
        if index != self._hovered_index:
            self._hovered_index = index
            self.update()
        super().mouseMoveEvent(event)

    def leaveEvent(self, event):
        self._hovered_index = None
        self.update()
        super().leaveEvent(event)


class SecurePassGUI(QMainWindow):
    """Main application window with vertical layout and professional design"""

    def __init__(self):
        super().__init__()
        self.controller = PasswordController()
        self.password_history = []
        self.check_history = []

        # Initialize all widget attributes
        self.length_slider = None
        self.length_display = None
        self.password_display = None
        self.check_input = None
        self.result_frame = None
        self.score_label = None
        self.level_label = None
        self.progress_bar = None
        self.suggestions_label = None
        self.suggestions_text = None
        self.copy_btn = None
        self.history_list = None
        self.history_export_btn = None
        self.check_export_btn = None
        self.strength_bar = None
        self.strength_label = None

        self.setup_window()
        self.setup_ui()
        self.center_window()

    def setup_window(self):
        """Configure main window properties"""
        self.setWindowTitle("SecurePass Pro")
        self.setMinimumSize(420, 620)
        self.setMaximumSize(540, 780)
        self.setStyleSheet(self._get_style_sheet())

    def center_window(self):
        """Center window on screen with vertical aspect ratio"""
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
            QListWidget {
                background-color: #1a1a2e;
                color: #e8e8f0;
                border: 1px solid #2a2a40;
                border-radius: 6px;
                font-family: 'Consolas';
                font-size: 11px;
                padding: 4px;
            }
            QListWidget::item {
                padding: 6px 10px;
                border-radius: 4px;
            }
            QListWidget::item:hover {
                background-color: #2a2a40;
            }
            QListWidget::item:selected {
                background-color: #4a6fa5;
                color: white;
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
            QFrame#history_frame {
                background-color: #1a1a2e;
                border: 1px solid #2a2a40;
                border-radius: 10px;
                padding: 10px;
            }
        """

    def setup_ui(self):
        """Build the entire user interface"""
        central = QWidget()
        self.setCentralWidget(central)
        main_layout = QVBoxLayout(central)
        main_layout.setContentsMargins(20, 16, 20, 16)
        main_layout.setSpacing(12)

        self._build_header(main_layout)

        tabs = QTabWidget()
        tabs.addTab(self._build_generator_tab(), "⚡ Generate")
        tabs.addTab(self._build_checker_tab(), "🛡️ Checker")
        main_layout.addWidget(tabs)

        self._build_footer(main_layout)

    def _build_header(self, parent):
        """Build the header with title and subtitle"""
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
        """Build the password generator tab"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.setSpacing(10)

        # Password generation card
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
        self.password_display.setPlaceholderText("Your secure password will appear here")
        card_layout.addWidget(self.password_display)

        copy_layout = QHBoxLayout()
        copy_layout.setSpacing(8)

        self.copy_btn = QPushButton("📋 Copy")
        self.copy_btn.setObjectName("copy_btn")
        self.copy_btn.clicked.connect(self._copy_password)
        copy_layout.addWidget(self.copy_btn)

        refresh_btn = QPushButton("🔄 Regenerate")
        refresh_btn.setObjectName("copy_btn")
        refresh_btn.clicked.connect(self._on_generate)
        copy_layout.addWidget(refresh_btn)

        card_layout.addLayout(copy_layout)

        # Strength meter inside the same card
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

        # History section
        self._build_history_section(layout)

        layout.addStretch()
        return tab

    def _build_history_section(self, parent):
        """Build the password history section"""
        history_frame = QFrame()
        history_frame.setObjectName("history_frame")
        history_layout = QVBoxLayout(history_frame)
        history_layout.setSpacing(6)

        header_layout = QHBoxLayout()
        history_title = QLabel("📜 Password History")
        history_title.setObjectName("section_title")
        header_layout.addWidget(history_title)

        header_layout.addStretch()

        self.history_export_btn = QPushButton("📤 Export")
        self.history_export_btn.setObjectName("export_btn")
        self.history_export_btn.clicked.connect(self._export_history)
        header_layout.addWidget(self.history_export_btn)

        history_layout.addLayout(header_layout)

        self.history_list = ClickableListWidget(self)
        self.history_list.setMinimumHeight(60)
        self.history_list.setMaximumHeight(100)
        self.history_list.itemClicked.connect(self._on_history_item_clicked)
        history_layout.addWidget(self.history_list)

        parent.addWidget(history_frame)

    def _build_checker_tab(self):
        """Build the password checker tab"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.setSpacing(10)

        # Checker input card
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

        check_btn = QPushButton("🔍 Analyze Password")
        check_btn.clicked.connect(self._on_check)
        card_layout.addWidget(check_btn)

        layout.addWidget(card)

        # Result display
        self._build_result_display(layout)

        # Export button
        export_layout = QHBoxLayout()
        export_layout.addStretch()

        self.check_export_btn = QPushButton("📄 Export Report as TXT")
        self.check_export_btn.setObjectName("export_btn")
        self.check_export_btn.clicked.connect(self._export_check_report)
        self.check_export_btn.setVisible(False)
        export_layout.addWidget(self.check_export_btn)

        layout.addLayout(export_layout)

        layout.addStretch()
        return tab

    def _build_result_display(self, parent):
        """Build the result display for checker tab"""
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

        self.suggestions_label = QLabel("Suggestions:")
        self.suggestions_label.setObjectName("section_title")
        self.suggestions_label.setStyleSheet("margin-top: 4px;")
        result_layout.addWidget(self.suggestions_label)

        self.suggestions_text = QLabel("")
        self.suggestions_text.setWordWrap(True)
        self.suggestions_text.setStyleSheet(
            "color: #a0a0b8; font-size: 11px; font-family: 'Segoe UI';"
        )
        result_layout.addWidget(self.suggestions_text)

        parent.addWidget(self.result_frame)

    def _build_footer(self, parent):
        """Build the footer with status tips"""
        footer = QLabel(
            "🔒 All operations are performed locally. Your passwords never leave your device."
        )
        footer.setStyleSheet("color: #606080; font-size: 8px; font-family: 'Segoe UI';")
        footer.setAlignment(Qt.AlignmentFlag.AlignCenter)
        parent.addWidget(footer)

    def _update_length_display(self, value):
        """Update the length label when slider changes"""
        self.length_display.setText(str(value))

    def _on_generate(self):
        """Handle generate button click"""
        length = self.length_slider.value()
        password = self.controller.generate(length)
        self.password_display.setText(password)

        # Add to history
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.password_history.append((timestamp, password))
        self._update_history_list()

        # Update strength meter
        self._update_strength_meter(password)

    def _update_history_list(self):
        """Update the history list widget"""
        self.history_list.clear()
        for i, (timestamp, pwd) in enumerate(reversed(self.password_history[-10:])):
            item_text = f"[{timestamp}] {pwd}"
            item = QListWidgetItem(item_text)
            item.setData(Qt.ItemDataRole.UserRole, i)
            self.history_list.addItem(item)

    def _on_history_item_clicked(self, item):
        """Handle click on history item - show delete button"""
        # Get the actual index in the reversed list
        idx = len(self.password_history) - self.history_list.row(item) - 1

        # Show delete confirmation
        reply = QMessageBox.question(
            self,
            "Delete Password",
            f"Delete this password from history?\n\n{item.text()}",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )

        if reply == QMessageBox.StandardButton.Yes:
            del self.password_history[idx]
            self._update_history_list()

    def _update_strength_meter(self, password):
        """Update the strength meter with animation"""
        result = self.controller.check(password)
        score = result["score"]

        self.strength_bar.setValue(score)

        if score >= 85:
            color = "#4a9eff"
            level_text = "🔵 Excellent"
        elif score >= 70:
            color = "#4caf50"
            level_text = "🟢 Good"
        elif score >= 50:
            color = "#ffc107"
            level_text = "🟡 Medium"
        elif score >= 30:
            color = "#ff9800"
            level_text = "🟠 Weak"
        else:
            color = "#f44336"
            level_text = "🔴 Very Weak"

        self.strength_bar.setStyleSheet(
            f"QProgressBar::chunk {{ background-color: {color}; border-radius: 5px; }}"
        )
        self.strength_label.setText(f"{level_text} ({score}/100)")

    def _copy_password(self):
        """Copy current password to clipboard"""
        pwd = self.password_display.text()
        if pwd:
            pyperclip.copy(pwd)
            self.copy_btn.setText("✅ Copied!")
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
        """Reset copy button to original state"""
        self.copy_btn.setText("📋 Copy")
        self.copy_btn.setStyleSheet("")

    def _on_check(self):
        """Handle check button click"""
        password = self.check_input.text()
        if not password:
            QMessageBox.warning(self, "Empty", "Please enter a password to check.")
            return

        result = self.controller.check(password)
        self._display_check_result(result)

        # Store for export
        self.last_check_result = {
            "password": password,
            "result": result,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        self.check_export_btn.setVisible(True)

    def _display_check_result(self, result):
        """Display the check result with animations"""
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
            self.suggestions_text.setText("✅ No improvements needed. Your password is excellent!")

    def _export_history(self):
        """Export password history to TXT and Excel"""
        if not self.password_history:
            QMessageBox.warning(self, "Empty", "No passwords in history to export.")
            return

        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Export History",
            f"password_history_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            "Excel Files (*.xlsx);;Text Files (*.txt)"
        )

        if not file_path:
            return

        try:
            if file_path.endswith('.xlsx'):
                self._export_history_excel(file_path)
            else:
                self._export_history_txt(file_path)

            QMessageBox.information(self, "Success", f"History exported to:\n{file_path}")

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to export: {str(e)}")

    def _export_history_txt(self, file_path):
        """Export history as TXT"""
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write("=" * 60 + "\n")
            f.write("SECUREPASS PRO - PASSWORD HISTORY\n")
            f.write(f"Exported: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("=" * 60 + "\n\n")

            for i, (timestamp, pwd) in enumerate(self.password_history, 1):
                f.write(f"{i:3}. [{timestamp}] {pwd}\n")

            f.write("\n" + "=" * 60 + "\n")
            f.write(f"Total passwords: {len(self.password_history)}\n")

    def _export_history_excel(self, file_path):
        """Export history as Excel"""
        wb = Workbook()
        ws = wb.active
        ws.title = "Password History"

        ws['A1'] = "#"
        ws['B1'] = "Timestamp"
        ws['C1'] = "Password"
        ws['D1'] = "Length"

        for i, (timestamp, pwd) in enumerate(self.password_history, 1):
            ws[f'A{i+1}'] = i
            ws[f'B{i+1}'] = timestamp
            ws[f'C{i+1}'] = pwd
            ws[f'D{i+1}'] = len(pwd)

        ws.column_dimensions['A'].width = 8
        ws.column_dimensions['B'].width = 20
        ws.column_dimensions['C'].width = 40
        ws.column_dimensions['D'].width = 12

        wb.save(file_path)

    def _export_check_report(self):
        """Export check result as TXT"""
        if not hasattr(self, 'last_check_result'):
            QMessageBox.warning(self, "Empty", "No check result to export.")
            return

        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Export Report",
            f"password_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
            "Text Files (*.txt)"
        )

        if not file_path:
            return

        try:
            data = self.last_check_result
            result = data["result"]

            with open(file_path, 'w', encoding='utf-8') as f:
                f.write("=" * 60 + "\n")
                f.write("SECUREPASS PRO - PASSWORD SECURITY REPORT\n")
                f.write("=" * 60 + "\n\n")

                f.write(f"Password: {data['password']}\n")
                f.write(f"Checked: {data['timestamp']}\n\n")

                f.write("-" * 60 + "\n")
                f.write("ANALYSIS RESULTS\n")
                f.write("-" * 60 + "\n")

                f.write(f"Score: {result['score']}/100\n")
                f.write(f"Level: {result['level']}\n\n")

                if result['suggestions']:
                    f.write("Suggestions:\n")
                    for s in result['suggestions']:
                        f.write(f"  • {s}\n")
                else:
                    f.write("✅ No suggestions. Password is excellent!\n")

                f.write("\n" + "=" * 60 + "\n")
                f.write("Generated by SecurePass Pro\n")

            QMessageBox.information(self, "Success", f"Report exported to:\n{file_path}")

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
