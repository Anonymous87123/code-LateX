# Deterministic Qualification Oracle Catalog Design

Date: 2026-07-14

Status: design only. No Skill production file was changed.

## Decision

Replace inline `assertions[].result` and caller-owned `replays[].expected` with a
fixture-specific oracle suite selected by stable ID from a catalog shipped inside
the Skill. A manifest supplies artifact references and a suite ID; it never supplies
an expected value, comparison operator, selector, command, regex, or result.

Keep genuinely subjective judgments in a separate review channel. The catalog owns
the rubric and aggregation rule. A model or human supplies bound answers in a hashed
review artifact, and the auditor derives the result. Such reviews remain explicitly
caller-attested unless an external trust service is added later.

The smallest safe manifest claim becomes:

```json
{
  "claim_id": "MODE-02-CLAIM-001",
  "atom_id": "MODE-02",
  "oracle_suite_id": "MODE-02/basic-rewrite/v1"
}
```

There is no assertion result in the manifest.

## Current-state findings

The reviewed implementation is
`scripts/audit_humanize_generation_qualification.py` in the local
`humanize-academic-chinese` Skill.

1. `_case_assertions_and_claims` accepts `assertions[].result` directly from the
   manifest and permits `PASS`, `FAIL`, or `NOT_EVALUATED` (current script lines
   1430-1516).
2. `_audit_case` treats those caller values as qualification facts. An inline
   `FAIL` can fail an atom and an inline `PASS` helps pass it once the evidence level
   is high enough (lines 1653-1686).
3. Deterministic replay is safer, because the tool is allowlisted and run with
   `shell=False`, but `replays[].expected` is also supplied by the manifest. This is
   a second expected-answer input that should move into the catalog.
4. E3 run records bind input, output, prompt, context, the Skill snapshot, contract,
   and requirements. They do not bind a separately identified grader catalog.
5. Existing built-in measurements already demonstrate the right shape:
   idempotency, route stability, protected-span equality, and blind-review ballot
   validation compute or validate outcomes rather than accepting a generic PASS.
6. `generation-qualification-requirements.json` expands to 163 required atoms and
   assigns minimum evidence and severity. The catalog should not duplicate or
   weaken those policies.
7. `evaluation-contract.md` already separates exact, include/exclude, structural,
   and human blind-review assertions. That split is the basis for the check types
   below.
8. The 17 focused unit tests pass, but they encode the vulnerability: the E3 helper
   takes `assertion_result` and tests both PASS and FAIL by changing only that
   manifest field. There is no negative test preventing a caller from claiming PASS.

## Threat model

The design must prevent a manifest author from obtaining a different qualification
result without changing catalog-bound evidence. Specifically, the caller must not
be able to:

- flip an inline result;
- change a replay's expected status or exit code;
- omit a difficult check from a multi-check atom;
- attach a check to a different atom;
- substitute an easier input, prompt, context, rubric, or fixture;
- swap artifact roles;
- inject a command, Python expression, JSONPath expression, regex, or normalizer;
- replay an E3 record created under another catalog version;
- use a subjective review to override a deterministic failure;
- label caller-attested ballots as externally verified human clearance.

The catalog does not solve reviewer honesty or human identity verification. It makes
that residual trust explicit and prevents it from being confused with deterministic
grading.

## Catalog placement and identity

Proposed production path:

```text
references/generation-qualification-oracles.json
```

Rules:

- Qualification mode always loads this exact path under the resolved Skill root.
- A production CLI flag must not replace it with a file from the evidence root.
- Tests may inject an in-memory catalog through a private API, not a public
  qualification CLI option.
- The file uses strict UTF-8 JSON, rejects duplicate keys, and rejects unknown
  fields at every schema object.
- `catalog_version` is SemVer for catalog content. `schema_version` versions the
  grammar and evaluator semantics.
- The catalog records the exact contract and requirements hashes. It does not record
  the Skill snapshot hash, avoiding a self-referential hash cycle.
- The Skill snapshot naturally includes the catalog and catalog-owned fixture files.

## Minimal catalog schema

An illustrative, intentionally partial skeleton is in
`oracle-catalog-v1.example.json` beside this document. It is valid JSON and uses
schema-shaped placeholders, but it is not qualification-ready because it does not
cover all 163 atoms. The normative top-level shape is:

```json
{
  "schema_version": "humanize-generation-oracle-catalog/v1",
  "catalog_version": "1.0.0",
  "grader_engine_version": "1",
  "contract_binding": {
    "version": "2026-07-14",
    "sha256": "<64 lowercase hex>"
  },
  "requirements_binding": {
    "version": "1.1.0",
    "sha256": "<64 lowercase hex>"
  },
  "policy": {
    "unknown_fields": "REJECT",
    "text_encoding": "UTF-8",
    "unicode_normalization": "NONE"
  },
  "checks": [],
  "review_rubrics": [],
  "suites": []
}
```

### Check

```json
{
  "id": "validator/MODE-02/pass/v1",
  "atom_id": "MODE-02",
  "type": "replay_result",
  "source": "validator",
  "configuration": {
    "tool_id": "validate_humanize_output",
    "args": [
      "${ARTIFACT:input}",
      "${ARTIFACT:output}",
      "--scene",
      "RESEARCH",
      "--format",
      "json"
    ],
    "expected": {
      "status": "PASS",
      "delivery_gate_status": "PASS",
      "exit_code": 0,
      "academic_correctness": "NOT_EVALUATED"
    }
  }
}
```

`configuration` is trusted because it is in the Skill catalog. The evidence
manifest cannot override any member.

### Suite

```json
{
  "id": "MODE-02/basic-rewrite/v1",
  "atom_id": "MODE-02",
  "fixture_bindings": {
    "input": {"sha256": "<hash>"},
    "prompt": {"sha256": "<hash>"},
    "context": {"sha256": "<hash>"}
  },
  "required_checks": [
    "validator/MODE-02/pass/v1",
    "text/MODE-02/no-audit-ledger/v1"
  ],
  "required_reviews": []
}
```

Each suite belongs to exactly one qualification atom. The suite, not the caller,
defines the complete required check set. This avoids cherry-picking. Alternative
suites are allowed only when the catalog deliberately registers each as a complete
fixture for the same atom.

`fixture_bindings` must bind every static artifact that gives the check meaning,
normally `input`, `prompt`, and `context`, plus any source-role map, expected
structure annotation, rubric, or anonymous bundle template. `output` and run records
are dynamic, but must be bound by the E3 run record.

### Review rubric

```json
{
  "id": "style/PATH-05/equal-weight/v1",
  "atom_id": "PATH-05/positive",
  "reviewer_kinds": ["MODEL", "HUMAN"],
  "minimum_distinct_reviewers": 1,
  "questions": [
    {
      "id": "paragraphs-not-equal-weight",
      "answer_type": "PASS_FAIL"
    }
  ],
  "aggregation": "ALL_PASS"
}
```

Rubric wording should live in a catalog-owned file referenced by path and hash when
it is long. A rubric entry may contain stable question identifiers and the hash of
that file. The manifest cannot add questions or alter aggregation.

## Manifest v2

Proposed schema:

```text
humanize-generation-qualification-manifest/v2
```

Changes from v1:

- remove `assertions`;
- replace `claim.assertion_ids` with `claim.oracle_suite_id`;
- remove `replays[].expected`, and preferably remove manifest `replays` entirely;
- add optional `reviews`, which only map a catalog rubric ID to a hashed artifact;
- add `oracle_catalog_sha256` to all current bindings.

Example:

```json
{
  "schema_version": "humanize-generation-qualification-manifest/v2",
  "bindings": {
    "skill_snapshot_sha256": "<hash>",
    "contract_sha256": "<hash>",
    "requirements_sha256": "<hash>",
    "oracle_catalog_sha256": "<hash>"
  },
  "cases": [
    {
      "id": "MODE-02-CASE-001",
      "artifacts": {
        "input": {"path": "input.md", "sha256": "<hash>"},
        "output": {"path": "output.md", "sha256": "<hash>"},
        "prompt": {"path": "prompt.txt", "sha256": "<hash>"},
        "context": {"path": "context.json", "sha256": "<hash>"},
        "raw_run": {"path": "raw-run.json", "sha256": "<hash>"}
      },
      "generation": {"...": "existing E3 fields"},
      "claims": [
        {
          "claim_id": "MODE-02-CLAIM-001",
          "atom_id": "MODE-02",
          "oracle_suite_id": "MODE-02/basic-rewrite/v1"
        }
      ]
    }
  ],
  "archived_failures": []
}
```

The auditor expands the suite into check instances. Public results include the
catalog hash, suite ID, canonical suite hash, check ID, status, and non-sensitive
observed values or hashes. They never echo fixture bodies or raw reviewer identity.

## Binding rules

1. Load and validate requirements and contract, then load the fixed catalog path.
2. Verify the catalog's contract and requirements hashes against the current files.
3. Expand requirements to the canonical 163 atoms. Every suite atom must exist and
   its catalog severity/evidence policy, if displayed, must be derived from
   requirements rather than independently configurable.
4. Validate unique check, rubric, and suite IDs. Every check and rubric binds exactly
   one atom, and a suite may reference only entries bound to its atom. IDs are
   immutable within a catalog version. Any semantic check change gets a new ID
   suffix or catalog major version.
5. Verify every suite has at least one required deterministic check or one required
   review. Empty suites are invalid.
6. Verify every required check/review ID exists. A suite may not reference the same
   check twice.
7. Verify every atom has at least one complete suite before the catalog is accepted.
   This is catalog completeness, not evidence coverage.
8. Resolve a claim's suite and require `suite.atom_id == claim.atom_id`.
9. Verify all static fixture artifact bytes against `fixture_bindings`. A copied
   fixture is acceptable only when its bytes match the catalog hash.
10. Artifact roles are canonical. A caller cannot remap `input` to `output` or pass
    selector parameters.
11. Snapshot all case artifacts once before grading, as the current auditor does,
    and recheck path state and bytes before publishing the report.
12. Execute only hardcoded evaluator types. The catalog may configure those builtins;
    neither catalog nor manifest can name import paths, source code, shell commands,
    JSONPath programs, or plugins.
13. Catalog-owned replay arguments still pass through the existing tool allowlist,
    placeholder validation, staged copy, timeout, `shell=False`, and JSON result
    validation.
14. Add `oracle_catalog_sha256` to top-level bindings, case bindings, generation run
    record schema v2, route observations, review artifacts, and report provenance.
15. A run record without the current catalog hash can reach at most archived E1. It
    cannot be upgraded by copying its old outcome into a v2 manifest.
16. Derive a canonical SHA-256 for each suite and check definition. Report those
    hashes so an audit can identify the exact oracle even if display IDs are reused
    accidentally.

## Deterministic check types

Keep v1 deliberately small and parser-backed.

| Type | Purpose | Core operators |
|---|---|---|
| `replay_result` | Run an allowlisted Skill tool and compare machine state | exact status, delivery status, exit code, academic correctness, selected JSON fields |
| `json_value` | Inspect a strict JSON artifact or replay result | `EQUALS`, `IN`, `PRESENT`, `ABSENT`, exact array/set equality, integer count |
| `utf8_literal` | Check exact visible text without caller regex | required/forbidden literal and min/max occurrence count |
| `artifact_relation` | Compare bytes or catalog-owned protected spans | byte equality, span equality, SHA-256 equality, zero changed spans |
| `structure_relation` | Compare parsed Markdown, TeX, paragraph, heading, table, scope, or ledger structure | exact fingerprint, allowed delta, containment within catalog-owned scope |
| `measurement_result` | Consume existing auditor measurements | idempotency true, route fingerprint stable, protected spans unchanged |

Do not add a generic expression evaluator in v1. Regex is also unnecessary in the
manifest. If trusted catalog regex becomes necessary, add a new check type with
explicit engine/version, match limits, and test vectors; do not overload
`utf8_literal`.

Check semantics:

- false expectation: `FAIL`;
- required artifact absent, hash-mismatched, role-swapped, or malformed: evidence
  integrity `FAIL` and claim `NOT_EVALUATED`;
- output fails a required parser because its required format is malformed: check
  `FAIL`;
- unsupported check type or invalid catalog: fatal catalog integrity `FAIL` before
  case grading;
- all deterministic checks pass, but a required review is absent: `NOT_EVALUATED`;
- any deterministic check fails: claim `FAIL`, regardless of review votes;
- all required deterministic checks and reviews pass at the atom's minimum evidence
  level: claim `PASS`.

## Subjective review channel

Subjective review is not represented as a deterministic assertion.

Proposed review artifact schema:

```json
{
  "schema_version": "humanize-generation-oracle-review/v1",
  "review_id": "REVIEW-001",
  "case_id": "PATH-05-CASE-001",
  "suite_id": "PATH-05/positive/v1",
  "rubric_id": "style/PATH-05/equal-weight/v1",
  "reviewer": {
    "kind": "MODEL",
    "id_sha256": "<hash>",
    "identity_verified": false
  },
  "bindings": {
    "input_sha256": "<hash>",
    "output_sha256": "<hash>",
    "generation_run_record_sha256": "<hash>",
    "anonymous_bundle_sha256": "<hash>",
    "rubric_sha256": "<hash>",
    "oracle_catalog_sha256": "<hash>"
  },
  "answers": [
    {"question_id": "paragraphs-not-equal-weight", "answer": "PASS"}
  ]
}
```

Rules:

- Reject inline `overall_result`; the auditor derives it from required question
  answers and catalog aggregation.
- MODEL review requires a distinct review run record, prompt, and context from the
  generation run and an attestation that expected answers were not staged.
- HUMAN review retains the current hashed reviewer identity and duplicate-reviewer
  checks. E4 still requires two distinct HUMAN ballots where requirements demand it.
- Preserve `identity_verified=false` and a caller-attested status for local human
  reviews. This is evidence provenance, not external human clearance.
- A model self-check and a human ballot do not change `academic_correctness`, which
  remains `NOT_EVALUATED`.
- Reviews never clear deterministic invariant, scope, replay, or structure failures.
- Missing review evidence yields `NOT_EVALUATED`, not PASS and not an invented fourth
  overall qualification state.

## Atom-to-check guidance

| Atom family | Primary deterministic checks | Subjective supplement |
|---|---|---|
| `MODE`, `OUT`, `DEC`, `ROUTE` | replay state, JSON values, required/forbidden literals and fields | only when output intent cannot be encoded reliably |
| `INT`, `LONG` | structure relation, scope fingerprint, coverage ledger, replay state | rhythm or responsibility judgments only |
| `ROLE`, `PROTECTED` | byte/span relation and validator replay | none for hard protection |
| `REPORT` | mapping state, script non-execution evidence, literal exclusion, replay state | optional explanation-quality review |
| `IDEMPOTENCY`, `STABILITY` | existing bound multi-run measurements | none |
| `VOICE`, `SCENE`, `PATH` | exact fixture constraints, literal and structure checks | bound model/human rubric for read-feel questions |
| `BLIND_REVIEW` | ballot/rubric/bundle/run binding and reviewer distinctness | the ballot answers themselves |

An atom may require both deterministic and subjective checks. For example, PATH-05
can mechanically enforce paragraph-count and sentence-grid changes while a reviewer
judges whether the output still feels equally weighted. Neither half substitutes for
the other.

## Migration strategy

### Release 1: catalog and shadow mode

1. Add the catalog schema, strict loader, catalog linter, and built-in evaluator
   registry.
2. Add fixture hashes and complete suites for a small vertical slice: one P0 role
   atom, one normal rewrite atom, one PATH atom with subjective review, one LONG atom,
   and all four existing automatic measurement kinds.
3. Run catalog results beside v1 results in tests only. Do not use v1 inline PASS as
   an oracle when comparing results.
4. Update requirements to schema v2 and add `oracle_catalog_sha256` to the fixed
   evidence binding contract.

### Release 2: manifest and run record v2

1. Add manifest v2, generation run record v2, route observation v2, review artifact
   v1, and report v2.
2. Require v2 for every current `cases` entry.
3. Permit v1 only under `archived_failures`; its inline result is displayed as
   historical metadata and never contributes coverage.
4. Reject `assertions`, `result`, manifest replay `expected`, evaluator parameters,
   and public catalog override flags in v2.
5. Re-run all E3/E4 evidence. Old run records cannot be upgraded because they did
   not bind the oracle catalog.

### Release 3: complete matrix and retire v1 qualification

1. Author at least one complete suite for every one of the 163 atoms.
2. Lint that every suite is fixture-bound and every atom is catalog-covered.
3. Convert historical v1 manifests with a mechanical tool that copies IDs and
   artifact descriptors but drops all results and expected values. The converter
   emits unresolved `oracle_suite_id` TODOs; it must never synthesize PASS.
4. Remove v1 from the set of current qualification schemas. Keep a read-only archival
   parser if historical reports must remain inspectable.
5. Publish only when a fresh complete v2 evidence matrix passes.

## Required tests

### Catalog schema and completeness

- reject duplicate JSON keys, unknown fields, unknown check types, unsafe IDs, and
  duplicate IDs;
- reject stale contract/requirements hashes;
- reject unknown atoms, suite/atom mismatch, missing check IDs, duplicate check IDs,
  empty suites, and an atom with no complete suite;
- reject a catalog path outside the fixed Skill location and a symlink escape;
- prove catalog canonical hash changes when any expected value or fixture hash
  changes.

### Manifest trust-boundary regression

- v2 rejects `assertions[].result` and any manifest-owned expected value;
- changing only a legacy result from FAIL to PASS cannot change a v2 outcome;
- unknown suite, atom/suite mismatch, artifact role swap, fixture substitution, and
  manifest evaluator parameters fail;
- caller cannot omit one required check from a suite;
- extra unreferenced review artifacts do not contribute to a claim;
- duplicate atom coverage remains rejected.

### Built-in check behavior

- every check type has PASS, FAIL, malformed-input, missing-input, and boundary tests;
- UTF-8 literals are byte-stable and use no implicit Unicode normalization;
- JSON parsing rejects duplicate keys and non-finite values if the strict parser is
  extended to reject them;
- Markdown and TeX structure checks include protected environments, comments,
  tables, headings, nested spans, and scope boundaries;
- replay tests prove the catalog owns tool ID, args, expected status, and exit code;
- timeout, non-JSON stdout, status/exit mismatch, and tool hash drift fail closed.

### Binding and provenance

- catalog drift invalidates top-level bindings, E3 run records, route observations,
  and reviews;
- input, prompt, context, rubric, bundle, and source annotation substitution fails;
- copied run IDs or run-record hashes do not satisfy independence;
- mutate an artifact during grading and before report publication to verify TOCTOU
  failure;
- report exposes catalog/suite/check hashes without exposing protected content.

### Subjective reviews

- missing required review yields `NOT_EVALUATED`;
- unknown question, missing question, caller-owned overall result, wrong rubric hash,
  wrong output hash, and wrong generation binding fail;
- same model generation and review run is rejected as non-independent;
- duplicate human identity and AGENT-as-HUMAN are rejected;
- two distinct bound human ballots meet E4 provenance while retaining
  `identity_verified=false`;
- a subjective PASS cannot override any deterministic FAIL;
- reviewer disagreement derives FAIL according to `ALL_PASS` and is not rewritten by
  a prose summary.

### Qualification aggregation and compatibility

- P0/P1 failure, incomplete matrix, full pass, evidence integrity failure, archived
  v1 evidence, and no manifest preserve the existing three qualification states and
  exit codes;
- current v1 cases never contribute PASS after the migration boundary;
- complete synthetic matrix tests use catalog-derived results only;
- integration fixtures cover formula mutation (P0 FAIL), safe rewrite (PASS), high
  style warning (review required), route instability (FAIL), and missing subjective
  review (`NOT_EVALUATED`).

## Acceptance criteria

The migration is complete only when all of the following are true:

- no current qualification code reads a caller-supplied generic assertion result;
- no current deterministic replay reads caller-supplied expected machine fields;
- every current claim resolves to a complete, fixture-bound suite in the Skill
  catalog;
- all current run/review/report provenance binds the exact catalog hash;
- subjective review is separate, provenance-labeled, and unable to override hard
  failures;
- old evidence is archived or rerun, never silently upgraded;
- the complete 163-atom qualification result is derived entirely from catalog checks,
  bound reviews, and evidence-level rules.

## Non-goals

- judging facts, citations, calculations, causality, research quality, or authorship;
- predicting or optimizing detector scores;
- introducing an external human identity service;
- accepting arbitrary grader code or manifest expressions;
- requiring one exact golden prose output for generative fixtures.
