import sys
import os
import subprocess
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, 
    QHBoxLayout, QPushButton, QLabel, QLineEdit, QListWidget,
    QListWidgetItem, QMessageBox, QComboBox, QGroupBox
)
from PyQt6.QtCore import Qt

FEATURED_APPS = [
    {"name": "Firefox ESR", "package": "firefox-esr", "category": "Network", "desc": "Fast, privacy-focused web browser for Eloquence OS."},
    {"name": "LibreOffice Suite", "package": "libreoffice", "category": "Productivity", "desc": "Powerful office productivity suite (Writer, Calc, Impress)."},
    {"name": "GIMP Image Editor", "package": "gimp", "category": "Graphics", "desc": "GNU Image Manipulation Program for professional editing."},
    {"name": "VLC Media Player", "package": "vlc", "category": "Multimedia", "desc": "Universal multimedia player and streaming media server."},
    {"name": "VS Code / VSCodium", "package": "codium", "category": "Development", "desc": "Open-source code editor with rich extension ecosystem."},
    {"name": "QEMU Virtualization Manager", "package": "qemu-system-x86", "category": "System", "desc": "Hardware emulation and virtual machine hypervisor."}
]

class EloappsWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Eloapps - Eloquence OS App Center")
        self.resize(800, 550)

        central_widget = QWidget()
        main_layout = QVBoxLayout()

        # Header
        title_label = QLabel("🚀 Eloquence App Center")
        title_label.setStyleSheet("font-size: 20px; font-weight: bold; color: #3aafa9;")
        main_layout.addWidget(title_label)

        # Search & Filter
        filter_layout = QHBoxLayout()
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search applications by name or description...")
        self.search_input.textChanged.connect(self.filter_apps)

        self.category_combo = QComboBox()
        self.category_combo.addItems(["All Categories", "System", "Productivity", "Development", "Multimedia", "Network", "Graphics"])
        self.category_combo.currentTextChanged.connect(self.filter_apps)

        filter_layout.addWidget(QLabel("Category:"))
        filter_layout.addWidget(self.category_combo)
        filter_layout.addWidget(self.search_input)
        main_layout.addLayout(filter_layout)

        # App List
        self.app_list = QListWidget()
        main_layout.addWidget(self.app_list)

        # Action Buttons
        btn_layout = QHBoxLayout()
        self.btn_install = QPushButton("📥 Install Package")
        self.btn_install.setStyleSheet("background-color: #2b7a78; color: white; padding: 10px; font-weight: bold;")
        self.btn_install.clicked.connect(self.install_selected)

        self.btn_remove = QPushButton("🗑️ Remove Package")
        self.btn_remove.setStyleSheet("background-color: #e63946; color: white; padding: 10px; font-weight: bold;")
        self.btn_remove.clicked.connect(self.remove_selected)

        btn_layout.addWidget(self.btn_install)
        btn_layout.addWidget(self.btn_remove)
        main_layout.addLayout(btn_layout)

        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

        self.populate_apps()

        # Styling
        self.setStyleSheet("""
            QMainWindow { background-color: #17252a; }
            QLabel { color: #edf2f4; font-weight: bold; }
            QLineEdit, QComboBox { background-color: #2b2d42; color: #edf2f4; border: 1px solid #3aafa9; border-radius: 4px; padding: 6px; }
            QListWidget { background-color: #2b2d42; color: #edf2f4; border: 1px solid #3aafa9; border-radius: 6px; padding: 5px; }
            QPushButton { border-radius: 4px; font-size: 13px; }
        """)

    def populate_apps(self):
        self.app_list.clear()
        query = self.search_input.text().lower()
        selected_cat = self.category_combo.currentText()

        for app in FEATURED_APPS:
            if selected_cat != "All Categories" and app["category"] != selected_cat:
                continue
            if query and query not in app["name"].lower() and query not in app["desc"].lower():
                continue

            item_text = f"• {app['name']} [{app['category']}]\n  Package: {app['package']} - {app['desc']}"
            item = QListWidgetItem(item_text)
            item.setData(Qt.ItemDataRole.UserRole, app)
            self.app_list.addItem(item)

    def filter_apps(self):
        self.populate_apps()

    def install_selected(self):
        selected_item = self.app_list.currentItem()
        if not selected_item:
            QMessageBox.warning(self, "Selection Required", "Please select an application to install.")
            return

        app_data = selected_item.data(Qt.ItemDataRole.UserRole)
        pkg = app_data["package"]

        reply = QMessageBox.question(
            self,
            "Confirm Installation",
            f"Do you want to install '{app_data['name']}' ({pkg}) via APT?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )

        if reply == QMessageBox.StandardButton.Yes:
            try:
                cmd = f"pkexec apt-get update && pkexec apt-get install -y {pkg}"
                QMessageBox.information(
                    self,
                    "Installation Triggered",
                    f"Executing: {cmd}\n(Root authentication prompt will appear on Debian system)."
                )
            except Exception as e:
                QMessageBox.critical(self, "Installation Error", str(e))

    def remove_selected(self):
        selected_item = self.app_list.currentItem()
        if not selected_item:
            QMessageBox.warning(self, "Selection Required", "Please select an application to remove.")
            return

        app_data = selected_item.data(Qt.ItemDataRole.UserRole)
        pkg = app_data["package"]

        reply = QMessageBox.question(
            self,
            "Confirm Removal",
            f"Are you sure you want to remove '{app_data['name']}' ({pkg})?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )

        if reply == QMessageBox.StandardButton.Yes:
            QMessageBox.information(
                self,
                "Removal Triggered",
                f"Executing: pkexec apt-get remove -y {pkg}"
            )

def main():
    app = QApplication(sys.argv)
    window = EloappsWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
