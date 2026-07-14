Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

. "$PSScriptRoot\local-runtime.ps1"

function Wait-ForBackendListener {
  param(
    [Parameter(Mandatory)]$Paths,
    [int]$TimeoutSeconds = 120
  )

  $health = Wait-ForBackendHealth -Url "$($Paths.BackendUrl)/health" -TimeoutSeconds $TimeoutSeconds
  $processId = Get-ListenerPid -Port 8000
  if ($null -eq $processId) {
    throw "Backend health is up, but no listener was found on port 8000."
  }

  if (-not (Test-BackendProcess -ProcessId $processId -Paths $Paths)) {
    throw "Port 8000 is occupied by an unexpected process (pid $processId)."
  }

  Write-PidFile -Path $Paths.BackendPid -ProcessId $processId
  return $health
}

function Wait-ForFrontendListener {
  param(
    [Parameter(Mandatory)]$Paths,
    [int]$TimeoutSeconds = 120
  )

  $response = Wait-ForHttpStatus -Url $Paths.FrontendUrl -ExpectedStatus 200 -TimeoutSeconds $TimeoutSeconds
  $processId = Get-ListenerPid -Port 5173
  if ($null -eq $processId) {
    throw "Frontend is responding, but no listener was found on port 5173."
  }

  if (-not (Test-FrontendProcess -ProcessId $processId -Paths $Paths)) {
    throw "Port 5173 is occupied by an unexpected process (pid $processId)."
  }

  Write-PidFile -Path $Paths.FrontendPid -ProcessId $processId
  return $response
}

$paths = Get-LocalRuntimePaths
Ensure-LocalRuntimeDirectories -Paths $paths
Initialize-LocalEnvFiles -Paths $paths

Write-Host "[XCripto Local Runtime]"

$backendState = Get-LocalRuntimeState -Paths $paths
Write-Host ""
Write-Host "[START] Backend"
if ($backendState.BackendPid -and (Test-BackendProcess -ProcessId $backendState.BackendPid -Paths $paths)) {
  $backendHealth = Wait-ForBackendHealth -Url "$($paths.BackendUrl)/health" -TimeoutSeconds 30
  Write-PidFile -Path $paths.BackendPid -ProcessId $backendState.BackendPid
  Write-Host "[PASS] Backend already running on $($paths.BackendUrl) (pid $($backendState.BackendPid))"
} else {
  Remove-PidFile -Path $paths.BackendPid
  $backendEnv = @{
    XMIP_DISABLE_DOTENV             = '1'
    APP_NAME                        = 'XMIP Backend'
    ENVIRONMENT                     = 'local'
    DEBUG                           = 'false'
    AUTH_ENABLED                    = 'true'
    API_KEY                         = 'dev-secret'
    API_KEY_HEADER_NAME             = 'X-API-Key'
    AUTO_CREATE_TABLES              = 'false'
    DATABASE_URL                    = 'sqlite+aiosqlite:///./xcripto-local.db'
    CORS_ALLOWED_ORIGINS            = 'http://localhost:5173,http://127.0.0.1:5173'
    CORS_ALLOW_CREDENTIALS          = 'false'
    REQUEST_LOGGING_ENABLED         = 'true'
    REQUEST_BODY_LOGGING_ENABLED    = 'false'
    RESPONSE_BODY_LOGGING_ENABLED   = 'false'
    REQUEST_TIMEOUT_SECONDS         = '30'
    OPERATIONAL_AUDIT_ENABLED       = 'true'
    DB_HEALTHCHECK_ENABLED          = 'true'
    CONNECTORS_ENABLED              = 'false'
    RSS_CONNECTOR_ENABLED           = 'false'
    CONNECTOR_RUN_MODE              = 'manual'
    CONNECTOR_AUDIT_ENABLED         = 'true'
    CONNECTOR_REQUIRE_SOURCE_REFERENCE = 'true'
    CONNECTOR_AUTO_PROMOTE          = 'false'
    TELEGRAM_BOT_TOKEN              = ''
    TELEGRAM_CHANNEL_ID             = ''
    X_API_KEY                       = ''
    X_API_SECRET                    = ''
    X_ACCESS_TOKEN                  = ''
    X_ACCESS_TOKEN_SECRET           = ''
    BINANCE_SQUARE_OPENAPI_KEY      = ''
    PUBLIC_SITE_URL                 = 'http://localhost:3000'
  }

  $backendPython = Join-Path $paths.BackendDir '.venv\Scripts\python.exe'
  if (-not (Test-Path -LiteralPath $backendPython)) {
    throw "Backend virtualenv not found at $backendPython"
  }

  $backendArgs = @('-m', 'uvicorn', 'app.main:app', '--host', '127.0.0.1', '--port', '8000')
  $alembicArgs = @('-m', 'alembic', 'upgrade', 'head')
  $alembicProcess = Start-ManagedProcess -FilePath $backendPython -Arguments $alembicArgs -WorkingDirectory $paths.BackendDir -Environment $backendEnv -LogPath $paths.BackendLog
  $alembicProcess.WaitForExit()
  if ($alembicProcess.ExitCode -ne 0) {
    throw "Alembic upgrade failed with exit code $($alembicProcess.ExitCode). See $($paths.BackendLog)."
  }

  $backendProcess = Start-ManagedProcess -FilePath $backendPython -Arguments $backendArgs -WorkingDirectory $paths.BackendDir -Environment $backendEnv -LogPath $paths.BackendLog
  Start-Sleep -Seconds 2
  $backendHealth = Wait-ForBackendListener -Paths $paths -TimeoutSeconds 120
  Write-Host "[PASS] Backend listening on $($paths.BackendUrl) (pid $((Read-PidFile -Path $paths.BackendPid)))"
}

Write-Host ""
Write-Host "[START] Frontend"
$frontendState = Get-LocalRuntimeState -Paths $paths
if ($frontendState.FrontendPid -and (Test-FrontendProcess -ProcessId $frontendState.FrontendPid -Paths $paths)) {
  $frontendResponse = Wait-ForHttpStatus -Url $paths.FrontendUrl -ExpectedStatus 200 -TimeoutSeconds 30
  Write-PidFile -Path $paths.FrontendPid -ProcessId $frontendState.FrontendPid
  Write-Host "[PASS] Dashboard already running on $($paths.FrontendUrl) (pid $($frontendState.FrontendPid))"
} else {
  Remove-PidFile -Path $paths.FrontendPid
  $frontendEnv = @{
    VITE_API_BASE_URL = 'http://127.0.0.1:8000'
    VITE_API_KEY      = 'dev-secret'
    VITE_ACTOR_ROLE   = 'admin'
    VITE_ACTOR_ID     = 'local-admin'
  }

  $npmExe = 'npm.cmd'
  $frontendArgs = @('run', 'dev', '--', '--host', 'localhost', '--port', '5173')
  $frontendProcess = Start-ManagedProcess -FilePath $npmExe -Arguments $frontendArgs -WorkingDirectory $paths.FrontendDir -Environment $frontendEnv -LogPath $paths.FrontendLog
  Start-Sleep -Seconds 2
  $frontendResponse = Wait-ForFrontendListener -Paths $paths -TimeoutSeconds 120
  Write-Host "[PASS] Dashboard listening on $($paths.FrontendUrl) (pid $((Read-PidFile -Path $paths.FrontendPid)))"
}

Write-Host ""
Write-Host "Local runtime logs:"
Write-Host "  Backend : $($paths.BackendLog)"
Write-Host "  Frontend: $($paths.FrontendLog)"
