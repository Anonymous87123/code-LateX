# Batch 111 Review: solutions #1116-1120

## Scope

- Global solution numbers: #1116-1120
- Source ranges after index rebuild:
  - #1116: lines 45428-45433
  - #1117: lines 45439-45448
  - #1118: lines 45455-45462
  - #1119: lines 45472-45486
  - #1120: lines 45493-45511

## Changes made

- #1116: strengthened the Green formula setup by naming the positively oriented region \(D\) and recording that \(P,Q\) have continuous partial derivatives. This keeps the method aligned with the earlier path-independence/Green-formula wording.
- #1117: expanded the alternating-series check by writing \(b_n=n^{1-p}+n^{-p}\) and explicitly explaining why \(b_n\) is eventually decreasing when \(p>1\).
- #1119: added the missing chain-rule data \(u_x=1,\ v_x=-y^2/x^2\) and the equality \(f_{21}=f_{12}\) from continuity of second partial derivatives.

## Per-solution review

- #1116: correct after the clarification. Green's formula gives \(\iint_D(Q_x-P_y)\,\mathrm dA\), and \(Q_x=P_y=2x\), so every positively oriented closed curve gives integral \(0\). The formula remains inline because its estimated rendered width is below the 3/4-line threshold and it is a local method statement, not the final answer skeleton.
- #1117: correct and clearer. Alternating convergence holds for \(p>1\); absolute convergence holds exactly for \(p>2\), hence conditional convergence is \(1<p\le2\). The comparison formulas are short-to-medium local steps and were kept inline.
- #1118: correct and complete. The sine series corresponds to the odd \(2\pi\)-periodic extension; \(-\pi/2\) is a continuity point, so \(S(-\pi/2)=-f(\pi/2)=-\pi^2/8\). The final substitution chain is short enough to remain inline.
- #1119: correct after the chain-rule detail was added. The final mixed derivative is displayed because it is the requested result and has several terms; intermediate derivative data remains inline because it is below the long-inline threshold and reads better as explanatory text.
- #1120: correct and complete. Symmetry removes the cross terms, the ellipsoid is reduced by \(x=r\sin\varphi\cos\theta,\ y=2r\sin\varphi\sin\theta,\ z=r\cos\varphi\), and the Jacobian gives \(I=8\pi/5\). The coordinate change and final integral remain display formulas because they are the computational backbone; the expansion and symmetry reduction remain inline.

## Verification

- Rebuilt index: `python solution_quality_audit\build_solution_index.py`
  - `total_solutions`: 1322
  - `auto_flagged`: 1090
  - `long_inline_flagged`: 111
  - `short_display_flagged`: 835, with #1119 and #1120 display formulas manually approved for answer/computation structure.
- Compiled: `latexmk -xelatex -interaction=nonstopmode -halt-on-error elegantbook2.tex` completed successfully.
- Log scan: no `Overfull`, `Underfull`, LaTeX warning, package warning, undefined-control-sequence, or missing-character hits.
- Rendered and inspected:
  - `tmp\pdfs\batch_111_1116_1120_after_fix-692.png`
  - `tmp\pdfs\batch_111_1116_1120_after_fix-693.png`
  - `tmp\pdfs\batch_111_1116_1120_after_fix-694.png`

## Decision

Batch #1116-#1120 is released after content, calculation, method-consistency, and formula-layout review.
