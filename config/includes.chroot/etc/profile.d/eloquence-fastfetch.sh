#!/usr/bin/env sh

# Display Eloquence OS Fastfetch Banner on interactive interactive terminal login
if [ -n "${PS1:-}" ] && [ -x "$(command -v fastfetch)" ]; then
    fastfetch -c /etc/fastfetch/config.jsonc
fi
