# Batch 109 Review: solutions #1106-1110

## Scope

- Global solution numbers: #1106-1110
- Source ranges after index rebuild:
  - #1106: lines 45147-45170
  - #1107: lines 45180-45201
  - #1108: lines 45207-45222
  - #1109: lines 45242-45274
  - #1110: lines 45282-45312

## Changes made

- #1106: expanded the mixed-partial calculation. The solution now defines the positional partial-derivative notation for \(g\), gives the intermediate chain-rule derivative
  \(\partial_x[xg_2(x,xy)]\), and then states the final answer. This removes the former jump from \(z_y\) directly to the result.
- #1110: promoted the long path-independence condition \(P_y=Q_x\) from a cramped inline equation to display math. This equation is the key step that yields the differential equation for \(f\), and the precheck rendering showed the inline version breaking awkwardly across lines.
- No formula-only edits were made to #1107, #1108, or #1109. Their displayed formulas are computation skeletons, area-element formulas, or Gauss-formula chains, not minor variable definitions; the remaining inline formulas are below the 3/4 text-width threshold.

## Per-solution review

- #1106: correct and now clearer. Differentiating first with respect to \(y\) gives
  \(z_y=f'(y/x)+xg_2(x,xy)\). Differentiating with respect to \(x\) gives
  \( -y f''(y/x)/x^2+g_2+xg_{21}+xyg_{22}\), with all \(g\)-partials evaluated at \((x,xy)\). The notation is now consistent with the earlier compound-function section.
- #1107: correct and complete. The two original regions combine to
  \(1/2\le y\le1,\ y^2\le x\le y\). Integrating in \(x\) gives the final value \((1-\pi)/\pi^3\). The displayed aligned computation is necessary for the change of order and final evaluation.
- #1108: correct and clear. The surface element is \(\mathrm dS=\sqrt2\,\mathrm dx\,\mathrm dy\), and the projection is the annular region between the two tangent circles, with area \(3\pi/4\). The final area is \(3\sqrt2\pi/4\).
- #1109: correct and complete. The normal direction is matched to the exterior of \(\Omega:\ 1+x^2+z^2\le y\le3\), the cap contribution is subtracted with the correct sign, and the result is \(146\pi/3\). The long displayed formulas are core Gauss-formula bookkeeping and should remain displayed.
- #1110: correct and now better laid out. Path independence gives \(f'+f=e^x\), whence \(f=(e^x-e^{-x})/2\). The potential
  \(-\tfrac12(e^x-e^{-x})\sin(y/2)\) gives the endpoint value
  \(-\tfrac12(e-e^{-1})\sin(1/2)\).

## Verification

- Rebuilt index: `python solution_quality_audit\build_solution_index.py`
  - `total_solutions`: 1322
  - `auto_flagged`: 1090
  - `long_inline_flagged`: 112
  - `short_display_flagged`: 834, with the increase caused by the manually approved #1110 key equation.
- Compiled: `latexmk -xelatex -interaction=nonstopmode -halt-on-error elegantbook2.tex` completed successfully.
- Log scan: no `Overfull`, `Underfull`, LaTeX warning, package warning, undefined-control-sequence, or missing-character hits.
- Rendered and inspected:
  - `tmp\pdfs\batch_109_1106_1110_after_fix-688.png`
  - `tmp\pdfs\batch_109_1106_1110_after_fix-689.png`
  - `tmp\pdfs\batch_109_1106_1110_after_fix-690.png`
  - `tmp\pdfs\batch_109_1106_1110_after_fix-691.png`

## Decision

Batch #1106-#1110 is released after the #1106 and #1110 edits and strict formula-layout recheck.
