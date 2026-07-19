# Coverage-aware short PATCH review

## Scope and configuration

- Source: `tests/fixtures/humanize_forward_v10/course_before.tex`
- Source SHA-256: `9805eab8480836f942078c112dfcd4160c293cd18bfd79ae0e308c02db956b65`
- `mode=REWRITE`
- `scene=COURSE`
- `intensity=BALANCED`
- `requested_output=PATCH; effective_output=PATCH`
- `voice_profile=NONE; voice_disclosure=SCENE_DEFAULT`
- `report_context=NONE`
- `source_kind=DOCUMENT`
- Selection schema: `humanize-short-patch-selection/v2`
- Emitted bundle schema: `humanize-short-patch/v2`

No Skill file or source fixture was edited. The verifier's live-source comparison returned `MATCH` for the source SHA above.

## Commands and statuses

1. Source audit scan

   ```powershell
   python C:\Users\Lenovo\.codex\skills\humanize-academic-chinese\scripts\scan_humanize_chinese.py tests\fixtures\humanize_forward_v10\course_before.tex --scene COURSE --include-protected --include-excluded --format json
   ```

   Status: scanner coverage `PASS`; process exit `0`; high findings `4`.

2. Build source-bound v2 bundle

   ```powershell
   python C:\Users\Lenovo\.codex\skills\humanize-academic-chinese\scripts\build_humanize_short_patch.py tests\fixtures\humanize_forward_v10\course_before.tex --selection-spec build\maturity-v37-coverage-fresh-20260719\selection.json --output build\maturity-v37-coverage-fresh-20260719\patch.bundle.json --format json
   ```

   Status: `BUNDLED`; process exit `0`; hunks `5`; partition `NON_OVERLAPPING`.

3. Apply bundle

   ```powershell
   python C:\Users\Lenovo\.codex\skills\humanize-academic-chinese\scripts\apply_humanize_short_patch.py tests\fixtures\humanize_forward_v10\course_before.tex --bundle build\maturity-v37-coverage-fresh-20260719\patch.bundle.json --output build\maturity-v37-coverage-fresh-20260719\short-patch-review --format json
   ```

   Status: `DELIVERY REVIEW`; applicator/result exit `2`; patch application `PASS`; structural validation `PASS`; coverage `PASS`; unified validator `REVIEW/2`; unresolved hunks `2`. The surrounding command runner rendered the intentional nonzero review exit as a generic command failure and displayed exit `1`; the applicator JSON and archived `result.json` both record the contract exit `2`.

4. Verify closed record, current policy, and live source

   ```powershell
   python C:\Users\Lenovo\.codex\skills\humanize-academic-chinese\scripts\verify_humanize_short_patch.py build\maturity-v37-coverage-fresh-20260719\short-patch-review --live-source tests\fixtures\humanize_forward_v10\course_before.tex --format json
   ```

   Status: verifier `PASS`; process exit `0`; record integrity `PASS`; coverage policy `PASS`; coverage replay `PASS`; current-policy replay `PASS`; current policy `MATCH`; live source `MATCH`. Candidate delivery remains `REVIEW/2`.

5. Candidate audit rescan

   ```powershell
   python C:\Users\Lenovo\.codex\skills\humanize-academic-chinese\scripts\scan_humanize_chinese.py build\maturity-v37-coverage-fresh-20260719\short-patch-review\candidate.review.tex --scene COURSE --include-protected --include-excluded --format json
   ```

   Status: scanner coverage `PASS`; process exit `0`; findings `0`; candidates `0`.

## Coverage inventory

| Inventory | Count / disposition |
|---|---:|
| lexical high | 4 |
| lexical candidate | 4 |
| lexical protected | 0 |
| lexical excluded | 0 |
| lexical KEEP declarations | 0 |
| lexical `DELETE_STYLE_SHELL` dispositions | 4 |
| selected spans | 5 |
| patch hunks | 5: 3 delete, 2 unresolved |
| explicit conflict pairs | 1: `UNRESOLVED_PAIR` |

The four high findings are `LEX-EMPH-01 -> H001`, `LEX-COACH-01 -> H002`, and `LEX-MARKET-01` plus `LEX-FOUNDATION-01 -> H004`. Coverage scope is only `ENUMERATED_HIGH_AND_BOUND_DECLARATIONS_ONLY`; semantic completeness is false.

## Unresolved source claims

- `H003`: `若已知速度随时间减小，就可以直接套用匀变速公式。`
- `H005`: `先确认题目给出的量是否满足匀变速条件，再判断公式中的加速度方向；若条件不满足，不能因为公式看起来相似就直接代入。`

They are bound as `C001 / OPPOSING_PERMISSION` and copied byte-for-byte into the candidate. No academic correctness decision was made.

## Validation limits

- Hard invariant layer: `PASS`.
- Style signal layer: `PASS`; before high candidates `4`, after candidates `0`.
- Speech-act layer: `REVIEW` because deleting the memory-command shell removes one `必须` marker (`SPEECH_ACT_MODALITY_SCOPE_CHANGED`).
- Paired-quality status: `BLOCKED_BY_MECHANICAL_GATE`.
- `semantic_judgment=NOT_EVALUATED`; `academic_correctness=NOT_EVALUATED`.
- `humanize_quality_claim_allowed=false`; no completion claim is made.

## Usability problems observed

1. Build stdout reports `schema_version=humanize-short-patch/v1`, while the emitted bundle file is correctly `humanize-short-patch/v2`. This makes console-only audit reporting ambiguous.
2. The intentional applicator `REVIEW/2` is surfaced by the surrounding command runner as a generic failure with exit `1`, even though stdout and `result.json` record exit `2`. Callers must parse the structured result instead of trusting the wrapper label.
3. `patch.diff` shows only changed bytes, so the two unchanged `UNRESOLVED` hunks are invisible there. A reviewer must cross-reference `patch.bundle.json` or `coverage.json` to discover the conflict pair.
4. Selection v2 repeats exact span text and reasons in both `hunks` and `coverage.selected_spans`. This is mechanically strict but creates avoidable duplication and mismatch risk for manual authors.
5. The course rule explicitly permits deleting a pure memory-command shell, but the generic modality invariant still places the candidate in speech-act `REVIEW`. The status is conservative and correct by contract, but the result does not distinguish sanctioned style-shell modal deletion from other modality loss.
