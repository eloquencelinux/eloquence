import os
import platform
import shutil
import subprocess

class QemuManager:
    def __init__(self):
        self.arch = platform.machine()
        self.qemu_bin = self._detect_qemu_binary()

    def _detect_qemu_binary(self):
        """Detects appropriate QEMU binary based on host architecture or available PATH executables."""
        candidates = []
        if self.arch in ["x86_64", "AMD64", "x64"]:
            candidates = ["qemu-system-x86_64", "/usr/bin/qemu-system-x86_64"]
        elif self.arch in ["arm64", "aarch64"]:
            candidates = ["qemu-system-aarch64", "/usr/bin/qemu-system-aarch64"]
        else:
            candidates = ["qemu-system-x86_64", "qemu-system-aarch64"]

        for cand in candidates:
            bin_path = shutil.which(cand) or (cand if os.path.exists(cand) else None)
            if bin_path:
                return bin_path

        # Fallback default
        return "/usr/bin/qemu-system-x86_64"

    def check_availability(self):
        """Checks if QEMU executable exists on the system."""
        return shutil.which(self.qemu_bin) is not None or os.path.exists(self.qemu_bin)

    def check_kvm_support(self):
        """Checks if /dev/kvm exists and is readable/writable."""
        return os.path.exists("/dev/kvm") and os.access("/dev/kvm", os.R_OK | os.W_OK)

    def build_command(self, vm_name, iso_path=None, disk_path=None, memory="4G", cpus="2"):
        """Constructs QEMU launch command for target VM."""
        cmd = [
            self.qemu_bin,
            "-name", vm_name,
            "-m", memory,
            "-smp", str(cpus),
            "-display", "gtk"
        ]

        if self.check_kvm_support():
            cmd.append("-enable-kvm")

        if iso_path and os.path.exists(iso_path):
            cmd.extend(["-boot", "d", "-cdrom", iso_path])

        if disk_path and os.path.exists(disk_path):
            cmd.extend(["-hda", disk_path])

        return cmd

    def start_vm(self, vm_name, iso_path=None, disk_path=None, memory="4G", cpus="2"):
        """Launches VM process in background."""
        if not self.check_availability():
            raise FileNotFoundError(f"QEMU binary '{self.qemu_bin}' not found on system.")

        cmd = self.build_command(vm_name, iso_path, disk_path, memory, cpus)
        process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            start_new_session=True
        )
        return process
