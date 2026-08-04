#!/usr/bin/env sh
set -e

echo "===> Triggering Debian live-build engine..."
lb build "${@}"
