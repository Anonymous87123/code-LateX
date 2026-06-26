# Batch 120 Review: solutions #1161-1165

## Scope

- Global solution numbers: #1161-1165
- Source ranges after index rebuild:
  - #1161: lines 46472-46484
  - #1162: lines 46494-46500
  - #1163: lines 46511-46529
  - #1164: lines 46542-46554
  - #1165: lines 46562-46578

## Changes made

- #1161: displayed the central power-series summation chain. This is not a long-inline promotion by width alone; it is the key computation skeleton converting the given series to the known logarithmic expansion. Endpoint checks and convergence interval remain in prose/inline form.
- #1162: standardized the exponential notation as \(\mathrm{e}\) and kept the actual endpoint value computation inline because it is short and low-status.
- #1163: displayed the translated homogeneous differential equation and its exact-form equivalent as the method skeleton. The potential-function calculation and final implicit solution remain compact inline/prose where appropriate.
- #1164: changed the final \(\mathrm{d}y/\mathrm{d}t\) result from display-style inline math to normal inline math; the formula is short enough to stay inline under the 3/4-line threshold.
- #1165: displayed the final radial integration step because it is the closing computation skeleton after the cylindrical-coordinate setup and inner \(z\)-integration.

## Per-solution review

- #1161: correct and complete. With \(t=x/4\), the standard expansion \(-\ln(1-t)=\sum_{n=1}^{\infty}t^n/n\) gives the sum function for \(|x|<4\). At \(x=-4\), \(\sum(-1)^n/n=-\ln2\) matches the limiting value; at \(x=4\), the harmonic series diverges. Therefore the sum function is \(-\ln(1-x/4)\) on the convergence domain \([-4,4)\).
- #1162: correct. A cosine series on \([0,\pi]\) corresponds to even extension followed by \(2\pi\)-periodic extension. The endpoint \(x=0\) remains continuous after even extension, so the Fourier sum equals \(f(0)=\mathrm{e}\), not the odd-extension endpoint value used for sine series.
- #1163: correct and method-consistent. The numerator and denominator lines meet at \((0,2)\), so \(X=x,\ Y=y-2\) reduces the equation to a homogeneous first-order equation. Written as \((2X-Y)\,\mathrm{d}X-(X+2Y)\,\mathrm{d}Y=0\), it is exact, giving the potential \(X^2-XY-Y^2=C\) and hence \(x^2-x(y-2)-(y-2)^2=C\).
- #1164: correct. Differentiating \(y=f(x,t)\) and \(x=g(y,t)\) with respect to \(t\) gives \(y'=f_xx'+f_t\) and \(x'=g_yy'+g_t\). Substitution yields \((1-f_xg_y)y'=f_t+f_xg_t\), so \(\mathrm{d}y/\mathrm{d}t=(f_t+f_xg_t)/(1-f_xg_y)\) under the implicit-function nonzero-denominator condition.
- #1165: correct. The two surfaces intersect at \(r^2=1-r^2\), so \(0\le r\le1/\sqrt2\), \(r^2\le z\le1-r^2\), \(0\le\theta\le2\pi\). The integrand becomes \(r^2+z^2\) with Jacobian \(r\), and the evaluated integral is \(11\pi/96\).

## Verification

- Rebuilt index: `python solution_quality_audit\build_solution_index.py`
  - `total_solutions`: 1322
  - `auto_flagged`: 1094
  - `long_inline_flagged`: 109
  - `short_display_flagged`: 845, with #1161, #1163, and #1165 manually reviewed as necessary computation or method skeleton displays.
- Compiled: `latexmk -xelatex -interaction=nonstopmode -halt-on-error elegantbook2.tex` completed successfully.
- Log scan: no `Overfull`, `Underfull`, LaTeX warning, package warning, undefined-control-sequence, or missing-character hits.
- Rendered and inspected:
  - `tmp\pdfs\batch_120_1161_1165_final_v1-704.png`
  - `tmp\pdfs\batch_120_1161_1165_final_v1-705.png`
  - `tmp\pdfs\batch_120_1161_1165_final_v1-706.png`

## Decision

Batch #1161-#1165 is released after content, calculation, method-consistency, and formula-layout review. The added displays are limited to computation/method skeletons; short endpoint values, substitutions, and final derivative notation remain inline.
