[CmdletBinding()]
param(
    [Parameter(Position = 0)]
    [string]$RepositoryPath = (Get-Location).Path,

    [string]$ClaudeIdeDirectory = (Join-Path $env:USERPROFILE ".claude\ide"),

    [int[]]$IgnorePid = @()
)

$ErrorActionPreference = "Stop"

function Get-NormalizedPath {
    param([Parameter(Mandatory)][string]$Path)

    return [System.IO.Path]::GetFullPath($Path).TrimEnd("\", "/")
}

function Test-PathOverlap {
    param(
        [Parameter(Mandatory)][string]$First,
        [Parameter(Mandatory)][string]$Second
    )

    $left = Get-NormalizedPath -Path $First
    $right = Get-NormalizedPath -Path $Second
    $comparison = [System.StringComparison]::OrdinalIgnoreCase

    return $left.Equals($right, $comparison) -or
        $left.StartsWith("$right\", $comparison) -or
        $right.StartsWith("$left\", $comparison)
}

$repository = Get-NormalizedPath -Path (Resolve-Path -LiteralPath $RepositoryPath).Path
$activeOverlaps = @()

if (Test-Path -LiteralPath $ClaudeIdeDirectory) {
    foreach ($lockFile in Get-ChildItem -LiteralPath $ClaudeIdeDirectory -Filter "*.lock" -File) {
        try {
            $lock = Get-Content -LiteralPath $lockFile.FullName -Raw | ConvertFrom-Json
        }
        catch {
            Write-Warning "Skipped unreadable IDE lock: $($lockFile.Name)"
            continue
        }

        $processId = [int]$lock.pid
        if ($IgnorePid -contains $processId) {
            continue
        }

        $process = Get-Process -Id $processId -ErrorAction SilentlyContinue
        if (-not $process) {
            continue
        }

        foreach ($workspaceFolder in @($lock.workspaceFolders)) {
            if ($workspaceFolder -and (Test-PathOverlap -First $repository -Second $workspaceFolder)) {
                $activeOverlaps += [pscustomobject]@{
                    Pid = $processId
                    Ide = [string]$lock.ideName
                    Workspace = Get-NormalizedPath -Path $workspaceFolder
                }
            }
        }
    }
}

$workingTreeChanges = @(
    git -c "safe.directory=$repository" -C $repository status --porcelain=v1 2>$null
)

$desktopProcessCount = @(
    Get-Process -Name "claude" -ErrorAction SilentlyContinue |
        Where-Object { $_.Path -like "*WindowsApps\Claude_*" }
).Count

Write-Output "Repository: $repository"
Write-Output "Working tree changes: $($workingTreeChanges.Count)"
Write-Output "Claude Desktop app processes: $desktopProcessCount (presence only)"

if ($activeOverlaps.Count -gt 0) {
    Write-Output "Potential overlapping IDE sessions:"
    $activeOverlaps |
        Sort-Object Pid, Workspace -Unique |
        Format-Table Pid, Ide, Workspace -AutoSize |
        Out-String |
        Write-Output
    Write-Output "BLOCKED: an active Claude IDE lock overlaps this repository. Use a separate worktree or hand off ownership."
    exit 2
}

Write-Output "CLEAR: no active overlapping Claude IDE lock was found."
exit 0
