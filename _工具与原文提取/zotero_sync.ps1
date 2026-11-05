param([Parameter(ValueFromRemainingArguments = $true)][string[]]$Args)
# Import new paper folders into the running Zotero (connector on 127.0.0.1:23119).
$py = "C:\Users\32531\.dsh\dsh-runtimes\dsh-primary-runtime\dependencies\python\python.exe"
$env:PYTHONIOENCODING = "utf-8"
& $py (Join-Path $PSScriptRoot "zotero_import.py") @Args
exit $LASTEXITCODE
