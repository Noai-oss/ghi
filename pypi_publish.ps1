param(
    [Parameter(Mandatory = $true)]
    [string] $ReleaseVersion
)

$ErrorActionPreference = "Stop"

# PowerShell 5.1 does not stop on native command failures.
function run {
    $command = $args[0]
    $arguments = @()
    if ($args.Count -gt 1) {
        $arguments = $args[1..($args.Count - 1)]
    }

    & $command @arguments
    if ($LASTEXITCODE -ne 0) {
        exit $LASTEXITCODE
    }
}

if ($ReleaseVersion -notmatch '^\d+\.\d+\.\d+$') {
    Write-Error "usage: .\pypi_publish.ps1 x.y.z"
    exit 2
}

if (-not $env:UV_PUBLISH_TOKEN) {
    Write-Error "UV_PUBLISH_TOKEN is not set"
    exit 2
}

run git tag -a "$ReleaseVersion" -m "$ReleaseVersion"
run uv build --no-sources --clear
run uvx twine check dist/*
run git push origin "$ReleaseVersion"
run uv publish
