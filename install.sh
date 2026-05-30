#!/usr/bin/env bash
# Claude Code status line installer — macOS / Linux
# Usage: bash install.sh

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CLAUDE_DIR="$HOME/.claude"
DEST="$CLAUDE_DIR/statusline-command.py"
SETTINGS="$CLAUDE_DIR/settings.json"

mkdir -p "$CLAUDE_DIR"
cp "$SCRIPT_DIR/statusline-command.py" "$DEST"
echo "Copied statusline-command.py -> $DEST"

# Detect python3
if command -v python3 &>/dev/null; then
    PY=python3
elif command -v python &>/dev/null && python --version 2>&1 | grep -q 'Python 3'; then
    PY=python
else
    echo "Error: Python 3 not found. Install it and re-run." >&2
    exit 1
fi

COMMAND="$PY \"$DEST\""

# Merge statusLine into settings.json using python
$PY - <<PYEOF
import json, os

settings_path = os.path.expanduser("$SETTINGS")
if os.path.exists(settings_path):
    with open(settings_path) as f:
        settings = json.load(f)
else:
    settings = {}

settings["statusLine"] = {"type": "command", "command": "$COMMAND"}

with open(settings_path, "w") as f:
    json.dump(settings, f, indent=2)
    f.write("\n")

print(f"Updated {settings_path}")
PYEOF

echo "Done. Restart Claude Code to see the status line."
