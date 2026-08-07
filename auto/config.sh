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

# Auto-link Debian Trixie qemu-binfmt binaries to /usr/bin/ if needed
if [ ! -f "/usr/bin/qemu-x86_64-static" ]; then
    for p in /usr/libexec/qemu-binfmt/x86_64-binfmt-P /usr/bin/qemu-x86_64; do
        if [ -f "$p" ]; then
            ln -sf "$p" /usr/bin/qemu-x86_64-static 2>/dev/null || true
            break
        fi
    done
fi

if [ ! -f "/usr/bin/qemu-aarch64-static" ]; then
    for p in /usr/libexec/qemu-binfmt/aarch64-binfmt-P /usr/bin/qemu-aarch64; do
        if [ -f "$p" ]; then
            ln -sf "$p" /usr/bin/qemu-aarch64-static 2>/dev/null || true
            break
        fi
    done
fi

if [ "${TARGET_ARCH}" != "${HOST_ARCH}" ]; then
    if [ -f "/usr/bin/qemu-${QEMU_ARCH}-static" ]; then
        echo "[INFO] Enabling cross-architecture QEMU static bootstrapping (/usr/bin/qemu-${QEMU_ARCH}-static)..."
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
        echo "[INFO] Cross-architecture build using host binfmt_misc kernel emulation..."
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
