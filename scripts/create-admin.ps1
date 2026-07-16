Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

. "$PSScriptRoot\local-runtime.ps1"

$paths = Get-LocalRuntimePaths
$python = Join-Path $paths.BackendDir '.venv\Scripts\python.exe'
if (-not (Test-Path -LiteralPath $python)) {
  throw "Backend virtualenv not found at $python"
}

$script = Join-Path $paths.BackendDir 'scripts\create_admin.py'
if (-not (Test-Path -LiteralPath $script)) {
  throw "Admin bootstrap script not found at $script"
}

Push-Location $paths.BackendDir
try {
  & $python $script @args
} finally {
  Pop-Location
}
