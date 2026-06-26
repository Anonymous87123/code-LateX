# Batch 122 Review: solutions #1171-1175

## Scope

- Global solution numbers: #1171-1175
- Source ranges after index rebuild:
  - #1171: lines 46724-46731
  - #1172: lines 46740-46761
  - #1173: lines 46772-46791
  - #1174: lines 46805-46821
  - #1175: lines 46828-46846

## Changes made

- #1171: changed short display-style inline estimates back to normal inline math and standardized \(\mathrm{e}^{-nx}\) in the explanatory sentence.
- #1172: displayed the distance-square objective and the one-variable reduction/derivative chain. These are the main minimization skeletons, not mechanical promotion of short formulas. Added the missing global-minimum justification after reducing to one variable.
- #1173: changed the first derivative formula to normal inline math, displayed the two chain-rule derivative formulas for \(f_1\) and \(f_2\), and stated the continuity assumption needed to use \(f_{21}=f_{12}\).
- #1174: changed endpoint formulas from display-style inline math to normal inline math and cleaned the prose spacing. The piecewise answer remains displayed as the final standard form.
- #1175: standardized exponential notation to \(\mathrm{e}\) in the exercise and solution, while keeping the short final substitution computation inline.

## Per-solution review

- #1171: correct. For \(x\ge0\), \(0\le1-\mathrm{e}^{-nx}\le1\) and \(n^2+x^2\ge n^2\), so the terms are bounded by \(1/n^2\). The Weierstrass test proves uniform convergence on \([0,+\infty)\).
- #1172: correct and complete after the added global-minimum sentence. The squared distance is coercive, so a minimum exists. The stationary equations imply \(x=y\) because \((0,0)\) is not stationary. The one-variable derivative has the only zero \(s=2^{-1/3}\), giving \(d_{\min}^2=33/4-3\sqrt[3]{4}\) and \(d_{\min}=\sqrt{33/4-3\sqrt[3]{4}}\).
- #1173: correct. The chain rule gives \(z_y=2xyf_1+x^2f_2\). Differentiating again and using \(f_{21}=f_{12}\) under the usual continuous-second-partial assumption yields \(4x^2y^2f_{11}+4x^3yf_{12}+x^4f_{22}+2xf_1\), with all partials evaluated at \((xy^2,x^2y)\).
- #1174: correct. At ordinary continuity points the Fourier sum equals \(f(x)\); at \(x=\pm\pi/2\) and the periodic endpoints \(x=\pm\pi\), the sum is the average of the two one-sided limits, namely \(0\).
- #1175: correct. Reversing the triangular region gives \(0\le y\le1\), \(0\le x\le2y\), so the integral becomes \(\int_0^1 2y\mathrm{e}^{y^2}\,\mathrm{d}y=\mathrm{e}-1\).

## Verification

- Rebuilt index: `python solution_quality_audit\build_solution_index.py`
  - `total_solutions`: 1322
  - `auto_flagged`: 1095
  - `long_inline_flagged`: 109
  - `short_display_flagged`: 848, with #1172 and #1173 manually reviewed as necessary computation/method skeleton displays.
- Compiled: `latexmk -xelatex -interaction=nonstopmode -halt-on-error elegantbook2.tex` completed successfully.
- Log scan: no `Overfull`, `Underfull`, LaTeX warning, package warning, undefined-control-sequence, or missing-character hits.
- Rendered and inspected:
  - `tmp\pdfs\batch_122_1171_1175_final_v1-706.png`
  - `tmp\pdfs\batch_122_1171_1175_final_v1-707.png`
  - `tmp\pdfs\batch_122_1171_1175_final_v1-708.png`

## Decision

Batch #1171-#1175 is released after content, calculation, method-consistency, and formula-layout review. The added displays are limited to central minimization and chain-rule skeletons; short estimates, endpoint values, and final substitutions remain inline.
