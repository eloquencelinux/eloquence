#!/usr/bin/env bash

case "${1:-}" in
    "virt")
        python3 -m elovirt.main
        ;;
    "find")
        python3 -m elofind.main
        ;;
    "office")
        python3 -m elooffice.main
        ;;
    "apps")
        python3 -m eloapps.main
        ;;
    *)
        echo "Usage: elo {virt | find | office | apps}"
        exit 1
        ;;
esac
