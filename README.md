<div align="center">

# ⚡ Eloquence GNU/Linux 2026.1

### *Modern, Secure & Enterprise-Ready Operating System*

[![Debian Base](https://img.shields.io/badge/Debian-Trixie%20Core-E63946?style=for-the-badge&logo=debian&logoColor=white)](https://www.debian.org)
[![Desktop](https://img.shields.io/badge/Desktop-Cinnamon-457B9D?style=for-the-badge&logo=linuxmint&logoColor=white)](https://projects.linuxmint.com/cinnamon/)
[![Architecture](https://img.shields.io/badge/Architecture-x86__64%20%7C%20ARM64-F4A261?style=for-the-badge&logo=arm&logoColor=white)]()
[![Installer](https://img.shields.io/badge/Installer-Calamares%20GUI-2A9D8F?style=for-the-badge)]()
[![Containerized](https://img.shields.io/badge/Docker-Ready%20Builds-264653?style=for-the-badge&logo=docker&logoColor=white)](docker-compose.yml)
[![License](https://img.shields.io/badge/License-GPLv3-1D3557?style=for-the-badge)](LICENSE)

<br/>

**Eloquence GNU/Linux** is an independent, highly refined, professional Linux operating system engineered for software developers, system administrators, creative professionals, and power users. Combining the rock-solid stability of Debian with a modern **Cinnamon Desktop Environment**, **Calamares GUI Installer**, **Plymouth animated boot experience**, and an enterprise-grade productivity software suite.

</div>

---

## 🌟 Key Highlights & Architectural Features

### 🖥️ 1. Modern Desktop Experience
- **Cinnamon Desktop Environment**: Fast, elegant, and resource-efficient desktop tailored for productivity.
- **Custom Visual Identity**: Pre-configured with the official **Eloquence Dark Space** wallpaper, Phoenix branding, and dark GTK3 styling.
- **LightDM with Seamless Live Autologin**: Instant passwordless live boot into a fully functioning graphic desktop environment.

### 💿 2. Calamares Graphical System Installer
- **Branded Installation Experience**: Calamares installer featuring the official **Eloquence Phoenix logo** and tailored styling (`#17252a` / `#3aafa9`).
- **Clean Post-Install Cleanup**: Live installer shortcuts and temporary live user accounts are automatically pruned from the installed target system.
- **Flexible Disk Partitioning**: Full support for Btrfs, Ext4, XFS, and automated disk encryption (LUKS).

### 🚀 3. Plymouth Animated Boot Splash & Custom GRUB
- **Animated Startup Screen**: High-resolution, glowing Eloquence Phoenix logo on boot instead of text console logs.
- **Noise-Free Solid 24-bit Bootloader Splash**: Custom 1920x1080 GRUB/Syslinux bootloader menu offering:
  1. `⚡ 1. Eloquence GNU/Linux 2026.1 (Live Desktop Session)`
  2. `💿 2. Install Eloquence GNU/Linux (Direct Calamares GUI Installer)`
  3. `🛡️ 3. Eloquence GNU/Linux (Fail-safe / Safe Graphics Mode)`
  4. `⚡ 4. Eloquence GNU/Linux (Copy to RAM Mode)`

### 📦 4. Complete Stock Software Suite

| Category | Application | Description |
| :--- | :--- | :--- |
| **Productivity** | **LibreOffice Complete** | Full office suite: Writer (Docs), Calc (Sheets), Impress (Slides), Draw, Math. |
| **Internet & Web** | **Firefox ESR & Thunderbird** | Fast, privacy-oriented web browsing and professional email client. |
| **Multimedia** | **VLC Media Player & Rhythmbox** | Universal high-performance video and audio playback engines. |
| **Graphics & Design** | **GIMP & Inkscape** | Advanced raster photo editing and scalable vector graphics creation. |
| **System & Security** | **Timeshift, GParted, GUFW** | System snapshot restore points, partition manager, and graphical firewall. |
| **Virtualization** | **Virt-Manager & QEMU/KVM** | Hardware-accelerated native kernel virtual machine management. |

---

## 💻 System Requirements

| Specification | Minimum | Recommended |
| :--- | :--- | :--- |
| **Processor** | 64-bit Dual-Core (x86_64 or ARM64) | 64-bit Quad-Core CPU (Intel, AMD, Apple Silicon, ARM) |
| **Memory (RAM)**| 2 GB RAM | 4 GB+ RAM |
| **Storage** | 15 GB Free Disk Space | 30 GB+ SSD Storage |
| **Display** | 1024 x 768 Resolution | 1920 x 1080 HD or 4K Display |

---

## 🐳 Containerized Build Guide (Docker)

Build clean Live ISOs on any operating system (macOS, Ubuntu, Debian, Fedora, Arch) without installing build toolchains on the host:

```bash
# Clone repository
git clone https://github.com/eloquencelinux/eloquence.git
cd eloquence

# Build x86_64 Live ISO inside Docker container:
make docker-iso-x64

# Build ARM64 Live ISO inside Docker container:
make docker-iso-arm64

# Or using Docker Compose directly:
docker-compose up --build
```
> Generated ISO images are saved automatically to `build_output/`.

---

## 🏗️ Native Host Build Guide

If you are running Debian / Ubuntu as root:

```bash
# Build x86_64 / amd64 Live ISO
make build-iso-x64

# Build ARM64 / aarch64 Live ISO
make build-iso-arm64

# Run configuration and shell syntax audit
make test
```

---

## 📁 Repository Structure

```text
eloquence/
├── Dockerfile                   # Docker build container recipe
├── docker-compose.yml           # Docker Compose build service
├── Makefile                     # Build targets (native & containerized)
├── LICENSE                      # GNU General Public License v3
├── README.md                    # System documentation and build manual
├── auto/
│   ├── build.sh                 # Live-build invocation script
│   └── config.sh                # Live-build architecture & parameter configuration
├── config/
│   ├── bootloaders/             # Custom GRUB & Syslinux splash and menu configurations
│   ├── calamares/               # Calamares installer settings, branding & cleanup modules
│   ├── package-lists/           # Desktop and system package manifests (eloquence.list.chroot)
│   ├── hooks/normal/            # Chroot branding, user setup, lockscreen & Plymouth hooks
│   └── includes.chroot/         # Pre-configured system files, wallpapers, themes & desktop entries
└── scripts/
    ├── build.sh                 # Master ISO generator script
    └── verify-iso.sh            # Post-build ISO verification and check tool
```

---

## 📜 License & Copyright

**Eloquence GNU/Linux** is free software distributed under the terms of the **GNU General Public License v3.0 (GPLv3)**.

Copyright (C) 30 October 2025 Eloquence GNU/Linux. See [LICENSE](LICENSE) for the full license text.
