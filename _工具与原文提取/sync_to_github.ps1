# Sync this workspace to GitHub.
# Usage: powershell -NoProfile -ExecutionPolicy Bypass -File sync_to_github.ps1 [-Message "commit message"]
# ASCII-only on purpose (the workspace path contains non-ASCII characters).

param(
  [string]$Message = ''
)

$ErrorActionPreference = 'Stop'

$git  = 'C:\Program Files\Git\cmd\git.exe'
$root = Split-Path $PSScriptRoot -Parent

if (-not $Message) {
  $Message = 'update: sync paper archive ' + (Get-Date -Format 'yyyy-MM-dd HH:mm')
}

& $git -C $root add -A
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

# Anything staged?
$pending = & $git -C $root diff --cached --name-only
if (-not $pending) {
  Write-Output 'nothing to commit'
  exit 0
}

& $git -C $root commit -m $Message | Out-Null
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

& $git -C $root push origin main
exit $LASTEXITCODE
