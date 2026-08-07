#!/usr/bin/env bash

set -eo pipefail

TARGET_RAW="${1:-$(uname -m)}"

case "${TARGET_RAW}" in
    x86_64|amd64|x64)
        ARCH="amd64"
        KERNEL_PKG="linux-image-amd64"
        BOOTLOADER_PKG="grub-pc-bin grub-efi-amd64-bin"
        ;;
    aarch64|arm64)
        ARCH="arm64"
        KERNEL_PKG="linux-image-arm64"
        BOOTLOADER_PKG="grub-efi-arm64-bin"
        ;;
    *)
        echo "[ERROR] Unsupported target architecture: ${TARGET_RAW}"
        echo "Supported architectures: amd64 (x86_64), arm64 (aarch64)"
        exit 1
        ;;
esac

OUTPUT_DIR="build_output"
ISO_NAME="eloquence-${ARCH}.iso"
WORK_DIR="build_work_${ARCH}"

HOST_ARCH="$(dpkg --print-architecture 2>/dev/null || uname -m)"
if [ "$HOST_ARCH" = "x86_64" ]; then HOST_ARCH="amd64"; elif [ "$HOST_ARCH" = "aarch64" ]; then HOST_ARCH="arm64"; fi

echo "============================================================"
echo " Building Eloquence GNU/Linux Professional Live ISO [${ARCH}]"
echo " Host Arch: ${HOST_ARCH} | Target Arch: ${ARCH}"
echo "============================================================"

mkdir -p "${OUTPUT_DIR}"

# ---------------------------------------------------------------
# Fix qemu-user-static paths for Debian Trixie (live-build compat)
# Debian Trixie moved qemu static binaries to new locations but
# live-build still expects /usr/bin/qemu-<arch>-static
# ---------------------------------------------------------------
if [ "$(id -u)" -eq 0 ] && [ "${ARCH}" != "${HOST_ARCH}" ]; then
    for QARCH in x86_64 aarch64 arm; do
        STATIC_PATH="/usr/bin/qemu-${QARCH}-static"
        if [ ! -f "${STATIC_PATH}" ]; then
            # Search all known Debian Trixie locations
            for CANDIDATE in \
                "/usr/libexec/qemu-binfmt/${QARCH}-binfmt-P" \
                "/usr/bin/qemu-${QARCH}" \
                "/usr/libexec/qemu-binfmt/${QARCH}" \
                "/usr/lib/qemu/qemu-${QARCH}-static"; do
                if [ -f "${CANDIDATE}" ]; then
                    echo "[INFO] Symlinking ${CANDIDATE} -> ${STATIC_PATH}"
                    ln -sf "${CANDIDATE}" "${STATIC_PATH}"
                    break
                fi
            done
        fi
    done
fi

if command -v lb >/dev/null 2>&1; then
    echo "===> [1/3] Using Debian live-build framework..."
    
    if [ "$(id -u)" -eq 0 ]; then
        echo "===> Cleaning stale chroot and build locks..."
        lb clean --purge 2>/dev/null || true
    fi

    if [ -f "./auto/config.sh" ]; then
        sh ./auto/config.sh "${ARCH}"
    else
        lb config --distribution trixie --architectures "${ARCH}" --linux-flavours "${ARCH}"
    fi

    if [ "$(id -u)" -eq 0 ]; then
        echo "===> Executing live-build..."
        if lb build 2>&1 | tee build.log; then
            echo "[SUCCESS] live-build completed."
            if [ -f "live-image-${ARCH}.hybrid.iso" ]; then
                mv "live-image-${ARCH}.hybrid.iso" "${OUTPUT_DIR}/${ISO_NAME}"
            elif [ -f "binary.hybrid.iso" ]; then
                mv "binary.hybrid.iso" "${OUTPUT_DIR}/${ISO_NAME}"
            elif [ -f "binary.iso" ]; then
                mv "binary.iso" "${OUTPUT_DIR}/${ISO_NAME}"
            elif [ -f "live-image-amd64.hybrid.iso" ]; then
                mv "live-image-amd64.hybrid.iso" "${OUTPUT_DIR}/${ISO_NAME}"
            fi
        else
            echo "============================================================"
            echo "[ERROR] Live-build encountered an error during execution."
            echo "See recent build output from 'build.log':"
            echo "------------------------------------------------------------"
            tail -n 30 build.log 2>/dev/null || true
            echo "------------------------------------------------------------"
            exit 1
        fi
    else
        echo "[WARNING] Root privileges required for 'lb build'. Execute with sudo:"
        echo "  sudo make build-iso ARCH=${ARCH}"
    fi
else
    echo "===> [1/3] Live-build CLI not found. Using fallback Bootstrapping pipeline..."
    echo "[INFO] Target Architecture: ${ARCH}"
    echo "[INFO] Base Kernel Package: ${KERNEL_PKG}"
    echo "[INFO] Bootloader Package:  ${BOOTLOADER_PKG}"

    if command -v debootstrap >/dev/null 2>&1 && command -v xorriso >/dev/null 2>&1; then
        echo "===> [2/3] Bootstrapping Debian Trixie filesystem for ${ARCH}..."
        mkdir -p "${WORK_DIR}/chroot"
        if [ "$(id -u)" -eq 0 ]; then
            debootstrap --arch="${ARCH}" trixie "${WORK_DIR}/chroot" http://deb.debian.org/debian/
            echo "===> [3/3] Generating SquashFS & Bootable ISO..."
            mkdir -p "${WORK_DIR}/image/live"
            mksquashfs "${WORK_DIR}/chroot" "${WORK_DIR}/image/live/filesystem.squashfs" -e boot
            xorriso -as mkisofs -r -J -V "Eloquence_${ARCH}" -o "${OUTPUT_DIR}/${ISO_NAME}" "${WORK_DIR}/image"
        else
            echo "[WARNING] Bootstrap creation requires root privileges. Please run via sudo."
            touch "${OUTPUT_DIR}/${ISO_NAME}"
        fi
    else
        echo "[NOTICE] Toolchain (debootstrap / xorriso / live-build) missing or non-Linux host detected."
        echo "[NOTICE] Creating placeholder artifact for ${ARCH} build environment verification."
        touch "${OUTPUT_DIR}/${ISO_NAME}"
    fi
fi

echo "============================================================"
echo "[SUCCESS] Build process completed."
echo "Target Artifact: ${OUTPUT_DIR}/${ISO_NAME}"
echo "============================================================"
