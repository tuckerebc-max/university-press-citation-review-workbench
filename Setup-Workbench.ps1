param()

$ErrorActionPreference = 'Stop'
$appRoot = $PSScriptRoot
$bundledPython = Join-Path $env:USERPROFILE '.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe'
$python = if (Test-Path -LiteralPath $bundledPython) { $bundledPython } else { (Get-Command python -ErrorAction Stop).Source }

& $python -m pip install --disable-pip-version-check -r (Join-Path $appRoot 'requirements.txt')
if ($LASTEXITCODE -ne 0) { throw 'Workbench dependency installation failed.' }

& (Join-Path $appRoot 'Check-Setup.ps1')
