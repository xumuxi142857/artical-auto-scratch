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

# github.com:443 is flaky on this network (api.github.com stays up); retry with backoff.
$pushed = $false
for ($i = 1; $i -le 8; $i++) {
  & $git -C $root push origin main
  if ($LASTEXITCODE -eq 0) { $pushed = $true; break }
  Write-Output ("push failed (attempt " + $i + "), retrying in 45s")
  Start-Sleep -Seconds 45
}

if (-not $pushed) {
  Write-Output 'push still failing; commit is local only -- run sync again later'
  exit 1
}
exit 0
