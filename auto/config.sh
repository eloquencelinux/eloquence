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

LIVE_BOOTAPPEND="boot=live components quiet splash live-config.username=eloquence live-config.user-default-groups=sudo,video,audio,netdev,nopasswdlogin"

echo "[INFO] Host Architecture:   ${HOST_ARCH}"
echo "[INFO] Target Architecture: ${TARGET_ARCH} (${IMAGE_TYPE})"
echo "[INFO] Bootloader Target:   ${BOOTLOADER}"

# Common lb config arguments
LB_ARGS="--distribution trixie \
    --architectures ${TARGET_ARCH} \
    --linux-flavours ${TARGET_ARCH} \
    --binary-images ${IMAGE_TYPE} \
    --bootloaders ${BOOTLOADER} \
    --bootappend-live \"${LIVE_BOOTAPPEND}\" \
    --debian-installer none \
    --archive-areas main\ contrib\ non-free\ non-free-firmware \
    --apt-recommends false"

if [ "${TARGET_ARCH}" != "${HOST_ARCH}" ]; then
    echo "[INFO] Cross-architecture build detected (${HOST_ARCH} -> ${TARGET_ARCH})."
    echo "[INFO] Using kernel binfmt_misc for transparent emulation (no legacy qemu-static flags)."
fi

eval lb config ${LB_ARGS}
