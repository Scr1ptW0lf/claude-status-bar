#!/usr/bin/env python3
"""Claude Code status line installer — Windows / macOS / Linux

Local:  python install.py
Remote: curl -fsSL https://raw.githubusercontent.com/Scr1ptW0lf/claude-status-bar/master/install.py | python3
        (Invoke-WebRequest https://raw.githubusercontent.com/Scr1ptW0lf/claude-status-bar/master/install.py).Content | python
"""
import json
import os
import shutil
import sys
import urllib.request

RAW_BASE = "https://raw.githubusercontent.com/Scr1ptW0lf/claude-status-bar/master"
CLAUDE_DIR = os.path.join(os.path.expanduser("~"), ".claude")
DEST = os.path.join(CLAUDE_DIR, "statusline-command.py")
SETTINGS_PATH = os.path.join(CLAUDE_DIR, "settings.json")

os.makedirs(CLAUDE_DIR, exist_ok=True)

# When piped via stdin, __file__ doesn't exist — download the script instead
local = os.path.join(os.path.dirname(os.path.abspath(__file__)), "statusline-command.py") \
    if "__file__" in dir() else None

if local and os.path.exists(local):
    shutil.copy2(local, DEST)
else:
    print("Downloading statusline-command.py from GitHub...")
    urllib.request.urlretrieve(f"{RAW_BASE}/statusline-command.py", DEST)

print(f"Installed -> {DEST}")

py = sys.executable
command = f'"{py}" "{DEST}"'

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
