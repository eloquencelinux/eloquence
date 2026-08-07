# Eloquence GNU/Linux

[![CI Status](https://github.com/eloquencelinux/eloquence/actions/workflows/ci.yml/badge.svg)](https://github.com/eloquencelinux/eloquence/actions/workflows/ci.yml)
[![Debian](https://img.shields.io/badge/Debian-Trixie-red.svg)](https://www.debian.org)
[![Desktop](https://img.shields.io/badge/Desktop-Cinnamon-purple.svg)](https://projects.linuxmint.com/cinnamon/)
[![Docker](https://img.shields.io/badge/Docker-Containerized-blue.svg)]()
[![Architecture](https://img.shields.io/badge/Arch-x86__64%20%7C%20ARM64-orange.svg)]()
[![License](https://img.shields.io/badge/License-GPLv3-blue.svg)](LICENSE)

**Eloquence GNU/Linux** is a modern, enterprise-ready Linux distribution engineered for high performance, security, and multi-architecture compatibility (`x86_64` amd64 and `aarch64` arm64), featuring the **Cinnamon Desktop Environment**, **Calamares GUI Installer**, and the standard stock Linux productivity suite.

---

## ⚡ Pre-Installed Stock Applications & Utilities

| Category | Pre-installed Software | Description |
| :--- | :--- | :--- |
| **Office & Productivity** | **LibreOffice** (Writer, Calc, Impress, Draw, Math) | Complete, professional document processing suite. |
| **Internet & Web** | **Firefox ESR**, **Thunderbird** | Fast, privacy-respecting browser and email client. |
| **Multimedia & Audio** | **VLC Media Player**, **Rhythmbox**, **Evince** | Universal media playback and PDF document viewing. |
| **Graphics & Design** | **GIMP**, **Inkscape**, **Simple Scan** | Professional photo editing, vector illustration, and scanning. |
| **System & Security** | **Timeshift**, **GParted**, **Synaptic**, **GUFW / UFW** | System snapshots, partition management, and firewall. |
| **Virtualization** | **Virt-Manager**, **QEMU / KVM**, **Libvirt** | Native hardware-accelerated virtual machine manager. |

---

## 🐳 Containerized Docker Build Guide

Build ISOs anywhere (Ubuntu, Debian, macOS, Fedora, Arch) without host dependency setup:

```bash
# Build x86_64 / amd64 ISO via Docker:
make docker-iso-x64

# Build ARM64 / aarch64 ISO via Docker:
make docker-iso-arm64

# Or using Docker Compose directly:
docker-compose up --build
```

---

## 🏗️ Native Build Guide (x86_64 & ARM64)

```bash
# Build x86_64 / amd64 Live ISO (Cinnamon Desktop)
make build-iso-x64

# Build ARM64 / aarch64 Live ISO (Cinnamon Desktop)
make build-iso-arm64

# Run test & configuration audit
make test
```

---

## 📜 License

Distributed under the GPL-3.0 License. Copyright (C) 30 October 2025 Eloquence GNU/Linux. See [LICENSE](LICENSE) for details.
