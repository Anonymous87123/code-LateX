# Batch 114 Review: solutions #1131-1135

## Scope

- Global solution numbers: #1131-1135
- Source ranges after index rebuild:
  - #1131: lines 45764-45776
  - #1132: lines 45782-45789
  - #1133: lines 45804-45812
  - #1134: lines 45822-45834
  - #1135: lines 45840-45858

## Changes made

- #1131: split the overlong inline Green-formula chain into a displayed derivation, named the enclosed region \(D\), and made the clockwise-versus-counterclockwise sign change explicit in formal wording.
- #1132: compressed the unnecessary long absolute-series comparison into the short inline comparison \(b_n\sim n^{1-p}\), and added the endpoint explanation for \(p=2\).
- #1133: replaced nonstandard \(f(0-0), f(0+0)\) notation with \(f(0-), f(0+)\).
- #1134: split one source/rendering line that had packed \(s,r,u_x,u_{xx}\) together; retained the intermediate formulas inline because each is short, and clarified the meaning of \(f_i,f_{ij}\).
- #1135: added the missing explicit statement that the ellipsoid change of variables gives \(x^2/4+y^2+z^2=r^2\).

## Per-solution review

- #1131: correct and method-consistent. For positive orientation, Green's formula gives \(\iint_D(Q_x-P_y)\,\mathrm dA=2\pi ab\); the stated clockwise orientation reverses the sign, so the answer is \(-2\pi ab\). The displayed formula is retained because it is the main Green-formula computation and replaced an overlong inline chain.
- #1132: correct and complete. The alternating series can converge only when \(b_n\to0\), namely \(p>1\); for \(p>1\), \(b_n\) is eventually decreasing. Absolute convergence is governed by \(b_n\sim n^{1-p}\), so it occurs only for \(p>2\). Therefore conditional convergence is \(1<p\le2\), with \(p=2\) included.
- #1133: correct. The Fourier sum at the jump point is the average of the one-sided limits \(-1\) and \(2\), so \(S(0)=1/2\). The computation is short and stays inline.
- #1134: correct. The chain-rule calculation for \(u_{xx}\) is shown before passing to \(y,z\), and the final Laplacian formula is displayed as the answer skeleton. Splitting the first solution line removed the long-inline source risk without promoting short intermediate formulas unnecessarily.
- #1135: correct. Symmetry of the ellipsoid removes all cross terms. The generalized spherical substitution has Jacobian \(2r^2\sin\varphi\) and turns \(x^2/4+y^2+z^2\) into \(r^2\), giving \(I=8\pi/5\). The displayed formulas are the computation backbone.

## Verification

- Rebuilt index: `python solution_quality_audit\build_solution_index.py`
  - `total_solutions`: 1322
  - `auto_flagged`: 1090
  - `long_inline_flagged`: 111
  - `short_display_flagged`: 838, with #1131, #1134, and #1135 displays manually approved as computation skeletons.
- Compiled: `latexmk -xelatex -interaction=nonstopmode -halt-on-error elegantbook2.tex` completed successfully.
- Log scan: no `Overfull`, `Underfull`, LaTeX warning, package warning, undefined-control-sequence, or missing-character hits.
- Rendered and inspected:
  - `tmp\pdfs\batch_114_1131_1135_final-696.png`
  - `tmp\pdfs\batch_114_1131_1135_final-697.png`

## Decision

Batch #1131-#1135 is released after content, calculation, method-consistency, and formula-layout review.
