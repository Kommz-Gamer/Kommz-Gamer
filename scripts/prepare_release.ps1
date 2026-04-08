param(
  [string]$ExePath = '',
  [string]$VersionFile = 'version.txt',
  [string]$BaseDownloadUrl = '',
  [string]$ChangelogFileName = ''
)

$projectRoot = Split-Path -Parent $PSScriptRoot
$resolvedVersionFile = if ([System.IO.Path]::IsPathRooted($VersionFile)) {
  $VersionFile
} else {
  Join-Path $projectRoot $VersionFile
}

if (!(Test-Path $resolvedVersionFile)) {
  throw "Version file introuvable: $resolvedVersionFile"
}

$version = (Get-Content $resolvedVersionFile -Raw).Trim()
if (-not $version) {
  throw "Version vide dans $resolvedVersionFile"
}

if (-not $ExePath) {
  $candidates = @(
    (Join-Path $projectRoot ("dist\Kommz_Gamer_V{0}.exe" -f $version)),
    (Join-Path $projectRoot 'dist\Kommz_Gamer.exe'),
    (Join-Path $projectRoot 'dist\Kommz_Diamond.exe')
  )
  $ExePath = $candidates | Where-Object { Test-Path $_ } | Select-Object -First 1
} elseif (-not [System.IO.Path]::IsPathRooted($ExePath)) {
  $ExePath = Join-Path $projectRoot $ExePath
}

if (!(Test-Path $ExePath)) {
  throw "EXE introuvable: $ExePath"
}

$sha256 = (Get-FileHash -Path $ExePath -Algorithm SHA256).Hash.ToLower()
$fileName = [System.IO.Path]::GetFileName($ExePath)
$downloadUrl = if ($BaseDownloadUrl) { "$BaseDownloadUrl/$fileName" } else { '' }
$changelogName = if ($ChangelogFileName) { $ChangelogFileName } else { "CHANGELOG_V{0}.md" -f $version }
$changelogUrl = if ($BaseDownloadUrl) { "$BaseDownloadUrl/$changelogName" } else { '' }
$releaseEnvPath = Join-Path $projectRoot 'dist\.env.release'
$releaseMetadataPath = Join-Path $projectRoot 'dist\release-metadata.json'
$releaseEnv = @(
  "DESKTOP_STABLE_VERSION=$version"
  "DESKTOP_DOWNLOAD_URL=$downloadUrl"
  "DESKTOP_DOWNLOAD_SHA256=$sha256"
  "DESKTOP_CHANGELOG_URL=$changelogUrl"
)

Write-Host "DESKTOP_STABLE_VERSION=$version"
Write-Host "DESKTOP_DOWNLOAD_URL=$downloadUrl"
Write-Host "DESKTOP_DOWNLOAD_SHA256=$sha256"
Write-Host "DESKTOP_CHANGELOG_URL=$changelogUrl"

$payload = [ordered]@{
  version = $version
  filename = $fileName
  sha256 = $sha256
  changelog_filename = $changelogName
  changelog_url = $changelogUrl
  generated_at_utc = (Get-Date).ToUniversalTime().ToString('s') + 'Z'
}
$payload | ConvertTo-Json -Depth 4 | Set-Content -Path $releaseMetadataPath -Encoding UTF8
$releaseEnv | Set-Content -Path $releaseEnvPath -Encoding UTF8
Write-Host "release metadata: $releaseMetadataPath"
Write-Host "release env: $releaseEnvPath"
