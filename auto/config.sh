#!/usr/bin/env sh
set -e

TARGET_ARCH="${1:-amd64}"

if [ "$TARGET_ARCH" = "x86_64" ] || [ "$TARGET_ARCH" = "x64" ]; then
    TARGET_ARCH="amd64"
elif [ "$TARGET_ARCH" = "aarch64" ]; then
    TARGET_ARCH="arm64"
fi

IMAGE_TYPE="iso-hybrid"
if [ "$TARGET_ARCH" = "arm64" ]; then
    IMAGE_TYPE="hdd"
fi

echo "[INFO] Configuring Debian Live-Build for architecture: ${TARGET_ARCH} (${IMAGE_TYPE})"

lb config \
    --distribution trixie \
    --architectures "${TARGET_ARCH}" \
    --linux-flavours "${TARGET_ARCH}" \
    --binary-images "${IMAGE_TYPE}" \
    --archive-areas "main contrib non-free non-free-firmware" \
    --apt-recommends false \
    "${@}"
