import sys
import os
import argparse
import subprocess

def run_gui():
    from PyQt6.QtWidgets import (
        QApplication, QMainWindow, QWidget, QVBoxLayout, 
        QHBoxLayout, QPushButton, QLabel, QMessageBox, QGroupBox, QGridLayout
    )
    from PyQt6.QtGui import QPixmap, QIcon
    from PyQt6.QtCore import Qt

    class ElowelcomeWindow(QMainWindow):
        def __init__(self):
            super().__init__()
            self.init_ui()

        def init_ui(self):
            self.setWindowTitle("Welcome to Eloquence GNU/Linux 2026.1")
            self.resize(850, 600)

            central_widget = QWidget()
            main_layout = QVBoxLayout()

            # Top Branding Banner
            header_layout = QHBoxLayout()
            
            logo_label = QLabel()
            logo_path = "/usr/share/pixmaps/eloquence-logo.png"
            if not os.path.exists(logo_path):
                logo_path = "config/includes.chroot/usr/share/pixmaps/eloquence-logo.png"

            if os.path.exists(logo_path):
                pixmap = QPixmap(logo_path).scaled(90, 90, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
                logo_label.setPixmap(pixmap)
            
            title_box = QVBoxLayout()
            title_label = QLabel("⚡ Welcome to Eloquence GNU/Linux")
            title_label.setStyleSheet("font-size: 24px; font-weight: bold; color: #3aafa9;")
            sub_label = QLabel("Enterprise-grade, high-performance Linux distribution with Cinnamon Desktop & 8-in-1 Suite.")
            sub_label.setStyleSheet("color: #a0aab2; font-size: 13px;")

            title_box.addWidget(title_label)
            title_box.addWidget(sub_label)

            header_layout.addWidget(logo_label)
            header_layout.addLayout(title_box)
            header_layout.addStretch()

            main_layout.addLayout(header_layout)

            # Quick Actions Grid
            actions_group = QGroupBox("🚀 Quick Getting Started Actions")
            actions_layout = QGridLayout()

            btn_update = QPushButton("⚡ Update System Packages")
            btn_update.setStyleSheet("background-color: #2b7a78; color: white; padding: 12px; font-weight: bold;")
            btn_update.clicked.connect(self.update_system)

            btn_theme = QPushButton("🎨 Toggle Theme (Dark / Light)")
            btn_theme.setStyleSheet("background-color: #3aafa9; color: white; padding: 12px; font-weight: bold;")
            btn_theme.clicked.connect(self.launch_tweak)

            btn_install_os = QPushButton("💿 Install Eloquence to Disk")
            btn_install_os.setStyleSheet("background-color: #e63946; color: white; padding: 12px; font-weight: bold;")
            btn_install_os.clicked.connect(self.launch_installer)

            btn_guard = QPushButton("🛡️ Security & Privacy Center")
            btn_guard.setStyleSheet("background-color: #1d3557; color: white; padding: 12px; font-weight: bold;")
            btn_guard.clicked.connect(self.launch_guard)

            actions_layout.addWidget(btn_update, 0, 0)
            actions_layout.addWidget(btn_theme, 0, 1)
            actions_layout.addWidget(btn_install_os, 1, 0)
            actions_layout.addWidget(btn_guard, 1, 1)

            actions_group.setLayout(actions_layout)
            main_layout.addWidget(actions_group)

            # Popular Apps Quick Install Group
            apps_group = QGroupBox("📦 1-Click Popular Software Installers")
            apps_layout = QHBoxLayout()

            btn_vscode = QPushButton("💻 VS Code")
            btn_vscode.clicked.connect(lambda: self.install_app("code"))

            btn_firefox = QPushButton("🦊 Firefox")
            btn_firefox.clicked.connect(lambda: self.install_app("firefox-esr"))

            btn_vlc = QPushButton("🎬 VLC Player")
            btn_vlc.clicked.connect(lambda: self.install_app("vlc"))

            btn_gimp = QPushButton("🎨 GIMP")
            btn_gimp.clicked.connect(lambda: self.install_app("gimp"))

            apps_layout.addWidget(btn_vscode)
            apps_layout.addWidget(btn_firefox)
            apps_layout.addWidget(btn_vlc)
            apps_layout.addWidget(btn_gimp)

            apps_group.setLayout(apps_layout)
            main_layout.addWidget(apps_group)

            # Footer
            footer_layout = QHBoxLayout()
            footer_label = QLabel("Eloquence GNU/Linux 2026.1 (Trixie)")
            footer_label.setStyleSheet("color: #7f8c8d; font-size: 11px;")

            btn_close = QPushButton("Done / Close")
            btn_close.clicked.connect(self.close)

            footer_layout.addWidget(footer_label)
            footer_layout.addStretch()
            footer_layout.addWidget(btn_close)

            main_layout.addLayout(footer_layout)

            central_widget.setLayout(main_layout)
            self.setCentralWidget(central_widget)

            # Styling
            self.setStyleSheet("""
                QMainWindow { background-color: #17252a; }
                QLabel { color: #edf2f4; font-weight: bold; }
                QGroupBox { color: #3aafa9; font-weight: bold; border: 1px solid #2b7a78; border-radius: 6px; margin-top: 10px; padding: 10px; }
                QPushButton { border-radius: 4px; font-size: 13px; background-color: #2b2d42; color: #edf2f4; padding: 8px; font-weight: bold; }
                QPushButton:hover { background-color: #3aafa9; color: white; }
            """)

        def update_system(self):
            QMessageBox.information(self, "System Update", "Launching system update via APT...")
            subprocess.Popen(["pkexec", "apt", "update"])

        def launch_tweak(self):
            subprocess.Popen(["python3", "-m", "elotweak.main"])

        def launch_installer(self):
            subprocess.Popen(["pkexec", "calamares"])

        def launch_guard(self):
            subprocess.Popen(["python3", "-m", "eloguard.main"])

        def install_app(self, pkg_name):
            QMessageBox.information(self, "App Installer", f"Installing package: '{pkg_name}'...")
            subprocess.Popen(["pkexec", "apt", "install", "-y", pkg_name])

    app = QApplication(sys.argv)
    window = ElowelcomeWindow()
    window.show()
    sys.exit(app.exec())

def main():
    parser = argparse.ArgumentParser(description="Elowelcome - Eloquence First-Run Experience")
    args, unknown = parser.parse_known_args()
    run_gui()

if __name__ == "__main__":
    main()
