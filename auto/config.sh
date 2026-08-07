#!/usr/bin/env sh
set -e

TARGET_ARCH="${1:-amd64}"

if [ "$TARGET_ARCH" = "x86_64" ] || [ "$TARGET_ARCH" = "x64" ]; then
    TARGET_ARCH="amd64"
elif [ "$TARGET_ARCH" = "aarch64" ]; then
    TARGET_ARCH="arm64"
fi

HOST_ARCH="$(dpkg --print-architecture 2>/dev/null || uname -m)"
if [ "$HOST_ARCH" = "x86_64" ]; then
    HOST_ARCH="amd64"
elif [ "$HOST_ARCH" = "aarch64" ]; then
    HOST_ARCH="arm64"
fi

IMAGE_TYPE="iso-hybrid"
BOOTLOADER="syslinux,grub-efi"

if [ "$TARGET_ARCH" = "arm64" ]; then
    IMAGE_TYPE="iso-hybrid"
    BOOTLOADER="grub-efi"
fi

QEMU_ARCH="${TARGET_ARCH}"
if [ "${TARGET_ARCH}" = "arm64" ]; then
    QEMU_ARCH="aarch64"
elif [ "${TARGET_ARCH}" = "amd64" ]; then
    QEMU_ARCH="x86_64"
fi

LIVE_BOOTAPPEND="boot=live components quiet splash live-config.username=eloquence live-config.user-default-groups=sudo,video,audio,netdev,nopasswdlogin"

echo "[INFO] Host Architecture:   ${HOST_ARCH}"
echo "[INFO] Target Architecture: ${TARGET_ARCH} (${IMAGE_TYPE})"
echo "[INFO] Bootloader Target:   ${BOOTLOADER}"
echo "[INFO] Installer Framework: Calamares GUI Installer (Debian-Installer: none)"

if [ "${TARGET_ARCH}" != "${HOST_ARCH}" ]; then
    QEMU_STATIC_BIN="/usr/bin/qemu-${QEMU_ARCH}-static"
    if [ ! -f "${QEMU_STATIC_BIN}" ]; then
        echo "[INFO] Installing cross-architecture emulator (qemu-user-static) for ${TARGET_ARCH}..."
        if command -v apt-get >/dev/null 2>&1 && [ "$(id -u)" -eq 0 ]; then
            apt-get update -y && apt-get install -y --no-install-recommends qemu-user-static binfmt-support 2>/dev/null || true
        fi
    fi

    if [ -f "${QEMU_STATIC_BIN}" ]; then
        echo "[INFO] Enabling cross-architecture QEMU static bootstrapping (qemu-${QEMU_ARCH}-static)..."
        lb config \
            --distribution trixie \
            --architectures "${TARGET_ARCH}" \
            --linux-flavours "${TARGET_ARCH}" \
            --binary-images "${IMAGE_TYPE}" \
            --bootloaders "${BOOTLOADER}" \
            --bootappend-live "${LIVE_BOOTAPPEND}" \
            --debian-installer none \
            --archive-areas "main contrib non-free non-free-firmware" \
            --bootstrap-qemu-arch "${TARGET_ARCH}" \
            --bootstrap-qemu-static "qemu-${QEMU_ARCH}-static" \
            --apt-recommends false \
            "${@}"
    else
        echo "[WARNING] qemu-${QEMU_ARCH}-static not found. Configuring without QEMU bootstrap hook..."
        lb config \
            --distribution trixie \
            --architectures "${TARGET_ARCH}" \
            --linux-flavours "${TARGET_ARCH}" \
            --binary-images "${IMAGE_TYPE}" \
            --bootloaders "${BOOTLOADER}" \
            --bootappend-live "${LIVE_BOOTAPPEND}" \
            --debian-installer none \
            --archive-areas "main contrib non-free non-free-firmware" \
            --apt-recommends false \
            "${@}"
    fi
else
    lb config \
        --distribution trixie \
        --architectures "${TARGET_ARCH}" \
        --linux-flavours "${TARGET_ARCH}" \
        --binary-images "${IMAGE_TYPE}" \
        --bootloaders "${BOOTLOADER}" \
        --bootappend-live "${LIVE_BOOTAPPEND}" \
        --debian-installer none \
        --archive-areas "main contrib non-free non-free-firmware" \
        --apt-recommends false \
        "${@}"
fi
