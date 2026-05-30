#!/usr/bin/env python3
"""Claude Code status line installer — Windows / macOS / Linux
Usage: python install.py   (or: python3 install.py)
"""
import json
import os
import shutil
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
CLAUDE_DIR = os.path.join(os.path.expanduser("~"), ".claude")
DEST = os.path.join(CLAUDE_DIR, "statusline-command.py")
SETTINGS_PATH = os.path.join(CLAUDE_DIR, "settings.json")

os.makedirs(CLAUDE_DIR, exist_ok=True)
shutil.copy2(os.path.join(SCRIPT_DIR, "statusline-command.py"), DEST)
print(f"Copied statusline-command.py -> {DEST}")

# Use the same interpreter that's running this script
py = sys.executable
command = f'{py} "{DEST}"'

if os.path.exists(SETTINGS_PATH):
    with open(SETTINGS_PATH) as f:
        settings = json.load(f)
else:
    settings = {}

settings["statusLine"] = {"type": "command", "command": command}

with open(SETTINGS_PATH, "w") as f:
    json.dump(settings, f, indent=2)
    f.write("\n")

print(f"Updated {SETTINGS_PATH}")
print("Done. Restart Claude Code to see the status line.")
