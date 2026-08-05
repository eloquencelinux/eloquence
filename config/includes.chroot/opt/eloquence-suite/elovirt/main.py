import sys
import os
import psutil
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, 
    QHBoxLayout, QPushButton, QLabel, QListWidget, QMessageBox,
    QFileDialog, QSpinBox, QGroupBox, QFormLayout
)
from PyQt6.QtCore import Qt
from elovirt.qemu_wrapper import QemuManager

class ElovirtWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.qemu = QemuManager()
        self.running_vms = {}
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Elovirt - Eloquence Virtualization Manager")
        self.resize(750, 520)

        central_widget = QWidget()
        main_layout = QVBoxLayout()

        # Header
        title_label = QLabel("⚡ Elovirt Control Center")
        title_label.setStyleSheet("font-size: 20px; font-weight: bold; color: #3aafa9; margin-bottom: 5px;")
        main_layout.addWidget(title_label)

        sub_label = QLabel(f"QEMU Binary: {self.qemu.qemu_bin} | KVM Available: {'Yes' if self.qemu.check_kvm_support() else 'No (Software Emulation)'}")
        sub_label.setStyleSheet("font-size: 12px; color: #a0aab2; margin-bottom: 10px;")
        main_layout.addWidget(sub_label)

        # VM List Group
        vm_group = QGroupBox("Virtual Machines")
        vm_layout = QVBoxLayout()
        self.vm_list = QListWidget()
        self.vm_list.addItems([
            "Eloquence-OS-Live (x64 ISO)",
            "Development-Node-01 (Debian arm64)",
            "Test-Sandbox-VM"
        ])
        vm_layout.addWidget(self.vm_list)
        vm_group.setLayout(vm_layout)
        main_layout.addWidget(vm_group)

        # Launch Controls
        controls_layout = QHBoxLayout()
        
        self.btn_start = QPushButton("▶ Launch VM")
        self.btn_start.setStyleSheet("background-color: #2b7a78; color: white; padding: 10px; font-weight: bold;")
        self.btn_start.clicked.connect(self.handle_start_vm)
        
        self.btn_stop = QPushButton("⏹ Stop VM")
        self.btn_stop.setStyleSheet("background-color: #e63946; color: white; padding: 10px; font-weight: bold;")
        self.btn_stop.clicked.connect(self.handle_stop_vm)

        self.btn_refresh = QPushButton("🔄 Refresh Status")
        self.btn_refresh.setStyleSheet("background-color: #3aafa9; color: white; padding: 10px; font-weight: bold;")
        self.btn_refresh.clicked.connect(self.handle_refresh_status)

        controls_layout.addWidget(self.btn_start)
        controls_layout.addWidget(self.btn_stop)
        controls_layout.addWidget(self.btn_refresh)
        main_layout.addLayout(controls_layout)

        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

        # Dark Theme Styling
        self.setStyleSheet("""
            QMainWindow {
                background-color: #17252a;
            }
            QGroupBox {
                font-weight: bold;
                color: #edf2f4;
                border: 1px solid #2b7a78;
                border-radius: 6px;
                margin-top: 10px;
                padding-top: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px;
            }
            QListWidget {
                background-color: #2b2d42;
                color: #edf2f4;
                border: 1px solid #3aafa9;
                border-radius: 4px;
                font-size: 14px;
                padding: 5px;
            }
            QListWidget::item:selected {
                background-color: #3aafa9;
                color: #17252a;
            }
            QPushButton {
                border-radius: 4px;
                font-size: 13px;
            }
            QPushButton:hover {
                opacity: 0.85;
            }
        """)

    def handle_start_vm(self):
        selected_item = self.vm_list.currentItem()
        if not selected_item:
            QMessageBox.warning(self, "Selection Required", "Please select a Virtual Machine to start.")
            return
        
        vm_name = selected_item.text().split(" (")[0]
        
        if vm_name in self.running_vms:
            proc = self.running_vms[vm_name]
            if proc.poll() is None:
                QMessageBox.information(self, "VM Running", f"Virtual machine '{vm_name}' is already active.")
                return

        try:
            if not self.qemu.check_availability():
                QMessageBox.warning(
                    self,
                    "QEMU Not Installed",
                    f"QEMU binary '{self.qemu.qemu_bin}' was not found. Please install QEMU via package manager."
                )
                return

            proc = self.qemu.start_vm(vm_name=vm_name, memory="2G", cpus="2")
            self.running_vms[vm_name] = proc
            selected_item.setText(f"{vm_name} (Running - PID: {proc.pid})")
            QMessageBox.information(self, "VM Started", f"Virtual machine '{vm_name}' launched with PID {proc.pid}.")
        except Exception as e:
            QMessageBox.critical(self, "Execution Error", f"Failed to launch VM: {str(e)}")

    def handle_stop_vm(self):
        selected_item = self.vm_list.currentItem()
        if not selected_item:
            QMessageBox.warning(self, "Selection Required", "Please select a Virtual Machine to stop.")
            return
        
        vm_name = selected_item.text().split(" (")[0]
        if vm_name in self.running_vms:
            proc = self.running_vms[vm_name]
            if proc.poll() is None:
                proc.terminate()
                proc.wait(timeout=3)
                selected_item.setText(f"{vm_name} (Stopped)")
                QMessageBox.information(self, "VM Stopped", f"Virtual machine '{vm_name}' has been terminated.")
                del self.running_vms[vm_name]
                return

        QMessageBox.information(self, "VM Status", f"Virtual machine '{vm_name}' is not currently running.")

    def handle_refresh_status(self):
        updated_count = 0
        for i in range(self.vm_list.count()):
            item = self.vm_list.item(i)
            vm_name = item.text().split(" (")[0]
            if vm_name in self.running_vms:
                proc = self.running_vms[vm_name]
                if proc.poll() is None:
                    item.setText(f"{vm_name} (Running - PID: {proc.pid})")
                else:
                    item.setText(f"{vm_name} (Stopped)")
                    del self.running_vms[vm_name]
            else:
                item.setText(f"{vm_name} (Stopped)")
            updated_count += 1

        QMessageBox.information(self, "Status Refreshed", f"Checked status for {updated_count} virtual machines.")

def main():
    app = QApplication(sys.argv)
    window = ElovirtWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
