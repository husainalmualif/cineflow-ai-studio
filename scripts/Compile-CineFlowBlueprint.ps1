<#
.SYNOPSIS
    Thin PowerShell wrapper around cineflow_compiler.py (Single Source of Truth).
.DESCRIPTION
    Forwards all blueprint compilation arguments directly to scripts/cineflow_compiler.py
    to guarantee 100% behavioral parity across Windows PowerShell and Python CLI callers
    without duplicating compiler logic.
#>
[CmdletBinding()]
param(
    [string]$Title = "CineFlow Masterpiece Production",
    [string]$Purpose = "Commercials & TVCs",
    [string]$Format = "Live-Action",
    [string]$StyleVariant = "Commercial Promo",
    [string]$AspectRatio = "9:16",
    [int]$RuntimeSeconds = 20,
    [string]$Macro = "/anamorphic",
    [string]$RenderRuntime = "remotion",
    [string]$DesignStyle = "kinetic_typography",
    [string]$SpokenScript = "الوقت لا ينتظر أحدا. ابدأ رحلتك اليوم واصنع مستقبلك بيدك الآن.",
    [string]$OutputPath = "cineflow_blueprint.json"
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$CompilerPy = Join-Path $ScriptDir "cineflow_compiler.py"

$PythonCmd = $null
foreach ($candidate in @(
    "C:\Users\husai\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe",
    "python",
    "python3"
)) {
    if (Get-Command $candidate -ErrorAction SilentlyContinue) {
        $PythonCmd = $candidate
        break
    }
}

if (-not $PythonCmd) {
    throw "Python 3.9+ runtime not found. Please install Python to run cineflow_compiler.py."
}

& $PythonCmd $CompilerPy `
    --title $Title `
    --purpose $Purpose `
    --format $Format `
    --style $StyleVariant `
    --aspect $AspectRatio `
    --runtime $RuntimeSeconds `
    --macro $Macro `
    --render-runtime $RenderRuntime `
    --design-style $DesignStyle `
    --script $SpokenScript `
    --output $OutputPath

if ($LASTEXITCODE -ne 0) {
    throw "cineflow_compiler.py exited with code $LASTEXITCODE"
}
