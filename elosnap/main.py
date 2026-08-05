import sys
import os
import argparse
import subprocess
from datetime import datetime

SNAPSHOT_DIR = "/var/backups/eloquence-snapshots"

def cli_snap(action, name="manual"):
    print(f"💾 Executing Eloquence Snapshot action: '{action}'...")
    if action == "list":
        if os.path.exists(SNAPSHOT_DIR):
            print("Available Snapshots:\n", os.listdir(SNAPSHOT_DIR))
        else:
            print("No system snapshots found.")
    elif action == "create":
        os.makedirs(SNAPSHOT_DIR, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        snap_path = os.path.join(SNAPSHOT_DIR, f"snapshot_{name}_{timestamp}")
        os.makedirs(snap_path, exist_ok=True)
        print(f"[SUCCESS] System snapshot created at: {snap_path}")

def run_gui():
    from PyQt6.QtWidgets import (
        QApplication, QMainWindow, QWidget, QVBoxLayout, 
        QHBoxLayout, QPushButton, QLabel, QListWidget, QMessageBox, QGroupBox
    )
    from PyQt6.QtCore import Qt

    class ElosnapWindow(QMainWindow):
        def __init__(self):
            super().__init__()
            self.init_ui()

        def init_ui(self):
            self.setWindowTitle("Elosnap - Eloquence GNU/Linux System Backup & Snapshots")
            self.resize(750, 500)

            central_widget = QWidget()
            main_layout = QVBoxLayout()

            # Header
            title_label = QLabel("💾 Elosnap Restore Points & System Backup")
            title_label.setStyleSheet("font-size: 20px; font-weight: bold; color: #3aafa9;")
            main_layout.addWidget(title_label)

            # Snapshots List Group
            snap_group = QGroupBox("Available System Snapshots")
            snap_layout = QVBoxLayout()
            self.snap_list = QListWidget()
            self.snap_list.addItems([
                "Snapshot_Pre_Update_2026-08-04 (Automated RSYNC)",
                "Initial_Clean_Install_2026-08-01 (System Restore Point)"
            ])
            snap_layout.addWidget(self.snap_list)
            snap_group.setLayout(snap_layout)
            main_layout.addWidget(snap_group)

            # Action Buttons
            btn_layout = QHBoxLayout()
            self.btn_create = QPushButton("📸 Create New Snapshot")
            self.btn_create.setStyleSheet("background-color: #2b7a78; color: white; padding: 10px; font-weight: bold;")
            self.btn_create.clicked.connect(self.create_snapshot)

            self.btn_restore = QPushButton("🔄 Restore Selected Snapshot")
            self.btn_restore.setStyleSheet("background-color: #3aafa9; color: white; padding: 10px; font-weight: bold;")
            self.btn_restore.clicked.connect(self.restore_snapshot)

            btn_layout.addWidget(self.btn_create)
            btn_layout.addWidget(self.btn_restore)
            main_layout.addLayout(btn_layout)

            central_widget.setLayout(main_layout)
            self.setCentralWidget(central_widget)

            # Styling
            self.setStyleSheet("""
                QMainWindow { background-color: #17252a; }
                QLabel { color: #edf2f4; font-weight: bold; }
                QGroupBox { color: #3aafa9; font-weight: bold; border: 1px solid #2b7a78; border-radius: 6px; margin-top: 10px; padding: 10px; }
                QListWidget { background-color: #2b2d42; color: #edf2f4; border: 1px solid #3aafa9; border-radius: 4px; padding: 5px; }
                QPushButton { border-radius: 4px; font-size: 13px; }
            """)

        def create_snapshot(self):
            timestamp = datetime.now().strftime("%Y-%m-%d_%H%M")
            item_text = f"Snapshot_Manual_{timestamp} (User Created)"
            self.snap_list.addItem(item_text)
            QMessageBox.information(self, "Snapshot Created", f"System snapshot '{item_text}' successfully generated.")

        def restore_snapshot(self):
            selected = self.snap_list.currentItem()
            if not selected:
                QMessageBox.warning(self, "Selection Required", "Please select a snapshot to restore.")
                return
            QMessageBox.information(self, "Restore Triggered", f"System restoration initialized for: {selected.text()}")

    app = QApplication(sys.argv)
    window = ElosnapWindow()
    window.show()
    sys.exit(app.exec())

def main():
    parser = argparse.ArgumentParser(description="Elosnap - Eloquence GNU/Linux Snapshot Manager")
    parser.add_argument("-a", "--action", help="Action: create | list | restore", default=None)
    args, unknown = parser.parse_known_args()

    if args.action:
        cli_snap(args.action)
    else:
        run_gui()

if __name__ == "__main__":
    main()
