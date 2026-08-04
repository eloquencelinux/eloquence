# Eloquence OS & Eloquence Suite

[![CI Status](https://github.com/eloquencelinux/eloquence/actions/workflows/ci.yml/badge.svg)](https://github.com/eloquencelinux/eloquence/actions/workflows/ci.yml)
[![Debian](https://img.shields.io/badge/Debian-Trixie-red.svg)](https://www.debian.org)
[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org)
[![PyQt6](https://img.shields.io/badge/GUI-PyQt6-green.svg)](https://www.riverbankcomputing.com)
[![Architecture](https://img.shields.io/badge/Arch-x86__64%20%7C%20ARM64-orange.svg)]()
[![License](https://img.shields.io/badge/License-GPLv3-blue.svg)](LICENSE)

**Eloquence OS** is a modern, enterprise-ready, Debian-based Linux distribution designed for high performance, security, and multi-architecture compatibility (`x86_64` amd64 and `aarch64` arm64).

---

## ⚡ Key Features

- **Debian Trixie Core**: Built on Debian's modern testing branch for updated packages, Wayland support, and system stability.
- **Dual-Architecture Live ISOs**: Native build pipelines for both **x86_64 (amd64)** and **ARM64 (aarch64)**.
- **Integrated Desktop Suite**: Pre-packaged with `eloquence-suite`, a set of custom desktop applications with unified Dark styling:
  - 🖥️ **Elovirt**: Virtual Machine Manager for QEMU/KVM with live status tracking.
  - 🔍 **Elofind**: Fast file finder GUI & CLI with live pattern matching.
  - 📝 **Elooffice**: Lightweight document editor and Markdown reader with PDF/HTML export.
  - 🚀 **Eloapps**: Eloquence App Center for graphical package management.
- **Calamares Installer**: Seamless installation to disk with custom Eloquence branding.

---

## 💻 Central CLI Interface (`elo`)

Eloquence OS provides a central CLI tool (`elo`) to launch applications or execute system utilities:

```bash
# Launch Virtual Machine Manager
elo virt

# Launch File Finder GUI
elo find

# Run File Finder in CLI mode
elo find -q "config" -p "/etc"

# Launch Document Editor
elo office

# Launch App Center
elo apps

# Display Help
elo help
```

---

## 🏗️ Development & Build Guide

### 1. Installation in Editable Mode

```bash
git clone https://github.com/eloquencelinux/eloquence.git
cd eloquence
make install
```

### 2. Live ISO Generation (Multi-Arch)

Generate bootable Live ISO images using Debian `live-build` or `debootstrap`:

```bash
# Build x86_64 (amd64) Live ISO
make build-iso-x64

# Build ARM64 (aarch64) Live ISO
make build-iso-arm64

# Custom Architecture Build
make build-iso ARCH=amd64
```

ISO artifacts are saved to `build_output/eloquence-<arch>.iso`.

---

## 🧪 Testing & Quality Assurance

```bash
# Run Python syntax validation across all suite modules
make test

# Run shell script linters
make lint

# Clean temporary build caches
make clean
```

---

## 📁 Repository Structure

```
.
├── .github/                  # CI/CD Workflows & Issue Templates
│   ├── ISSUE_TEMPLATE/
│   └── workflows/
├── auto/                     # Debian live-build hooks & configurations
├── bin/
│   └── elo.sh                # Central CLI launcher
├── config/                   # Calamares installer, desktop entries & package lists
│   ├── calamares/
│   ├── desktop-entries/
│   ├── hooks/
│   └── includes.chroot/
├── eloapps/                  # App Center package
├── elofind/                   # File Search package
├── elooffice/                # Document Editor package
├── elovirt/                  # Virtualization Manager package
├── CONTRIBUTING.md           # Developer contribution guide
├── LICENSE                   # GPL-3.0 License
├── Makefile                  # Build tasks & test automation
├── pyproject.toml            # Setuptools package configuration
├── README.md                 # Project documentation
└── scripts/
    └── build.sh              # Multi-arch ISO builder pipeline
```

---

## 📜 License

Distributed under the GPL-3.0 License. See [LICENSE](LICENSE) for details.
