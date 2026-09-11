param(
    [ValidateRange(1024, 65535)]
    [int]$Port = 8765,
    [switch]$NoBrowser
)

$ErrorActionPreference = 'Stop'
$appRoot = $PSScriptRoot
$bundledPython = Join-Path $env:USERPROFILE '.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe'
$python = if (Test-Path -LiteralPath $bundledPython) { $bundledPython } else { (Get-Command python -ErrorAction Stop).Source }
$codex = Get-Command codex -ErrorAction Stop
& $codex.Source login status *> $null
if ($LASTEXITCODE -ne 0) { throw "Codex CLI is not signed in. Run 'codex login' and retry." }
$env:PYTHONPATH = $appRoot
$arguments = @('-X', 'utf8', '-m', 'upress_workbench.server', '--port', [string]$Port)
if ($NoBrowser) { $arguments += '--no-browser' }
& $python @arguments
