$ErrorActionPreference = "Stop"

$AuditRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$Workspace = Resolve-Path (Join-Path $AuditRoot "..\..")
$Skill = Join-Path $HOME ".codex\skills\humanize-academic-chinese"
$Harness = Join-Path $Skill "scripts\audit_humanize_generation_qualification.py"

Push-Location $Workspace
try {
    python -m unittest tests.test_audit_humanize_generation_qualification -v
    if ($LASTEXITCODE -ne 0) {
        throw "qualification unit tests failed with exit $LASTEXITCODE"
    }

    python $Harness tests\fixtures\humanize_generation_qualification\manifest.json `
        --artifact-root tests --format text
    $FixtureExit = $LASTEXITCODE
    if ($FixtureExit -ne 2) {
        throw "baseline fixture should be NOT_EVALUATED/2, got exit $FixtureExit"
    }
}
finally {
    Pop-Location
}

$Proof = Join-Path $AuditRoot "proof\self-attested-false-positive"
Push-Location $Proof
try {
    python $Harness manifest.json --artifact-root . --format text
    $ProofExit = $LASTEXITCODE
    if ($ProofExit -ne 2) {
        throw "proof should be incomplete NOT_EVALUATED/2, got exit $ProofExit"
    }
}
finally {
    Pop-Location
}

Write-Output "Verified: 17 unit tests pass; baseline and proof both exit NOT_EVALUATED/2."
Write-Output "Inspect harness-report.json for proof case E3 and MODE-01=PASS."
