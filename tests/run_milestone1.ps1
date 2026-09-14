# SPDX-License-Identifier: GPL-3.0-or-later

param(
    [string]$Blender = "C:\Program Files\Blender Foundation\Blender 5.2\blender.exe"
)

$ErrorActionPreference = "Stop"
$root = Split-Path -Parent $PSScriptRoot
$source = Join-Path $root "src\rigged_anatomy"
$headlessTest = Join-Path $root "tests\headless\test_vertical_slice.py"
$lifecycleTest = Join-Path $root "tests\headless\test_installed_lifecycle.py"
$tempRoot = Join-Path ([System.IO.Path]::GetTempPath()) "rigged-anatomy-m1-$PID"
$archive = Join-Path $tempRoot "rigged_anatomy-0.1.0.zip"
$userResources = Join-Path $tempRoot "blender-user"
$previousResources = $env:BLENDER_USER_RESOURCES

function Invoke-Blender {
    param([string[]]$Arguments)
    & $Blender @Arguments
    if ($LASTEXITCODE -ne 0) {
        throw "Blender exited with code $LASTEXITCODE."
    }
}

try {
    New-Item -ItemType Directory -Path $tempRoot | Out-Null
    New-Item -ItemType Directory -Path $userResources | Out-Null
    New-Item -ItemType Directory -Path (Join-Path $userResources "extensions\blender_org") -Force | Out-Null

    Invoke-Blender @("--background", "--factory-startup", "--python-exit-code", "1", "--python", $headlessTest)
    Invoke-Blender @("--command", "extension", "validate", $source)
    Invoke-Blender @("--command", "extension", "build", "--source-dir", $source, "--output-filepath", $archive)
    Invoke-Blender @("--command", "extension", "validate", $archive)

    $env:BLENDER_USER_RESOURCES = $userResources
    Invoke-Blender @("--command", "extension", "install-file", "-r", "user_default", "-e", $archive)
    Invoke-Blender @("--background", "--python-exit-code", "1", "--python", $lifecycleTest, "--", "lifecycle")
    Invoke-Blender @("--command", "extension", "remove", "rigged_anatomy")
    Invoke-Blender @("--background", "--python-exit-code", "1", "--python", $lifecycleTest, "--", "uninstalled")
}
finally {
    $env:BLENDER_USER_RESOURCES = $previousResources
    if (Test-Path -LiteralPath $tempRoot) {
        Remove-Item -LiteralPath $tempRoot -Recurse -Force
    }
}
