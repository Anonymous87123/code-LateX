# Batch 150 Review: solutions #1311-1315

## Scope

- Global solution numbers: #1311-#1315
- Source ranges after index rebuild:
  - #1311: lines 49926-49930
  - #1312: lines 49946-49951
  - #1313: lines 49964-49969
  - #1314: lines 49979-49987
  - #1315: lines 50000-50017

## Changes Made

- #1311: added the missing endpoint-radius reasoning. Conditional convergence at \(x=-3\) means the point is on the boundary of the convergence interval, so the radius cannot exceed \(3\).
- #1312: clarified that the sine series represents the odd extension of \(f(x)=x^2\) with period \(2\), so the value at \(-1/2\) follows directly from the odd-extension value rather than from recomputing \(b_n\).
- #1313: expanded the ODE step by setting \(u=\sin^2y\), reducing the equation to \(xu'+u=\sin x\), and using \((xu)'=\sin x\).
- #1314: made the symmetry, area, surface element, moment integral, and \(\bar z\) evaluation explicit.
- #1315: separated the exact differential part from the remaining integral, stated the endpoint contribution, introduced the upper semicircle parameterization, and kept the long substitution computation as an aligned display.

## Formula Layout Decisions

- #1311: all formulas are short radius/endpoint statements and remain inline.
- #1312: \(S(-1/2)=-f(1/2)=-1/4\) is a short local conclusion and remains inline.
- #1313: the substitutions \(u=\sin^2y\), \(xu'+u=\sin x\), and \((xu)'=\sin x\) are short and remain inline.
- #1314: the moment integral \(N\) was kept inline because the rendered line stays within the text width and the chain is below the long-inline threshold; no short display is introduced.
- #1315: the final integral evaluation is genuinely long and central, so it remains in an aligned display. The displayed block is not a short formula and does not create visual crowding.

## Per-Solution Review

- #1311: correct. Since the series is conditionally convergent at \(x=-3\), \(R\ge3\); if \(R>3\), then \(|x|=3\) would be inside the convergence interval and the convergence would be absolute, contradiction. Hence \(R=3\).
- #1312: correct. The sine series is the Fourier sine expansion, i.e. the odd periodic extension on period \(2\). At the continuous point \(-1/2\), the sum equals \(-f(1/2)=-1/4\).
- #1313: correct. The substitution \(u=\sin^2y\) gives \(u'=\sin(2y)y'\), so the equation becomes \((xu)'=\sin x\), yielding \(x\sin^2y+\cos x=C\).
- #1314: correct. For the upper hemisphere, \(\bar x=\bar y=0\), \(S=2\pi a^2\), and \(N=\pi a^3\), so \(\bar z=a/2\).
- #1315: correct. The exact differential \(\mathrm d(e^x\sin y)\) contributes \(0\) at both endpoints. The remaining parameter integral over the upper semicircle gives \(9\pi a^4/64\).

## Verification

- Rebuilt index: `python solution_quality_audit\build_solution_index.py`
  - `total_solutions`: 1322
  - `auto_flagged`: 1068
  - `long_inline_flagged`: 80
  - `jump_keyword_flagged`: 548
  - `short_display_flagged`: 885
- Batch index check:
  - #1311, #1312, and #1313 remain `AUTO_FLAGGED_NEEDS_MANUAL` only because the heuristic marks them as short; manual review confirms the essential reasoning is now present.
  - #1314 is `AUTO_INDEXED_NO_HEURISTIC_FLAG`.
  - #1315 is `AUTO_INDEXED_NO_HEURISTIC_FLAG` with one necessary long display.
- Batch solution-line check: no source line of length `>=150` inside the #1311-#1315 solution windows.
- Compiled: `latexmk -xelatex -interaction=nonstopmode -halt-on-error elegantbook2.tex`
  - Result: up to date, no rebuild needed.
- Log scan: no `Overfull`, `Underfull`, `LaTeX Warning`, package warning, undefined-control-sequence, or missing-character hits.
- PDF info: `750` pages, A4.
- Rendered and inspected:
  - `tmp\pdfs\batch_150_1311_1315_current_check-746.png`
  - `tmp\pdfs\batch_150_1311_1315_current_check-747.png`
  - `tmp\pdfs\batch_150_1311_1315_current_check-748.png`

## Decision

Batch #1311-#1315 is released after content, calculation, method-consistency, and formula-layout review. The short/local formulas remain inline, and only the long central calculation in #1315 remains displayed.
