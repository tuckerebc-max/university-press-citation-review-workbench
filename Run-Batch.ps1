param(
    [Parameter(Mandatory = $true)][string]$InputFolder,
    [Parameter(Mandatory = $true)][string]$OutputFolder,
    [Parameter(Mandatory = $true)][string]$CaseOwner,
    [string]$Project = 'University Press chapter review',
    [ValidateSet('public', 'unpublished_approved')][string]$Classification = 'unpublished_approved',
    [ValidateSet('baseline', 'incremental', 'full', 'release', 'proof')][string]$Mode = 'baseline',
    [string]$Model = 'default',
    [ValidateRange(1, 3)][int]$Concurrency = 1,
    [switch]$Crossref,
    [Parameter(Mandatory = $true)][switch]$ApproveCodex
)

$ErrorActionPreference = 'Stop'
$appRoot = $PSScriptRoot
$bundledPython = Join-Path $env:USERPROFILE '.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe'
$python = if (Test-Path -LiteralPath $bundledPython) { $bundledPython } else { (Get-Command python -ErrorAction Stop).Source }
$codex = Get-Command codex -ErrorAction Stop
& $codex.Source login status *> $null
if ($LASTEXITCODE -ne 0) { throw "Codex CLI is not signed in. Run 'codex login' and retry." }
$env:PYTHONPATH = $appRoot
$arguments = @(
    '-X', 'utf8', '-m', 'upress_workbench.cli',
    '--input', $InputFolder,
    '--output', $OutputFolder,
    '--owner', $CaseOwner,
    '--project', $Project,
    '--classification', $Classification,
    '--mode', $Mode,
    '--concurrency', [string]$Concurrency,
    '--approve-codex'
)
if ($Model.Trim()) { $arguments += @('--model', $Model.Trim()) }
if ($Crossref) { $arguments += '--crossref' } else { $arguments += '--no-crossref' }
& $python @arguments
