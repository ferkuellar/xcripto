Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

. "$PSScriptRoot\local-runtime.ps1"

$paths = Get-LocalRuntimePaths
$state = Get-LocalRuntimeState -Paths $paths

Write-Host "[XCripto Local Runtime]"
Write-Host ""

function Stop-IfScoped {
  param(
    [Parameter(Mandatory)][string]$Role,
    [Parameter(Mandatory)][string]$PidPath,
    [Parameter(Mandatory)][int]$Port
  )

  $stoppedAny = $false
  $processId = Read-PidFile -Path $PidPath
  if ($processId -eq $null) {
    $processId = Get-ListenerPid -Port $Port
  }

  if ($processId -ne $null -and (Stop-ScopedProcess -ProcessId $processId -Paths $paths -Role $Role)) {
    $stoppedAny = $true
    Write-Host "[STOP] $Role pid $processId"
    Remove-PidFile -Path $PidPath
  } elseif ($processId -ne $null) {
    Write-Host "[SKIP] $Role pid $processId does not match local runtime"
  } else {
    Write-Host "[SKIP] $Role not running"
  }

  return $stoppedAny
}

$backendStopped = Stop-IfScoped -Role 'backend' -PidPath $paths.BackendPid -Port 8000
$frontendStopped = Stop-IfScoped -Role 'frontend' -PidPath $paths.FrontendPid -Port 5173

Write-Host ""
if ($backendStopped -or $frontendStopped) {
  Write-Host "Local runtime stopped."
} else {
  Write-Host "Local runtime already stopped."
}
