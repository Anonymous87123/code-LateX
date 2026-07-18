# Humanize qualification campaign audit

Audit date: 2026-07-14

Scope:

- `humanize-academic-chinese` Skill and its forward-testing contract;
- `audit_humanize_generation_qualification.py` and qualification requirements;
- the qualification manifest fixture and its 17 unit tests;
- existing `humanize_forward_v6` blind-run artifacts.

No production or test file was modified. Everything produced by this audit is under this directory.

## Executive result

The current machine status is correctly `NOT_EVALUATED`: evidence integrity is `PASS`, all 163 required atoms are `NOT_EVALUATED`, and the qualification process exits 2. The manifest fixture is intentionally weak archived E1 evidence and correctly contributes no current coverage.

The harness is a solid artifact-integrity and coverage-accounting layer, but it is not yet sufficient to establish real E3 evidence on its own. Its ordinary behavior assertions are caller-supplied results, its blindness/fresh-context fields are caller attestations, and it has no generator execution provenance or independent assertion-result binding. The harness itself discloses this boundary with `blindness_verified=false`, `run_independence_verified=false`, and `human_identity_verified=false`.

This is not a theoretical distinction. The proof bundle in `proof/self-attested-false-positive/` contains:

- a prompt that requires `DIAGNOSE` with the contract's annotated table;
- an output that is merely the unchanged input and therefore violates `MODE-01`;
- a context artifact that explicitly says `expected_answer_present=true` and `fresh_context=false`;
- a caller-authored run record and a bare `result=PASS` assertion.

The current harness accepts that case as E3 and marks `MODE-01=PASS`, while still leaving the overall qualification `NOT_EVALUATED` because the other 162 atoms are uncovered. See the generated `harness-report.json` and the proof README.

## Snapshot inspected

| Item | SHA-256 |
|---|---|
| Skill snapshot | `c0cb4cc79203d02b066e4309728208e1c72e5d0e854cbf9f43c195f72001e97f` |
| Evaluation contract | `f1d9da16e594e7362bfaf43455463eba1759ef59e0e4e0a2c03da1fc56195e3a` |
| Qualification requirements | `079bb8056b0727dca228f3ebd924dd2d981397450f7ac0673526c58c291c33fe` |
| Qualification harness | `638838946ee3ff7116e25daf75bb9e13c5081ef72a84b534620d6c70fef89f0c` |
| Qualification unit test | `2b4f67d10b41913e910ac38bc9e9d5ccea5ae4917c463bf7e43d8e6f937593c5` |
| Manifest fixture | `6386a3211542bcebc11a2686899f7858eec0366fd79754fcce77bbe809d6431b` |

These hashes describe the audited state only. Any Skill change invalidates the E3 binding and requires a new campaign.

## What works now

- The requirements expand to a non-shrinkable 163-atom matrix and are aligned with contract IDs.
- Artifact paths are confined to `artifact_root`; bytes, size, and SHA-256 are checked.
- The Skill, contract, and requirements are bound to their current hashes and rechecked after the audit.
- Replay rejects arbitrary commands, uses one allowlisted tool, invokes it with `shell=False`, stages copies, and verifies that source and staged artifacts were not changed.
- Validator status, delivery status, process exit code, layer statuses, `academic_correctness`, and before/after hashes are cross-checked.
- Archived evidence and `tests_total` cannot inflate current qualification coverage.
- Idempotency and route-stability measurements bind distinct run-record bytes and concrete artifacts.
- E4 ballots bind rubric, anonymous bundle, and generation output and correctly avoid claiming verified identity.
- Unit verification passed: 17 tests, 0 failures.

## Material gaps

### 1. Behavior PASS is self-declared

`_case_assertions_and_claims` accepts only an assertion ID and a caller-written result. There is no assertion type, oracle hash, evaluator identity/tool hash, output evidence, or assertion-result artifact. `_audit_case` then treats ordinary `behavior` as automatically true. The validator replay confirms only validator behavior, not that a diagnosis has nine columns, a DRAFT used supplied content, a scene route is correct, or a LONG fixture was fully covered.

Relevant implementation points: harness lines 1430-1516, especially 1460; lines 1645-1661, especially `"behavior": True`. The test helper demonstrates the intended current shape at test lines 77-157.

### 2. Blindness is an attestation, not an observed property

The run record is explicitly described as caller-attested at harness line 921. `fresh_context=true` and the fixed attestation string are compared, but context bytes are only required to be non-empty. The harness does not parse a context schema, enumerate reachable files, detect oracle/gold paths, inspect prompt leakage, or prove isolation. Its final trust boundary correctly reports `blindness_verified=false` at line 1939.

### 3. The output is not bound to an actual generator invocation

The run record has no provider/model identifier, API request ID, invocation timestamp, raw response, tool transcript, runner identity/signature, mounted-root inventory, or execution receipt. A complete E3 bundle can be assembled after the fact from arbitrary files. Distinct run IDs and distinct run-record hashes prove distinct JSON bytes, not distinct model executions.

### 4. Replay coverage is narrower than the contract

The only replay tool is `validate_humanize_output`. There is no allowlisted replay for DIAGNOSE schema, DRAFT supplied-content constraints, route observations, output/structure locks, detector-report mapping, Voice Profile behavior, long-document coverage/finalization, or hidden assertions. Expected validator status is itself supplied by the manifest.

### 5. Atom-to-fixture semantics are not validated

A case can claim any atom regardless of its prompt, parameters, scene, variant, or source-role map. A single E3 case can claim many unrelated behavior atoms as long as each has a unique bare assertion. The fixture schema shown in the contract is not enforced by the harness.

### 6. Replication and failure retention are awkward

The harness rejects duplicate coverage of an atom globally. This prevents independent replication claims, and it encourages a manifest assembler to select one attempt. A real campaign therefore needs an external, pre-registered no-cherry-picking ledger; otherwise failed attempts can be omitted while a later passing attempt becomes the sole claim.

### 7. E4 is honest but not identity-verifiable

Two distinct reviewer hashes are required, but both identities and their human status are caller asserted. Ballots contain a single PASS/FAIL result, not per-rubric answers or evidence. The current contract intentionally says identity is unverified, so E4 requires an external coordinator or trust service to be credible.

## Recommended decision

Do not populate a 163-atom PASS manifest by hand. First add an isolated campaign runner, typed hidden assertions, independent assertion-result artifacts, and a preflight verifier/manifest assembler. Until those exist, retain the overall status `NOT_EVALUATED`, even if additional ad hoc forward runs look good.

The practical campaign design is in `campaign-spec.md`; the missing-tool inventory is in `tooling-gaps.md`.

