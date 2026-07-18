# v12h research fresh-forward audit

Date: 2026-07-15

## Scope

- Source: user-supplied, model-generated `main.tex`.
- Source bytes: 54834.
- Source SHA-256: `f97c5dc63e66d094e2ec73fbd2c935393a3370229db1d46baae9772bdacd0625`.
- Snapshot ID: `266e59b6eab82802`.
- Scene: `RESEARCH`.
- Voice: deterministic RESEARCH scene default; no personal-voice claim.
- Prepared units: 36 total, 28 PENDING, 8 SKIPPED_PROTECTED.

## Generator attempts

The first ephemeral CLI attempt failed before generation with HTTP 401 because the machine's
cached API key was invalid. It produced no response file and no rewrite bundle. This is an
infrastructure failure, not a Skill behavior result.

The second ephemeral process used read-only mode and returned exactly one JSON bundle. It was a
fresh process and did not receive expected output or the suspected validation failure. It was not
E3-isolated: the process could still read the host-installed full Skill, so oracle
unreachability was not verified.

- Raw response: `fresh-agent-raw-response.json`.
- Raw response SHA-256: `d80154e784793cf4445d79a23862bf3cf7637600de54e404abc5baa06d1b5e19`.
- Selected unit: `U-bc353709e690`.
- Chunk binding: `05a8f69ced246be04a7115ee5b98839f041dcf639ee43140f9844aa9ac0840ad`.
- Voice profile: `27bc2f98075de1183522db6025dd20899d4fd0a2ab2383887b987a691c08fe78`.
- Decision: `REWRITE`.

The response was copied without semantic or field repair into
`rewrites/U-bc353709e690.json`. The stored file differs from the raw response only by the final
newline produced by the patch writer.

## First finalization

The bundle identity gate passed:

- rewrite bindings matched: 1;
- rewrite bindings mismatched: 0;
- Voice bindings matched: 1.

The unit then failed the hard-invariant layer because both the before and after fragment contained
`begin{document}` without the later chunk's matching end. The failure was a false document-scope
classification, not a generated TeX deletion.

## FRAGMENT correction

The validator now exposes `document_scope=FRAGMENT` for per-unit checks. It allows only identical
pre-existing boundary imbalance. Environment order drift, environment-problem drift, brace-problem
drift, protected-content drift, and all other hard invariants still fail. Accepted units are then
assembled and checked again at full-document scope.

Three regression layers cover this behavior:

- invariant checker: unchanged fragment boundary passes; environment removal fails;
- unified validator: scope is explicit and DRAFT cannot request fragment mode;
- finalizer: a unit containing `begin{document}` but not `end{document}` can pass locally, while the
  assembled full TeX remains balanced.

## Second finalization

Replaying the untouched generated bundle after the correction produced:

- hard invariant layer: PASS;
- protected hashes: PASS;
- document scope: FRAGMENT;
- speech-act layer: REVIEW;
- warning: `SPEECH_ACT_REPORTING_OBSERVATION_CHANGED`;
- unit state: UNRESOLVED;
- overall state: REVIEW/2;
- remaining units: 27 PENDING, 1 UNRESOLVED, 8 SKIPPED_PROTECTED;
- source files modified: 0;
- full format errors: 0;
- Voice conformance: NOT_EVALUATED;
- cross-unit repetition: NOT_EVALUATED;
- fresh second-pass convergence: NOT_RUN.

The correction removed a false structural failure but did not clear the real semantic warning. No
DONE or full-completion claim was manufactured.

## Current release binding

The implementation stabilized after this run as v12h:

- tests: 393, overall OK, skipped 1;
- qualification atoms: 166;
- projection tree: `ad1bf7f3af0e5bf9175b40ac8e05d394be00d95ce531499e85b6889e6e01bbba`;
- qualification: integrity PASS, behavior NOT_EVALUATED, 0/166 PASS, evidence cap E2.

This run is evidence that the current bundle identity contract is generator-usable and that the
failure-state split is meaningful. It is not evidence of full-document Humanize quality or E3/E4
generation qualification.
