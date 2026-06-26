# Batch 125 Review: solutions #1186-1190

## Scope

- Global solution numbers: #1186-1190
- Source ranges after index rebuild:
  - #1186: lines 47081-47093
  - #1187: lines 47107-47120
  - #1188: lines 47127-47146
  - #1189: lines 47152-47164
  - #1190: lines 47176-47195

## Changes made

- #1186: removed display-style inline math from the exercise and solution, added the evaluation convention for \(f_i,f_{ij}\), and displayed the two chain-rule derivative identities to avoid the previous awkward inline break.
- #1187: normalized inline math delimiters in the exercise statement. The displayed piecewise sum function remains the final standard form.
- #1188: removed display-style forcing from the exercise integral, normalized the region notation, and separated the last simplification into clear steps. The integration-by-parts result is displayed because it is a central computation and was visually close enough to the line-width threshold to read poorly inline.
- #1189: removed display-style forcing from the exercise integral and from the polar-angle differential identity. The displayed change-of-variables computation remains the main method skeleton.
- #1190: converted the very long exercise-statement surface integral to display math, displayed the symmetry equality for the fourth-power surface integrals, and kept the final numerical substitution inline.

## Per-solution review

- #1186: correct. With \(u=x+y\) and \(v=xy\), \(z_x=f_1+yf_2\). Differentiating with respect to \(y\) gives \(f_{11}+xf_{12}+f_2+y(f_{21}+xf_{22})\), and under the usual continuous-second-partial assumption this becomes \(f_{11}+(x+y)f_{12}+xyf_{22}+f_2\).
- #1187: correct. The Fourier sum equals \(f(x)\) at continuity points, equals \((1+0)/2=1/2\) at \(x=0\), and equals \((\pi^2+(-\pi+1))/2\) at the periodic endpoints \(x=\pm\pi\).
- #1188: correct. The region \(0\le y\le1,\ y^2\le x\le y\) becomes \(0\le x\le1,\ x\le y\le\sqrt{x}\). This gives \(\frac12\int_0^1(x-x^2)\sin(x^2)\,\mathrm{d}x\), and the integration-by-parts step yields \(I=\frac14\{1-\int_0^1\cos(x^2)\,\mathrm{d}x\}\).
- #1189: correct. The positive scaling \(u=2x,\ v=y\) preserves orientation and maps \(L\) to an ellipse winding once around the origin. The transformed integrand is \(\frac12\,\mathrm{d}\theta\), so the integral is \(\pi\).
- #1190: correct. On the upper hemisphere, \(\sqrt{x^2+y^2+z^2}=a\), and the lower-side orientation is the negative of the outward unit normal. Thus the integrand becomes \(-a^{-2}(x^4+y^4+z^4)\,\mathrm{d}S\). By sphere symmetry each fourth-power integral over the upper hemisphere is \(2\pi a^6/5\), giving \(I=-6\pi a^4/5\).

## Verification

- Compiled: `latexmk -xelatex -interaction=nonstopmode -halt-on-error elegantbook2.tex` completed successfully.
- Log scan: no `Overfull`, `Underfull`, LaTeX warning, package warning, undefined-control-sequence, or missing-character hits.
- Rebuilt index: `python solution_quality_audit\build_solution_index.py`
  - `total_solutions`: 1322
  - `auto_flagged`: 1097
  - `long_inline_flagged`: 106
  - `short_display_flagged`: 854
  - Remaining short-display flags in this batch were manually reviewed as central chain-rule, integration-by-parts, change-of-variables, or surface-symmetry computation blocks.
- Rendered and inspected:
  - `tmp\pdfs\batch_125_1186_1190_final_v1-711.png`
  - `tmp\pdfs\batch_125_1186_1190_final_v1-712.png`
  - `tmp\pdfs\batch_125_1186_1190_final_v1-713.png`

## Decision

Batch #1186-#1190 is released after content, calculation, method-consistency, and formula-layout review. Short explanatory formulas were kept inline, while long problem data and central computation blocks were displayed.
