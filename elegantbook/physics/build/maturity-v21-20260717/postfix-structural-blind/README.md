# STRUCTURAL blind rewrite run

This directory contains a fresh, one-unit blind trial of the installed
`humanize-academic-chinese` workflow against `physics1.tex`.

- Final verdict: `REVIEW` (contract exit code `2`)
- Selected unit: `U-b325e0f1a375`, `机械波 / 弦振动的简正模式`
- Configuration: `REWRITE / COURSE / STRUCTURAL / PATCH / SCENE_DEFAULT / NONE`
- Source role: `TEST_INPUT`; it was not used as positive Voice evidence.
- Structural plan: `PASS`; one adjacent source-paragraph merge was applied to
  the candidate validation artifact.
- Hard invariants: `PASS`; formulas, TeX, numbers, and protected spans were
  preserved.
- Blocking gate: `SPEECH_ACT_MODALITY_SCOPE_CHANGED`; the count of `必须`
  changed from 3 to 2, so the selected unit remained `UNRESOLVED/REVIEW`.
- Structural semantics: `NOT_EVALUATED`.
- Original source modified: no; its SHA-256 remained
  `41a3720133f7ae54731f3a6dea71071fe87dbddea21667819077e16502c3a8ca`.

Key artifacts:

- `input-manifest.json`: test inputs, source role, configuration, and hashes.
- `run/source/F00001.tex`: frozen full source input.
- `run/chunks/U-b325e0f1a375.json`: prepared masked unit input.
- `rewrites/U-b325e0f1a375.json`: submitted strict rewrite bundle.
- `run/validation/U-b325e0f1a375.before.tex`: restored selected input.
- `run/validation/U-b325e0f1a375.after.tex`: rejected candidate output.
- `run/validation/U-b325e0f1a375.validation.json`: complete unit verdict.
- `run/finalization_metadata.json`: complete finalizer verdict.
- `commands-and-outputs.md`: reproducible command record.
- `evaluation.md`: practical usability assessment.

The candidate was not accepted into the published partial document.
`run/rendered_partial/physics1.tex` is byte-identical to the source.
