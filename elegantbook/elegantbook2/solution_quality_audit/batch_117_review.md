# Batch 117 Review: solutions #1146-1150

## Scope

- Global solution numbers: #1146-1150
- Source ranges after index rebuild:
  - #1146: lines 46108-46117
  - #1147: lines 46123-46131
  - #1148: lines 46142-46151
  - #1149: lines 46158-46195
  - #1150: lines 46203-46229

## Changes made

- #1146: no source change. The convergence-domain argument is correct, and all formulas are short local comparisons or endpoint checks that should remain inline.
- #1147: no source change. The solution correctly uses the odd periodic extension viewpoint for a half-range sine series and keeps the endpoint average calculation compact.
- #1148: standardized the exponential notation inside the solution from mixed \(e^x\)/\(\mathrm{e}^x\) to \(\mathrm{e}^x\), matching the problem statement and the homogeneous solution. No display promotion was made because the ansatz, coefficient comparison, and final answer stay below the long-inline threshold.
- #1149: no source change. The two aligned blocks are necessary chain-rule computation skeletons; short definitions of \(u,v,f_1,f_2\) remain inline.
- #1150: no source change. The spherical-coordinate bounds and final integral are correct and appropriately displayed as a multistep computation.

## Per-solution review

- #1146: correct. For \(|x|<1\), the term is comparable to \(x^n\); for \(|x|>1\), it is comparable to \(x^{-n}\). At \(x=\pm1\), the term does not tend to \(0\). The convergence domain is \((-\infty,-1)\cup(-1,1)\cup(1,+\infty)\).
- #1147: correct and method-consistent. A sine expansion on \([0,\pi]\) corresponds to an odd extension, so the one-sided endpoint limits at \(0\) are \(1\) and \(-1\), whose Fourier endpoint average is \(0\).
- #1148: correct. The characteristic roots are \(-2\) and \(1\). Because \(1\) is a root, \(y^*=x\mathrm{e}^x(Ax+B)\) is the proper trial form. Substitution gives \(L[y^*]=\mathrm{e}^x(6Ax+3B+2A)\), so \(A=3,\ B=-2\), and the stated general solution follows.
- #1149: correct. The chain-rule expansion gives \(z_{xx}=2f_1+2y^2f_2+4x^2f_{11}+8x^2y^2f_{12}+4x^2y^4f_{22}\) and \(z_{yx}=4xyf_{11}+4xy(x^2+y^2)f_{12}+4xyf_2+4x^3y^3f_{22}\), with all \(f\)-partials evaluated at \((x^2+y^2,x^2y^2)\).
- #1150: correct. The cone is \(\varphi=\pi/4\), the sphere is \(\rho=1\), and the bounded region is \(0\le\theta\le2\pi,\ 0\le\varphi\le\pi/4,\ 0\le\rho\le1\). Symmetry cancels the \(x\) and \(y\) integrals, leaving the \(z\)-integral \(\pi/8\).

## Verification

- Rebuilt index: `python solution_quality_audit\build_solution_index.py`
  - `total_solutions`: 1322
  - `auto_flagged`: 1090
  - `long_inline_flagged`: 109
  - `short_display_flagged`: 840, with #1149 and #1150 displays manually reviewed as computation skeletons.
- Compiled: `latexmk -xelatex -interaction=nonstopmode -halt-on-error elegantbook2.tex` completed successfully.
- Log scan: no `Overfull`, `Underfull`, LaTeX warning, package warning, undefined-control-sequence, or missing-character hits.
- Rendered and inspected:
  - `tmp\pdfs\batch_117_1146_1150_final_v1-700.png`
  - `tmp\pdfs\batch_117_1146_1150_final_v1-701.png`
  - `tmp\pdfs\batch_117_1146_1150_final_v1-702.png`

## Decision

Batch #1146-#1150 is released after content, calculation, method-consistency, and formula-layout review.
