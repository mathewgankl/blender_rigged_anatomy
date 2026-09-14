[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)]
    [string]$ProjectRoot
)

$ErrorActionPreference = "Stop"
$bundleRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$manifestPath = Join-Path $bundleRoot "skills-lock.json"
$manifest = Get-Content -LiteralPath $manifestPath -Raw | ConvertFrom-Json
$projectRootFull = [IO.Path]::GetFullPath($ProjectRoot).TrimEnd('\')
$bundleRootFull = [IO.Path]::GetFullPath($bundleRoot).TrimEnd('\')
$operations = @()

foreach ($file in $manifest.files) {
    $source = [IO.Path]::GetFullPath((Join-Path $bundleRootFull $file.source))
    $target = [IO.Path]::GetFullPath((Join-Path $projectRootFull $file.target))

    if (-not $source.StartsWith("$bundleRootFull\", [StringComparison]::OrdinalIgnoreCase)) {
        throw "Source escapes bundle: $($file.source)"
    }
    if (-not $target.StartsWith("$projectRootFull\", [StringComparison]::OrdinalIgnoreCase)) {
        throw "Target escapes project: $($file.target)"
    }
    if (-not (Test-Path -LiteralPath $source -PathType Leaf)) {
        throw "Missing bundle file: $($file.source)"
    }

    $sourceHash = (Get-FileHash -LiteralPath $source -Algorithm SHA256).Hash.ToLowerInvariant()
    if ($sourceHash -ne $file.sha256) {
        throw "Bundle hash mismatch: $($file.source)"
    }

    if (Test-Path -LiteralPath $target) {
        $targetHash = (Get-FileHash -LiteralPath $target -Algorithm SHA256).Hash.ToLowerInvariant()
        if ($targetHash -ne $sourceHash) {
            throw "Refusing to overwrite local file: $($file.target)"
        }
    } else {
        $operations += [PSCustomObject]@{ Source = $source; Target = $target }
    }
}

foreach ($operation in $operations) {
    $parent = Split-Path -Parent $operation.Target
    if (-not (Test-Path -LiteralPath $parent)) {
        New-Item -ItemType Directory -Path $parent -Force | Out-Null
    }
    Copy-Item -LiteralPath $operation.Source -Destination $operation.Target
}

"Installed $($operations.Count) file(s) from bundle $($manifest.bundleVersion)."
