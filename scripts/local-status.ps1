Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

. "$PSScriptRoot\local-runtime.ps1"

$paths = Get-LocalRuntimePaths
$state = Get-LocalRuntimeState -Paths $paths

function Get-HttpStatus {
  param([Parameter(Mandatory)][string]$Url)
  try {
    return [int](Invoke-WebRequest -UseBasicParsing -Uri $Url -TimeoutSec 5 -ErrorAction Stop).StatusCode
  } catch {
    return $null
  }
}

$backendHttp = Get-HttpStatus -Url "$($paths.BackendUrl)/health"
$frontendHttp = Get-HttpStatus -Url $paths.FrontendUrl

$backendState = if ($state.BackendPid) { 'RUNNING' } else { 'STOPPED' }
$frontendState = if ($state.FrontendPid) { 'RUNNING' } else { 'STOPPED' }

$backendHealth = if ($backendHttp -ne $null) { "health=$backendHttp" } else { 'health=down' }
$frontendHttpLabel = if ($frontendHttp -ne $null) { "http=$frontendHttp" } else { 'http=down' }

$dbPath = $paths.BackendDbPath
if (Test-Path -LiteralPath $paths.BackendEnv) {
  $databaseLine = Get-Content -LiteralPath $paths.BackendEnv | Where-Object { $_ -match '^DATABASE_URL=' } | Select-Object -First 1
  if ($databaseLine -and $databaseLine -match '^DATABASE_URL=sqlite\+aiosqlite:///\.\/(.+)$') {
    $dbPath = Join-Path $paths.BackendDir $Matches[1]
  }
}

Write-Host "XCripto Local Runtime Status"
Write-Host ""
Write-Host ("Backend   {0}  {1}  {2}" -f $backendState, $paths.BackendUrl, $backendHealth)
Write-Host ("Frontend  {0}  {1}  {2}" -f $frontendState, $paths.FrontendUrl, $frontendHttpLabel)
Write-Host ("Database  SQLITE  {0}" -f $dbPath)
