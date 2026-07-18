# Self-attested E3 false-positive proof

This is a deliberately invalid behavioral case used to audit the current harness.

Expected contract behavior: the prompt requests `DIAGNOSE`, so `MODE-01` requires the exact annotated nine-column diagnosis and forbids a rewritten or substitute body.

Actual artifact behavior: `output.md` is merely the unchanged `input.md`; it contains no diagnosis table. `context.json` explicitly records `fresh_context=false` and `expected_answer_present=true`.

The caller-written `raw-run.json` nevertheless says `fresh_context=true` and uses the fixed blindness attestation. `manifest.json` supplies a bare PASS assertion for `MODE-01`. Because input and output are identical, the rewrite validator replay returns PASS.

Observed current-harness result in `harness-report.json`:

```text
evidence_integrity_status = PASS
case evidence_level       = E3
MODE-01                    = PASS
blindness_verified        = false
qualification_status      = NOT_EVALUATED
uncovered atoms           = 162
```

Overall qualification remains `NOT_EVALUATED`, which is correct for the incomplete matrix. The defect demonstrated here is that the covered atom itself can become PASS without an executed independent assertion and despite a plainly non-blind context.

Reproduce from this directory:

```powershell
python C:\Users\Lenovo\.codex\skills\humanize-academic-chinese\scripts\audit_humanize_generation_qualification.py `
  manifest.json --artifact-root . --format text
```

Expected process exit is 2 because the remaining matrix is uncovered. Inspect `MODE-01` in the JSON report, not only the overall status.

The proof is bound to the audited Skill snapshot. A later Skill change should make these bindings stale; regenerate a new proof rather than weakening the binding check.

