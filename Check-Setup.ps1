param()

$ErrorActionPreference = 'Stop'
$appRoot = $PSScriptRoot
$bundledPython = Join-Path $env:USERPROFILE '.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe'
$python = if (Test-Path -LiteralPath $bundledPython) { $bundledPython } else { (Get-Command python -ErrorAction Stop).Source }
$codex = Get-Command codex -ErrorAction Stop

Write-Host "Python:" -ForegroundColor Cyan
& $python --version
if ($LASTEXITCODE -ne 0) { throw 'Python could not be started.' }

Write-Host "Workbench dependency:" -ForegroundColor Cyan
& $python -c "import docx; print('python-docx available')"
if ($LASTEXITCODE -ne 0) { throw "Dependencies are missing. Run: python -m pip install -r requirements.txt" }

Write-Host "Codex CLI:" -ForegroundColor Cyan
& $codex.Source --version
if ($LASTEXITCODE -ne 0) { throw 'Codex CLI could not be started.' }

Write-Host "Codex authentication:" -ForegroundColor Cyan
& $codex.Source login status
if ($LASTEXITCODE -ne 0) { throw "Codex CLI is not signed in. Run: codex login" }

$env:PYTHONPATH = $appRoot
& $python -X utf8 -c "from upress_workbench.provider import inspect_codex_cli; from upress_workbench.review import load_skill_policy; status=inspect_codex_cli(); assert status['available'] and status['authenticated']; [load_skill_policy(name) for name in ('reference-citation-integrity','scholarly-editorial-integrity')]; print('Vendored skills verified')"
if ($LASTEXITCODE -ne 0) { throw 'Workbench integrity checks failed.' }

Write-Host "Setup is ready." -ForegroundColor Green
