#!/usr/bin/env bash

set -euo pipefail

function show_help() {
    echo "========================================================"
    echo " ⚡ Eloquence GNU/Linux Central Suite CLI Utility"
    echo "========================================================"
    echo "Usage: elo <command> [options]"
    echo ""
    echo "Available commands:"
    echo "  welcome - Launch Eloquence Welcome First-Run Experience"
    echo "  virt    - Launch Elovirt Virtualization Manager (QEMU/KVM)"
    echo "  find    - Launch Elofind File Search Utility (GUI or CLI -q)"
    echo "  office  - Launch Elooffice Document Editor & Markdown Reader"
    echo "  apps    - Launch Eloapps App Center (APT Package Manager)"
    echo "  guard   - Launch Eloguard Security & Privacy Manager"
    echo "  tweak   - Launch Elotweak System & Theme Switcher (Dark/Light)"
    echo "  snap    - Launch Elosnap Backup & System Snapshot Manager"
    echo "  web     - Launch Eloweb WebApp Creator & Browser"
    echo "  help    - Display this help message"
    echo "========================================================"
}

CMD="${1:-}"
shift || true

case "${CMD}" in
    "welcome")
        python3 -m elowelcome.main "$@"
        ;;
    "virt")
        python3 -m elovirt.main "$@"
        ;;
    "find")
        python3 -m elofind.main "$@"
        ;;
    "office")
        python3 -m elooffice.main "$@"
        ;;
    "apps")
        python3 -m eloapps.main "$@"
        ;;
    "guard")
        python3 -m eloguard.main "$@"
        ;;
    "tweak")
        python3 -m elotweak.main "$@"
        ;;
    "snap")
        python3 -m elosnap.main "$@"
        ;;
    "web")
        python3 -m eloweb.main "$@"
        ;;
    "help"|"-h"|"--help")
        show_help
        ;;
    *)
        echo "[ERROR] Unknown command: '${CMD}'"
        show_help
        exit 1
        ;;
esac
