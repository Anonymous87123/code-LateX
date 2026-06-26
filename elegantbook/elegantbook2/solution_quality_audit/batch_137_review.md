# Batch 137 Review: solutions #1246-1250

## Scope

- Global solution numbers: #1246-#1250
- Source ranges after index rebuild:
  - #1246: lines 48532-48539
  - #1247: lines 48548-48559
  - #1248: lines 48565-48576
  - #1249: lines 48590-48597
  - #1250: lines 48610-48617

## Changes Made

- #1246: expanded the direction-derivative reasoning by starting from \(D_{\mathbf e}u=\nabla u\cdot\mathbf e\), invoking Cauchy's inequality, then computing the gradient value and norm.
- #1247: converted the first-kind curve-integral evaluation chain from large inline math to a displayed central computation.
- #1248: converted the trigonometric-series decomposition and summation into a displayed computation chain using the standard cosine and sine Taylor series.
- #1249: split the long Fourier endpoint sentence into separate one-sided-limit checks and added an explicit reminder that the left limit at \(-\pi\) is taken through the \(2\pi\)-periodic extension.
- #1250: added the distinction that a nonzero right-hand side makes the equation nonhomogeneous but does not affect linearity.

## Formula Layout Decisions

- #1246: kept all formulas inline because the gradient and norm formulas are short.
- #1247: displayed the integral evaluation because it is the central computation and includes multiple integrals.
- #1248: displayed the summation split because it is the main evaluation chain and is visually heavy inline.
- #1249: kept the endpoint values and final average inline after shortening them; no display math is needed.
- #1250: kept classification formulas inline because they are short option references.

## Per-Solution Review

- #1246: correct. The maximum directional derivative is \(\|\nabla u(2,-1,-1)\|=\|(-2,4,2)\|=2\sqrt6\).
- #1247: correct. On the unit first-quadrant arc, \(x=\cos t,\ y=\sin t,\ \mathrm{d}s=\mathrm{d}t\), giving \(\pi/2+1\).
- #1248: correct. The summand splits into even and odd factorial Taylor series, so the sum is \(\cos1+2\sin1\).
- #1249: correct. The periodic one-sided limits at \(-\pi\) are \(0\) and \(\pi^2\), so the Fourier series converges to \(\pi^2/2\).
- #1250: correct. Only item 1 is second-order linear; item 2 is first-order, item 3 is nonlinear in \(y''\), and item 4 is nonlinear in \(y\).

## Verification

- Rebuilt index: `python solution_quality_audit\build_solution_index.py`
  - `total_solutions`: 1322
  - `auto_flagged`: 1093
  - `long_inline_flagged`: 94
  - `short_display_flagged`: 883
- Batch index check:
  - #1246, #1249, and #1250 are `AUTO_INDEXED_NO_HEURISTIC_FLAG`.
  - #1247 and #1248 have only `短display待判定`; both displays were manually retained as central computation formulas.
- Batch solution-line check: no source line of length `>=170` inside the #1246-#1250 solution windows.
- Compiled: `latexmk -xelatex -interaction=nonstopmode -halt-on-error elegantbook2.tex` completed successfully.
- Log scan: no `Overfull`, `Underfull`, `LaTeX Warning`, package warning, undefined-control-sequence, or missing-character hits.
- PDF info: `749` pages.
- Rendered and inspected:
  - `tmp\pdfs\batch_137_1246_1250_final-728.png`
  - `tmp\pdfs\batch_137_1246_1250_final-729.png`
  - `tmp\pdfs\batch_137_1246_1250_final-730.png`

## Decision

Batch #1246-#1250 is released after content, calculation, method-consistency, and formula-layout review. Remaining display flags are intentional central formulas; the batch has no long inline formulas.
