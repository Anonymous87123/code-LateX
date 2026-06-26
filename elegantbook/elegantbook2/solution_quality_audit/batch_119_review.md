# Batch 119 Review: solutions #1156-1160

## Scope

- Global solution numbers: #1156-1160
- Source ranges after index rebuild:
  - #1156: lines 46380-46393
  - #1157: lines 46402-46420
  - #1158: lines 46431-46438
  - #1159: lines 46444-46453
  - #1160: lines 46459-46466

## Changes made

- #1156: standardized the exponential notation to \(\mathrm{e}^{-nx}\) and changed short inline bounds/comparisons back to normal inline math. No display promotion was made because the comparison remains below the long-inline threshold after style correction.
- #1157: promoted the three Lagrange first-order equations to a displayed system. This is a short display by script heuristics, but it is the central optimization skeleton and was visually clearer than the previous dense inline chain.
- #1158: changed the final directional-derivative computation from display-style inline math to normal inline math; the computation and conclusion are unchanged.
- #1159: changed the short expanded plane equation from display-style inline math to normal inline math.
- #1160: changed the final \(\frac12\) answer from display-style inline math to normal inline math.

## Per-solution review

- #1156: correct. For \(x\ge0\), \(0\le1-\mathrm{e}^{-nx}\le1\), and \(n^2+\sin x\ge n^2-1>0\) for \(n\ge2\). The uniform majorant \(\sum_{n=2}^{\infty}1/(n^2-1)\) converges, so the Weierstrass test proves uniform convergence on \([0,+\infty)\).
- #1157: correct and complete. Since \(x,y,z>0\), maximizing \(u=x^2y^3z^4\) is equivalent to maximizing \(\ln u\). The Lagrange equations give \(\lambda x=2,\ \lambda y=3,\ \lambda z=4\), hence \(x:y:z=2:3:4\) and \((x,y,z)=(2,3,4)\). The boundary limit \(u\to0\) confirms the interior critical point gives the maximum.
- #1158: correct. \(\nabla z(1,1)=(2,4)\), so the directional derivative in the gradient direction is \(\|\nabla z(1,1)\|=2\sqrt5\).
- #1159: correct. At \(t=1\), the tangent vector is \((1,2,3)\), so the normal plane through \((1,1,1)\) is \(x+2y+3z-6=0\).
- #1160: correct. The inequality \((x-y)^2\ge0\) gives \(2xy\le x^2+y^2=1\), with equality at \(x=y=1/\sqrt2\). The maximum is \(\frac12\).

## Verification

- Rebuilt index: `python solution_quality_audit\build_solution_index.py`
  - `total_solutions`: 1322
  - `auto_flagged`: 1092
  - `long_inline_flagged`: 109
  - `short_display_flagged`: 842, with #1157's display manually reviewed as the Lagrange first-order-condition skeleton.
- Compiled: `latexmk -xelatex -interaction=nonstopmode -halt-on-error elegantbook2.tex` completed successfully.
- Log scan: no `Overfull`, `Underfull`, LaTeX warning, package warning, undefined-control-sequence, or missing-character hits.
- Rendered and inspected:
  - `tmp\pdfs\batch_119_1156_1160_final_v1-703.png`
  - `tmp\pdfs\batch_119_1156_1160_final_v1-704.png`
  - `tmp\pdfs\batch_119_1156_1160_final_v1-705.png`

## Decision

Batch #1156-#1160 is released after content, calculation, method-consistency, and formula-layout review.
