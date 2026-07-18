# Practical usability evaluation

## Outcome

The installed workflow returned `REVIEW/2`; this result was preserved. The
rewrite was not forced through with a warning proposal or a fabricated human
approval.

The structural part worked as designed. The plan was byte-bound to the frozen
unit, covered all five source paragraphs exactly once, kept the title locked,
and merged only the adjacent final two `EXPOSITION` paragraphs. The finalizer
reported `structural_plan_check.status=PASS`, one merged source paragraph, and
`structural_semantic_mapping=NOT_EVALUATED`.

The protection layer was also effective. The exact candidate passed hard
invariants: formulas, TeX commands, environments, numbers, and protected spans
were unchanged. The source file itself remained byte-identical to the initial
SHA-256. The same bundle replayed deterministically with
`assembly_replay_idempotency=PASS`.

## Paired quality gate

The source solution has one job: derive the base and harmonic frequencies from
the fixed-end boundary condition and the string wave speed. The candidate
retains that job and the original order of reasoning. It removes the blank
paragraph break between the symbolic relation and numerical substitution,
replaces the stiff passive opening `两端都被固定`, and removes the second causal
restatement after the same condition has already been stated at the start.

That gives a concrete reading benefit: the boundary condition, speed, base
frequency, and harmonics read as one solution rather than two mechanically
separated mini-sections. No new subject, predicate, numerical result, degree,
or use case was introduced. The post-rewrite lexical scan emitted no high-risk
or repair-template finding.

The validator nevertheless flagged the deletion of the repeated final clause
because it reduced the document-wide count of `必须` from 3 to 2. That is a
reasonable fail-closed decision: the tool cannot establish from counts alone
that the removed modal clause is semantically redundant. The warning remains
pending and the selected unit is correctly recorded as `UNRESOLVED`.

## Usability judgment

For auditable TeX preservation and structural authorization, the workflow is
practically strong. It gives reproducible hashes, explicit paragraph mappings,
source-safe partial publication, and a clear separation between mechanical
structure validation and semantic approval.

For a one-section structural rewrite, it is conservative to the point of
requiring human follow-up. A local removal of duplicated teaching prose can be
blocked by a coarse modal-token count even when hard invariants and style
signals pass. This is acceptable for a safety-oriented review pipeline, but it
means the tool should be treated as a candidate generator plus audit gate, not
as an unattended final editor.

The top-level run is also `REVIEW` because only one of 50 editable units was in
scope for this trial; 49 bundles are intentionally missing. That overall
incompleteness is separate from the selected unit's speech-act warning.

Compilation was not requested from the optional finalizer hook and remains
`NOT_RUN`; TeX structural invariants were run. Academic correctness, author
identity, and personal voice conformance remain `NOT_EVALUATED` or not
applicable. `voice=SCENE_DEFAULT` was used, and no claim of reproducing an
individual writing style is made.
