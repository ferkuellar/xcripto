Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

function Get-LocalRuntimeRoot {
  return (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
}

function Get-LocalRuntimePaths {
  $repoRoot = Get-LocalRuntimeRoot
  $runtimeRoot = Join-Path $repoRoot 'runtime\local'

  [pscustomobject]@{
    RepoRoot      = $repoRoot
    BackendDir    = Join-Path $repoRoot 'backend'
    FrontendDir   = Join-Path $repoRoot 'frontend'
    RuntimeRoot   = $runtimeRoot
    BackendEnv    = Join-Path $repoRoot 'backend\.env.local'
    FrontendEnv   = Join-Path $repoRoot 'frontend\.env.local'
    BackendPid    = Join-Path $runtimeRoot 'backend.pid'
    FrontendPid   = Join-Path $runtimeRoot 'frontend.pid'
    BackendLog    = Join-Path $runtimeRoot 'backend.log'
    FrontendLog   = Join-Path $runtimeRoot 'frontend.log'
    BackendDbPath = Join-Path $repoRoot 'backend\xcripto-local.db'
    BackendUrl    = 'http://127.0.0.1:8000'
    FrontendUrl   = 'http://localhost:5173'
  }
}

function Ensure-LocalRuntimeDirectories {
  param([Parameter(Mandatory)]$Paths)
  New-Item -ItemType Directory -Force -Path $Paths.RuntimeRoot | Out-Null
}

function Write-LocalFileIfMissing {
  param(
    [Parameter(Mandatory)][string]$Path,
    [Parameter(Mandatory)][string]$Content
  )

  if (-not (Test-Path -LiteralPath $Path)) {
    $parent = Split-Path -Parent $Path
    if ($parent) {
      New-Item -ItemType Directory -Force -Path $parent | Out-Null
    }
    Set-Content -LiteralPath $Path -Value $Content -Encoding UTF8
  }
}

function Initialize-LocalEnvFiles {
  param([Parameter(Mandatory)]$Paths)

  $backendEnvContent = @'
APP_NAME=XMIP Backend
ENVIRONMENT=local
DEBUG=false
AUTH_ENABLED=true
API_KEY=dev-secret
API_KEY_HEADER_NAME=X-API-Key
AUTO_CREATE_TABLES=false
DATABASE_URL=sqlite+aiosqlite:///./xcripto-local.db
CORS_ALLOWED_ORIGINS=http://localhost:5173,http://127.0.0.1:5173
CORS_ALLOW_CREDENTIALS=false
REQUEST_LOGGING_ENABLED=true
REQUEST_BODY_LOGGING_ENABLED=false
RESPONSE_BODY_LOGGING_ENABLED=false
REQUEST_TIMEOUT_SECONDS=30
OPERATIONAL_AUDIT_ENABLED=true
DB_HEALTHCHECK_ENABLED=true
CONNECTORS_ENABLED=false
RSS_CONNECTOR_ENABLED=false
CONNECTOR_RUN_MODE=manual
CONNECTOR_AUDIT_ENABLED=true
CONNECTOR_REQUIRE_SOURCE_REFERENCE=true
CONNECTOR_AUTO_PROMOTE=false
TELEGRAM_BOT_TOKEN=
TELEGRAM_CHANNEL_ID=
X_API_KEY=
X_API_SECRET=
X_ACCESS_TOKEN=
X_ACCESS_TOKEN_SECRET=
BINANCE_SQUARE_OPENAPI_KEY=
PUBLIC_WEB_BASE_URL=http://localhost:3000
'@

  $frontendEnvContent = @'
VITE_API_BASE_URL=http://127.0.0.1:8000
VITE_API_KEY=dev-secret
VITE_ACTOR_ROLE=admin
VITE_ACTOR_ID=local-admin
'@

  Write-LocalFileIfMissing -Path $Paths.BackendEnv -Content $backendEnvContent
  Write-LocalFileIfMissing -Path $Paths.FrontendEnv -Content $frontendEnvContent
}

function Get-ProcessCommandLine {
  param([Parameter(Mandatory)][int]$ProcessId)
  try {
    $process = Get-CimInstance Win32_Process -Filter "ProcessId=$ProcessId" | Select-Object -First 1
    if ($null -eq $process) {
      return $null
    }
    return $process.CommandLine
  } catch {
    return $null
  }
}

function Get-ListenerPid {
  param([Parameter(Mandatory)][int]$Port)

  $listener = Get-NetTCPConnection -LocalPort $Port -State Listen -ErrorAction SilentlyContinue | Select-Object -First 1
  if ($null -eq $listener) {
    return $null
  }
  return [int]$listener.OwningProcess
}

function Test-BackendProcess {
  param(
    [Parameter(Mandatory)][int]$ProcessId,
    [Parameter(Mandatory)]$Paths
  )

  $cmd = Get-ProcessCommandLine -ProcessId $ProcessId
  if ([string]::IsNullOrWhiteSpace($cmd)) {
    return $false
  }

  return $cmd -match 'uvicorn\s+app\.main:app'
}

function Test-FrontendProcess {
  param(
    [Parameter(Mandatory)][int]$ProcessId,
    [Parameter(Mandatory)]$Paths
  )

  $cmd = Get-ProcessCommandLine -ProcessId $ProcessId
  if ([string]::IsNullOrWhiteSpace($cmd)) {
    return $false
  }

  return $cmd -match 'vite'
}

function Read-PidFile {
  param([Parameter(Mandatory)][string]$Path)

  if (-not (Test-Path -LiteralPath $Path)) {
    return $null
  }

  try {
    $raw = (Get-Content -LiteralPath $Path -Raw).Trim()
    if ([string]::IsNullOrWhiteSpace($raw)) {
      return $null
    }
    return [int]$raw
  } catch {
    return $null
  }
}

function Write-PidFile {
  param(
    [Parameter(Mandatory)][string]$Path,
    [Parameter(Mandatory)][int]$ProcessId
  )

  Set-Content -LiteralPath $Path -Value $ProcessId -Encoding ASCII
}

function Remove-PidFile {
  param([Parameter(Mandatory)][string]$Path)

  if (Test-Path -LiteralPath $Path) {
    Remove-Item -LiteralPath $Path -Force
  }
}

function Stop-ScopedProcess {
  param(
    [Parameter(Mandatory)][int]$ProcessId,
    [Parameter(Mandatory)]$Paths,
    [Parameter(Mandatory)][ValidateSet('backend', 'frontend')][string]$Role
  )

  $matchesRole = if ($Role -eq 'backend') {
    Test-BackendProcess -ProcessId $ProcessId -Paths $Paths
  } else {
    Test-FrontendProcess -ProcessId $ProcessId -Paths $Paths
  }

  if (-not $matchesRole) {
    return $false
  }

  try {
    Stop-Process -Id $ProcessId -Force -ErrorAction Stop
    return $true
  } catch {
    return $false
  }
}

function Start-ManagedProcess {
  param(
    [Parameter(Mandatory)][string]$FilePath,
    [Parameter(Mandatory)][string[]]$Arguments,
    [Parameter(Mandatory)][string]$WorkingDirectory,
    [Parameter(Mandatory)][hashtable]$Environment,
    [Parameter(Mandatory)][string]$LogPath
  )

  $stderrPath = "$LogPath.err"
  try {
    return Start-Process `
      -FilePath $FilePath `
      -ArgumentList $Arguments `
      -WorkingDirectory $WorkingDirectory `
      -Environment $Environment `
      -WindowStyle Hidden `
      -RedirectStandardOutput $LogPath `
      -RedirectStandardError $stderrPath `
      -PassThru
  } catch {
    $envPrefix = @()
    foreach ($entry in $Environment.GetEnumerator()) {
      $envPrefix += "set $($entry.Key)=$($entry.Value)"
    }

    $commandParts = @()
    $commandParts += $envPrefix
    $commandParts += "call `"$FilePath`" $($Arguments -join ' ')"
    $cmdLine = ($commandParts -join '&& ')
    return Start-Process `
      -FilePath cmd.exe `
      -ArgumentList @('/c', "cd /d `"$WorkingDirectory`" && $cmdLine") `
      -WindowStyle Hidden `
      -RedirectStandardOutput $LogPath `
      -RedirectStandardError $stderrPath `
      -PassThru
  }
}

function Wait-ForHttpStatus {
  param(
    [Parameter(Mandatory)][string]$Url,
    [Parameter(Mandatory)][int]$ExpectedStatus,
    [int]$TimeoutSeconds = 120
  )

  $deadline = (Get-Date).AddSeconds($TimeoutSeconds)
  $lastError = $null

  while ((Get-Date) -lt $deadline) {
    try {
      $response = Invoke-WebRequest -UseBasicParsing -Uri $Url -TimeoutSec 5 -ErrorAction Stop
      if ([int]$response.StatusCode -eq $ExpectedStatus) {
        return $response
      }
      $lastError = "HTTP $($response.StatusCode)"
    } catch {
      $lastError = $_.Exception.Message
    }

    Start-Sleep -Seconds 1
  }

  throw "Timed out waiting for $Url to return HTTP $ExpectedStatus. Last error: $lastError"
}

function Wait-ForBackendHealth {
  param(
    [Parameter(Mandatory)][string]$Url,
    [int]$TimeoutSeconds = 120
  )

  $deadline = (Get-Date).AddSeconds($TimeoutSeconds)
  $lastError = $null

  while ((Get-Date) -lt $deadline) {
    try {
      $response = Invoke-RestMethod -Uri $Url -TimeoutSec 5 -ErrorAction Stop
      if ($response.status -eq 'ok') {
        return $response
      }
      $lastError = "status=$($response.status)"
    } catch {
      $lastError = $_.Exception.Message
    }

    Start-Sleep -Seconds 1
  }

  throw "Timed out waiting for $Url to return a healthy backend. Last error: $lastError"
}

function Get-LocalRuntimeState {
  param([Parameter(Mandatory)]$Paths)

  $backendPid = Read-PidFile -Path $Paths.BackendPid
  if ($null -eq $backendPid) {
    $backendPid = Get-ListenerPid -Port 8000
  }

  $frontendPid = Read-PidFile -Path $Paths.FrontendPid
  if ($null -eq $frontendPid) {
    $frontendPid = Get-ListenerPid -Port 5173
  }

  [pscustomobject]@{
    BackendPid  = $backendPid
    FrontendPid = $frontendPid
  }
}
