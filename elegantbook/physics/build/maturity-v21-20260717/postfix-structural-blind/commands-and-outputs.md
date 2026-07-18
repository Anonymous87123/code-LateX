# Commands and outputs

All commands below were run from `D:\code LateX\elegantbook\physics` in
PowerShell. Skill and contract files were read as UTF-8 before the test; those
read-only setup calls did not create test inputs or mutate the repository.

## Source discovery

```powershell
rg -n '^\\(part|chapter|section|subsection|subsubsection)\*?\{' -- 'physics1.tex'
```

The source contained 4685 lines and 50 prepared editable units. The selected
heading was reported at source line 2279:

```text
2279:\section{弦振动的简正模式}
```

The first metadata attempt used .NET APIs unavailable in this PowerShell
runtime and failed without writing anything:

```powershell
[Security.Cryptography.SHA256]::HashData(...)
[Convert]::ToHexString(...)
```

```text
Method invocation failed: SHA256 does not contain HashData.
Method invocation failed: Convert does not contain ToHexString.
```

The compatible retry was:

```powershell
$p='D:\code LateX\elegantbook\physics\physics1.tex'
$b=[IO.File]::ReadAllBytes($p)
[pscustomobject]@{
  Bytes=$b.Length
  Lines=(Get-Content -Encoding UTF8 -LiteralPath $p).Count
  Sha256=(Get-FileHash -Algorithm SHA256 -LiteralPath $p).Hash.ToLowerInvariant()
}
```

```text
Bytes  : 359087
Lines  : 4685
Sha256 : 41a3720133f7ae54731f3a6dea71071fe87dbddea21667819077e16502c3a8ca
```

## Prepare

```powershell
python 'C:\Users\Lenovo\.codex\skills\humanize-academic-chinese\scripts\prepare_humanize_long_document.py' `
  'D:\code LateX\elegantbook\physics\physics1.tex' `
  --output 'D:\code LateX\elegantbook\physics\build\maturity-v21-20260717\postfix-structural-blind\run' `
  --scene COURSE --intensity STRUCTURAL
```

```json
{
  "budgets": {"max_author_chars": 7000, "max_lines": 600, "min_author_chars": 1200},
  "files_total": 1,
  "intensity": "STRUCTURAL",
  "no_editable_scope": false,
  "processable_editable_units": 50,
  "protected_spans_total": 3164,
  "scene": "COURSE",
  "snapshot_id": "86560cfc8ac43bc9",
  "status": "READY",
  "unit_statuses": {"PENDING": 50, "SKIPPED_PROTECTED": 10},
  "units_total": 60,
  "voice_profile_sha256": "e8271e953d604cab9c4b4c0b6dd670d69145c0e44ee46c1ea5d40410903ce16c"
}
```

The complete prepare artifacts are in `run/`, especially `run_metadata.json`,
`snapshot.json`, `units.jsonl`, `coverage_ledger.csv`,
`protected_spans.jsonl`, `chunks/`, and `prepare_integrity.json`.

## Selection and scan

The prepared inventory was parsed with `ConvertFrom-Json`. Only four units had
contiguous runs of at least two movable paragraphs. The chosen unit was the
only one where the run reached the end of the unit, so merging it did not shift
a later locked paragraph:

```text
unit_id        heading_path               movable run
U-b325e0f1a375 机械波 / 弦振动的简正模式  4-5
```

```powershell
python 'C:\Users\Lenovo\.codex\skills\humanize-academic-chinese\scripts\scan_humanize_chinese.py' `
  '...\run\chunks\U-b325e0f1a375.json' --scene COURSE --format text
```

```text
说明：扫描结果只能作为上下文复核候选。不得输出作者身份、AIGC 分数或任何概率判断。
```

No lexical finding was emitted. The structural diagnosis therefore came from
continuous reading, not from treating a scanner hit as a pathology.

## Rewrite bundle

The exact submitted JSON is `rewrites/U-b325e0f1a375.json`. Its SHA-256 is:

```text
4c8667125cbb80b57f6e35eb6a97c140593f36ebb1ef72a31a3127d320ac694c
```

It maps source paragraphs 1, 2, and 3 unchanged and merges source paragraphs
4 and 5 into target paragraph 4. All protected IDs remain in their original
order.

## Finalize

```powershell
python 'C:\Users\Lenovo\.codex\skills\humanize-academic-chinese\scripts\finalize_humanize_long_document.py' `
  --run-dir '...\postfix-structural-blind\run' `
  --rewrites '...\postfix-structural-blind\rewrites'
```

The complete stdout-equivalent record is `run/finalization_metadata.json`.
Key output from the first run:

```json
{
  "status": "REVIEW",
  "exit_code": 2,
  "structural_changes_applied": 1,
  "structural_plan_results": {"U-b325e0f1a375": "PASS"},
  "structural_semantic_mapping": "NOT_EVALUATED",
  "unit_statuses": {"PENDING": 49, "SKIPPED_PROTECTED": 10, "UNRESOLVED": 1},
  "validation_results": {"U-b325e0f1a375": "REVIEW"},
  "source_files_modified": 0,
  "compile_check": {"status": "NOT_RUN"}
}
```

The selected unit's complete validator output is
`run/validation/U-b325e0f1a375.validation.json`. Its decisive fields are:

```json
{
  "delivery_gate_status": "REVIEW",
  "delivery_gate_exit_code": 2,
  "hard_invariant_layer_status": "PASS",
  "style_signal_layer_status": "PASS",
  "speech_act_layer_status": "REVIEW",
  "review_reasons": ["speech_act_warning"],
  "structural_plan_check": {
    "status": "PASS",
    "source_paragraphs": 5,
    "target_paragraphs": 4,
    "merged_source_paragraphs": 1,
    "semantic_mapping": "NOT_EVALUATED"
  }
}
```

The pending warning was:

```text
SPEECH_ACT_MODALITY_SCOPE_CHANGED
before: 可=1, 应=1, 必须=3
after:  可=1, 应=1, 必须=2
warning fingerprint: 9e95973a4135c5311981634f8e30daa4dbc050e0a7394db375260671fa661c07
request SHA-256: 1f2f83eef512044b811d5127be6ea713565ba74896cfce20898e27a55676df03
```

No proposal or reviewer metadata was submitted.

## Idempotent replay

The same finalizer command was replayed with `$LASTEXITCODE` captured:

```text
assembly_replay_idempotency=PASS
status=REVIEW
CAPTURED_EXIT_CODE=2
```

This is same-bundle assembly replay only; fresh second-pass convergence was
`NOT_RUN`.

## Post-finalize checks

```powershell
python '...\scan_humanize_chinese.py' `
  '...\run\validation\U-b325e0f1a375.after.tex' --scene COURSE --format text
```

No lexical finding was emitted.

```text
hard_invariant_layer_status : PASS
style_signal_layer_status   : PASS
speech_act_layer_status     : REVIEW
plan_status                 : PASS
merged_source_paragraphs    : 1
semantic_mapping            : NOT_EVALUATED
assembly_replay_idempotency : PASS
source_files_modified       : 0
compile_check               : NOT_RUN
```

Final source check:

```text
CurrentSha256  : 41a3720133f7ae54731f3a6dea71071fe87dbddea21667819077e16502c3a8ca
ExpectedSha256 : 41a3720133f7ae54731f3a6dea71071fe87dbddea21667819077e16502c3a8ca
Unchanged      : True
```

`run/rendered_partial/physics1.tex` has the same SHA-256 as the source, proving
the rejected candidate was not published.
