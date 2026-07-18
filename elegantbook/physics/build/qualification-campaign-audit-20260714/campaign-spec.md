# Reproducible E3 campaign specification

## 1. Campaign objective

Collect current-snapshot evidence for all required behavior atoms without exposing fixture-specific expected decisions, pathology IDs, repair strategies, gold text, or hidden assertions to the generator.

Qualification remains fail-closed:

- an infrastructure-invalid run may be repeated only with a recorded invalidation reason;
- a behavior failure is an authoritative campaign failure and is not replaced by a more favorable retry;
- any Skill, contract, requirements, prompt template, runner, or oracle change starts a new campaign ID;
- generated content is never used as a new author sample unless separately supplied and approved by the user;
- `academic_correctness` remains `NOT_EVALUATED`.

## 2. Roles and trust boundaries

| Role | May see | Must not see or do |
|---|---|---|
| Fixture author | contract, source fixture, hidden oracle | run the generator after seeing results |
| Sealer/coordinator | public fixture and oracle | edit either after sealing |
| Generator runner | read-only Skill snapshot and public case package | oracle, gold output, test tree, prior outputs, campaign report |
| Generator | effective system/developer/user context and public mounted files | hidden assertions, atom IDs, expected decisions, evaluator rubric |
| Assertion evaluator | frozen input/output, hidden assertion spec, run binding | alter generator artifacts or infer a missing result |
| Human reviewer | anonymous original/output bundle and rubric | atom ID, generator identity, validator status, expected answer |
| Qualification auditor | all sealed artifacts and derived manifest | treat caller claims as independent evidence |

The generator must run in an OS/container boundary that mounts only the Skill snapshot and one public case. A subagent sharing this workspace is not sufficient: all agents can read the same fixture, gold, test, and report directories.

### Minimum harness-owned runner contract

The smallest useful implementation should make the harness, not the manifest author, own these steps:

1. Accept only a sealed public fixture ID, frozen Skill snapshot, model configuration, and an oracle handle that is not passed to the runner.
2. Create a new empty execution root and a new process/container identity. Mount the Skill and public fixture read-only, provide a separate write-only result directory, and make the workspace, oracle, gold, tests, previous runs, and reports unreachable.
3. Build the effective user prompt from the sealed public template and params. Capture exact system/developer/user bytes, non-input mounts, tool/network policy, model/provider ID, and request ID before accepting output.
4. Invoke the generator once. Capture the provider receipt/raw response and every tool event. The caller may not supply `fresh_context`, `blindness_attestation`, output bytes, or the run record.
5. Freeze input/output/prompt/context/transcript bytes, compute hashes, and emit `run-record.json` itself. Set blindness/freshness from observed isolation state; if isolation cannot be observed, cap the run below E3.
6. Open the oracle only after the run seal exists. Recompute deterministic assertions on staged copies, emit typed assertion-result artifacts, and derive manifest assertion values from those results.
7. Retain every pre-registered attempt in an append-only ledger. Only an objective runner failure may be marked `INFRA_INVALID`; a valid behavioral FAIL cannot be retried away inside the campaign.

Minimum runner receipt fields are: schema version, campaign/case/run IDs, runner executable hash, process/container identity, start/end time, model/provider/deployment and provider request ID, exact input/prompt/context/output hashes, Skill/contract/requirements hashes, mounted and excluded root manifests, network/tool policy, raw-response/transcript hashes, exit/termination status, and run-seal hash.

Independence is an execution property, not distinct JSON. Repeated runs require distinct process/container identities, provider request IDs, and runner receipts. Route-stability runs share exact input/prompt/non-input-context hashes. Idempotency run 2 uses run 1 output as its input while keeping prompt and non-input context identical. The oracle/evaluator process starts only after each generator process has terminated and cannot write generator artifacts.

The harness must recalculate from hidden typed oracle specs: exact/forbidden strings and counts, protected byte spans, headings/paragraphs/TeX structure, scope and lock diffs, validator status/layers/exits/hashes, route observation fields, long-document ledger equations, idempotency chains, and all claim reductions. It must not accept a manifest-authored `assertion.result` for these. Semantic reading-quality assertions may be produced by an independently captured evaluator run, but the harness still recalculates its bindings and reduction. Human taste, voice fidelity, and reviewer identity remain outside deterministic recomputation.

## 3. Artifact layout

```text
campaign-<id>/
  campaign.json
  preregistration.json
  snapshots/
    skill-snapshot.json
    runner-snapshot.json
    evaluator-snapshot.json
  fixtures/
    <case-id>/
      public/
        input.<ext>
        prompt.txt
        params.json
        locks.json
        public-manifest.json
      oracle/
        assertions.json
        oracle-manifest.json
      seal.json
  runs/
    <case-id>/
      attempt-001/
        request/
          prompt.txt
          input.<ext>
          context.json
          mounted-files.json
        response/
          raw-response.json
          output.<ext>
        transcript/
          events.jsonl
          tool-calls.jsonl
          stdout-stderr.jsonl
        checks/
          validator.json
          validator.exit-code.txt
          scanner-before.json
          scanner-after.json
        run-record.json
        run-seal.json
  evaluations/
    <case-id>/attempt-001/
      assertion-results.json
      evaluator-run-record.json
      evidence/
  reviews/
    <review-id>/
      rubric.md
      anonymous-bundle.json
      ballots/
      review-seal.json
  ledger/
    attempts.jsonl
    invalidations.jsonl
    selected-runs.json
  manifests/
    qualification-manifest.json
    manifest-derivation.json
  reports/
    preflight.json
    qualification.json
```

`oracle/` is stored outside every generator-visible mount during execution. Archiving it next to the public fixture is allowed only after the run has been sealed, or inside storage to which the runner identity has no read access.

## 4. Public prompt and context

The public prompt contains only the natural task, exact configuration, user locks, input location, and required delivery target. It must not contain:

- contract atom IDs such as `MODE-01` or `PATH-08`;
- pathology names chosen by the fixture author;
- expected decisions (`KEEP`, `DELETE`, `UNRESOLVED`) unless they are the user's actual request;
- repair instructions tailored to the hidden oracle;
- gold snippets, gold paths, assertion text, scoring thresholds, or prior-run feedback.

The exact effective prompt is stored byte-for-byte. Input is a separate artifact rather than pasted into the prompt so idempotency can reuse the same prompt hash.

`context.json` must be generated by the isolated runner, not authored by the case writer. It records:

- schema/capture version, runner hash, model/provider/deployment ID, request ID, and timestamps;
- exact system and developer messages, or access-controlled archived bytes plus their hashes;
- working directory, tool capability list, network policy, and environment allowlist;
- all non-input mounted roots, read-only flags, and Merkle/file manifests;
- an explicit list of roots not mounted, including oracle, tests, gold outputs, and previous runs;
- Skill snapshot hash and campaign ID;
- whether any prior conversation or persistent memory was supplied;
- the externally observed process/agent identity that received the staged context.

The input hash remains separately bound by the run record. The context artifact should describe the non-input execution environment so first and second idempotency runs can legitimately share the same context hash.

The complete raw response and tool transcript are retained. A markdown run summary is never a substitute for them.

## 5. Fixture authoring and sealing

1. Expand the 163 required atoms from the requirements file.
2. Pre-register each atom's fixture, assertion IDs, severity, run count, and reviewer requirement.
3. Author public input and prompt without a gold output.
4. Author hidden, typed assertions in a separate root.
5. Run a leakage linter over the public package against the oracle and contract IDs.
6. Have a second author review the public/oracle separation.
7. Seal public and oracle manifests independently; then seal their pair in `seal.json`.
8. Freeze the Skill, runner, evaluator, and prompt-template hashes before the first model invocation.

The leakage linter can catch exact/near-exact strings, IDs, paths, and serialized expected values. It cannot prove that a natural-language prompt contains no semantic hint, so the second-author review remains required.

## 6. Typed independent assertions

The source oracle must describe executable assertions; it must never contain a bare final `result` field. Example assertion classes:

| Class | Suitable checks |
|---|---|
| `enum` | route, mode, decision, status, output type |
| `exact_bytes` | quotes, formulas, code, titles, protected spans |
| `contains` / `excludes` | required information, forbidden boilerplate, leaked metadata |
| `regex_count` | repeated sentence shells, high-risk phrases, table columns |
| `structure` | headings, paragraph movement, section scope, TeX environments |
| `validator` | status/layer/exit mapping and before/after evidence hashes |
| `long_ledger` | unit accounting, pending count, rollback, partial/full claim |
| `route_observation` | scene, roles, decisions, owners across independent runs |
| `idempotency` | second input equals first output and substantive patch is empty |
| `semantic_rubric` | information retention, no new claim, scene voice, natural emphasis |

`assertion-results.json` is emitted only by an evaluator. Every result binds:

- assertion/oracle SHA-256;
- input, output, prompt, context, and run-record SHA-256;
- evaluator tool/model and version hash;
- evaluator prompt/context and raw transcript when an evaluator model is used;
- PASS/FAIL/NOT_EVALUATED plus concrete spans, hashes, fields, or observations;
- timestamp and evaluator execution receipt.

Deterministic checks should decide exact and structural properties. A separate evaluator, blind to the generator identity and without a gold rewrite, may assess bounded semantic rubrics. One evaluator assertion is still not a verified human review and must not be labeled E4.

The current qualification manifest's bare assertion results must be generated from verified result artifacts by the manifest assembler. Hand-written assertion results are forbidden by campaign policy.

## 7. Run protocol

1. The coordinator selects the next pre-registered case without opening its oracle.
2. The sealer copies only `public/` into a new, empty run root.
3. The isolated runner mounts the frozen Skill read-only and makes all other workspace roots unreachable.
4. The runner captures effective prompt/context before model execution and seals those bytes.
5. The generator executes once. All file reads, writes, tool calls, stdout/stderr, and raw response events are captured.
6. The runner freezes the output and emits a run record bound to all artifacts and current qualification hashes.
7. The evaluator receives the sealed run and hidden oracle only after generation ends.
8. Deterministic replay and typed assertions run on staged copies.
9. The evaluator seals assertion results. It cannot edit the output or caller-write a PASS.
10. The ledger marks the attempt `VALID_PASS`, `VALID_FAIL`, or `INFRA_INVALID`.

Only `INFRA_INVALID` may be repeated in the same campaign. The invalidation record must predate the replacement run and name an objective infrastructure failure. `VALID_FAIL` stays authoritative.

## 8. Campaign sizing

A conservative campaign can use 77 primary fixtures:

- 48 pathology fixtures: 16 pathologies times positive/negative/conflict;
- 10 Voice Profile fixtures;
- 13 long-document fixtures;
- 6 report-informed adversarial fixtures.

Assign MODE, INT, OUT, DEC, ROUTE, ROLE, and the 12 scene/variant atoms to these fixtures only when the public task actually exercises that behavior and the hidden oracle has an atom-specific assertion. A coverage planner must reject unrelated co-claims.

Additional invocations:

- select 3 primary fixtures per scene for the 12 idempotency atoms, then run each output once more with the exact same generic prompt and non-input context: 12 more invocations;
- select one primary fixture for route/owner stability and run the identical input/prompt/context twice more: 2 more invocations.

That yields 91 planned generator invocations: 77 primary, 12 idempotency reruns, and 2 extra stability runs. Twelve primary outputs, three per scene, also receive blind review by two distinct human reviewers, producing at least 24 independent ballots for the E4 atoms.

This is a planning baseline, not a reason to force unrelated atoms into one case. If the coverage planner cannot justify an assignment, add a fixture.

## 9. Blind human review

Review bundles contain only the original, candidate, neutral labels, and rubric. They exclude model identity, atom ID, validator output, oracle, and previous ballots. Review order is randomized. Each reviewer answers the six contract questions separately and records short evidence; the ballot reducer applies fail-closed PASS/FAIL.

Reviewers submit independently before any adjudication. A disagreement is not rewritten into consensus; it remains a failed ballot or triggers a separately recorded third review without erasing the first two.

The current local harness cannot verify reviewer identity. A coordinator can retain a private identity ledger and issue stable reviewer hashes, but this remains caller-attested unless an external service signs the ballot with a key inaccessible to the agent.

## 10. Replay and publication

Deterministic replay recreates staged copies and reruns validators/assertions. It verifies old evidence; it does not recreate the original model output. A generator rerun is a new run record because model APIs are not guaranteed deterministic.

Publication sequence:

1. verify campaign seal and no-cherry-picking ledger;
2. replay all deterministic assertion results;
3. verify evaluator and human-review bindings;
4. derive the qualification manifest mechanically;
5. run the current qualification harness against the frozen Skill snapshot;
6. compare the live Skill hash with that snapshot;
7. publish preflight, harness report, failed atoms, uncovered atoms, and trust-boundary fields together.

Until the harness consumes typed assertion-result artifacts itself, the preflight verifier is a mandatory companion gate. A harness `PASS` without a matching preflight report is not self-contained qualification evidence.

## 11. What cannot be automated honestly

- Proof that a caller-attested context was truly the generator's only reachable context, without an external isolation boundary and runner receipt.
- Proof that a reviewer is human or that two reviewer hashes represent two people, without an external identity/trust service.
- Natural rhythm, scene-appropriate formality, author-voice fidelity, and whether a rewrite creates a new rhetorical tic. These require blind human judgment.
- Full semantic equivalence, absence of subtle invented implications, and preservation of claim strength in all Chinese prose. Automated checks can find candidates, not close the question.
- Academic correctness, citation validity, data truth, causal validity, or research quality. These remain outside the Skill.
- Exact replay of a nondeterministic model generation. Only request/context/capture integrity and downstream deterministic checks are replayable.
- Proof that a fixture author did not encode the answer indirectly in natural wording. Linting helps; independent human review of fixture leakage is still required.
