#!/usr/bin/env bash

set -euo pipefail

function show_help() {
    echo "Eloquence OS Central CLI Utility"
    echo "Usage: elo <command> [options]"
    echo ""
    echo "Available commands:"
    echo "  virt    - Launch Elovirt Virtualization Manager"
    echo "  find    - Launch Elofind File Search Utility (GUI or CLI with -q)"
    echo "  office  - Launch Elooffice Document Editor"
    echo "  apps    - Launch Eloapps App Center"
    echo "  help    - Display this help message"
}

CMD="${1:-}"
shift || true

case "${CMD}" in
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
    "help"|"-h"|"--help")
        show_help
        ;;
    *)
        echo "[ERROR] Unknown command: '${CMD}'"
        show_help
        exit 1
        ;;
esac
