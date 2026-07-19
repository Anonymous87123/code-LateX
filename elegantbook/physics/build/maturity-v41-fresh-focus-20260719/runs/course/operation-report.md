# Course short-patch operation report

## 1. Scope and configuration

- Source: `fixtures/course.tex` (read only; not modified)
- Source size: 971 bytes, 7 content lines plus a final newline
- Source SHA-256: `5ae03ae68826d5d93c2cf4e3135ce55607c16bc0946af08f2e8eb97e6b6261cd`
- Mode: `REWRITE`
- Scene: `COURSE`
- Intensity: `LIGHT`
- Requested/effective output: `PATCH` / `PATCH`
- Source kind / document format: `DOCUMENT` / `TEX`
- Voice: `voice_profile=NONE; voice_disclosure=SCENE_DEFAULT`
- Report context: `NONE`
- Corpus action support: `NONE`
- Locked scope: formulas, TeX commands, definitions, terminology, numbers, modalities, and physics claims were outside the editable prose surface.
- Explicit protected terms: `质点的瞬时角动量表达式`, `质点的角动量定理（微分形式）`, `角动量定理的冲量矩形式`, `质点系的总角动量`.

The source decoded as strict UTF-8 on the first read. No garbled-text retry or skip was needed.

## 2. Actual execution

1. Read the current Skill instructions and only the directly required `REWRITE`, `COURSE`, `LIGHT`, predicate-source, style-gate, quick-checklist, and short-patch workflow references.
2. Read the designated source continuously. The AUTO lexical scan returned zero high findings. Continuous reading identified three local, out-of-lexicon prose issues: an opening presenter shell, a mechanical integration-operation phrase, and a reader-facing system-introduction phrase.
3. Created `focus.json` with three exact source strings and ran authoring `create` in `FOCUS` mode. All three suggestions were uniquely located and available; none was suppressed by TeX/math protection.
4. Filled three source-bound hunks and three bound selections. The first finalize attempt failed because `intensity` and `protected_terms` had been edited after create, invalidating the authoring inventory hash.
5. Re-created the authoring scaffold with `LIGHT` and all protected terms supplied on the create command line. Finalize, build, and apply then succeeded structurally. The first applied candidate remained mechanically `REVIEW` because H003 removed the condition marker `当`.
6. Re-created the immutable authoring/bundle chain once more and changed H003 from `对于由 ` to `当考察由 `. This preserved the condition marker while removing the reader-facing `面对` phrasing.
7. Applied the final bundle to `candidate-review-retry2/`, ran the unified validator, rescanned the candidate with AUTO, and ran the short-patch verifier with the live source bound.

## 3. Errors, retries, and recovery cost

- Hard tool/contract errors: **1**.
  - `scaffold ... finalize` returned `FAIL: inventory_sha256 mismatch` once.
- Recovery cycles: **2**.
  - Recovery 1: re-created the authoring scaffold with immutable configuration supplied at create time; did not edit or recompute hashes manually.
  - Recovery 2: treated `SPEECH_ACT_CONDITION_CHANGED` as a real semantic-force warning, restored `当`, rebuilt a new bundle, and re-applied; no warning proposal or status override was used.
- UTF-8 retries: **0**.
- Manual byte offsets: **0**.
- FOCUS declarations: **3** exact strings.
- FOCUS create executions: **3** (initial, post-hash recovery, post-warning recovery).
- Final auto-located UTF-8 source starts: `0`, `716`, `848`.
- Suppressed FOCUS spans: **0**.
- Final authoring decisions entered manually: **3 hunks + 3 selected-span reasons**.

Retained failed/superseded evidence is not part of the final candidate chain:

- Hash-mismatch attempt: `selection.authoring.json` (finalize failed before any selection or bundle was published).
- First mechanically reviewed chain: `selection.authoring.retry1.json` -> `selection.v2.json` -> `patch.bundle.json` -> `candidate-review/` (superseded after `SPEECH_ACT_CONDITION_CHANGED`).
- Final chain: `selection.authoring.retry2.json` -> `selection.v2.retry2.json` -> `patch.bundle.retry2.json` -> `candidate-review-retry2/`.

## 4. Final non-overlapping hunks

| Hunk | Source byte range | Decision | Before | After | Predicate-source decision |
|---|---:|---|---|---|---|
| H001 | `[0, 21)` | `DELETE_STYLE_SHELL` | `现在，我们尝试` | empty | Deletes only the presenter shell; the differentiation object and operation remain. |
| H002 | `[716, 749)` | `REWRITE` | `内两边施加定积分，可得` | `内对等式两边积分，可得` | `ENTAILED_PARAPHRASE`; preserves interval, operation target, modality, and result role. |
| H003 | `[848, 861)` | `REWRITE` | `当面对由 ` | `当考察由 ` | `ENTAILED_PARAPHRASE`; preserves the condition marker `当` and the system-introduction role. |

- `patch_hunks_source_partition=NON_OVERLAPPING`
- Unlisted source policy: `COPY_EXACT`
- Unresolved hunks: `0`
- Final candidate SHA-256: `79db57b25d22f3266aa2f2a3236567e2e6b155d871364c4eeaae9f97bc9fe16c`

## 5. Mechanical state

- Candidate assembly: `PASS`
- Structural validation: `PASS`
- Coverage: `PASS`
- Coverage scope: `ENUMERATED_HIGH_AND_BOUND_DECLARATIONS_ONLY`
- Task scene / scan scene / source kind: `COURSE` / `AUTO` / `DOCUMENT`
- Unified mechanical validation: `PASS`
- Hard invariant layer: `PASS`
- Speech-act layer: `PASS`
- Style-signal layer: `PASS`
- Candidate AUTO rescan: zero reported findings, exit `0`
- Source snapshot SHA equals live source SHA: `MATCH`
- Verifier: `INTEGRITY PASS exit=0`, `CURRENT_POLICY_REPLAY PASS`, `COVERAGE PASS`, live source matched
- Delivery gate: `REVIEW`, exit `2`
- Paired-quality review: `PENDING_EXTERNAL_REVIEW`
- Semantic judgment: `NOT_EVALUATED`
- Academic correctness: `NOT_EVALUATED`
- `humanize_quality_claim_allowed=false`

## 6. Delivery boundary

The deliverable is a mechanically validated **review candidate**, not a final or externally cleared rewrite. Coverage PASS is limited to scanner-enumerated high findings (none) plus the three bound FOCUS declarations; it does not prove complete discovery of natural-language issues. The local model cannot grant paired-quality clearance, judge academic correctness, verify the physics, infer authorship, or claim the prose quality is final.

No source file was modified. The review candidate is `candidate-review-retry2/candidate.review.tex`; the exact patch is `candidate-review-retry2/patch.diff`; deterministic review and validation evidence are in the same closed artifact directory. A standalone TeX compile was not run because the fixture is a fragment rather than a complete document; TeX/math/term preservation was checked by the short-patch validator and verifier.
