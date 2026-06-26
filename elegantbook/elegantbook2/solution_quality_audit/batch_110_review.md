# Batch 110 Review: solutions #1111-1115

## Scope

- Global solution numbers: #1111-1115
- Source ranges after index rebuild:
  - #1111: lines 45318-45328
  - #1112: lines 45337-45351
  - #1113: lines 45360-45383
  - #1114: lines 45394-45401
  - #1115: lines 45407-45418

## Changes made

- #1113: added the symmetry justification for taking the isosceles triangle's vertex at the upper vertex \((0,2)\). The Lagrange calculation was correct, but the setup now states why this representative configuration is sufficient.
- #1115: converted the final long inline formula for \(\operatorname{div}(\operatorname{grad}u)\) into display math. This removes the flagged long inline chain while keeping the shorter first- and second-derivative formulas inline.
- #1112: reviewed the inline summation and remainder formulas against the stricter 3/4 text-width rule. They are proof components but not long enough to justify further display splitting; keeping them inline preserves the flow of the proof.

## Per-solution review

- #1111: correct and complete. The identity \(\cos^2x=(1+\cos2x)/2\) and the Maclaurin series for \(\cos 2x\) give the stated power series with infinite radius of convergence. The displayed series is the final expansion skeleton and is appropriate.
- #1112: correct and complete. The Weierstrass test proves uniform convergence on \([c,1]\). On \((0,1)\), choosing \(x_N=1/(N+1)\) makes the remainder fail to tend uniformly to \(0\), proving non-uniform convergence. The inline formulas were visually checked and left inline.
- #1113: correct and clearer after the edit. The horizontal base chord gives endpoints \((-x,y)\), \((x,y)\); by symmetry it suffices to take the upper vertex. The Lagrange multiplier system yields the nondegenerate maximum at \((x,y)=(3,-1)\), giving area \(9\).
- #1114: correct and complete. The forcing term is a degree-one polynomial times \(e^x\), and \(r=1\) is a simple root of the homogeneous characteristic equation, so the particular form is \(x(ax+b)e^x\).
- #1115: correct and now better laid out. The second derivatives add to
  \(\bigl[6+4(x^2+y^2+z^2)\bigr]e^{x^2+y^2+z^2}\); the long result chain is displayed, while the shorter derivative computations remain inline.

## Verification

- Rebuilt index: `python solution_quality_audit\build_solution_index.py`
  - `total_solutions`: 1322
  - `auto_flagged`: 1090
  - `long_inline_flagged`: 111
  - `short_display_flagged`: 835, with #1115's display manually approved because it replaces a flagged long inline formula.
- Compiled: `latexmk -xelatex -interaction=nonstopmode -halt-on-error elegantbook2.tex` completed successfully.
- Log scan: no `Overfull`, `Underfull`, LaTeX warning, package warning, undefined-control-sequence, or missing-character hits.
- Rendered and inspected:
  - `tmp\pdfs\batch_110_1111_1115_after_fix-690.png`
  - `tmp\pdfs\batch_110_1111_1115_after_fix-691.png`
  - `tmp\pdfs\batch_110_1111_1115_after_fix-692.png`

## Decision

Batch #1111-#1115 is released after the #1113 and #1115 edits and strict formula-layout recheck.
