# SPDX-License-Identifier: GPL-3.0-or-later

param(
    [string]$Blender = "C:\Program Files\Blender Foundation\Blender 5.2\blender.exe",
    [string]$MsHumanSource = $env:RA_MS_HUMAN_700_SOURCE
)

$ErrorActionPreference = "Stop"
$root = Split-Path -Parent $PSScriptRoot
$previousSource = $env:RA_MS_HUMAN_700_SOURCE

function Invoke-BlenderTest {
    param([string]$Path)
    & $Blender --background --factory-startup --python-exit-code 1 --python $Path
    if ($LASTEXITCODE -ne 0) {
        throw "Blender exited with code $LASTEXITCODE."
    }
}

try {
    $env:RA_MS_HUMAN_700_SOURCE = $MsHumanSource
    Invoke-BlenderTest (Join-Path $root "tests\headless\test_role_registry.py")
    Invoke-BlenderTest (Join-Path $root "tests\headless\test_semantic_mappings.py")
    Invoke-BlenderTest (Join-Path $root "tests\headless\test_source_manifest.py")
    Invoke-BlenderTest (Join-Path $root "tests\headless\test_catalog_schemas.py")
    Invoke-BlenderTest (Join-Path $root "tests\headless\test_anatomy_asset_conversion.py")
    & (Join-Path $root "tests\run_milestone1.ps1") -Blender $Blender
}
finally {
    $env:RA_MS_HUMAN_700_SOURCE = $previousSource
}
