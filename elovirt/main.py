import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, 
    QHBoxLayout, QPushButton, QLabel, QLineEdit, QListWidget, QMessageBox
)
from PyQt6.QtCore import Qt
from elovirt.qemu_wrapper import QemuManager

class ElovirtWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.qemu = QemuManager()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Elovirt - Elo-Suite Virtualization Manager")
        self.resize(700, 450)

        central_widget = QWidget()
        main_layout = QVBoxLayout()

        title_label = QLabel("Elovirt Control Center")
        title_label.setStyleSheet("font-size: 18px; font-weight: bold; color: #ffffff;")
        main_layout.addWidget(title_label)

        self.vm_list = QListWidget()
        self.vm_list.addItems(["Development-VM-01 (Stopped)", "Debian-Test-Node (Stopped)"])
        main_layout.addWidget(self.vm_list)

        controls_layout = QHBoxLayout()
        
        self.btn_start = QPushButton("Start Selected VM")
        self.btn_start.setStyleSheet("background-color: #2b7a78; color: white; padding: 8px;")
        self.btn_start.clicked.connect(self.handle_start_vm)
        
        self.btn_refresh = QPushButton("Refresh Status")
        self.btn_refresh.setStyleSheet("background-color: #3aafa9; color: white; padding: 8px;")

        controls_layout.addWidget(self.btn_start)
        controls_layout.addWidget(self.btn_refresh)
        main_layout.addLayout(controls_layout)

        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

        # Apply dark theme styling to the entire window
        self.setStyleSheet("""
            QMainWindow {
                background-color: #17252a;
            }
            QListWidget {
                background-color: #2b2d42;
                color: #edf2f4;
                border: 1px solid #3aafa9;
                border-radius: 4px;
            }
            QPushButton {
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover {
                opacity: 0.8;
            }
        """)

    def handle_start_vm(self):
        selected_item = self.vm_list.currentItem()
        if not selected_item:
            QMessageBox.warning(self, "Selection Error", "Please select a virtual machine to launch.")
            return
        
        try:
            QMessageBox.information(self, "Elovirt Status", f"Initializing sequence for: {selected_item.text()}")
        except Exception as e:
            QMessageBox.critical(self, "Execution Error", str(e))

def main():
    app = QApplication(sys.argv)
    window = ElovirtWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
