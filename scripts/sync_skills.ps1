<#
.SYNOPSIS
Safely copy or junction this repository's skills into one or more agent skill directories.

.EXAMPLE
.\scripts\sync_skills.ps1 -Destination "$HOME\.claude\skills", "$HOME\.codex\skills" -WhatIf

.EXAMPLE
.\scripts\sync_skills.ps1 -Destination "$HOME\.claude\skills" -Force
#>
[CmdletBinding(SupportsShouldProcess = $true)]
param(
    [Parameter(Mandatory = $true)]
    [string[]] $Destination,

    [ValidateSet("Copy", "Junction")]
    [string] $Mode = "Copy",

    [switch] $Force,
    [switch] $SkipValidation
)

$ErrorActionPreference = "Stop"
$RepoRoot = Split-Path -Parent $PSScriptRoot
$SkillsRoot = Join-Path $RepoRoot "skills"

if (-not (Test-Path $SkillsRoot -PathType Container)) {
    throw "Skills directory not found: $SkillsRoot"
}

if (-not $SkipValidation) {
    & python (Join-Path $PSScriptRoot "validate_repo.py") --strict
    if ($LASTEXITCODE -ne 0) {
        throw "Repository validation failed. No files were installed."
    }
}

$SkillDirectories = Get-ChildItem -Path $SkillsRoot -Directory | Sort-Object Name
foreach ($DestinationRootRaw in $Destination) {
    $DestinationRoot = $ExecutionContext.SessionState.Path.GetUnresolvedProviderPathFromPSPath($DestinationRootRaw)
    if ($PSCmdlet.ShouldProcess($DestinationRoot, "Create destination directory")) {
        New-Item -ItemType Directory -Path $DestinationRoot -Force | Out-Null
    }

    foreach ($Skill in $SkillDirectories) {
        $Target = Join-Path $DestinationRoot $Skill.Name
        if (Test-Path $Target) {
            if (-not $Force) {
                Write-Warning "Skipping existing skill '$Target'. Re-run with -Force to replace it."
                continue
            }
            if ($PSCmdlet.ShouldProcess($Target, "Remove existing skill before replacement")) {
                Remove-Item -Path $Target -Recurse -Force
            }
        }

        if ($Mode -eq "Junction") {
            if ($PSCmdlet.ShouldProcess($Target, "Create junction to $($Skill.FullName)")) {
                New-Item -ItemType Junction -Path $Target -Target $Skill.FullName | Out-Null
            }
        }
        else {
            if ($PSCmdlet.ShouldProcess($Target, "Copy skill from $($Skill.FullName)")) {
                Copy-Item -Path $Skill.FullName -Destination $Target -Recurse
            }
        }
    }
}

Write-Host "Processed $($SkillDirectories.Count) skills for $($Destination.Count) destination(s)."
