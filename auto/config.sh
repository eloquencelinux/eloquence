#!/usr/bin/env sh
set -e

lb config \
    --distribution trixie \
    --architectures arm64 \
    --linux-flavours arm64 \
    --binary-images iso-hybrid \
    --archive-areas "main contrib non-free non-free-firmware" \
    --apt-recommends false \
    "${@}"
