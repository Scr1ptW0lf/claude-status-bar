import sys
import json
import subprocess
import os
from datetime import datetime, timezone

data = json.load(sys.stdin)

# --- Current folder ---
cwd = (data.get('workspace') or {}).get('current_dir') or data.get('cwd', '')
dir_name = os.path.basename(cwd) if cwd else ''

# --- Git branch (optional) ---
branch = ''
if cwd:
    try:
        r = subprocess.run(
            ['git', '-C', cwd, '--no-optional-locks', 'symbolic-ref', '--short', 'HEAD'],
            capture_output=True, text=True)
        if r.returncode == 0:
            branch = r.stdout.strip()
        else:
            r = subprocess.run(
                ['git', '-C', cwd, '--no-optional-locks', 'rev-parse', '--short', 'HEAD'],
                capture_output=True, text=True)
            if r.returncode == 0:
                branch = r.stdout.strip()
    except Exception:
        pass

# --- Model ---
model = (data.get('model') or {}).get('display_name', '')

# --- Context window usage ---
ctx = data.get('context_window') or {}
used_pct = ctx.get('used_percentage')
remaining_pct = ctx.get('remaining_percentage')
total_input = ctx.get('total_input_tokens')
ctx_size = ctx.get('context_window_size')

# --- Rate limits ---
rl = data.get('rate_limits') or {}
five_hour_obj = rl.get('five_hour') or {}
five_pct = five_hour_obj.get('used_percentage')
week_pct = (rl.get('seven_day') or {}).get('used_percentage')

# Reset time for 5-hour window
five_reset_str = ''
reset_at = five_hour_obj.get('resets_at') or five_hour_obj.get('reset_at')
if reset_at:
    try:
        secs_left = int(reset_at) - datetime.now(timezone.utc).timestamp()
        if secs_left > 0:
            h, m = divmod(int(secs_left) // 60, 60)
            five_reset_str = f'{h}h{m:02d}m' if h else f'{m}m'
    except Exception:
        pass

# --- Colors (ANSI) ---
Y, C, M, G, R, B, X = '\033[33m', '\033[36m', '\033[35m', '\033[32m', '\033[31m', '\033[34m', '\033[0m'

parts = []

# Folder + branch
if dir_name:
    folder_str = f'{Y}{dir_name}{X}'
    if branch:
        folder_str += f' {C}({branch}){X}'
    parts.append(folder_str)

# Model
if model:
    parts.append(f'{M}{model}{X}')

# Context usage
if used_pct is not None and remaining_pct is not None:
    ctx_color = R if round(remaining_pct) <= 20 else G
    ctx_str = f'ctx:{round(used_pct)}%'
    if total_input is not None and ctx_size is not None:
        def fmt_k(n):
            if n >= 1000:
                return f'{n/1000:.1f}k'
            return str(n)
        ctx_str += f' ({fmt_k(total_input)}/{fmt_k(ctx_size)})'
    parts.append(f'{ctx_color}{ctx_str}{X}')

# Rate limits (claude.ai subscription)
limits = []
if five_pct is not None:
    entry = f'5h:{round(five_pct)}%'
    if five_reset_str:
        entry += f' rst:{five_reset_str}'
    limits.append(entry)
if week_pct is not None:
    limits.append(f'7d:{round(week_pct)}%')
if limits:
    limits_color = R if any(
        p is not None and round(p) >= 80
        for p in [five_pct, week_pct]
    ) else Y
    parts.append(f'{limits_color}[{" ".join(limits)}]{X}')

print(' | '.join(parts))
