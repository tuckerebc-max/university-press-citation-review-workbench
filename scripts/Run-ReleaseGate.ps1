param([string]$PythonPath)

$ErrorActionPreference = 'Stop'
$appRoot = (Resolve-Path -LiteralPath (Join-Path $PSScriptRoot '..')).Path
$python = if ($PythonPath) { (Resolve-Path -LiteralPath $PythonPath).Path } else { (Get-Command python -ErrorAction Stop).Source }
$node = (Get-Command node -ErrorAction Stop).Source

function Invoke-GateStep {
    param([string]$Name, [scriptblock]$Command)
    Write-Host "`n[$Name]" -ForegroundColor Cyan
    & $Command
    if ($LASTEXITCODE -ne 0) { throw "$Name failed with exit code $LASTEXITCODE." }
}

Push-Location $appRoot
try {
    Invoke-GateStep 'Application tests' { & $python -X utf8 -m unittest discover -s tests -v }
    Invoke-GateStep 'Python compilation' { & $python -m compileall -q upress_workbench }
    Invoke-GateStep 'JavaScript parse' { & $node --check upress_workbench/static/app.js }
    Invoke-GateStep 'RCI package validator' { & $python vendor/reference-citation-integrity/scripts/validate_package.py }
    Invoke-GateStep 'RCI evaluation suite' { & $python vendor/reference-citation-integrity/evals/scorer.py --validate-suite }
    Invoke-GateStep 'SEI package validator' { & $python vendor/scholarly-editorial-integrity/scripts/validate_package.py }
    Invoke-GateStep 'SEI evaluation suite' { & $python vendor/scholarly-editorial-integrity/evals/scorer.py --validate-suite --self-test }
    Invoke-GateStep 'Secret-pattern scan' { & $python scripts/check_no_secrets.py }
    Invoke-GateStep 'Ruff' { & $python -m ruff check . }
    Invoke-GateStep 'Bandit' { & $python -m bandit -q -r upress_workbench -s B606 }
    Invoke-GateStep 'Dependency audit' { & $python -m pip_audit -r requirements.txt }
    Invoke-GateStep 'Unstaged whitespace check' { & git diff --check }
    Invoke-GateStep 'Staged whitespace check' { & git diff --cached --check }
    Write-Host "`nRelease gate passed." -ForegroundColor Green
}
finally {
    Pop-Location
}
