# Batch 116 Review: solutions #1141-1145

## Scope

- Global solution numbers: #1141-1145
- Source ranges after index rebuild:
  - #1141: lines 46007-46020
  - #1142: lines 46029-46054
  - #1143: lines 46065-46072
  - #1144: lines 46078-46085
  - #1145: lines 46091-46102

## Changes made

- #1141: no source change after manual review. The Weierstrass-test proof is complete, and the displayed series in the exercise/solution is justified by mathematical status rather than line length alone.
- #1142: corrected the sign in the Lagrange-equation subtraction, added the excluded alternative \(\lambda=-1/(3xy)\) check, stated \(x,y,z>0\), and added the endpoint argument that makes the stationary point the global maximum. The Lagrange system and corrected factorization remain displayed as the proof skeleton; short substitutions such as \(z=(36-3t^2)/(4t)\), \(V(t)\), and \(V'(t)\) remain inline.
- #1143: added the explicit final answer sentence \(2\sqrt2\), while keeping the gradient computation inline because it is below the long-inline threshold and reads as a compact fill-in solution.
- #1144: no source change. The solution correctly avoids the invalid symmetric form with zero denominators and gives the tangent line as \(y=1,\ z=1\).
- #1145: no source change. The Hessian matrix is appropriately displayed, and the remaining determinant/value checks are short enough to stay inline.

## Per-solution review

- #1141: correct and complete. Since \(|\cos(nx)|/n^2\le 1/n^2\) and \(\sum 1/n^2\) converges independently of \(x\), the Weierstrass test proves uniform convergence on all real \(x\). The added tail-estimate sentence keeps the method connected to uniform convergence rather than pointwise comparison only.
- #1142: correct after repair. The cost constraint is \(3xy+2xz+2yz=36\). Maximizing \(\ln V\) gives the displayed Lagrange equations. Subtracting the first two equations now gives \((y-x)(1/(xy)+3\lambda)=0\); the second factor leads to \(z=0\), impossible, so \(x=y\). Then \(V(t)=(36t-3t^3)/4\) on \(0<t<2\sqrt3\), \(V'(t)=0\) gives \(t=2\), endpoint volume tends to \(0\), and \(z=3\).
- #1143: correct. The maximum directional derivative is the gradient norm, and \(\nabla u(0,1,1)=(0,2,2)\), so the answer is \(2\sqrt2\).
- #1144: correct. The parameter value is \(t=0\), and the tangent vector is \((1,0,0)\), so the line through \((1,1,1)\) is \(y=1,\ z=1\).
- #1145: correct. Critical points are \((0,0)\) and \((1,1)\). The Hessian test excludes \((0,0)\), confirms \((1,1)\) as a local minimum, and gives minimum value \(-1\).

## Verification

- Rebuilt index: `python solution_quality_audit\build_solution_index.py`
  - `total_solutions`: 1322
  - `auto_flagged`: 1090
  - `long_inline_flagged`: 109
  - `short_display_flagged`: 840, with #1142 and #1145 displays manually reviewed as proof/computation skeletons rather than accidental short displays.
- Compiled: `latexmk -xelatex -interaction=nonstopmode -halt-on-error elegantbook2.tex` completed successfully before final review.
- Log scan: no `Overfull`, `Underfull`, LaTeX warning, package warning, undefined-control-sequence, or missing-character hits.
- Rendered and inspected:
  - `tmp\pdfs\batch_116_1141_1145_final_v3-699.png`
  - `tmp\pdfs\batch_116_1141_1145_final_v3-700.png`
  - `tmp\pdfs\batch_116_1141_1145_final_v3-701.png`

## Decision

Batch #1141-#1145 is released after content, calculation, method-consistency, and formula-layout review.
