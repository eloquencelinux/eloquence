import subprocess
import shutil
import os

class QemuManager:
    def __init__(self):
        self.qemu_bin = shutil.which("qemu-system-x86_64") or "/usr/bin/qemu-system-x86_64"

    def check_availability(self):
        return os.path.exists(self.qemu_bin)

    def build_command(self, vm_name, iso_path, memory="4G", cpus="2"):
        """Constructs the QEMU launch command for a target virtual machine."""
        cmd = [
            self.qemu_bin,
            "-name", vm_name,
            "-m", memory,
            "-smp", cpus,
            "-boot", "d",
            "-cdrom", iso_path,
            "-enable-kvm",
            "-display", "gtk"
        ]
        return cmd

    def start_vm(self, vm_name, iso_path, memory="4G", cpus="2"):
        """Launches the virtual machine process."""
        if not self.check_availability():
            raise FileNotFoundError("QEMU binary not found on the system.")
        
        cmd = self.build_command(vm_name, iso_path, memory, cpus)
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return process
