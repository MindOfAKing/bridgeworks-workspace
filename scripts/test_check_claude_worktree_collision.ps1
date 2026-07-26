[CmdletBinding()]
param()

$ErrorActionPreference = "Stop"

$scriptPath = Join-Path $PSScriptRoot "check_claude_worktree_collision.ps1"
$repository = (Resolve-Path -LiteralPath (Join-Path $PSScriptRoot "..")).Path
$testRoot = Join-Path ([System.IO.Path]::GetTempPath()) "bridgeworks-collision-test-$([guid]::NewGuid())"
$fakeSecret = "must-not-appear-in-output"

try {
    New-Item -ItemType Directory -Path $testRoot | Out-Null
    $lock = @{
        pid = $PID
        workspaceFolders = @($repository)
        ideName = "Test IDE"
        transport = "ws"
        runningInWindows = $true
        authToken = $fakeSecret
    }
    $lock | ConvertTo-Json -Compress | Set-Content -LiteralPath (Join-Path $testRoot "$PID.lock")

    $blockedOutput = & $scriptPath -RepositoryPath $repository -ClaudeIdeDirectory $testRoot 2>&1 | Out-String
    $blockedCode = $LASTEXITCODE

    if ($blockedCode -ne 2) {
        throw "Expected collision exit code 2, received $blockedCode."
    }
    if ($blockedOutput -notmatch "BLOCKED") {
        throw "Collision output did not contain the BLOCKED marker."
    }
    if ($blockedOutput -match [regex]::Escape($fakeSecret)) {
        throw "Collision output exposed a lock-file credential."
    }

    $clearOutput = & $scriptPath -RepositoryPath $repository -ClaudeIdeDirectory $testRoot -IgnorePid $PID 2>&1 | Out-String
    $clearCode = $LASTEXITCODE

    if ($clearCode -ne 0) {
        throw "Expected clear exit code 0, received $clearCode."
    }
    if ($clearOutput -notmatch "CLEAR") {
        throw "Clear output did not contain the CLEAR marker."
    }

    Write-Output "Claude worktree collision preflight tests: passed"
}
finally {
    if (Test-Path -LiteralPath $testRoot) {
        $resolvedTestRoot = (Resolve-Path -LiteralPath $testRoot).Path
        $resolvedTempRoot = [System.IO.Path]::GetFullPath([System.IO.Path]::GetTempPath()).TrimEnd("\", "/")
        if (-not $resolvedTestRoot.StartsWith("$resolvedTempRoot\", [System.StringComparison]::OrdinalIgnoreCase)) {
            throw "Refusing to remove unexpected test path: $resolvedTestRoot"
        }
        Remove-Item -LiteralPath $resolvedTestRoot -Recurse -Force
    }
}
