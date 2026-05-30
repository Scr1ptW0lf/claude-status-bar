# Claude Code status line installer — Windows
# Usage: .\install.ps1

$ErrorActionPreference = 'Stop'

$scriptDir  = Split-Path -Parent $MyInvocation.MyCommand.Definition
$claudeDir  = "$env:USERPROFILE\.claude"
$dest       = "$claudeDir\statusline-command.py"
$settingsPath = "$claudeDir\settings.json"

if (-not (Test-Path $claudeDir)) {
    New-Item -ItemType Directory -Force $claudeDir | Out-Null
}

Copy-Item "$scriptDir\statusline-command.py" $dest -Force
Write-Host "Copied statusline-command.py -> $dest"

# Detect python launcher
$py = $null
foreach ($candidate in @('py', 'python3', 'python')) {
    if (Get-Command $candidate -ErrorAction SilentlyContinue) {
        $py = $candidate
        break
    }
}
if (-not $py) {
    Write-Error "Python not found. Install Python 3 and re-run."
    exit 1
}

$command = "$py `"$dest`""

# Merge statusLine into existing settings.json
if (Test-Path $settingsPath) {
    $settings = Get-Content $settingsPath -Raw | ConvertFrom-Json
} else {
    $settings = [pscustomobject]@{}
}

# Add or replace the statusLine property
$statusLine = [pscustomobject]@{ type = 'command'; command = $command }
if ($settings.PSObject.Properties['statusLine']) {
    $settings.statusLine = $statusLine
} else {
    $settings | Add-Member -NotePropertyName 'statusLine' -NotePropertyValue $statusLine
}

$settings | ConvertTo-Json -Depth 10 | Set-Content $settingsPath -Encoding utf8
Write-Host "Updated $settingsPath"
Write-Host "Done. Restart Claude Code to see the status line."
