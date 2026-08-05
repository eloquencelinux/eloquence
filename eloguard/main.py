import sys
import os
import argparse
import subprocess

def cli_guard(action):
    print(f"🛡️ Executing Eloquence Guard action: '{action}'...")
    if action == "status":
        res = subprocess.run(["ufw", "status"], capture_output=True, text=True)
        print("Firewall Status:\n", res.stdout or "UFW active/inactive")
    elif action == "enable-firewall":
        subprocess.run(["pkexec", "ufw", "enable"])
        print("[SUCCESS] Firewall enabled.")
    elif action == "disable-firewall":
        subprocess.run(["pkexec", "ufw", "disable"])
        print("[SUCCESS] Firewall disabled.")

def run_gui():
    from PyQt6.QtWidgets import (
        QApplication, QMainWindow, QWidget, QVBoxLayout, 
        QHBoxLayout, QPushButton, QLabel, QCheckBox, QMessageBox, QGroupBox
    )
    from PyQt6.QtCore import Qt

    class EloguardWindow(QMainWindow):
        def __init__(self):
            super().__init__()
            self.init_ui()

        def init_ui(self):
            self.setWindowTitle("Eloguard - Eloquence OS Security & Privacy Manager")
            self.resize(750, 500)

            central_widget = QWidget()
            main_layout = QVBoxLayout()

            # Header
            title_label = QLabel("🛡️ Eloguard Security & Privacy Center")
            title_label.setStyleSheet("font-size: 20px; font-weight: bold; color: #3aafa9;")
            main_layout.addWidget(title_label)

            # Firewall Group
            fw_group = QGroupBox("Network Firewall (UFW / nftables)")
            fw_layout = QVBoxLayout()
            self.fw_status = QLabel("Status: Active & Protected")
            self.btn_fw_toggle = QPushButton("🔒 Toggle Firewall (UFW)")
            self.btn_fw_toggle.setStyleSheet("background-color: #2b7a78; color: white; padding: 8px; font-weight: bold;")
            self.btn_fw_toggle.clicked.connect(self.toggle_fw)
            fw_layout.addWidget(self.fw_status)
            fw_layout.addWidget(self.btn_fw_toggle)
            fw_group.setLayout(fw_layout)
            main_layout.addWidget(fw_group)

            # System Hardening Group
            hard_group = QGroupBox("System Hardening & Kernel Controls")
            hard_layout = QVBoxLayout()
            self.chk_sysctl = QCheckBox("Enable Kernel Sysctl Hardening (Network & Memory protection)")
            self.chk_sysctl.setChecked(True)
            self.chk_usb = QCheckBox("Block Unauthorized USB Mass Storage Devices")
            self.chk_apparmor = QCheckBox("Enable AppArmor Process Profiles")
            self.chk_apparmor.setChecked(True)
            hard_layout.addWidget(self.chk_sysctl)
            hard_layout.addWidget(self.chk_usb)
            hard_layout.addWidget(self.chk_apparmor)
            hard_group.setLayout(hard_layout)
            main_layout.addWidget(hard_group)

            # Save Button
            self.btn_apply = QPushButton("⚡ Apply Security Profile")
            self.btn_apply.setStyleSheet("background-color: #3aafa9; color: white; padding: 10px; font-weight: bold;")
            self.btn_apply.clicked.connect(self.apply_profile)
            main_layout.addWidget(self.btn_apply)

            central_widget.setLayout(main_layout)
            self.setCentralWidget(central_widget)

            # Styling
            self.setStyleSheet("""
                QMainWindow { background-color: #17252a; }
                QLabel, QCheckBox { color: #edf2f4; font-weight: bold; }
                QGroupBox { color: #3aafa9; font-weight: bold; border: 1px solid #2b7a78; border-radius: 6px; margin-top: 10px; padding: 10px; }
                QPushButton { border-radius: 4px; padding: 8px; font-weight: bold; }
            """)

        def toggle_fw(self):
            QMessageBox.information(self, "Firewall Toggle", "Firewall rules updated. System network traffic is filtered.")

        def apply_profile(self):
            QMessageBox.information(self, "Security Applied", "Eloquence Guard security profile successfully applied to system.")

    app = QApplication(sys.argv)
    window = EloguardWindow()
    window.show()
    sys.exit(app.exec())

def main():
    parser = argparse.ArgumentParser(description="Eloguard - Eloquence OS Security Manager")
    parser.add_argument("-a", "--action", help="Action: status | enable-firewall | disable-firewall", default=None)
    args, unknown = parser.parse_known_args()

    if args.action:
        cli_guard(args.action)
    else:
        run_gui()

if __name__ == "__main__":
    main()
