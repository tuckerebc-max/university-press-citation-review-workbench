param([string]$Model = 'default')

$ErrorActionPreference = 'Stop'
$appRoot = (Resolve-Path -LiteralPath (Join-Path $PSScriptRoot '..')).Path
$bundledPython = Join-Path $env:USERPROFILE '.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe'
$python = if (Test-Path -LiteralPath $bundledPython) { $bundledPython } else { (Get-Command python -ErrorAction Stop).Source }
$env:PYTHONPATH = $appRoot

& $python -X utf8 (Join-Path $PSScriptRoot 'codex_smoke.py') --model $Model
if ($LASTEXITCODE -ne 0) { throw 'Codex provider smoke test failed.' }
