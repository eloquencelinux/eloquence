# Eloquence GNU/Linux & Eloquence Suite

[![CI Status](https://github.com/eloquencelinux/eloquence/actions/workflows/ci.yml/badge.svg)](https://github.com/eloquencelinux/eloquence/actions/workflows/ci.yml)
[![Debian](https://img.shields.io/badge/Debian-Trixie-red.svg)](https://www.debian.org)
[![Desktop](https://img.shields.io/badge/Desktop-Cinnamon-purple.svg)](https://projects.linuxmint.com/cinnamon/)
[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org)
[![PyQt6](https://img.shields.io/badge/GUI-PyQt6-green.svg)](https://www.riverbankcomputing.com)
[![Docker](https://img.shields.io/badge/Docker-Containerized-blue.svg)]()
[![Architecture](https://img.shields.io/badge/Arch-x86__64%20%7C%20ARM64-orange.svg)]()
[![License](https://img.shields.io/badge/License-GPLv3-blue.svg)](LICENSE)

**Eloquence GNU/Linux** is a modern, enterprise-ready, Debian-based Linux distribution engineered for high performance, security, and multi-architecture compatibility (`x86_64` amd64 and `aarch64` arm64), featuring the **Cinnamon Desktop Environment** and headless **CLI Mode**.

---

## ⚡ Key Features & Integrated Suite

Eloquence GNU/Linux comes pre-packaged with **Eloquence Suite** (`eloquence-suite`), a 9-in-1 set of custom desktop & CLI applications:

| Utility | Command | Description |
| :--- | :--- | :--- |
| **Elowelcome**| `elo welcome`| First-Run Welcome Wizard & Quick System Setup. |
| **Elovirt** | `elo virt` | Virtualization manager for QEMU/KVM with dynamic x64/ARM64 binary selection. |
| **Elofind** | `elo find` | High-speed file search utility supporting GUI & CLI filters (`-q`, `-p`). |
| **Elooffice** | `elo office` | Lightweight document editor with Rich Text, Markdown reader, and PDF/HTML export. |
| **Eloapps** | `elo apps` | App Center GUI for browsing, installing, and managing Debian APT packages. |
| **Eloguard** | `elo guard` | Security & Privacy Center (Firewall, Sysctl Hardening, USB Blocking). |
| **Elotweak** | `elo tweak` | System Tweaks & One-Click Light/Dark Mode Switcher. |
| **Elosnap** | `elo snap` | System Restore Points & Snapshot Backup Manager. |
| **Eloweb** | `elo web` | WebApp Creator (converts WhatsApp, Notion, ChatGPT into desktop apps). |

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
# Install dependencies in editable mode
make install

# Build x86_64 / amd64 Live ISO (Cinnamon Desktop)
make build-iso-x64

# Build ARM64 / aarch64 Live ISO (Cinnamon Desktop)
make build-iso-arm64

# Run test suite
make test
```

---

## 📜 License

Distributed under the GPL-3.0 License. Copyright (C) 30 October 2025 Eloquence GNU/Linux. See [LICENSE](LICENSE) for details.
