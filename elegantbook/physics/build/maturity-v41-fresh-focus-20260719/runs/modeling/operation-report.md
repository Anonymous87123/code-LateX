# Modeling Short-PATCH Operation Report

## Scope and Guardrails

- Source: `fixtures/modeling.tex` (UTF-8, 4214 bytes, SHA-256 `6d1657bb1e296b130a325340728ca9b4ecc8fd574ac1911a0a1d114589d975ad`).
- Source was read only; it was never overwritten. All generated files are under this run directory.
- Configuration: `mode=REWRITE`, `scene=MODELING`, `intensity=BALANCED`, `requested_output=PATCH`, `effective_output=PATCH`, `voice_profile=NONE`, `report_context=NONE`.
- Protected terms passed to the validator: 15. This includes `Hastings-Powell`, `K`, `3.22`, the state classifications, several quoted labels, and the TeX control-delimited K form; the validator separately enforced global direct-quotation invariance.
- No tests, other builds/runs, maturity reports, or expected answers were read.

## Actual Steps

1. Read the complete `humanize-academic-chinese` Skill and the directly required short-PATCH, checklist, and modeling references. The initial console read of the source was mojibake; a strict UTF-8 read succeeded and was used for every subsequent hash/offset.
2. Ran `scan_humanize_chinese.py --scene AUTO --format text`. It reported 3 high candidates: two `LEX-META-01` editing shells and one `LEX-FUTURE-01` future-work shell. The scanner output is archived as `scanner.txt`.
3. Ran the source-bound authoring scaffold (`CLAUSE_AND_SENTENCE`, `DOCUMENT`, `TEX`): `PENDING high=3`, `resolutions=3`, `suggestions=6`, `suppressed=4`. The scaffold is archived as `selection.authoring.json`; it was not treated as quality clearance.
4. Drafted the coverage-aware selection with 8 explicit source spans and 8 non-overlapping hunks, then built successive source-bound bundles.
5. Applied the final bundle with the strict applicator, producing the review candidate and closed evidence set in `short-patch-review-v6`.
6. Ran the verifier with `--live-source fixtures/modeling.tex`: integrity `PASS/0`, current-policy replay `PASS`, live source `MATCH`.

## Failures and Recovery

- Initial builder attempt: `selection spec.hunks[0].start_byte does not match source_text`. Recovery: recomputed all UTF-8 byte starts from the source and rebuilt; the failed diagnostic is retained in `build.log`.
- First apply attempt (`patch.bundle.json`): `UNIFIED_VALIDATOR_FAILED`; diagnostic cause was hard error `DIRECT_QUOTATION_CHANGED` because the proposed deletion removed `“某个点的现象”` and `“一个可复核的区间判断”`. The bounded diagnostic artifacts are `candidate.diagnostic.tex` and `validator-diagnostic.json`. Recovery: changed H007 to retain both quoted phrases and rebuilt (`patch.bundle.v2.json` and later bundles remain archived).
- Second application passed hard invariants but left the high `后续需要进一步` signal and speech-act warnings. Recovery: restored the original conditional/modality markers where possible, removed only the redundant backend shell, and rebuilt through `patch.bundle.v5.json`.
- Final application (`patch.bundle.v5.json`) published `DELIVERY REVIEW exit=2`; no hard error, warning, or unexplained high finding remained.

## Span Registration Cost

- Scanner high inventory: 3.
- Scaffold suggestions: 6 available and 4 suppressed; all suppressed suggestions remained non-editable.
- Explicit final registry/selection: 8 source spans, 8 hunks, 7 `REWRITE` and 1 `UNRESOLVED`; 0 lexical keeps; 0 explicit conflicts.
- Protected-term bindings: 15. Source partition: `NON_OVERLAPPING`; unlisted source policy: `COPY_EXACT`.
- Byte ranges are UTF-8 half-open ranges and were accepted by the builder and applicator.

## Final Hunks

| Hunk | UTF-8 bytes | Decision | Final action |
|---|---:|---|---|
| H001 | 1510--1639 | `REWRITE` | Remove “这样处理的好处是” and state that problem four uses the same parameter axis. |
| H002 | 1639--1771 | `REWRITE` | Remove “对论文写作而言” while retaining “行为分类” and `不必`. |
| H003 | 2842--3019 | `REWRITE` | Turn “正文里既要保留” into the direct relation between coarse/fine scans and interval judgment. |
| H004 | 3138--3384 | `REWRITE` | Remove “参数扫描的写法也要服务于” and retain the original `如果...就可以` modality and quoted interval name. |
| H005 | 3384--3603 | `REWRITE` | Replace the empty指代 “这样的表述” with “这一判定”; sampling dependence and non-absolute threshold remain. |
| H006 | 3603--3753 | `REWRITE` | Remove “也正因为如此”; retain the original `不是...而是` judgment. |
| H007 | 3755--4070 | `REWRITE` | Remove the template close “这样处理后...也更符合...” while retaining `如果需要`/`还可以`, both locked quoted phrases, and the stated repeat-validation relation. |
| H008 | 4072--4213 | `UNRESOLVED` | The conditional graph-display instruction is preserved verbatim because graph delivery is not determined by this source fragment. |

## Final Validation and Delivery Boundary

- Applicator result: `status=REVIEW`, `exit_code=2`, `structural_validation=PASS`, `patch_application=PASS`, `unified_validator=PASS`, `hard_invariant_layer=PASS`, `paired_quality_review_status=PENDING_EXTERNAL_REVIEW`, `coverage_status=PASS`.
- Verifier: `INTEGRITY PASS exit=0 scope=SELF_CONSISTENCY_ONLY; CURRENT_POLICY_REPLAY PASS; COVERAGE PASS; DELIVERY REVIEW`.
- `UNRESOLVED`: H008 only. It is not silently treated as edited or complete.
- `semantic_judgment=NOT_EVALUATED`, `academic_correctness=NOT_EVALUATED`, `humanize_quality_claim_allowed=false`, and `completion_claim_allowed=false`.
- Mechanical PASS is not a claim about style quality, model correctness, numerical validity, author identity, detector outcomes, or generation eligibility. External paired-quality review is still required.

## Final Artifact Set

The final candidate and closed evidence set are in `short-patch-review-v6/`: `candidate.review.tex`, `review.md`, `patch.diff`, `patch.bundle.json`, `coverage.json`, `source.snapshot.bin`, `validation.json`, `result.json`, and `evidence-manifest.json`. Earlier failed/recovered logs and bundles remain in this run directory and are not overwritten.
