# v13 real-main regression audit

Date: 2026-07-16

## Scope

- Source: user-supplied, model-generated `main.tex`.
- Source bytes: 54834.
- Source SHA-256: `f97c5dc63e66d094e2ec73fbd2c935393a3370229db1d46baae9772bdacd0625`.
- Snapshot ID: `266e59b6eab82802`.
- Scene: `RESEARCH`.
- Voice: deterministic RESEARCH scene default; personal voice is not claimed.
- Prepared units: 36 total, 28 PENDING, 8 SKIPPED_PROTECTED.

## Evidence status

This is not a new fresh generation. The prose is the unchanged v12h fresh-agent output for
`U-bc353709e690`, rebound only to the v13 chunk and Voice hashes because the new feature-extractor
policy intentionally invalidates old Profile/chunk identities.

- Rebound bundle SHA-256: `50c3381ec0024e1dd4c736b7868b53ae3b26d03b87cf578ff24c670498339745`.
- v13 chunk binding: `5ab49578e80c1cfba7b3585ab60da81c5c3970f8443572819b496c1f266b196d`.
- v13 Voice Profile: `18887ba292c25e48d8f9fc598e1a33fa721d1fa8795b3d78f9964af0773b39e0`.

## Result

- hard invariant layer: PASS;
- document scope: FRAGMENT;
- speech-act layer: REVIEW;
- warning: `SPEECH_ACT_REPORTING_OBSERVATION_CHANGED`;
- style-signal layer: PASS;
- unit: UNRESOLVED;
- overall: REVIEW/2;
- remaining units: 27 PENDING, 1 UNRESOLVED, 8 SKIPPED_PROTECTED;
- full-format errors: 0;
- source files modified: 0.

The new document-level gates do not erase the semantic warning:

- Voice conformance: REVIEW because the editable inventory is incomplete;
- cross-unit repetition: REVIEW/PARTIAL, 0 introduced findings;
- fresh second-pass convergence: NOT_RUN;
- coverage and Humanize completion claims: false.

This run proves that v13 preserves the earlier failure split while adding honest partial-scope
global gates. It does not prove fresh generation quality, full-document Humanize completion, or
E3/E4 isolation.
