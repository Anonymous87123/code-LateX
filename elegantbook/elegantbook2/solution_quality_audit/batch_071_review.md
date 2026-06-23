# Batch 071 Review: Global Solutions #911-915

Scope: `elegantbook2.tex` global solutions #911-915, PDF pages 633-634.

## Changes Made

- #911: Moved the core comparison inequality into a display block:
  \(\sqrt{a_n}/n\le a_n/2+1/(2n^2)\).
  This removes the long inline proof line and makes the comparison-test structure explicit.
- #912: Corrected the answer from B to C. The previous solution counted \(C_1^2+C_2\) in option B as two constants, but it collapses to one effective arbitrary constant.
- #912: Rewrote the option analysis by effective independent constants: A has one effective constant, B has one, D has three, and C can be written as \(y=Ae^{kx}\) with two independent constants.
- #913: Moved the chain-rule formula for \(\varphi'(t)\) into a display block because it is the main derivation skeleton and was visually too long in the paragraph.

## No-Edit Decisions

- #914: Rechecked the change of order of integration. The region splits into \(-1\le x\le0,\ -x\le y\le1\) and \(0\le x\le1,\ 1-\sqrt{1-x^2}\le y\le1\), so A is correct. The displayed final integral is structural and should remain displayed.
- #915: Rechecked the right-semicircle parametrization \(x=a\cos t,\ y=a\sin t\), \(-\pi/2\le t\le\pi/2\), with \(\mathrm ds=a\,\mathrm dt\). The integral is \(2a^2\), so B is correct. The displayed integral setup is structural and should remain displayed.

## Self-Check

- Correctness: #912 had a real answer error and is now corrected to C. #911, #913, #914, and #915 were recalculated and remain mathematically correct.
- Completeness: #911 now shows the comparison inequality before invoking the comparison test; #912 now explains why the apparent constants in B are not independent; #913 shows the full chain-rule step before substitution.
- Method consistency: #911 uses the standard AM-GM/comparison-test proof; #912 follows the multiple-choice screening by effective arbitrary constants; #913 follows the multivariable chain rule; #914 uses geometric region splitting; #915 uses the first-kind curve-integral parametrization.
- Formula layout: Displays were added only for central derivation skeletons. Short substitutions and final choices remain inline.

## Verification

- Rebuilt `solution_quality_audit/solution_index.csv`; total solutions remain 1322 and total auto-flagged count is 1086.
- Batch index after edits: #911-#915 all have `inline_long_count = 0`.
- `latexmk -xelatex -interaction=nonstopmode -halt-on-error elegantbook2.tex` completed successfully.
- Log scan for `Overfull \hbox`, `Underfull \hbox`, LaTeX/package warnings, undefined control sequences, fatal errors, and `!` errors returned no matches.
- `pdfinfo` page count remains 741.
- Rendered and visually inspected pages 633-634 at 180 dpi; no crowding, overlap, clipped text, or inappropriate formula promotion/compression found.
