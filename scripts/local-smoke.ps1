Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

. "$PSScriptRoot\local-runtime.ps1"

$paths = Get-LocalRuntimePaths

function Assert-Status {
  param(
    [Parameter(Mandatory)][string]$Url,
    [Parameter(Mandatory)][int]$ExpectedStatus,
    [Parameter(Mandatory)][string]$Label
  )

  $response = Invoke-WebRequest -UseBasicParsing -Uri $Url -TimeoutSec 10 -ErrorAction Stop
  if ([int]$response.StatusCode -ne $ExpectedStatus) {
    throw "$Label returned HTTP $($response.StatusCode), expected $ExpectedStatus"
  }
  Write-Host "[PASS] $Label -> $ExpectedStatus"
}

$health = Invoke-RestMethod -Uri "$($paths.BackendUrl)/health" -TimeoutSec 10 -ErrorAction Stop
if ($health.status -ne 'ok') {
  throw "Backend health returned status '$($health.status)'"
}
Write-Host "[PASS] Backend health -> 200"

$news = Invoke-RestMethod -Uri "$($paths.BackendUrl)/api/v1/public/news" -TimeoutSec 10 -ErrorAction Stop
if ($null -eq $news -or -not ($news -is [array])) {
  throw "Public news API did not return a JSON array"
}
if ($news.Count -gt 0) {
  $first = $news[0]
  foreach ($field in @('id', 'title', 'summary', 'category', 'status', 'canonical_url')) {
    if (-not $first.PSObject.Properties.Name.Contains($field)) {
      throw "Public news API response missing expected field '$field'"
    }
  }
}
Write-Host "[PASS] Public news API -> 200"

Assert-Status -Url $paths.FrontendUrl -ExpectedStatus 200 -Label 'Dashboard'

Write-Host ""
Write-Host "LOCAL-OPS.1 SMOKE RESULT: PASS"
