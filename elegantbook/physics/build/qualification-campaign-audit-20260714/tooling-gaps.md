# Missing authoring and validation tools

## Required before a real E3 campaign

| Priority | Proposed tool | Required behavior |
|---|---|---|
| P0 | `plan_generation_qualification_campaign.py` | Expand the fixed 163 atoms, allocate them to fixtures, enforce required variants/run counts/review counts, and reject unrelated or duplicate assignments. |
| P0 | `lint_and_seal_qualification_fixture.py` | Validate the contract fixture schema, split public/oracle roots, scan public bytes for atom IDs, expected values, gold overlap and oracle paths, then emit independent manifests and a pair seal. |
| P0 | `run_blind_forward.py` | Launch a clean isolated runner with only the public case and read-only Skill snapshot; capture effective prompt/context, reachable-file inventory, model request/response, tool events, output, and an externally observed execution receipt. |
| P0 | `evaluate_qualification_assertions.py` | Execute typed hidden assertions, bind results to oracle/run/input/output/prompt/context hashes, retain concrete evidence, and forbid a source oracle from supplying its own final result. |
| P0 | `verify_qualification_campaign.py` | Verify seals, isolation receipts, assertion provenance, evaluator independence, no-cherry-picking ledger, atom-to-fixture compatibility, and all current bindings before the existing harness runs. |
| P0 | `assemble_qualification_manifest.py` | Derive manifest assertions/claims from verified result artifacts; never accept hand-authored `result=PASS`; emit a derivation ledger. |

The most important production change is to make the existing harness consume and validate assertion-result artifacts directly. A companion preflight tool is useful during migration, but two independent gates create drift risk.

## Contract-specific validators currently missing

| Priority | Validator | Gap closed |
|---|---|---|
| P1 | `validate_diagnose_contract.py` | Exact nine-column schema/order, no rewritten body, no false completion statement, ranked findings. |
| P1 | `validate_output_contract.py` | CLEAN/ANNOTATED/PATCH required and forbidden fields, scope disclosure, default voice disclosure. |
| P1 | `validate_draft_supply.py` | DRAFT output traceability to supplied content and explicit placeholders without invented completion. |
| P1 | `validate_structure_scope.py` | LIGHT/BALANCED/STRUCTURAL paragraph, heading, section, title and scope constraints. |
| P1 | `extract_route_observation.py` | Deterministic scene/role/decision/owner observation bound to the run, with schema validation. |
| P1 | `validate_report_informed_case.py` | Unique/duplicate/unmappable/score-only/malicious/mixed-evasion behavior without executing report content. |
| P1 | `validate_long_qualification_case.py` | Prepare/finalize manifest, unit accounting, protected hashes, rollback, partial/full claim, and compile status for LONG atoms. |
| P1 | `validate_voice_profile_case.py` | Sample length/scene separation/protected-span exclusion/default disclosure; leave perceptual fidelity to blind review. |
| P1 | `validate_no_new_information.py` | Candidate detector for new numbers, named entities, citations, conditions, modal/negation changes, and unsourced attribution. It must return REVIEW for semantic uncertainty. |

## Replay and review utilities

| Priority | Tool | Required behavior |
|---|---|---|
| P1 | `replay_qualification_case.py` | Recreate staged copies and rerun an allowlist of deterministic validators/assertion evaluators; verify source immutability and exact result binding. |
| P1 | `make_blind_review_bundle.py` | Produce randomized anonymous original/output bundles that exclude model identity, atom IDs, validator status, oracle, and expected answer. |
| P1 | `collect_blind_review_ballot.py` | Capture per-rubric answers, evidence, reviewer hash, timestamps, bundle/rubric/run bindings, and optional external signature. |
| P1 | `verify_context_capture.py` | Validate context schema, mounted-root inventory, excluded roots, effective messages, tool/network policy, runner receipt, and prompt/input separation. |
| P1 | `scan_qualification_secrets.py` | Detect credentials/PII before prompt/context/transcript artifacts are published; preserve original hashes in restricted storage. |
| P2 | `qualification_campaign_report.py` | Summarize 163 atoms, attempts, invalidations, failures, evidence levels, blind ballots, and snapshot drift without trusting declared test counts. |

## Existing tools that can be reused

- `validate_humanize_output.py`: validator replay and hard/speech/style layer mapping.
- `scan_humanize_chinese.py`: lexical candidate evidence, never a complete behavioral oracle.
- `extract_detector_report_scope.py`: report mapping cases.
- `prepare_humanize_long_document.py` and `finalize_humanize_long_document.py`: long-document state and integrity evidence.
- `build_humanize_action_profile.py` and `validate_humanize_candidate_queue.py`: source-action and candidate-queue cases where relevant.
- `audit_humanize_generation_qualification.py`: final current-binding, evidence-level, atom-coverage, replay-integrity, and qualification aggregation layer.

The qualification harness currently allowlists only `validate_humanize_output.py`. Adding other replays requires fixed positional artifact roles, strict option allowlists, staged copies, `shell=False`, bounded time/output, and before/after source hash checks matching the existing safety model.

## Tests missing from the current harness suite

- A context artifact that explicitly contains a gold answer must not reach E3.
- `fresh_context=true` in a run record must not override contradictory runner-observed context.
- A bare caller assertion must not qualify a behavior atom.
- An assertion result must fail when its oracle, evaluator, output, or run-record hash drifts.
- A MODE/PATH/SCENE atom must reject a fixture whose typed metadata and assertion family do not exercise that atom.
- A generator output assembled without a runner execution receipt must not reach E3.
- Multiple independent evidence items for one atom must be supported without allowing cherry-picking or overwriting failures.
- DIAGNOSE, DRAFT, ROUTE, REPORT, VOICE, and LONG cases must use matching replay/evaluator tools rather than the rewrite validator as a universal proxy.
- Reviewer ballots must include bound rubric-item answers, not only a final PASS/FAIL.
- An isolated-run integration test must prove test/gold/oracle paths are unreadable from the generator process.

