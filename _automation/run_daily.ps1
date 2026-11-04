# Daily unattended paper run for DeepSeek Harness.
# Registered in Windows Task Scheduler as "DSH-Daily-Papers".
# ASCII-only on purpose (the workspace path contains non-ASCII characters).

param(
  [string]$TaskFile = ''
)

$ErrorActionPreference = 'Stop'

$autoDir   = $PSScriptRoot
$root      = Split-Path $autoDir -Parent
$logDir    = Join-Path $autoDir 'logs'
$taskFile  = if ($TaskFile) { $TaskFile } else { Join-Path $autoDir 'daily_task.md' }
$dsh       = 'D:\dsHarness\resources\runtime\cli\bin\dsh.cmd'

New-Item -ItemType Directory -Force -Path $logDir | Out-Null

$stamp = Get-Date -Format 'yyyy-MM-dd'
$log   = Join-Path $logDir ($stamp + '.log')

if (-not (Test-Path $taskFile)) {
  "missing task file: $taskFile" | Out-File -FilePath $log -Append -Encoding utf8
  exit 2
}

# Full file access + no approval prompts, otherwise headless tools cannot write.
$env:DSH_PERMISSION_MODE = 'danger-full-access'
$env:PYTHONIOENCODING    = 'utf-8'

Set-Location $root

$rel = $taskFile
if ($rel.StartsWith($root, [StringComparison]::OrdinalIgnoreCase)) {
  $rel = $rel.Substring($root.Length).TrimStart('\') -replace '\\', '/'
}

$prompt = 'Read the file ' + $rel + ' in the current working directory and carry out every step it describes for today. Work only inside the current directory. Do not ask questions.'

"===== run started $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') =====" | Out-File -FilePath $log -Append -Encoding utf8

# Native tools write progress to stderr; 'Stop' would abort the whole run on the
# first such line, so relax it for the duration of the child process.
$ErrorActionPreference = 'Continue'
& $dsh headless $prompt *>&1 | Out-File -FilePath $log -Append -Encoding utf8
$code = $LASTEXITCODE
$ErrorActionPreference = 'Stop'

"===== run finished $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') exit=$code =====" | Out-File -FilePath $log -Append -Encoding utf8
exit $code
