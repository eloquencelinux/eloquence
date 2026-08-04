#!/usr/bin/env bash

set -euo pipefail

TARGET_DIR="${1:-build_output}"

if [ ! -d "${TARGET_DIR}" ]; then
    echo "[ERROR] Directory '${TARGET_DIR}' does not exist."
    exit 1
fi

if [ -f "${TARGET_DIR}/SHA256SUMS" ]; then
    echo "===> Verifying ISO checksums in '${TARGET_DIR}'..."
    (cd "${TARGET_DIR}" && sha256sum -c SHA256SUMS)
    echo "[SUCCESS] All ISO images match their SHA256 checksums."
else
    echo "===> Generating new SHA256 checksums in '${TARGET_DIR}'..."
    (cd "${TARGET_DIR}" && sha256sum *.iso > SHA256SUMS 2>/dev/null || true)
    cat "${TARGET_DIR}/SHA256SUMS"
fi
