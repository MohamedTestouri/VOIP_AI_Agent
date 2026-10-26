param(
    [string]$RepositoryUrl = "https://github.com/MohamedTestouri/VOIP_AI_Agent.git"
)
$ErrorActionPreference = "Stop"

if (!(Get-Command git -ErrorAction SilentlyContinue)) { throw "Git is required. Install Git and configure GitHub authentication first." }
if (!(Test-Path ".git")) { git init -b main }
$origin = git remote get-url origin 2>$null
if ($LASTEXITCODE -ne 0) {
    git remote add origin $RepositoryUrl
} elseif ($origin.TrimEnd('/') -ne $RepositoryUrl.TrimEnd('/')) {
    throw "Existing origin points to '$origin', not '$RepositoryUrl'. Refusing to push to a different repository."
}
git add -A
$hasCommit = git rev-parse --verify HEAD 2>$null
if ($LASTEXITCODE -ne 0) {
    git commit -m "chore: initialize VoIP AI engineering workspace"
} elseif ((git status --porcelain).Length -gt 0) {
    git commit -m "feat: add VoIP AI engineering workspace"
}
git push -u origin main
